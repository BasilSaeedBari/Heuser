import os
import re
import json
import hashlib
import sqlite3
import xml.etree.ElementTree as ET
import fitz
import httpx
import yake
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# ==============================================================================
# 1. CONFIGURATION
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
UPLOAD_DIR = os.path.join(DATA_DIR, 'uploads')
DB_PATH = os.path.join(DATA_DIR, 'papers.db')

MAX_UPLOAD_MB = 25
MIN_CHARS_PER_PAGE = 50
HTTP_TIMEOUT = 10
MAILTO = "qwen@example.com"
USER_AGENT = "PaperGraphApp/1.0 (mailto:qwen@example.com)"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ==============================================================================
# 2. ERRORS
# ==============================================================================
class AppError(Exception):
    def __init__(self, code: str, message: str, status: int, **kwargs):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.extra = kwargs

class NoFile(AppError):
    def __init__(self): super().__init__("no_file", "No file provided.", 400)

class FileTooLarge(AppError):
    def __init__(self): super().__init__("file_too_large", "File is too large.", 413)

class NotPdf(AppError):
    def __init__(self): super().__init__("not_pdf", "Not a valid PDF.", 415)

class UnreadablePdf(AppError):
    def __init__(self): super().__init__("unreadable_pdf", "Cannot read PDF.", 422)

class NoTextLayer(AppError):
    def __init__(self): super().__init__("no_text_layer", "No text layer found.", 422)

class Duplicate(AppError):
    def __init__(self, existing_id: int): 
        super().__init__("duplicate", f"Duplicate paper. Existing ID: {existing_id}", 409, existing_id=existing_id)

class NotFound(AppError):
    def __init__(self): super().__init__("not_found", "Resource not found.", 404)

class BadParameter(AppError):
    def __init__(self, msg="Bad parameter"): super().__init__("bad_parameter", msg, 400)

# ==============================================================================
# 3. DATABASE
# ==============================================================================
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS papers (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    sha256        TEXT    NOT NULL UNIQUE,
    original_name TEXT    NOT NULL,
    stored_path   TEXT    NOT NULL,
    title         TEXT    NOT NULL,
    abstract      TEXT,
    doi           TEXT,
    arxiv_id      TEXT,
    year          INTEGER,
    venue         TEXT,
    page_count    INTEGER NOT NULL,
    full_text     TEXT    NOT NULL,
    node_id       TEXT    NOT NULL UNIQUE,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_papers_doi ON papers(doi) WHERE doi IS NOT NULL;

CREATE TABLE IF NOT EXISTS authors (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL,
    name_key TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS paper_authors (
    paper_id  INTEGER NOT NULL REFERENCES papers(id)  ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
    position  INTEGER NOT NULL,
    PRIMARY KEY (paper_id, author_id)
);

CREATE TABLE IF NOT EXISTS tags (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS paper_tags (
    paper_id INTEGER NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    tag_id   INTEGER NOT NULL REFERENCES tags(id)   ON DELETE CASCADE,
    source   TEXT NOT NULL DEFAULT 'yake',
    PRIMARY KEY (paper_id, tag_id)
);

CREATE TABLE IF NOT EXISTS citations (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id  INTEGER NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    ref_index INTEGER NOT NULL,
    raw_text  TEXT    NOT NULL,
    cited_doi TEXT,
    cited_title TEXT,
    UNIQUE (paper_id, ref_index)
);

CREATE TABLE IF NOT EXISTS nodes (
    node_id    TEXT PRIMARY KEY,
    label      TEXT NOT NULL CHECK (label IN ('Paper','Author','Tag')),
    name       TEXT NOT NULL,
    properties TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS edges (
    edge_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id     TEXT NOT NULL REFERENCES nodes(node_id) ON DELETE CASCADE,
    target_id     TEXT NOT NULL REFERENCES nodes(node_id) ON DELETE CASCADE,
    relation_type TEXT NOT NULL CHECK (relation_type IN ('AUTHORED_BY','HAS_TAG','CITES')),
    weight        REAL NOT NULL DEFAULT 1.0,
    UNIQUE (source_id, target_id, relation_type)
);

CREATE TABLE IF NOT EXISTS activity_log (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ts        TEXT NOT NULL DEFAULT (datetime('now')),
    action    TEXT NOT NULL,
    paper_id  INTEGER,
    detail    TEXT NOT NULL,
    status    TEXT NOT NULL CHECK (status IN ('ok','error'))
);
"""

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db() -> None:
    conn = get_conn()
    conn.executescript(SCHEMA_SQL)
    conn.close()

def log_activity(conn, action: str, paper_id: int | None, detail: str, status: str) -> None:
    conn.execute("INSERT INTO activity_log (action, paper_id, detail, status) VALUES (?, ?, ?, ?)",
                 (action, paper_id, detail, status))

# ==============================================================================
# 4. SERVICES
# ==============================================================================

# --- Identifiers ---
def normalize_doi(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r'^https?://(dx\.)?doi\.org/', '', s)
    return s

def find_doi(text: str) -> str | None:
    m = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text)
    if m:
        doi = m.group(0).rstrip('.,;)')
        return normalize_doi(doi)
    return None

def find_arxiv_id(text: str) -> str | None:
    m = re.search(r'arXiv:(\d{4}\.\d{4,5}(v\d+)?)', text, re.IGNORECASE)
    if m: return m.group(1)
    m = re.search(r'arXiv\s+(\d{4}\.\d{4,5}(v\d+)?)', text, re.IGNORECASE)
    if m: return m.group(1)
    m = re.search(r'\b(\d{4}\.\d{4,5}(v\d+)?)\b', text)
    if m: return m.group(1)
    return None

# --- PDF Extraction ---
def is_pdf_bytes(data: bytes) -> bool:
    return data[:5] == b'%PDF-'

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def extract_document(path: str) -> dict:
    try:
        doc = fitz.open(path)
        if doc.needs_pass:
            raise UnreadablePdf()
    except Exception as e:
        if isinstance(e, UnreadablePdf): raise
        raise UnreadablePdf()
    
    meta = doc.metadata
    pages = []
    full_text = ""
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        width = page.rect.width
        blocks = page.get_text("dict")["blocks"]
        page_blocks = []
        
        for b in blocks:
            if b["type"] == 0:
                for line in b["lines"]:
                    for span in line["spans"]:
                        page_blocks.append({
                            "x0": span["bbox"][0], "y0": span["bbox"][1],
                            "x1": span["bbox"][2], "y1": span["bbox"][3],
                            "text": span["text"], "size": span["size"]
                        })
        
        # Sort by Y then X for reading order
        page_blocks.sort(key=lambda b: (b["y0"], b["x0"]))
        page_text = " ".join(b["text"] for b in page_blocks)
        # Fix hyphenation
        page_text = re.sub(r'-\n([a-z])', r'\1', page_text)
        
        full_text += page_text + "\n"
        pages.append({"page": page_num + 1, "width": width, "blocks": page_blocks})
    
    doc.close()
    
    if len(full_text.strip()) / max(len(pages), 1) < MIN_CHARS_PER_PAGE:
        raise NoTextLayer()
        
    return {
        "page_count": len(pages),
        "pages": pages,
        "full_text": full_text,
        "meta": {"title": meta.get("title"), "author": meta.get("author")}
    }

# --- Structure Detection ---
def detect_title(doc: dict, meta_title: str | None) -> str:
    if not doc["pages"]: return meta_title or "Untitled"
    page1 = doc["pages"][0]
    if not page1["blocks"]: return meta_title or "Untitled"
    
    max_size = max(b["size"] for b in page1["blocks"])
    title_blocks = [b for b in page1["blocks"] if b["size"] >= max_size * 0.9]
    title_blocks.sort(key=lambda b: b["y0"])
    
    if title_blocks:
        return " ".join(b["text"] for b in title_blocks).strip()
    return meta_title or "Untitled"

def detect_authors(doc: dict, title: str) -> list[str]:
    if not doc["pages"]: return []
    page1 = doc["pages"][0]
    title_y = min((b["y0"] for b in page1["blocks"] if title.lower() in b["text"].lower()), default=0)
    
    authors = []
    for b in page1["blocks"]:
        if b["y0"] > title_y and b["y0"] < title_y + 100:
            text = b["text"].strip()
            if not text or "@" in text or "university" in text.lower() or text.isdigit():
                continue
            authors.extend([a.strip() for a in re.split(r',| and ', text) if a.strip()])
    return authors[:10]

def detect_abstract(full_text: str) -> str | None:
    m = re.search(r'(?:Abstract|In brief|Summary)\s*\n?(.*?)(?:\n\s*(?:Introduction|Keywords|1\.|I\.)|\Z)', full_text, re.IGNORECASE | re.DOTALL)
    if m: return m.group(1).strip()[:2000]
    return full_text[:1000]

def detect_keywords(full_text: str) -> list[str]:
    m = re.search(r'(?:Keywords|Index Terms)[:\s]+(.*?)(?:\n|$)', full_text, re.IGNORECASE)
    if m:
        return [k.strip() for k in re.split(r'[,;/]', m.group(1)) if k.strip()]
    return []

def extract_references(full_text: str) -> list[dict]:
    m = re.search(r'(?:References|Bibliography|Notes)\s*\n(.*?)\Z', full_text, re.IGNORECASE | re.DOTALL)
    if not m: return []
    ref_text = m.group(1)
    entries = re.split(r'\n\s*(?:\[\d+\]|\d+\.\s)', ref_text)
    refs = []
    for i, e in enumerate(entries):
        e = e.strip()
        if e:
            refs.append({"index": i + 1, "raw_text": e, "doi": None, "title": None})
    return refs

# --- Metadata API ---
def _api_get(url: str, params: dict = None) -> dict | None:
    try:
        with httpx.Client(timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT}) as client:
            r = client.get(url, params=params)
            r.raise_for_status()
            return r.json()
    except Exception:
        return None

def lookup_crossref(doi: str) -> dict | None:
    data = _api_get(f"https://api.crossref.org/v1/works/{doi}", params={"mailto": MAILTO})
    if not data or "message" not in data: return None
    m = data["message"]
    authors = [f"{a.get('given','')} {a.get('family','')}".strip() for a in m.get("author", [])]
    return {
        "title": m.get("title", [""])[0],
        "authors": authors,
        "year": m.get("published-print", {}).get("date-parts", [[None]])[0][0] or m.get("published-online", {}).get("date-parts", [[None]])[0][0],
        "venue": m.get("container-title", [""])[0],
        "abstract": m.get("abstract"),
        "references": [{"doi": r.get("DOI"), "title": r.get("article-title")} for r in m.get("reference", []) if r.get("DOI")]
    }

def lookup_semantic_scholar(identifier: str) -> dict | None:
    prefix = "DOI:" if identifier.startswith("10.") else "ARXIV:"
    data = _api_get(f"https://api.semanticscholar.org/graph/v1/paper/{prefix}{identifier}", params={"fields": "title,authors,year,venue,abstract,references.externalIds,references.title"})
    if not data: return None
    authors = [a["name"] for a in data.get("authors", [])]
    refs = [{"doi": r["externalIds"].get("DOI"), "title": r.get("title")} for r in data.get("references", []) if r.get("externalIds", {}).get("DOI")]
    return {
        "title": data.get("title"), "authors": authors, "year": data.get("year"),
        "venue": data.get("venue"), "abstract": data.get("abstract"), "references": refs
    }

def lookup_arxiv(arxiv_id: str) -> dict | None:
    try:
        with httpx.Client(timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT}) as client:
            r = client.get("https://export.arxiv.org/api/query", params={"id_list": arxiv_id})
            r.raise_for_status()
            root = ET.fromstring(r.text)
            entry = root.find("{http://www.w3.org/2005/Atom}entry")
            if entry is None: return None
            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
            authors = [a.find("{http://www.w3.org/2005/Atom}name").text for a in entry.findall("{http://www.w3.org/2005/Atom}author")]
            year = int(entry.find("{http://www.w3.org/2005/Atom}published").text[:4])
            return {"title": title, "authors": authors, "year": year, "venue": "arXiv", "abstract": summary, "references": []}
    except Exception:
        return None

def enrich(doi: str | None, arxiv_id: str | None) -> dict | None:
    if doi:
        res = lookup_crossref(doi)
        if res: return res
        res = lookup_semantic_scholar(doi)
        if res: return res
    if arxiv_id:
        res = lookup_arxiv(arxiv_id)
        if res: return res
        res = lookup_semantic_scholar(arxiv_id)
        if res: return res
    return None

# --- Tagging ---
def extract_tags(title: str, abstract: str | None, full_text: str, pdf_keywords: list[str], top_n: int = 8) -> list[dict]:
    tags = []
    seen = set()
    
    for kw in pdf_keywords:
        k = kw.lower().strip()
        if k and len(k.split()) <= 3 and k not in seen:
            tags.append({"name": k, "source": "pdf_keywords"})
            seen.add(k)
            
    text = f"{title}\n{abstract or ''}\n{full_text[:3000]}"
    kw_extractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.9, top=top_n, windowsSize=1)
    yake_kws = kw_extractor.extract_keywords(text)
    
    for kw, score in yake_kws:
        k = kw.lower().strip()
        if k and k not in seen:
            tags.append({"name": k, "source": "yake"})
            seen.add(k)
            
    return tags[:top_n]

# --- Graph ---
def add_paper_to_graph(conn, paper: dict, authors: list[tuple[int, str]], tags: list[tuple[int, str]], citations: list[dict]) -> None:
    node_id = paper["node_id"]
    props = json.dumps({"in_library": True, "paper_id": paper["id"], "year": paper.get("year")})
    
    conn.execute("INSERT OR REPLACE INTO nodes (node_id, label, name, properties) VALUES (?, 'Paper', ?, ?)",
                 (node_id, paper["title"], props))
    
    for aid, aname in authors:
        conn.execute("INSERT OR IGNORE INTO nodes (node_id, label, name, properties) VALUES (?, 'Author', ?, '{}')", (f"author:{aid}", aname))
        conn.execute("INSERT OR IGNORE INTO edges (source_id, target_id, relation_type) VALUES (?, ?, 'AUTHORED_BY')", (node_id, f"author:{aid}"))
        
    for tid, tname in tags:
        conn.execute("INSERT OR IGNORE INTO nodes (node_id, label, name, properties) VALUES (?, 'Tag', ?, '{}')", (f"tag:{tid}", tname))
        conn.execute("INSERT OR IGNORE INTO edges (source_id, target_id, relation_type) VALUES (?, ?, 'HAS_TAG')", (node_id, f"tag:{tid}"))
        
    for c in citations:
        cid = c.get("cited_doi")
        if cid:
            c_node_id = f"work:{cid}"
        else:
            c_node_id = f"work:ref:{paper['id']}:{c['ref_index']}"
            
        conn.execute("INSERT OR IGNORE INTO nodes (node_id, label, name, properties) VALUES (?, 'Paper', ?, ?)",
                     (c_node_id, c.get("cited_title") or "Unknown", json.dumps({"in_library": False})))
        conn.execute("INSERT OR IGNORE INTO edges (source_id, target_id, relation_type) VALUES (?, ?, 'CITES')", (node_id, c_node_id))

def remove_paper_from_graph(conn, paper_id: int) -> None:
    paper = conn.execute("SELECT node_id FROM papers WHERE id=?", (paper_id,)).fetchone()
    if not paper: return
    node_id = paper["node_id"]
    
    conn.execute("DELETE FROM edges WHERE source_id=? OR target_id=?", (node_id, node_id))
    
    remaining = conn.execute("SELECT COUNT(*) FROM edges WHERE target_id=?", (node_id,)).fetchone()[0]
    if remaining > 0:
        conn.execute("UPDATE nodes SET properties=json_set(properties, '$.in_library', false, '$.paper_id', null) WHERE node_id=?", (node_id,))
    else:
        conn.execute("DELETE FROM nodes WHERE node_id=?", (node_id,))
        
    conn.execute("DELETE FROM nodes WHERE label='Author' AND node_id NOT IN (SELECT target_id FROM edges)")
    conn.execute("DELETE FROM nodes WHERE label='Tag' AND node_id NOT IN (SELECT target_id FROM edges)")
    conn.execute("DELETE FROM nodes WHERE node_id LIKE 'work:ref:%' AND node_id NOT IN (SELECT target_id FROM edges)")

def build_graph_json(conn, paper_id: int | None, tag: str | None, include_cited: bool) -> dict:
    nodes = {}
    edges = []
    
    rows = conn.execute("SELECT * FROM nodes").fetchall()
    for r in rows:
        props = json.loads(r["properties"])
        if not include_cited and not props.get("in_library"): continue
        if tag and r["label"] == 'Tag' and r["name"] != tag: continue
        
        group = "paper" if props.get("in_library") else ("cited" if r["label"] == "Paper" else r["label"].lower())
        nodes[r["node_id"]] = {
            "id": r["node_id"], "label": r["name"], "group": group,
            "title": str(props.get("year", "")), "paper_id": props.get("paper_id")
        }
        
    edge_rows = conn.execute("SELECT * FROM edges").fetchall()
    for e in edge_rows:
        if e["source_id"] in nodes and e["target_id"] in nodes:
            edges.append({"from": e["source_id"], "to": e["target_id"], "label": e["relation_type"]})
            
    stats = {"papers": 0, "authors": 0, "tags": 0, "cited": 0}
    for n in nodes.values():
        if n["group"] == "paper": stats["papers"] += 1
        elif n["group"] == "cited": stats["cited"] += 1
        elif n["group"] == "author": stats["authors"] += 1
        elif n["group"] == "tag": stats["tags"] += 1
        
    return {"nodes": list(nodes.values()), "edges": edges, "stats": stats}

# --- Pipeline ---
def process_upload(filename: str, data: bytes) -> dict:
    if not is_pdf_bytes(data):
        raise NotPdf()
    
    sha = sha256_bytes(data)
    stored_path = os.path.join(UPLOAD_DIR, f"{sha}.pdf")
    
    conn = get_conn()
    try:
        existing = conn.execute("SELECT id FROM papers WHERE sha256=?", (sha,)).fetchone()
        if existing:
            raise Duplicate(existing["id"])
            
        with open(stored_path, 'wb') as f:
            f.write(data)
            
        doc = extract_document(stored_path)
        meta_title = doc["meta"].get("title")
        title = detect_title(doc, meta_title)
        authors = detect_authors(doc, title)
        abstract = detect_abstract(doc["full_text"])
        pdf_kws = detect_keywords(doc["full_text"])
        refs = extract_references(doc["full_text"])
        
        doi = find_doi(doc["full_text"][:2000]) or find_doi(meta_title or "")
        arxiv_id = find_arxiv_id(doc["full_text"][:2000])
        
        if doi:
            existing_doi = conn.execute("SELECT id FROM papers WHERE doi=?", (doi,)).fetchone()
            if existing_doi:
                os.remove(stored_path)
                raise Duplicate(existing_doi["id"])
                
        enriched = enrich(doi, arxiv_id)
        if enriched:
            title = enriched.get("title") or title
            authors = enriched.get("authors") or authors
            abstract = enriched.get("abstract") or abstract
            if not refs and enriched.get("references"):
                refs = [{"index": i+1, "raw_text": r.get("title", ""), "doi": r.get("doi"), "title": r.get("title")} for i, r in enumerate(enriched["references"])]
                
        tags_data = extract_tags(title, abstract, doc["full_text"], pdf_kws)
        
        node_id = f"work:{doi}" if doi else f"work:sha:{sha[:16]}"
        
        conn.execute("""INSERT INTO papers (sha256, original_name, stored_path, title, abstract, doi, arxiv_id, year, venue, page_count, full_text, node_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                     (sha, filename, stored_path, title, abstract, doi, arxiv_id,
                      enriched.get("year") if enriched else None, enriched.get("venue") if enriched else None,
                      doc["page_count"], doc["full_text"], node_id))
        paper_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        author_ids = []
        for i, aname in enumerate(authors):
            name_key = aname.lower().strip()
            conn.execute("INSERT OR IGNORE INTO authors (name, name_key) VALUES (?, ?)", (aname, name_key))
            aid = conn.execute("SELECT id FROM authors WHERE name_key=?", (name_key,)).fetchone()[0]
            conn.execute("INSERT INTO paper_authors (paper_id, author_id, position) VALUES (?, ?, ?)", (paper_id, aid, i))
            author_ids.append((aid, aname))
            
        tag_ids = []
        for t in tags_data:
            conn.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (t["name"],))
            tid = conn.execute("SELECT id FROM tags WHERE name=?", (t["name"],)).fetchone()[0]
            conn.execute("INSERT INTO paper_tags (paper_id, tag_id, source) VALUES (?, ?, ?)", (paper_id, tid, t["source"]))
            tag_ids.append((tid, t["name"]))
            
        citations = []
        for r in refs:
            conn.execute("INSERT INTO citations (paper_id, ref_index, raw_text, cited_doi, cited_title) VALUES (?, ?, ?, ?, ?)",
                         (paper_id, r["index"], r["raw_text"], r.get("doi"), r.get("title")))
            citations.append(r)
            
        paper = conn.execute("SELECT * FROM papers WHERE id=?", (paper_id,)).fetchone()
        add_paper_to_graph(conn, dict(paper), author_ids, tag_ids, citations)
        log_activity(conn, "upload", paper_id, f"Uploaded {filename}", "ok")
        conn.commit()
        
        return {
            "id": paper_id, "title": title, "authors": authors, "year": paper["year"],
            "venue": paper["venue"], "doi": doi, "arxiv_id": arxiv_id,
            "tags": [t["name"] for t in tags_data], "page_count": doc["page_count"],
            "reference_count": len(refs), "enriched": enriched is not None,
            "created_at": paper["created_at"]
        }
    except Exception as e:
        conn.rollback()
        if os.path.exists(stored_path):
            os.remove(stored_path)
        if isinstance(e, Duplicate):
            log_activity(conn, "upload_rejected", None, f"duplicate: existing paper {e.extra['existing_id']}", "error")
        else:
            log_activity(conn, "upload_rejected", None, str(e), "error")
        conn.commit()
        raise
    finally:
        conn.close()

# ==============================================================================
# 5. FLASK APP & ROUTES
# ==============================================================================
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_MB * 1024 * 1024

init_db()

@app.errorhandler(AppError)
def handle_app_error(e):
    resp = {"error": {"code": e.code, "message": e.message}}
    if hasattr(e, 'extra'): resp["error"].update(e.extra)
    return jsonify(resp), e.status

@app.errorhandler(RequestEntityTooLarge)
def handle_large(e):
    return jsonify({"error": {"code": "file_too_large", "message": "File too large"}}), 413

@app.errorhandler(404)
def handle_404(e):
    if request.path.startswith('/api/'):
        return jsonify({"error": {"code": "not_found", "message": "Not found"}}), 404
    return INDEX_HTML

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": {"code": "internal_error", "message": "An internal error occurred"}}), 500

@app.route('/')
def index():
    return INDEX_HTML

@app.route('/api/papers', methods=['POST'])
def upload_paper():
    if 'file' not in request.files: raise NoFile()
    f = request.files['file']
    if not f.filename: raise NoFile()
    
    if not f.filename.lower().endswith('.pdf'): raise NotPdf()
    
    data = f.read()
    if len(data) > MAX_UPLOAD_MB * 1024 * 1024: raise FileTooLarge()
    
    if not is_pdf_bytes(data): raise NotPdf()
    
    paper = process_upload(secure_filename(f.filename), data)
    return jsonify({"paper": paper}), 201

@app.route('/api/papers', methods=['GET'])
def list_papers():
    q = request.args.get('q', '')
    tag = request.args.get('tag')
    year = request.args.get('year')
    sort = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')
    page = int(request.args.get('page', 1))
    per_page = min(int(request.args.get('per_page', 20)), 100)
    
    if sort not in ('created_at', 'title', 'year'): raise BadParameter("Invalid sort")
    if order not in ('asc', 'desc'): raise BadParameter("Invalid order")
    
    conn = get_conn()
    where_clauses = ["1=1"]
    params = []
    if q:
        where_clauses.append("(p.title LIKE ? OR p.abstract LIKE ? OR a.name LIKE ?)")
        params.extend([f"%{q}%"] * 3)
    if tag:
        where_clauses.append("t.name=?")
        params.append(tag)
    if year:
        where_clauses.append("p.year=?")
        params.append(int(year))
        
    where_sql = " AND ".join(where_clauses)
    
    total = conn.execute(f"""
        SELECT COUNT(DISTINCT p.id) FROM papers p 
        LEFT JOIN paper_authors pa ON p.id=pa.paper_id 
        LEFT JOIN authors a ON pa.author_id=a.id 
        LEFT JOIN paper_tags pt ON p.id=pt.paper_id 
        LEFT JOIN tags t ON pt.tag_id=t.id 
        WHERE {where_sql}
    """, params).fetchone()[0]
    
    query = f"""
        SELECT p.*, GROUP_CONCAT(DISTINCT a.name) as authors, GROUP_CONCAT(DISTINCT t.name) as tags 
        FROM papers p 
        LEFT JOIN paper_authors pa ON p.id=pa.paper_id 
        LEFT JOIN authors a ON pa.author_id=a.id 
        LEFT JOIN paper_tags pt ON p.id=pt.paper_id 
        LEFT JOIN tags t ON pt.tag_id=t.id 
        WHERE {where_sql}
        GROUP BY p.id ORDER BY p.{sort} {order} LIMIT ? OFFSET ?
    """
    params.extend([per_page, (page - 1) * per_page])
    rows = conn.execute(query, params).fetchall()
    
    items = []
    for r in rows:
        items.append({
            "id": r["id"], "title": r["title"], "authors": r["authors"].split(',') if r["authors"] else [],
            "year": r["year"], "doi": r["doi"], "tags": r["tags"].split(',') if r["tags"] else [],
            "page_count": r["page_count"]
        })
    conn.close()
    return jsonify({"items": items, "total": total, "page": page, "per_page": per_page})

@app.route('/api/papers/<int:id>', methods=['GET'])
def get_paper(id):
    conn = get_conn()
    p = conn.execute("SELECT * FROM papers WHERE id=?", (id,)).fetchone()
    if not p: raise NotFound()
    
    authors = [r["name"] for r in conn.execute("SELECT a.name FROM authors a JOIN paper_authors pa ON a.id=pa.author_id WHERE pa.paper_id=? ORDER BY pa.position", (id,)).fetchall()]
    tags = [r["name"] for r in conn.execute("SELECT t.name FROM tags t JOIN paper_tags pt ON t.id=pt.tag_id WHERE pt.paper_id=?", (id,)).fetchall()]
    refs = conn.execute("SELECT * FROM citations WHERE paper_id=? ORDER BY ref_index", (id,)).fetchall()
    
    cited_by = []
    if p["doi"] or p["title"]:
        cited_by = conn.execute("""
            SELECT id, title FROM papers WHERE id IN (
                SELECT paper_id FROM citations WHERE cited_doi=? OR cited_title=?
            )
        """, (p["doi"], p["title"])).fetchall()
    
    conn.close()
    return jsonify({"paper": {
        "id": p["id"], "title": p["title"], "abstract": p["abstract"], "authors": authors,
        "year": p["year"], "venue": p["venue"], "doi": p["doi"], "arxiv_id": p["arxiv_id"],
        "tags": tags, "page_count": p["page_count"], "original_name": p["original_name"],
        "references": [{"index": r["ref_index"], "raw_text": r["raw_text"], "doi": r["cited_doi"], "title": r["cited_title"]} for r in refs],
        "cited_by_in_library": [{"id": c["id"], "title": c["title"]} for c in cited_by],
        "created_at": p["created_at"]
    }})

@app.route('/api/papers/<int:id>', methods=['DELETE'])
def delete_paper(id):
    conn = get_conn()
    p = conn.execute("SELECT * FROM papers WHERE id=?", (id,)).fetchone()
    if not p: raise NotFound()
    
    remove_paper_from_graph(conn, id)
    conn.execute("DELETE FROM papers WHERE id=?", (id,))
    log_activity(conn, "delete", id, f"Deleted {p['title']}", "ok")
    conn.commit()
    conn.close()
    
    if os.path.exists(p["stored_path"]):
        os.remove(p["stored_path"])
        
    return jsonify({"deleted": True, "id": id})

@app.route('/api/papers/<int:id>/file', methods=['GET'])
def get_file(id):
    conn = get_conn()
    p = conn.execute("SELECT stored_path FROM papers WHERE id=?", (id,)).fetchone()
    conn.close()
    if not p: raise NotFound()
    return send_file(p["stored_path"], mimetype='application/pdf', as_attachment=False)

@app.route('/api/tags', methods=['GET'])
def list_tags():
    conn = get_conn()
    rows = conn.execute("SELECT t.name, COUNT(pt.paper_id) as count FROM tags t JOIN paper_tags pt ON t.id=pt.tag_id GROUP BY t.id ORDER BY count DESC").fetchall()
    conn.close()
    return jsonify({"items": [{"name": r["name"], "count": r["count"]} for r in rows]})

@app.route('/api/graph', methods=['GET'])
def get_graph():
    paper_id = request.args.get('paper_id', type=int)
    tag = request.args.get('tag')
    include_cited = request.args.get('include_cited', '1') == '1'
    
    conn = get_conn()
    data = build_graph_json(conn, paper_id, tag, include_cited)
    conn.close()
    return jsonify(data)

@app.route('/api/log', methods=['GET'])
def get_log():
    limit = min(int(request.args.get('limit', 50)), 200)
    conn = get_conn()
    rows = conn.execute("SELECT * FROM activity_log ORDER BY ts DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return jsonify({"items": [dict(r) for r in rows]})

# ==============================================================================
# 6. FRONTEND (HTML / CSS / JS)
# ==============================================================================
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Paper Graph</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/vis-network@9.1.9/styles/vis-network.css">
    <style>
        body { font-family: sans-serif; margin: 0; padding: 0; }
        header { background: #333; color: white; padding: 1rem; }
        header a { color: white; margin-right: 1rem; text-decoration: none; }
        #error-banner { background: #fdd; color: #900; padding: 1rem; text-align: center; display: none; }
        main { padding: 1rem; }
        section { margin-bottom: 2rem; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #f4f4f4; }
        button { padding: 5px 10px; cursor: pointer; }
        #upload-form { margin-bottom: 1rem; }
        #filter-bar { margin-bottom: 1rem; display: flex; gap: 10px; flex-wrap: wrap; }
        #pagination { margin-top: 1rem; display: flex; gap: 10px; align-items: center; }
        #graph-canvas { height: 70vh; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <header id="app-header">
        <nav>
            <a href="#/">Library</a>
            <a href="#/graph">Graph</a>
        </nav>
    </header>
    <div id="error-banner" role="alert"></div>
    <main>
        <section id="view-library">
            <form id="upload-form">
                <input type="file" id="file-input" accept=".pdf,application/pdf" required>
                <button type="submit" id="upload-btn">Upload</button>
                <span id="upload-status"></span>
            </form>
            <div id="filter-bar">
                <input type="text" id="search-input" placeholder="Search...">
                <select id="tag-filter"><option value="">All Tags</option></select>
                <select id="sort-select">
                    <option value="created_at">Date</option>
                    <option value="title">Title</option>
                    <option value="year">Year</option>
                </select>
                <select id="order-select">
                    <option value="desc">Desc</option>
                    <option value="asc">Asc</option>
                </select>
            </div>
            <table id="paper-table">
                <thead><tr><th>Title</th><th>Authors</th><th>Year</th><th>Tags</th><th>Pages</th><th>Actions</th></tr></thead>
                <tbody id="paper-tbody"></tbody>
            </table>
            <div id="pagination">
                <button id="prev-page">Prev</button>
                <span id="page-info"></span>
                <button id="next-page">Next</button>
            </div>
        </section>
        
        <section id="view-detail" style="display:none;">
            <h2 id="detail-title"></h2>
            <p id="detail-meta"></p>
            <p id="detail-abstract"></p>
            <ul id="detail-tags"></ul>
            <ol id="detail-references"></ol>
            <div id="detail-actions">
                <button id="delete-btn">Delete</button>
                <a id="graph-link" href="#/graph">Show in Graph</a>
                <a id="pdf-link" target="_blank">Open PDF</a>
            </div>
        </section>
        
        <section id="view-graph" style="display:none;">
            <div id="graph-filters">
                <select id="graph-tag-filter"><option value="">All Tags</option></select>
                <label><input type="checkbox" id="graph-include-cited" checked> Include Cited</label>
                <button id="graph-refresh">Refresh</button>
            </div>
            <div id="graph-canvas"></div>
            <div id="graph-legend"></div>
            <p id="graph-stats"></p>
        </section>
    </main>
    <footer>
        <details id="log-panel">
            <summary>Activity Log</summary>
            <ul id="log-list"></ul>
        </details>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/vis-network@9.1.9/dist/vis-network.min.js"></script>
    <script>
        const Api = {
            async request(method, url, body) {
                try {
                    const opts = { method, headers: {} };
                    if (body && !(body instanceof FormData)) {
                        opts.headers['Content-Type'] = 'application/json';
                        opts.body = JSON.stringify(body);
                    } else if (body instanceof FormData) {
                        opts.body = body;
                    }
                    const res = await fetch(url, opts);
                    const data = await res.json().catch(() => ({}));
                    if (!res.ok) {
                        throw { code: data.error?.code || 'unknown', message: data.error?.message || 'Error', status: res.status };
                    }
                    return data;
                } catch (e) {
                    if (e.code) throw e;
                    throw { code: 'network', message: 'Cannot reach the server.', status: 0 };
                }
            },
            upload(file) {
                const fd = new FormData();
                fd.append('file', file);
                return this.request('POST', '/api/papers', fd);
            },
            listPapers(params) {
                const q = new URLSearchParams(params).toString();
                return this.request('GET', `/api/papers?${q}`);
            },
            getPaper(id) { return this.request('GET', `/api/papers/${id}`); },
            deletePaper(id) { return this.request('DELETE', `/api/papers/${id}`); },
            listTags() { return this.request('GET', '/api/tags'); },
            getGraph(params) {
                const q = new URLSearchParams(params).toString();
                return this.request('GET', `/api/graph?${q}`);
            },
            getLog() { return this.request('GET', '/api/log?limit=50'); }
        };

        const Ui = {
            showError(msg) {
                const el = document.querySelector('#error-banner');
                el.textContent = msg;
                el.style.display = 'block';
                setTimeout(() => this.clearError(), 5000);
            },
            clearError() {
                document.querySelector('#error-banner').style.display = 'none';
            },
            escapeHtml(s) {
                const div = document.createElement('div');
                div.textContent = s;
                return div.innerHTML;
            }
        };

        const Library = {
            page: 1,
            init() {
                document.querySelector('#upload-form').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const fileInput = document.querySelector('#file-input');
                    const btn = document.querySelector('#upload-btn');
                    const status = document.querySelector('#upload-status');
                    if (!fileInput.files.length) return;
                    
                    btn.disabled = true;
                    status.textContent = 'Uploading...';
                    try {
                        await Api.upload(fileInput.files[0]);
                        status.textContent = 'Success!';
                        fileInput.value = '';
                        this.load();
                    } catch (err) {
                        Ui.showError(err.message);
                        status.textContent = 'Failed';
                    } finally {
                        btn.disabled = false;
                    }
                });
                
                ['search-input', 'tag-filter', 'sort-select', 'order-select'].forEach(id => {
                    document.querySelector(`#${id}`).addEventListener('change', () => { this.page = 1; this.load(); });
                });
                document.querySelector('#prev-page').addEventListener('click', () => { if(this.page>1){this.page--; this.load();} });
                document.querySelector('#next-page').addEventListener('click', () => { this.page++; this.load(); });
                
                this.loadTags();
                this.load();
            },
            async loadTags() {
                try {
                    const data = await Api.listTags();
                    const sel = document.querySelector('#tag-filter');
                    sel.innerHTML = '<option value="">All Tags</option>';
                    data.items.forEach(t => sel.add(new Option(`${t.name} (${t.count})`, t.name)));
                } catch(e) {}
            },
            async load() {
                const params = {
                    q: document.querySelector('#search-input').value,
                    tag: document.querySelector('#tag-filter').value,
                    sort: document.querySelector('#sort-select').value,
                    order: document.querySelector('#order-select').value,
                    page: this.page,
                    per_page: 20
                };
                try {
                    const data = await Api.listPapers(params);
                    const tbody = document.querySelector('#paper-tbody');
                    tbody.innerHTML = '';
                    if (data.items.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="6">No papers yet. Upload a PDF to begin.</td></tr>';
                    } else {
                        data.items.forEach(p => {
                            const tr = document.createElement('tr');
                            tr.innerHTML = `
                                <td><a href="#/paper/${p.id}">${Ui.escapeHtml(p.title)}</a></td>
                                <td>${Ui.escapeHtml(p.authors.join(', '))}</td>
                                <td>${p.year || ''}</td>
                                <td>${Ui.escapeHtml(p.tags.join(', '))}</td>
                                <td>${p.page_count}</td>
                                <td><a href="#/paper/${p.id}">View</a></td>
                            `;
                            tbody.appendChild(tr);
                        });
                    }
                    document.querySelector('#page-info').textContent = `Page ${data.page} of ${Math.ceil(data.total / data.per_page) || 1}`;
                } catch (err) {
                    Ui.showError(err.message);
                }
            }
        };

        const Detail = {
            async show(id) {
                try {
                    const data = await Api.getPaper(id);
                    const p = data.paper;
                    document.querySelector('#detail-title').textContent = p.title;
                    document.querySelector('#detail-meta').textContent = `${p.authors.join(', ')} | ${p.year || ''} | ${p.venue || ''} | DOI: ${p.doi || 'N/A'}`;
                    document.querySelector('#detail-abstract').textContent = p.abstract || '';
                    
                    const tagsUl = document.querySelector('#detail-tags');
                    tagsUl.innerHTML = '';
                    p.tags.forEach(t => {
                        const li = document.createElement('li');
                        li.textContent = t;
                        tagsUl.appendChild(li);
                    });
                    
                    const refsOl = document.querySelector('#detail-references');
                    refsOl.innerHTML = '';
                    p.references.forEach(r => {
                        const li = document.createElement('li');
                        li.textContent = r.raw_text;
                        refsOl.appendChild(li);
                    });
                    
                    document.querySelector('#delete-btn').onclick = async () => {
                        if (confirm('Delete this paper?')) {
                            await Api.deletePaper(id);
                            location.hash = '#/';
                        }
                    };
                    document.querySelector('#pdf-link').href = `/api/papers/${id}/file`;
                    document.querySelector('#graph-link').href = `#/graph?paper_id=${id}`;
                } catch (err) {
                    Ui.showError(err.message);
                }
            }
        };

        const GraphView = {
            network: null,
            async show(params) {
                try {
                    const data = await Api.getGraph(params);
                    const container = document.querySelector('#graph-canvas');
                    container.innerHTML = ''; 
                    
                    if (data.nodes.length === 0) {
                        container.innerHTML = '<p style="text-align:center; padding-top: 30vh;">No graph data. Upload papers to see the knowledge graph.</p>';
                        document.querySelector('#graph-stats').textContent = '';
                        return;
                    }

                    const nodes = new vis.DataSet(data.nodes.map(n => ({
                        id: n.id, label: n.label, group: n.group, title: n.title, paper_id: n.paper_id
                    })));
                    const edges = new vis.DataSet(data.edges);
                    
                    const options = {
                        nodes: { shape: 'dot', size: 16 },
                        edges: { arrows: { to: { enabled: true, scaleFactor: 0.5 } } },
                        groups: {
                            paper: { color: { background: '#2196F3' } },
                            cited: { color: { background: '#9E9E9E' } },
                            author: { color: { background: '#4CAF50' } },
                            tag: { color: { background: '#FF9800' } }
                        }
                    };
                    
                    if (this.network) this.network.destroy();
                    this.network = new vis.Network(container, { nodes, edges }, options);
                    
                    this.network.on('click', (p) => {
                        if (p.nodes.length > 0) {
                            const node = nodes.get(p.nodes[0]);
                            if (node.group === 'paper' && node.paper_id) {
                                location.hash = `#/paper/${node.paper_id}`;
                            }
                        }
                    });
                    
                    document.querySelector('#graph-stats').textContent = `Papers: ${data.stats.papers}, Authors: ${data.stats.authors}, Tags: ${data.stats.tags}, Cited: ${data.stats.cited}`;
                } catch (err) {
                    Ui.showError(err.message);
                }
            }
        };

        const Router = {
            start() {
                const route = () => {
                    document.querySelectorAll('main section').forEach(s => s.style.display = 'none');
                    Ui.clearError();
                    const hash = location.hash.slice(1) || '/';
                    const [path, query] = hash.split('?');
                    const params = new URLSearchParams(query || '');
                    
                    if (path.startsWith('/paper/')) {
                        document.querySelector('#view-detail').style.display = 'block';
                        Detail.show(path.split('/')[2]);
                    } else if (path === '/graph') {
                        document.querySelector('#view-graph').style.display = 'block';
                        GraphView.show(params);
                    } else {
                        document.querySelector('#view-library').style.display = 'block';
                        Library.init();
                    }
                    this.loadLog();
                };
                
                window.addEventListener('hashchange', route);
                route();
            },
            async loadLog() {
                try {
                    const data = await Api.getLog();
                    const ul = document.querySelector('#log-list');
                    ul.innerHTML = '';
                    data.items.forEach(l => {
                        const li = document.createElement('li');
                        li.textContent = `${l.ts} - ${l.action}: ${l.detail} (${l.status})`;
                        ul.appendChild(li);
                    });
                } catch(e) {}
            }
        };

        document.addEventListener('DOMContentLoaded', () => Router.start());
    </script>
</body>
</html>
"""

# ==============================================================================
# 7. MAIN
# ==============================================================================
if __name__ == '__main__':
    print("Starting Paper Graph App on http://127.0.0.1:5000")
    app.run(debug=False, use_reloader=False, port=8080)