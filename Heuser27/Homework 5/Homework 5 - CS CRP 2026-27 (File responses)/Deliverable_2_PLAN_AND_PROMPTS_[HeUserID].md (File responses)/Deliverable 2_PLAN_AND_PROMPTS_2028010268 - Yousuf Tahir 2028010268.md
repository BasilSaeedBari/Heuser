| Area                            | Library / technology                | Exact version                   | Purpose                                                      | Why chosen over alternatives                                 | Key implementation notes / gotchas                           | Official source                                              |
| ------------------------------- | ----------------------------------- | ------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Web framework                   | Flask                               | 3.1.3                           | Routes, HTML pages, JSON APIs, static files, PDF uploads     | Lightweight and simpler than FastAPI for a small form-based app; mature  upload and static-file support | Use enctype="multipart/form-data"; set MAX_CONTENT_LENGTH;  sanitize filenames with secure_filename; validate actual PDF content, not  just extension | https://flask.palletsprojects.com/en/stable/changes/         |
| Uploads                         | Werkzeug via Flask                  | Bundled with Flask              | Secure filename handling and upload support                  | Included with Flask; avoids an extra upload-specific dependency | Never trust client filenames; store uploads outside the static directory;  use request.files | https://flask.palletsprojects.com/en/stable/patterns/fileuploads/ |
| CORS                            | flask-cors                          | Pin at install time             | Allow browser requests from another origin                   | Needed only if the frontend is served from a different origin than Flask | Do not enable broad * CORS in production; restrict origins and methods | https://flask-cors.readthedocs.io/                           |
| PDF text/layout extraction      | PyMuPDF                             | Pin at install time             | Primary extraction of text, layout blocks, metadata, and page rendering  from academic PDFs | Best default for two-column papers; strong layout/block extraction and  performance compared with pypdf | Extract by page and block; preserve reading order carefully; use for  metadata plus first-page DOI/title detection | https://pymupdf.readthedocs.io/en/latest/about.html          |
| PDF tables / fine layout        | pdfplumber                          | 0.11.10                         | Optional table extraction and word/line coordinate analysis  | Better than PyMuPDF when tables or precise positional layout are the  priority | Use only for PDFs where tables matter; it complements rather than  replaces PyMuPDF | https://pypi.org/project/pdfplumber/ pymupdf.readthedocs+1   |
| PDF basic operations            | pypdf                               | 6.21.2                          | Metadata, page count, splitting, merging, simple text extraction | Actively maintained successor to deprecated PyPDF2           | Not the primary choice for complex two-column extraction; use PyMuPDF for  that | https://pypi.org/project/pypdf/ pypi                         |
| Deprecated PDF library          | PyPDF2                              | Do not use                      | Former PDF library                                           | Deprecated and merged/succeeded by pypdf in 2023             | Do not add to new projects; migrate imports from PyPDF2 to pypdf | https://pypi.org/project/pypdf/                              |
| HTTP client                     | httpx                               | Pin at install time             | Calls to Crossref, OpenAlex, Semantic Scholar, and arXiv     | Modern Python HTTP client with timeouts, connection pooling, and  sync/async support | Always set timeouts; retry on 429/5xx with exponential backoff; include a  descriptive User-Agent | https://pypi.org/project/httpx/                              |
| Metadata API: Crossref          | Crossref REST API                   | API, not a Python package       | DOI lookup and bibliographic metadata                        | Authoritative DOI metadata source; JSON responses            | Endpoint: https://api.crossref.org/v1/works/{doi}; add  mailto=you@example.com; public: 5 req/s single records and 1 req/s lists;  polite: 10 req/s single records and 3 req/s lists | https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/ |
| Metadata API: OpenAlex          | OpenAlex API                        | API, not a Python package       | Works, authors, institutions, citations, open-access metadata | Broad scholarly graph with straightforward JSON REST endpoints | Endpoint: https://api.openalex.org/works?search=...; response has meta  and results; default page size 25, maximum 100 | https://help.openalex.org/api/                               |
| Metadata API: Semantic Scholar  | Semantic Scholar Academic Graph API | API, not a Python package       | Paper search, paper details, citations, references           | Useful for citation graphs and paper-level fields            | Endpoint: https://api.semanticscholar.org/graph/v1/paper/{paper_id}; use  fields=; response max 10 MB; unauthenticated traffic is subject to shared  throttling | https://api.semanticscholar.org/api-docs                     |
| Metadata API: arXiv             | arXiv API                           | API, not a Python package       | Preprint search and metadata                                 | Best source for arXiv preprints                              | Endpoint: https://export.arxiv.org/api/query?search_query=...; returns  Atom XML, not JSON; parse with feedparser or xml.etree.ElementTree | https://info.arxiv.org/help/api/                             |
| Local database                  | sqlite3                             | Python standard library         | Store documents, extracted text, metadata, tags, and graph edges | Zero extra dependency and sufficient for a small local app   | Use parameterized queries with ?; do not format SQL strings with user  input | https://docs.python.org/3/library/sqlite3.html               |
| SQL safety                      | sqlite3 parameter binding           | Standard library feature        | SQL injection prevention                                     | Official SQLite/Python pattern; safer than string interpolation | Use cur.execute("... VALUES (?, ?, ?)", values); allowlist  dynamic column/sort names | https://docs.python.org/3/library/sqlite3.html               |
| ORM alternative                 | SQLAlchemy                          | Optional; pin at install time   | Only if the data model becomes complex                       | Use only when migrations, relationships, or multiple databases justify  the extra complexity | Not recommended for the initial small app; standard sqlite3 is simpler | https://www.sqlalchemy.org/                                  |
| Keyword extraction              | KeyBERT                             | 0.9.0                           | Semantic keyword/tag extraction from PDF text                | Good local semantic keyword extraction; maintained release from February  2025 | Requires a transformer/sentence-transformer model download on first use;  not ideal for a minimal offline install | https://pypi.org/project/keybert/                            |
| Lightweight keyword alternative | YAKE or RAKE                        | Pin at install time             | Fast, local keyword extraction without large models          | No large model downloads; suitable for a lightweight app     | Lower semantic quality than KeyBERT; useful for initial automatic tags | https://pypi.org/project/yake/ / https://pypi.org/project/rake-nltk/ |
| Graph visualization             | vis-network                         | 9.1.9                           | Citation/reference/entity graph in the browser               | Simple nodes/edges model; mature; easy CDN integration       | Requires both JS and CSS; use pinned CDN URLs; feed { nodes: [], edges:  [] } | https://github.com/visjs/vis-network/                        |
| Graph CDN JS                    | vis-network JS via jsDelivr         | 9.1.9                           | Browser graph rendering                                      | Exact version pinning avoids breaking changes                | https://cdn.jsdelivr.net/npm/vis-network@9.1.9/dist/vis-network.min.js | https://www.jsdelivr.com/documentation                       |
| Graph CDN CSS                   | vis-network CSS via jsDelivr        | 9.1.9                           | Required default graph styling                               | vis-network documentation states that its CSS file is required | https://cdn.jsdelivr.net/npm/vis-network@9.1.9/styles/vis-network.css | https://visjs.github.io/vis-network/docs/network/            |
| Alternative graph library       | Cytoscape.js                        | Pin current 3.x at install time | Optional richer graph styling and analysis                   | More powerful than vis-network, but heavier for this use case | Data uses an elements array of node/edge objects; no separate CSS is  required for core rendering | https://js.cytoscape.org/                                    |

# STACK TABLE







# Implementation Plan: Academic Paper PDF Extraction & Knowledge Graph App

Executor: Qwen 2.5 Coder 7B (small model, limited effective context).
Every build prompt in Section 8 is self-contained, produces ONE file (or one small group of functions) and states all interfaces explicitly.

> **Assumption notice.** Requirements F1–F10 were not included in the brief I received (only F11, F12 and Section 5). Section 1.3 lists the F1–F10 I inferred from the context pack and stack table. If your real list differs, only Section 1.3 and the matching endpoints need to change.

---

## 1. Overview & Design Decisions

### 1.1 What the app does
A local, web-based tool. The user uploads academic PDFs. The backend extracts text and structure (title, authors, abstract, keywords, DOI/arXiv ID, references), optionally enriches metadata from public scholarly APIs, auto-tags the paper, and stores everything in SQLite. A knowledge graph (papers, authors, tags, cited works) is maintained in SQLite and rendered in the browser with vis-network.

### 1.2 Key design decisions

| # | Decision | Reason |
|---|----------|--------|
| D1 | Flask 3.1.3 + plain `sqlite3`, no ORM | Smallest surface area for a 7B model; fewer abstractions to get wrong. |
| D2 | PyMuPDF is the only extractor used in the main path | Best two-column handling; pdfplumber/pypdf are not needed. PyPDF2 is never used. |
| D3 | **Graph storage = generic `nodes` + `edges` tables in SQLite** (not NetworkX, not a graph DB, not derived on the fly) | Matches the context pack schema; survives restarts; one query produces vis-network JSON; consistency with the relational tables is enforced inside one transaction. |
| D4 | One shared node id scheme for "works" (`work:<doi>`), so a cited reference and an uploaded paper become the same node when their DOIs match | Citation links between uploaded papers appear automatically. |
| D5 | YAKE for tagging (KeyBERT optional, off by default) | No model download; works offline. |
| D6 | External APIs (Crossref → Semantic Scholar → arXiv) are best-effort. Failures never fail an upload | Offline use must work; F12 requires graceful behaviour. |
| D7 | Frontend: one `index.html`, hash routing, vanilla ES6 modules-free scripts, vis-network from jsDelivr CDN | Section 5.2: no build, no Node, no frameworks. |
| D8 | Flask serves both the API and the static frontend (same origin) | flask-cors is then unnecessary and is NOT installed. |
| D9 | Uploads stored in `data/uploads/<sha256>.pdf`, outside `static/` | Never serve raw uploads by guessable client filename. |
| D10 | Duplicate detection by SHA-256 of file bytes, plus unique DOI | Satisfies F12 duplicates. |

### 1.3 Functional requirements used (F1–F10 inferred; F11–F12 given)

| ID | Requirement |
|----|-------------|
| F1 | Upload a PDF through the browser |
| F2 | Extract text page by page, correct reading order for two columns, fix hyphenation |
| F3 | Detect title, authors, abstract, keywords |
| F4 | Detect DOI and arXiv ID |
| F5 | Enrich metadata from Crossref / Semantic Scholar / arXiv when an identifier exists |
| F6 | Extract the reference list |
| F7 | Auto-generate topic tags |
| F8 | List, search and filter papers |
| F9 | Paper detail view |
| F10 | Interactive knowledge graph (papers, authors, tags, cited works) |
| F11 | Delete a paper and keep graph and database consistent |
| F12 | Handle bad input: non-PDF, scanned PDF without text, duplicates; clear error messages |

### 1.4 Constraints (Section 5, restated for the executor)
- Python backend, SQLite, libraries via pip listed in `requirements.txt`.
- FORBIDDEN anywhere in the project: Node.js, Bun, Deno, npm/yarn/pnpm, `package.json`, `node_modules`, Vite/Webpack/Babel/TypeScript, React/Vue/Angular/JSX.
- Frontend: HTML5 + CSS3 + vanilla ES6+ only; DOM via `document.querySelector`, `fetch`, etc.
- Third-party browser libraries only via CDN `<script>`/`<link>` tags (vis-network only).
- No build step for backend or frontend.

---

## 2. Technology Table

| Area | Library | Exact version | Purpose | Gotchas |
|------|---------|---------------|---------|---------|
| Web framework | Flask | 3.1.3 | Routes, static files, uploads | `MAX_CONTENT_LENGTH`; `secure_filename`; verify `%PDF-` magic bytes, not just extension |
| Uploads | Werkzeug (bundled with Flask) | bundled | Filename handling | Never trust client filenames; store outside `static/` |
| PDF extraction | PyMuPDF (`import fitz`) | pin at install (`pip freeze`) | Text blocks, metadata, page count | Sort blocks by column then y; AGPL license noted |
| HTTP client | httpx | pin at install | Crossref, Semantic Scholar, arXiv | Always set timeout; retry 429/5xx with backoff; set User-Agent |
| Keywords | YAKE | pin at install | Local keyword extraction | Weaker than KeyBERT; no download |
| Keywords (optional) | KeyBERT | 0.9.0 | Semantic keywords | Downloads a model on first use; disabled by default |
| Database | sqlite3 | stdlib | Storage | Parameterized `?` queries only; `PRAGMA foreign_keys=ON` per connection |
| Graph rendering | vis-network JS | 9.1.9 | Browser graph | `https://cdn.jsdelivr.net/npm/vis-network@9.1.9/dist/vis-network.min.js` |
| Graph CSS | vis-network CSS | 9.1.9 | Required styling | `https://cdn.jsdelivr.net/npm/vis-network@9.1.9/styles/vis-network.css` |
| Metadata API | Crossref REST | n/a | `GET https://api.crossref.org/v1/works/{doi}?mailto=...` | Polite pool needs `mailto` |
| Metadata API | Semantic Scholar Graph | n/a | `GET https://api.semanticscholar.org/graph/v1/paper/{id}?fields=...` | Shared throttling when unauthenticated |
| Metadata API | arXiv | n/a | `GET https://export.arxiv.org/api/query?id_list=...` | Returns Atom XML; parse with `xml.etree.ElementTree` |

**Not used:** PyPDF2 (deprecated), pypdf, pdfplumber, flask-cors, SQLAlchemy, Cytoscape.js, OpenAlex. Keep them out of `requirements.txt` to reduce what the executor can wander into.

`requirements.txt` (pin the starred lines after first install with `pip freeze`):
```
Flask==3.1.3
PyMuPDF      # pin at install
httpx        # pin at install
yake         # pin at install
```

---

## 3. Architecture

### 3.1 Folder tree and responsibilities

```
paper_graph/
├── app.py                  # Flask app factory, registers blueprints, serves index.html, error handlers
├── config.py               # Constants: paths, MAX_UPLOAD_MB, API timeouts, MAILTO, USER_AGENT
├── errors.py               # AppError + subclasses (code, message, http status)
├── db.py                   # get_conn(), init_db(), log_activity()
├── schema.sql              # All CREATE TABLE / INDEX statements
├── requirements.txt
├── services/
│   ├── __init__.py
│   ├── pdf_extract.py      # SHA-256, PDF magic check, page/block extraction, scanned detection, full_text
│   ├── structure.py        # title, authors, abstract, keywords, references detection
│   ├── identifiers.py      # DOI and arXiv ID regexes and normalisation
│   ├── metadata_api.py     # Crossref / Semantic Scholar / arXiv lookups, normalised output
│   ├── tagging.py          # YAKE tag extraction
│   ├── graph.py            # add_paper_to_graph, remove_paper_from_graph, build_graph_json
│   └── pipeline.py         # process_upload(): orchestrates everything in one transaction
├── routes/
│   ├── __init__.py
│   ├── papers.py           # /api/papers* blueprint
│   └── graph.py            # /api/graph, /api/tags, /api/log blueprint
├── static/
│   ├── index.html          # Single page, three views
│   ├── css/style.css
│   └── js/
│       ├── api.js          # fetch wrappers, error normalisation
│       ├── ui.js           # toast/error banner helpers, escapeHtml
│       ├── library.js      # upload form + paper table + search
│       ├── detail.js       # paper detail view
│       ├── graph.js        # vis-network setup
│       └── main.js         # hash router, boot
├── data/                   # runtime only: papers.db, uploads/  (git-ignored)
└── tests/
    └── test_smoke.py       # optional, small
```

### 3.2 Data flow: upload to graph

1. Browser `POST /api/papers` (multipart, field `file`).
2. `routes/papers.py` checks a file exists, extension `.pdf`, size ≤ limit; reads bytes.
3. `pdf_extract.is_pdf_bytes()` verifies `%PDF-` header → else 415 `not_pdf`.
4. `pdf_extract.sha256_bytes()` → if hash already in `papers` → 409 `duplicate`.
5. Save to `data/uploads/<sha>.pdf`.
6. `pdf_extract.extract_document()` → pages, `full_text`. If text is too small (scanned) → delete saved file, 422 `no_text_layer`. Unreadable/corrupt → 422 `unreadable_pdf`.
7. `structure.*` detect title, authors, abstract, keywords, references.
8. `identifiers.*` find DOI / arXiv ID in first 2 pages of text and PDF metadata. If DOI exists in `papers` → delete saved file, 409 `duplicate`.
9. `metadata_api.enrich()` (best effort) fills missing title/authors/year/venue/abstract and a reference list if local extraction found none.
10. `tagging.extract_tags()` from title + abstract + first 3000 words.
11. One DB transaction: insert `papers`, `authors`, `paper_authors`, `tags`, `paper_tags`, `citations`; then `graph.add_paper_to_graph()`; then `log_activity('upload', ...)`.
12. Respond 201 with the paper summary JSON.
13. Browser refreshes the table; the graph view calls `GET /api/graph`.

Deletion (F11): `DELETE /api/papers/<id>` → one transaction: `graph.remove_paper_from_graph()`, delete paper row (cascades), delete orphan authors/tags, log activity; then delete the file from disk after commit.

---

## 4. Database Schema (`schema.sql`)

Every connection runs `PRAGMA foreign_keys = ON;`.

```sql
CREATE TABLE IF NOT EXISTS papers (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    sha256        TEXT    NOT NULL UNIQUE,
    original_name TEXT    NOT NULL,
    stored_path   TEXT    NOT NULL,
    title         TEXT    NOT NULL,
    abstract      TEXT,
    doi           TEXT,                     -- lower-case, no URL prefix
    arxiv_id      TEXT,
    year          INTEGER,
    venue         TEXT,
    page_count    INTEGER NOT NULL,
    full_text     TEXT    NOT NULL,
    node_id       TEXT    NOT NULL UNIQUE,  -- 'work:<doi>' or 'work:sha:<first 16 of sha256>'
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_papers_doi ON papers(doi) WHERE doi IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_papers_year    ON papers(year);
CREATE INDEX IF NOT EXISTS ix_papers_title   ON papers(title);
CREATE INDEX IF NOT EXISTS ix_papers_created ON papers(created_at);

CREATE TABLE IF NOT EXISTS authors (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL,
    name_key TEXT NOT NULL UNIQUE           -- lower-case, whitespace-collapsed
);

CREATE TABLE IF NOT EXISTS paper_authors (
    paper_id  INTEGER NOT NULL REFERENCES papers(id)  ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
    position  INTEGER NOT NULL,
    PRIMARY KEY (paper_id, author_id)
);
CREATE INDEX IF NOT EXISTS ix_pa_author ON paper_authors(author_id);

CREATE TABLE IF NOT EXISTS tags (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE               -- lower-case
);

CREATE TABLE IF NOT EXISTS paper_tags (
    paper_id INTEGER NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    tag_id   INTEGER NOT NULL REFERENCES tags(id)   ON DELETE CASCADE,
    source   TEXT NOT NULL DEFAULT 'yake',  -- 'yake' | 'pdf_keywords'
    PRIMARY KEY (paper_id, tag_id)
);
CREATE INDEX IF NOT EXISTS ix_pt_tag ON paper_tags(tag_id);

CREATE TABLE IF NOT EXISTS citations (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id  INTEGER NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    ref_index INTEGER NOT NULL,
    raw_text  TEXT    NOT NULL,
    cited_doi TEXT,
    cited_title TEXT,
    UNIQUE (paper_id, ref_index)
);
CREATE INDEX IF NOT EXISTS ix_cit_doi ON citations(cited_doi);

-- Graph storage (design decision D3)
CREATE TABLE IF NOT EXISTS nodes (
    node_id    TEXT PRIMARY KEY,            -- 'work:<doi>' | 'work:sha:<16hex>' | 'work:ref:<paper_id>:<n>' | 'author:<id>' | 'tag:<id>'
    label      TEXT NOT NULL CHECK (label IN ('Paper','Author','Tag')),
    name       TEXT NOT NULL,
    properties TEXT NOT NULL DEFAULT '{}'   -- JSON text, e.g. {"in_library": true, "paper_id": 3, "year": 2017}
);
CREATE INDEX IF NOT EXISTS ix_nodes_label ON nodes(label);

CREATE TABLE IF NOT EXISTS edges (
    edge_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id     TEXT NOT NULL REFERENCES nodes(node_id) ON DELETE CASCADE,
    target_id     TEXT NOT NULL REFERENCES nodes(node_id) ON DELETE CASCADE,
    relation_type TEXT NOT NULL CHECK (relation_type IN ('AUTHORED_BY','HAS_TAG','CITES')),
    weight        REAL NOT NULL DEFAULT 1.0,
    UNIQUE (source_id, target_id, relation_type)
);
CREATE INDEX IF NOT EXISTS ix_edges_source ON edges(source_id);
CREATE INDEX IF NOT EXISTS ix_edges_target ON edges(target_id);

CREATE TABLE IF NOT EXISTS activity_log (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ts        TEXT NOT NULL DEFAULT (datetime('now')),
    action    TEXT NOT NULL,                -- 'upload' | 'delete' | 'upload_rejected'
    paper_id  INTEGER,                      -- no FK: survives deletion
    detail    TEXT NOT NULL,
    status    TEXT NOT NULL CHECK (status IN ('ok','error'))
);
CREATE INDEX IF NOT EXISTS ix_log_ts ON activity_log(ts);
```

### Consistency rules (graph ↔ relational)
- Node id for a paper = `papers.node_id`. A cited work with a DOI uses `work:<doi>` too, so it merges with an uploaded paper that has that DOI. A cited work without a DOI uses `work:ref:<paper_id>:<ref_index>`.
- Cited-work nodes that are not in the library have `properties.in_library = false`. On upload of a paper whose `node_id` already exists as a stub, UPDATE the stub: `label='Paper'`, `in_library=true`, `paper_id` set.
- On delete: remove the paper's outgoing `AUTHORED_BY`, `HAS_TAG`, `CITES` edges. Then for the paper node: if other edges still point to it (it is cited by another library paper), keep the node and set `in_library=false`, `paper_id=null`; otherwise delete it. Delete `Author`/`Tag` nodes and rows with no remaining edges/links. Delete `work:ref:*` stubs with no incoming edges.
- All of this happens in one transaction; file deletion happens after commit.

---

## 5. API Contract

Base: same origin. All JSON except the PDF download. **Error shape for every non-2xx:**
```json
{ "error": { "code": "not_pdf", "message": "The uploaded file is not a valid PDF." } }
```
Unhandled exceptions return `500 internal_error` with a generic message (no stack trace).

### 5.1 `POST /api/papers`
Upload one PDF. Request: `multipart/form-data`, field `file`.

201 response:
```json
{
  "paper": {
    "id": 3,
    "title": "Attention Is All You Need",
    "authors": ["Ashish Vaswani", "Noam Shazeer"],
    "year": 2017,
    "venue": "NeurIPS",
    "doi": "10.48550/arxiv.1706.03762",
    "arxiv_id": "1706.03762",
    "tags": ["transformer", "attention mechanism"],
    "page_count": 15,
    "reference_count": 40,
    "enriched": true,
    "created_at": "2026-10-22 17:20:00"
  }
}
```
Errors:

| Status | code | When |
|--------|------|------|
| 400 | `no_file` | No `file` part or empty filename |
| 413 | `file_too_large` | Over `MAX_UPLOAD_MB` (default 25) |
| 415 | `not_pdf` | Wrong extension or missing `%PDF-` header |
| 422 | `unreadable_pdf` | PyMuPDF cannot open it (corrupt / encrypted) |
| 422 | `no_text_layer` | Scanned PDF: fewer than 50 characters per page on average |
| 409 | `duplicate` | Same SHA-256 or same DOI; body also contains `"existing_id": 2` |

### 5.2 `GET /api/papers`
Query: `q` (matches title/abstract/author, substring, case-insensitive), `tag`, `year`, `sort` in `created_at|title|year` (default `created_at`), `order` in `asc|desc` (default `desc`), `page` (default 1), `per_page` (default 20, max 100). Sort/order are allow-listed.
```json
{
  "items": [ { "id": 3, "title": "...", "authors": ["..."], "year": 2017, "doi": "...", "tags": ["..."], "page_count": 15 } ],
  "total": 1, "page": 1, "per_page": 20
}
```
400 `bad_parameter` for an invalid `sort`/`order`/number.

### 5.3 `GET /api/papers/<id>`
```json
{
  "paper": {
    "id": 3, "title": "...", "abstract": "...", "authors": ["..."], "year": 2017, "venue": "...",
    "doi": "...", "arxiv_id": "...", "tags": ["..."], "page_count": 15, "original_name": "1706.03762.pdf",
    "references": [ { "index": 1, "raw_text": "...", "doi": null, "title": null } ],
    "cited_by_in_library": [ { "id": 5, "title": "..." } ],
    "created_at": "..."
  }
}
```
404 `not_found`.

### 5.4 `DELETE /api/papers/<id>` (F11)
200: `{ "deleted": true, "id": 3 }`. 404 `not_found`. Graph, relational rows, orphan authors/tags and the stored file are all removed.

### 5.5 `GET /api/papers/<id>/file`
Returns the stored PDF (`application/pdf`, inline). 404 `not_found`.

### 5.6 `GET /api/tags`
`{ "items": [ { "name": "transformer", "count": 4 } ] }` sorted by count desc.

### 5.7 `GET /api/graph`
Query (all optional): `paper_id` (return only that paper and its neighbours), `tag`, `include_cited` (`1`/`0`, default `1`).
```json
{
  "nodes": [
    { "id": "work:10.1234/abc", "label": "Attention Is All You Need", "group": "paper", "title": "2017", "paper_id": 3 },
    { "id": "author:7", "label": "Ashish Vaswani", "group": "author" },
    { "id": "tag:12", "label": "transformer", "group": "tag" },
    { "id": "work:10.5555/xyz", "label": "Neural Machine Translation...", "group": "cited" }
  ],
  "edges": [
    { "from": "work:10.1234/abc", "to": "author:7", "label": "AUTHORED_BY" },
    { "from": "work:10.1234/abc", "to": "tag:12",   "label": "HAS_TAG" },
    { "from": "work:10.1234/abc", "to": "work:10.5555/xyz", "label": "CITES" }
  ],
  "stats": { "papers": 1, "authors": 1, "tags": 1, "cited": 1 }
}
```
Node `group` is `paper` (in library), `cited` (stub), `author`, or `tag`. Format is directly consumable by vis-network.

### 5.8 `GET /api/log?limit=50`
`{ "items": [ { "id": 9, "ts": "...", "action": "upload_rejected", "paper_id": null, "detail": "duplicate: existing paper 2", "status": "error" } ] }`

### 5.9 `GET /` and static
`GET /` returns `static/index.html`. Static files under `/static/...`.

---

## 6. Frontend Specification

### 6.1 CDN (the only external resources)
In `index.html` `<head>`:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/vis-network@9.1.9/styles/vis-network.css">
<link rel="stylesheet" href="/static/css/style.css">
```
Before `</body>`, in this order, plain `<script>` tags (no `type="module"`, no bundler):
```html
<script src="https://cdn.jsdelivr.net/npm/vis-network@9.1.9/dist/vis-network.min.js"></script>
<script src="/static/js/api.js"></script>
<script src="/static/js/ui.js"></script>
<script src="/static/js/library.js"></script>
<script src="/static/js/detail.js"></script>
<script src="/static/js/graph.js"></script>
<script src="/static/js/main.js"></script>
```
All scripts share globals: `Api` (api.js), `Ui` (ui.js), `Library`, `Detail`, `GraphView`, `Router`. No other global names.

### 6.2 Views (hash-routed)
| Hash | View | Content |
|------|------|---------|
| `#/` | Library | Upload form, search/filter bar, paper table, pagination |
| `#/paper/<id>` | Detail | Metadata, abstract, tags, reference list, delete button, "show in graph" link, "open PDF" link |
| `#/graph` | Graph | Filters + vis-network canvas + legend |

Activity log is a collapsible panel at the bottom of every view.

### 6.3 DOM structure (ids are the contract between JS files)
```
body
├── header#app-header            nav links: a[href="#/"], a[href="#/graph"]
├── div#error-banner             hidden by default; role="alert"; shows API error messages
├── main
│   ├── section#view-library
│   │   ├── form#upload-form     input#file-input[type=file accept=".pdf,application/pdf"], button#upload-btn, span#upload-status
│   │   ├── div#filter-bar       input#search-input, select#tag-filter, select#sort-select, select#order-select
│   │   ├── table#paper-table    thead (Title, Authors, Year, Tags, Pages, Actions) / tbody#paper-tbody
│   │   └── div#pagination       button#prev-page, span#page-info, button#next-page
│   ├── section#view-detail
│   │   ├── h2#detail-title, p#detail-meta, p#detail-abstract
│   │   ├── ul#detail-tags, ol#detail-references
│   │   └── div#detail-actions   button#delete-btn, a#graph-link, a#pdf-link
│   └── section#view-graph
│       ├── div#graph-filters    select#graph-tag-filter, input#graph-include-cited[type=checkbox], button#graph-refresh
│       ├── div#graph-canvas     (height 70vh)
│       └── div#graph-legend, p#graph-stats
└── footer
    └── details#log-panel > summary + ul#log-list
```

### 6.4 Behaviour rules
- `api.js`: `Api.request(method, url, body)` returns parsed JSON or throws `{code, message, status}` built from the `{"error": {...}}` body; network failure → `{code:"network", message:"Cannot reach the server."}`.
- Upload: disable button while uploading, show status text, on error call `Ui.showError(message)` (never `alert`), on success reload the table and clear the file input.
- Delete: `confirm()` dialog, then `DELETE`, then go to `#/`.
- Every string inserted into the DOM goes through `textContent` or `Ui.escapeHtml()`; never raw `innerHTML` with API data.
- Graph: `new vis.Network(container, {nodes: new vis.DataSet(...), edges: new vis.DataSet(...)}, options)`. Colors by `group`: paper = blue, cited = grey, author = green, tag = orange. Clicking a `paper` node with a `paper_id` navigates to `#/paper/<paper_id>`. Show an empty-state message when there are no nodes.
- Empty library shows "No papers yet. Upload a PDF to begin."

---

## 7. Cross-cutting Rules for the Executor

1. Python 3.10+ syntax allowed; type hints on all function signatures; a one-line docstring each.
2. SQL always parameterized with `?`; dynamic `ORDER BY` only from an allow-list dict.
3. Raise `AppError` subclasses (from `errors.py`) in services; routes never build error JSON by hand: `app.py` has one `@app.errorhandler(AppError)` and one for `Exception`.
4. Every external HTTP call: `httpx.Client(timeout=10, headers={"User-Agent": config.USER_AGENT})`, max 2 retries on 429/5xx with 1 s then 2 s sleeps, all exceptions caught and converted to `None`.
5. No file other than the ones in the tree may be created. No `package.json`, no Node tooling.
6. Use only the libraries listed in Section 2 plus the standard library.

---

## 8. Build Sequence for Qwen 2.5 Coder 7B

Build in this order (each depends only on files above it). **Prompt template** (prepend to each):

```
You are writing ONE Python/JS file for a Flask + SQLite app. Output only the complete file in a single
code block, no explanation. Do not use Node.js, npm, frameworks or build tools. Use only the libraries
named below. Implement exactly the interfaces listed; do not rename anything.
```

Each prompt below gives: FILE, INPUTS (what already exists, with signatures), TASK.

| # | File | Key interface the prompt must state |
|---|------|-------------------------------------|
| 1 | `requirements.txt`, `config.py` | `BASE_DIR, DATA_DIR, UPLOAD_DIR, DB_PATH, MAX_UPLOAD_MB=25, MIN_CHARS_PER_PAGE=50, HTTP_TIMEOUT=10, MAILTO, USER_AGENT`; creates dirs at import |
| 2 | `errors.py` | `class AppError(Exception): code:str; message:str; status:int`; subclasses `NoFile(400)`, `FileTooLarge(413)`, `NotPdf(415)`, `UnreadablePdf(422)`, `NoTextLayer(422)`, `Duplicate(409, existing_id)`, `NotFound(404)`, `BadParameter(400)` |
| 3 | `schema.sql`, `db.py` | Paste Section 4 SQL verbatim. `get_conn() -> sqlite3.Connection` (row_factory=Row, foreign_keys ON), `init_db() -> None`, `log_activity(conn, action:str, paper_id:int\|None, detail:str, status:str) -> None` |
| 4 | `services/identifiers.py` | `normalize_doi(s:str)->str`; `find_doi(text:str)->str\|None` using `10\.\d{4,9}/[-._;()/:A-Za-z0-9]+` and trimming trailing `.,;)`; `find_arxiv_id(text:str)->str\|None` matching `arXiv:\d{4}\.\d{4,5}(v\d+)?` or bare `\d{4}\.\d{4,5}` near "arXiv" |
| 5 | `services/pdf_extract.py` | `is_pdf_bytes(data:bytes)->bool`; `sha256_bytes(data:bytes)->str`; `extract_document(path:str)->dict` returning `{"page_count":int,"pages":[{"page":int,"width":float,"blocks":[{"x0","y0","x1","y1","text","size"}]}],"full_text":str,"meta":{"title":str\|None,"author":str\|None}}`. Use `page.get_text("dict")`; reading order = blocks wider than 60% of page width first by y, otherwise left column (x0 < width/2) by y then right column by y; join hyphenated line ends (`-\n` + lowercase); raise `UnreadablePdf` on open failure or `doc.needs_pass`; raise `NoTextLayer` if `len(full_text)/page_count < MIN_CHARS_PER_PAGE` |
| 6 | `services/structure.py` | `detect_title(doc:dict, meta_title:str\|None)->str` (largest font size on page 1; merge consecutive blocks within 1.5× line height; fallback to meta title, then `"Untitled"`); `detect_authors(doc:dict, title:str)->list[str]` (blocks directly under the title, split on `,`/` and `, drop lines containing `@`, `University`, digits-only); `detect_abstract(full_text:str)->str\|None` (text after a line `Abstract`/`In brief`/`Summary`, up to next heading or 2000 chars; fallback first 1000 words of body); `detect_keywords(full_text:str)->list[str]` (line starting `Keywords:`/`Index Terms`, split on `,`/`;`); `extract_references(full_text:str)->list[dict]` finds a heading `References`/`Bibliography`/`Notes` (last occurrence), splits entries on `[n]` or `n ` at line start, returns `[{"index":int,"raw_text":str,"doi":str\|None,"title":None}]` |
| 7 | `services/metadata_api.py` | `lookup_crossref(doi)`, `lookup_semantic_scholar(identifier)`, `lookup_arxiv(arxiv_id)` each return a dict `{"title","authors":list[str],"year":int\|None,"venue":str\|None,"abstract":str\|None,"references":list[{"doi","title"}]}` or `None`; `enrich(doi, arxiv_id)->dict\|None` tries Crossref (if doi), then Semantic Scholar (`DOI:<doi>` or `ARXIV:<id>`), then arXiv; rules from Section 7 item 4 |
| 8 | `services/tagging.py` | `extract_tags(title:str, abstract:str\|None, full_text:str, pdf_keywords:list[str], top_n:int=8)->list[dict]` returns `[{"name":str,"source":"yake"\|"pdf_keywords"}]`; lower-case, dedupe, max 3 words, pdf_keywords first |
| 9 | `services/graph.py` | `add_paper_to_graph(conn, paper:dict, authors:list[tuple[int,str]], tags:list[tuple[int,str]], citations:list[dict])->None`; `remove_paper_from_graph(conn, paper_id:int)->None`; `build_graph_json(conn, paper_id:int\|None, tag:str\|None, include_cited:bool)->dict` (shape in 5.7). Implements the consistency rules in Section 4 exactly. No commit inside these functions |
| 10 | `services/pipeline.py` | `process_upload(filename:str, data:bytes)->dict` implementing steps 3–11 of Section 3.2, returning the `paper` dict of 5.1. Owns the transaction and commit/rollback; removes the stored file on any failure after it was written; logs `upload` / `upload_rejected` |
| 11 | `routes/papers.py` | Blueprint `bp_papers` for 5.1–5.5; query-param validation with `BadParameter`; delete implemented via `graph.remove_paper_from_graph`, orphan cleanup, file removal after commit |
| 12 | `routes/graph.py` | Blueprint `bp_graph` for 5.6–5.8 |
| 13 | `app.py` | `create_app()`: `MAX_CONTENT_LENGTH`, `init_db()`, register blueprints, `/` serves `static/index.html`, handlers for `AppError`, `RequestEntityTooLarge` (→ `file_too_large`), `404` for `/api/*`, `Exception` |
| 14 | `static/index.html`, `static/css/style.css` | DOM from 6.3 with exact ids; CDN tags from 6.1; simple responsive CSS, error banner styled red |
| 15 | `static/js/api.js`, `static/js/ui.js` | `Api.request`, `Api.upload(file)`, `Api.listPapers(params)`, `Api.getPaper(id)`, `Api.deletePaper(id)`, `Api.listTags()`, `Api.getGraph(params)`, `Api.getLog()`; `Ui.showError(msg)`, `Ui.clearError()`, `Ui.escapeHtml(s)`, `Ui.el(tag, attrs, text)` |
| 16 | `static/js/library.js`, `static/js/detail.js` | `Library.init()`, `Library.load()`; `Detail.show(id)`; behaviour per 6.4 |
| 17 | `static/js/graph.js`, `static/js/main.js` | `GraphView.show(params)`; `Router.start()` handling the three hashes and toggling `section` visibility |
| 18 | `tests/test_smoke.py` (optional) | Flask test client: upload text-PDF → 201; upload `.txt` → 415; same PDF twice → 409; delete → 200 and graph empty |

### Prompt-size discipline
- Prompts 5, 6, 7, 9, 10 are the largest. If Qwen's output is truncated or wrong, split by function: ask for ONE function per prompt, keeping the signature list from the table above and pasting only the already-written helper signatures (not their bodies).
- After each file, run `python -c "import <module>"` (or open in browser for JS) before moving on.

---

## 9. Acceptance Checklist

- [ ] `pip install -r requirements.txt && python app.py` starts with no other step; no Node tooling anywhere in the tree.
- [ ] Two-column PDF: extracted text reads in correct order; hyphenated words are rejoined.
- [ ] Briefing-style PDF without "Abstract": "In brief" or first body paragraph is used; "Notes" section parsed as references.
- [ ] PDF with DOI and internet: metadata enriched; offline: upload still succeeds with local data.
- [ ] `.txt` renamed to `.pdf` → `not_pdf` (415) message shown in banner.
- [ ] Scanned PDF → `no_text_layer` (422), no file left in `data/uploads/`.
- [ ] Same PDF twice → `duplicate` (409) mentioning the existing paper.
- [ ] Graph shows paper, author, tag and cited-work nodes; clicking a paper node opens its detail.
- [ ] Delete paper: row, file, edges, orphan authors/tags gone; if another paper cited it, it remains as a grey "cited" node; reload of `/api/graph` consistent.
- [ ] All API errors use the `{"error": {...}}` shape; no stack traces reach the browser.
