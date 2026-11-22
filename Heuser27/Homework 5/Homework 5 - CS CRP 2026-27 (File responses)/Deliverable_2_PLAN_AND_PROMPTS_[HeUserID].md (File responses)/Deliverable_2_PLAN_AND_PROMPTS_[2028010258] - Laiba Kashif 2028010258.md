## A)PROJECT OVERVIEW AND DESIGN DECISIONS
The Research Paper Library & Knowledge Graph is a web-based research management system with a Python backend and an SQLite database. It processes uploaded research-paper PDFs using PDF text extraction and metadata-identification techniques, enriches available metadata through scholarly APIs such as Crossref, arXiv, Semantic Scholar, and OpenAlex, and assigns topic tags using available keywords, API-provided topics, and local keyword extraction. The application supports paper metadata editing, duplicate detection, reference matching, searching and filtering, activity logging, and interactive graph visualisation of paper-author-topic relationships. 
PLAN AND PROMPTS - Research Paper Library & Knowledge Graph
Student ID: 2028010258 · Course: [CS CRP] · Homework 5 · Phase 3 deliverable (written 22 October 2026)
Status legend used throughout this document
[Verified] - checked on 22 Oct 2026 against the official package page, release page or documentation named next to it.
[Phase 1] - taken from my `Deliverable_1_CONTEXT` document and not re-checked in Phase 3.
[Proposal] - a design choice made in this plan (not a research finding).
[Unverified] - could not be confirmed; stated so it is not mistaken for fact.
Nothing in this document records an implementation result. Sections I and J are blank on purpose and are filled in during Phase 4.
---
A. Overview and key design decisions
A.1 Project summary (planned, not yet built)
The Research Paper Library & Knowledge Graph will be a single-user, web-based application for organising research papers. A user enters a display name, uploads a research-paper PDF, and the application will: extract the text with PyMuPDF; parse the title, authors, abstract, keywords, year, DOI/arXiv ID and reference list with heuristics; enrich the metadata through scholarly APIs (Crossref, arXiv, OpenAlex, Semantic Scholar) when an identifier is found; assign topic tags; store everything in SQLite; and log every upload, edit, tag change and deletion with a user name and timestamp. The user can search and filter the library, open a paper to correct its metadata and tags, view the activity log, and explore an interactive knowledge graph of papers, authors and topics. The backend is Python (FastAPI) with SQLite; the frontend is plain HTML/CSS/JavaScript with Cytoscape.js loaded from a pinned CDN URL. There is no build step.
A.2 Confirmed requirements (what the plan must satisfy)
Source	Requirement
Assignment §4.3, F1-F12	Upload (F1), parse title/authors/abstract + DOI/arXiv/year/venue (F2), separate reference records (F3), automatic tags (F4), SQLite persistence (F5), user/action/timestamp log (F6), library search/filter (F7), detail view + manual correction (F8), graph with ≥3 node types that updates as papers are added (F9), activity view (F10), delete with consistency (F11), graceful handling of non-PDF, scanned and duplicate files (F12).
Assignment §5	Web-based; Python + SQLite; no build step; no Node.js/Bun/Deno/npm/`package.json`; vanilla HTML/CSS/ES6; no JS frameworks; CDN libraries only via pinned `<script src="https://cdn.jsdelivr.net/...">`.
Phase 1 §6 [Phase 1]	PyMuPDF for extraction; heuristics for metadata and references; scholarly APIs for enrichment. Not implemented: GROBID, AnyStyle, OCR, LLM-based extraction, embeddings/semantic search. Scanned PDFs without a text layer are rejected with a clear error.
Phase 1 §7 [Phase 1]	Tag priority: author keywords → API topics → YAKE; record the source of every tag.
Phase 1 §8 [Phase 1]	Nodes Paper/Author/Topic; edges `AUTHORED_BY`, `HAS_TOPIC`, `CITES` (stored) and `CO_AUTHOR`, `RELATED_TOPIC` (derived when the graph is built).
Phase 1 §9 [Phase 1]	Handle multi-line titles, two-column layouts, missing abstract/keywords/DOI, many authors, split references, duplicate uploads; use backoff for API rate limits.
A.3 Key design decisions
#	Decision	Choice	Basis
D1	Serving and CORS	FastAPI serves the API under `/api` and the static frontend at `/`, so the normal route has no CORS issue. `CORSMiddleware` is also enabled so `frontend/index.html` still works if opened from disk (`file://`); the frontend then calls `http://127.0.0.1:8000`.	[Proposal]; assignment §5.2 item 5
D2	Graph storage	Stored (relational tables): `AUTHORED_BY` = `paper_authors`, `HAS_TOPIC` = `paper_topics`, `CITES` = `citations`. Derived while building the graph (no table): `CO_AUTHOR` (authors who share ≥1 paper), `RELATED_TOPIC` (topics that share ≥1 paper). Reasons: foreign keys with `ON DELETE CASCADE` keep graph and database consistent after deletes (F11); derived edges cannot go stale; no duplicated data.	Phase 1 §8.4 [Phase 1] for stored/derived split; table design [Proposal]
D3	No generic `nodes`/`edges` tables	Phase 1 §8.5 describes a generic two-table model. This plan instead uses dedicated junction tables (as Phase 1 §9 mentions `PaperAuthors`) because they give real foreign keys and simpler SQL for a 7B model to write.	[Proposal]
D4	Identifier-first metadata	The DOI/arXiv ID is searched only on page 1 (and PDF metadata), so a DOI belonging to a cited paper is not picked up. APIs are called only when an identifier exists. There is no title-search fallback (it risks attaching the wrong paper). Without an identifier the app works from PDF-derived data and says so.	Phase 1 §6 [Phase 1]; narrowing [Proposal]
D5	Merge rules	API title/authors/year/venue override heuristic PDF values when the API returned a non-empty value (priority Crossref > arXiv > OpenAlex > Semantic Scholar). The PDF abstract is kept if it has ≥50 characters, otherwise the first API abstract is used (arXiv > Semantic Scholar > OpenAlex > Crossref).	[Proposal]
D6	Tag priority	Exactly one automatic source per paper, tried in order: (1) author keywords from the PDF front matter or PDF metadata; (2) topics returned by a scholarly API (Crossref `subject`, OpenAlex topics/keywords, Semantic Scholar `fieldsOfStudy`); (3) YAKE on title + abstract + start of body text. Users can add or remove tags manually (source `manual`). Each tag stores its source and a confidence (`verified` for author/api/manual, `estimated` for yake).	Phase 1 §7 + Phase 2 [Phase 1]; storage details [Proposal]
D7	Scanned PDFs	Rejected (HTTP 422, code `no_text_layer`) when fewer than 200 non-whitespace characters can be extracted. No OCR.	Phase 1 §6 [Phase 1]
D8	Duplicates	Rejected (HTTP 409) when the file SHA-256, the DOI or the arXiv ID already exists (`duplicate_paper`). If only the normalised title matches (for example an arXiv preprint and its published version), the upload is rejected with `possible_duplicate` unless the client repeats it with `allow_duplicate=true`.	[Proposal]; Phase 1 §9 suggests DOI/arXiv/title matching
D9	Citation matching (`CITES`)	A reference is linked to a library paper only on an exact normalised DOI match, an exact arXiv-ID match, or when the library paper's normalised title (≥20 characters) appears inside the normalised reference text. Nothing else. When a paper is added or its DOI/title is edited, its matches are recomputed in both directions.	[Proposal]
D10	Identity of users	No login. The browser stores a display name and sends it in an `X-Username` header; the server requires it on every write request and logs it.	Assignment F6 / FAQ
D11	Transactions	Data-access functions never call `commit()`. Callers wrap a unit of work in `with conn:` so a failed upload leaves no half-written rows. One short-lived SQLite connection per request.	[Proposal]
D12	External API etiquette	Per-host minimum request intervals, 30-day response cache in SQLite, bounded retries with back-off on HTTP 429/5xx, no keys in code (read from environment variables), `OFFLINE_MODE=1` skips all external calls.	Phase 1 §5 + §9; limits re-verified in B.4
D13	Python version	Python 3.12 (inside every verified compatibility range, see B.1).	[Proposal]
A.4 Corrections and deviations relative to Phase 1
Phase 1 §5 states Crossref allows "up to 50 requests/second" in one place and 5/10 requests per second in the later detailed section. The official page (B.4) confirms 5 (public) / 10 (polite); the 50 figure is wrong and is not used.
Phase 1 §8.5 describes generic `nodes`/`edges` tables; this plan uses dedicated tables (D3).
Phase 1 §7 lists a controlled-vocabulary normalisation step. It is not implemented (see A.5); only case/whitespace normalisation and de-duplication are applied.
A.5 Out of scope
GROBID, AnyStyle, OCR/Tesseract, LLM-based extraction, embeddings or semantic search, a controlled tag vocabulary, venue nodes, author disambiguation (two authors with the same normalised name are treated as one person), full-text search, passwords/roles, and any title-based API search.
---
B. Technology stack
B.1 Technology table
All third-party packages are installed with `pip` into a virtual environment. Versions are the latest stable releases listed on the official package index on 22 Oct 2026 unless the "Why" column says otherwise.
Technology / package	Exact version	Purpose	Why it was selected	Official source URL
Python	3.12 (any 3.12.x) [Proposal]	Backend language	3.12 lies inside every package's verified Python range: FastAPI ≥3.10, PyMuPDF 2.0 ≥3.11, YAKE ≥3.10 (classifiers list up to 3.12), python-multipart ≥3.10, httpx ≥3.8. [Verified]. Uvicorn's `requires-python` was not inspected. [Unverified]	https://pypi.org/project/fastapi/
FastAPI	0.156.4 (released 20 Oct 2026) [Verified]	Web framework: JSON API, file upload, static-file serving, CORS, automatic validation	`UploadFile`, `StaticFiles` and `CORSMiddleware` are built in, so no extra web packages are needed; type-validated endpoints; MIT licence. FastAPI itself depends on Starlette and Pydantic, which pip resolves automatically. Release cadence is very fast (many releases on 20 Oct 2026); the pin freezes it.	https://pypi.org/project/fastapi/ · https://fastapi.tiangolo.com/tutorial/request-files/ · https://fastapi.tiangolo.com/tutorial/static-files/ · https://fastapi.tiangolo.com/tutorial/cors/
Uvicorn	0.54.0 (released 25 Sep 2026) [Verified]	ASGI server that runs FastAPI (`python -m uvicorn backend.main:app`). FastAPI does not include a server when installed without extras, so it is listed explicitly.	Standard ASGI server for FastAPI; BSD licence.	https://pypi.org/project/uvicorn/
python-multipart	0.0.32 (released 4 Jun 2026) [Verified]	Parses `multipart/form-data` so FastAPI can receive the uploaded PDF (`UploadFile`, `Form`). Required for file upload.	Needed by FastAPI for form/file parsing; Apache-2.0; no dependencies; Python ≥3.10.	https://pypi.org/project/python-multipart/
PyMuPDF (`pip install pymupdf`, `import pymupdf`)	2.0 (released 19 Oct 2026) [Verified]	Extracts text, text blocks with coordinates and font sizes, and PDF metadata	Gives positions and font sizes needed for column ordering and title detection (Phase 1 §6). Not PyPDF/PyPDF2. Requires Python ≥3.11. Licence: dual - GNU AGPL v3 or Artifex commercial; AGPL is acceptable for this coursework project but must be considered before any redistribution. The 2.0 release lists wheels for Linux (x86-64, aarch64), macOS arm64 and Windows x86-64 only; other platforms build from source.	https://pypi.org/project/pymupdf/ · https://pymupdf.readthedocs.io/
httpx	0.28.1 (released 6 Dec 2024; latest stable - `1.0.dev*` releases exist but are pre-releases) [Verified]	Async HTTP client (`httpx.AsyncClient`) for Crossref, OpenAlex, Semantic Scholar and arXiv lookups inside FastAPI's async upload handler	Same code works with `async`/`await` without blocking the event loop; strict timeouts; BSD-3-Clause. HTTP/2 extra is not installed.	https://pypi.org/project/httpx/ · https://www.python-httpx.org/
YAKE	0.7.3 (released 9 Feb 2026) [Verified]	Local, unsupervised keyword extraction - fallback only (priority 3 in D6)	Needs no model download, training data or network; chosen in Phase 1 §7. Licence: GPLv3 (per PyPI). Brings its own small dependencies (resolved by pip).	https://pypi.org/project/yake/ · https://github.com/INESCTEC/yake
`sqlite3` (standard library)	Ships with Python 3.12; not a pip package	Database access	Documentation states the module requires SQLite 3.15.2 or newer. Values are bound with `?` placeholders ("always use placeholders instead of string formatting"), which prevents SQL injection. The schema uses only features older than that (foreign keys, partial indexes, `INSERT OR IGNORE`, `strftime`); no `RETURNING`/upsert. No specific SQLite runtime version is claimed; `/api/health` reports `sqlite3.sqlite_version` at run time. [Verified]	https://docs.python.org/3/library/sqlite3.html
Cytoscape.js	3.34.4 (MIT) [Verified: npm and jsDelivr list 3.34.4 as the current version; GitHub's Releases page showed v3.34.3 as latest when checked, so the newest patch may not be tagged there yet]	Interactive graph in the browser	Designed for graph/network models (directed edges, selectors, layouts, events); needs only one JS file, no CSS file, no build step. Pinned URL: `https://cdn.jsdelivr.net/npm/cytoscape@3.34.4/dist/cytoscape.min.js` (jsDelivr's declared main file for the package is `dist/cytoscape.min.js`). No release date is claimed.	https://www.jsdelivr.com/package/npm/cytoscape · https://www.npmjs.com/package/cytoscape · https://js.cytoscape.org/
Standard-library modules also used (no installation): `hashlib`, `re`, `json`, `unicodedata`, `asyncio`, `pathlib`, `urllib.parse`, `xml.etree.ElementTree`, `contextlib`, `datetime`, `os`, `sys`, `unittest`.
Feature statements about FastAPI (`UploadFile`, `StaticFiles`, `CORSMiddleware`) rest on the three FastAPI documentation URLs above, which were consulted in Phase 2; they were not re-opened in this revision. [Phase 1/2]
B.2 `requirements.txt` (must match the table exactly)
```text
fastapi==0.156.4
uvicorn==0.54.0
python-multipart==0.0.32
pymupdf==2.0
httpx==0.28.1
yake==0.7.3
```
Only these six direct dependencies are pinned; pip chooses compatible transitive versions (Starlette, Pydantic, h11, click, numpy and others). After Phase 4 integration the build log may record `pip freeze` output if a fully locked file is wanted. Nothing in the plan imports a package that is not on this list. SQLite and Cytoscape.js are intentionally absent (standard library and CDN).
B.3 Libraries considered and not selected
`pypdf`/`PyPDF2` (Phase 1: sequential extraction scrambles multi-column text); `pdfplumber` (slower; only mentioned in Phase 1 as an alternative - not used, not a fallback); GROBID, AnyStyle, Tesseract/OCRmyPDF, LLM extraction, embeddings, RAKE, TF-IDF, a controlled vocabulary (Phase 1 research alternatives - not implemented, see A.5); vis-network (alternative to Cytoscape.js); SQLAlchemy (not needed for nine small tables); `requests` (synchronous).
B.4 External scholarly APIs: limits, terms and licensing
Request-rate limits (requests per second) are not the same as usage budgets (a daily allowance). Both are listed where they exist.
Service	Endpoint used (no secrets in URLs)	Authentication	Request-rate limit	Usage budget	Reuse / licensing	Sources
Crossref REST API	`https://api.crossref.org/works/{doi}`	None required. "Polite" pool: add your e-mail in the `mailto` parameter or in the User-Agent. "Metadata Plus" (paid key) is not used.	Public pool 5 req/s, 1 concurrent; Polite pool 10 req/s, 3 concurrent; Plus 150 req/s. Exceeding → HTTP 429 (wait, then retry slower); a manual block → 403. Limits are also returned in `x-rate-limit-*` and `x-concurrency-limit` headers. [Verified]	None stated	Phase 1 §5: Crossref says almost none of its deposited metadata is copyrighted, but individual abstracts may be copyrighted by publishers/authors, so abstracts are not assumed free to redistribute. [Phase 1, not re-checked] Best practice from the page: cache responses, send `mailto` and an identifying User-Agent, back off when response times rise. [Verified]	https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/ · https://www.crossref.org/documentation/retrieve-metadata/rest-api/
arXiv API (legacy Atom API)	`http://export.arxiv.org/api/query?id_list={arxiv_id}` (the HTTP form documented by arXiv; the client follows redirects)	None	At most 1 request every 3 seconds, one connection at a time [Verified]. Do not circumvent limits.	None stated	Descriptive metadata (titles, abstracts, authors, identifiers, classification terms) may be used under CC0 1.0. [Verified] Full-text e-prints have separate rights; the app does not redistribute arXiv PDFs. [Phase 1]	https://info.arxiv.org/help/api/tou.html · https://info.arxiv.org/help/api/user-manual.html
OpenAlex API	`https://api.openalex.org/works/https://doi.org/{doi}` (external-ID lookup form confirmed in the "Get Singleton" docs)	Optional free API key (`api_key` query parameter or `Authorization: Bearer`); the key requires a verified e-mail. Read from env var `OPENALEX_API_KEY`.	10 req/s without a key, 30 req/s with a free key; slower for a few heavy query types. HTTP 429 if the per-second limit or the budget is exceeded. [Verified]	A free key raises the daily budget 10× ("a free account's $1 a day"; Phase 1 gives $0.10/day without a key). The "Get Singleton" page lists single-entity lookups as Cost: Free. Headers `X-RateLimit-Remaining` / `-Reset` (reset at midnight UTC) report the budget. [Verified]	OpenAlex describes its scholarly metadata as CC0 (Phase 1 cites https://help.openalex.org/data/how-its-built/). CC0 covers OpenAlex's dataset, not the underlying papers. [Phase 1, not re-checked]	https://help.openalex.org/api/authentication/ · https://help.openalex.org/api/get-single-entities/
Semantic Scholar Academic Graph API	`https://api.semanticscholar.org/graph/v1/paper/{paper_id}` with `paper_id` such as `DOI:10.x/y` or `ARXIV:2101.00001`	Optional API key sent as header `x-api-key`; read from env var `S2_API_KEY`.	A personal key gets an introductory 1 request/second on all endpoints (official tutorial) [Verified]. Requests without a key share one pool among all anonymous users, documented in the official overview as 1,000 req/s shared and throttled during heavy use; I confirmed this figure only through secondary sources, so treat it as [Unverified]. Use 429 back-off either way.	None stated	API licence agreement limits use (Phase 1 summarises: internal/non-commercial research and education; public displays need attribution, a link with `utm_source=api`, and the Semantic Scholar name/logo). Check the agreement before any public deployment. [Phase 1, not re-checked]	https://www.semanticscholar.org/product/api/tutorial · https://api.semanticscholar.org/api-docs/ · https://api.semanticscholar.org/license/
How the application behaves (implemented in Prompts 0, 10-13): minimum seconds between requests per host: Crossref 0.25, OpenAlex 0.15, Semantic Scholar 1.1, arXiv 3.1 (all at or below the published limits); one request at a time; timeout 10 s; at most 2 retries on 429/5xx/transport errors with the `Retry-After` header (capped at 10 s) or 1 s then 2 s back-off; successful responses cached in SQLite for 30 days; failures never abort an upload - they become warnings and the PDF-derived metadata is kept; no keys or e-mail addresses are stored in source code (`CROSSREF_MAILTO`, `OPENALEX_API_KEY`, `S2_API_KEY`, `OFFLINE_MODE` environment variables). Limits and terms can change - recheck the linked pages before deployment.
---
C. Architecture
C.1 File and folder tree
```text
paper_library/                          <- single project root inside the zip
├── README.md                           install / run / use / limitations / AI statement        (Prompt 31)
├── requirements.txt                    six pinned dependencies from B.2                        (manual)
├── backend/
│   ├── __init__.py                     empty package marker                                     (manual)
│   ├── config.py                       paths, limits, API URLs, env-var helpers                 (Prompt 0)
│   ├── text_utils.py                   text normalisation, DOI and arXiv-ID detection           (Prompt 1)
│   ├── db.py                           SCHEMA_SQL, connection helper, init_db                   (Prompt 2)
│   ├── repo_aux.py                     activity-log and API-cache data access                   (Prompt 3)
│   ├── repo_write.py                   insert / update / delete data access                     (Prompt 4)
│   ├── repo_read.py                    read, search, duplicate lookup                           (Prompt 5)
│   ├── pdf_text.py                     PyMuPDF text, reading order, page-1 lines                (Prompt 6)
│   ├── parse_title_authors.py          title and author heuristics                              (Prompt 7)
│   ├── parse_abstract_keywords.py      abstract, keywords, year heuristics                      (Prompt 8)
│   ├── references.py                   reference-section detection and splitting                (Prompt 9)
│   ├── http_utils.py                   throttled async GET with retry/back-off                  (Prompt 10)
│   ├── clients_json.py                 Crossref, OpenAlex, Semantic Scholar clients             (Prompt 11)
│   ├── client_arxiv.py                 arXiv Atom client                                        (Prompt 12)
│   ├── enrichment.py                   cache + client calls + merge rules                       (Prompt 13)
│   ├── tagging.py                      author keywords > API topics > YAKE                      (Prompt 14)
│   ├── citations.py                    CITES matching                                           (Prompt 15)
│   ├── graph.py                        graph JSON incl. derived edges                           (Prompt 16)
│   ├── pipeline.py                     upload -> parse -> enrich -> tag -> store                (Prompt 17)
│   ├── api_errors.py                   ApiError + X-Username dependency                         (Prompt 19)
│   ├── routes_papers.py                /api/papers endpoints                                    (Prompt 20)
│   ├── routes_misc.py                  health, topics, graph, activity endpoints                (Prompt 21)
│   └── main.py                         app, CORS, error handlers, static mount                  (Prompt 22)
├── frontend/
│   ├── index.html                      page shell + pinned Cytoscape tag + script tags          (Prompt 23)
│   ├── css/styles.css                  layout and styling                                       (Prompt 24)
│   └── js/
│       ├── api.js                      fetch wrappers, username storage, helpers                (Prompt 25)
│       ├── app.js                      hash router, toasts, user box                            (Prompt 26)
│       ├── library.js                  library view: search, upload, list                       (Prompt 27)
│       ├── detail.js                   paper detail, edit, tags, delete                         (Prompt 28)
│       ├── graph.js                    Cytoscape graph view                                     (Prompt 29)
│       └── activity.js                 activity log view                                        (Prompt 30)
├── tests/
│   ├── __init__.py                     empty                                                    (manual)
│   └── test_core.py                    unittest checks (standard library only)                  (Prompt 18)
├── data/                               library.db is created here on first run
├── uploads/                            stored PDFs, named <sha256>.pdf
└── sample_papers/                      2-3 open-access PDFs for testing (added manually)
```
Manual work allowed by assignment §6.4.3 (skeleton): create the folders and empty files above, create the virtual environment, write `requirements.txt` from B.2, download sample PDFs, and put an empty placeholder `frontend/index.html` in place so the static mount works before Prompt 23.
C.2 Data flow: upload → graph
Upload - browser `POST /api/papers` (multipart, header `X-Username`). `routes_papers` reads at most 25 MB + 1 byte and calls `pipeline.ingest_pdf`.
Validate - non-empty, starts with `%PDF-`, ≤ 25 MB; compute SHA-256; reject an already stored file (`duplicate_paper`); save to `uploads/<sha256>.pdf`.
Text extraction - `pdf_text.extract_pdf` (PyMuPDF): raw text, column-ordered body text without margins, page-1 lines with font sizes, PDF metadata. Fewer than 200 characters → `no_text_layer`.
Metadata parsing - DOI and arXiv ID from page-1 text (`text_utils`); title/authors (`parse_title_authors`); abstract, keywords, year (`parse_abstract_keywords`); reference list (`references`).
Scholarly API enrichment - `enrichment.enrich_metadata`: cache lookup → throttled API calls → merge rules D5; failures become warnings.
Duplicate check on final identifiers - DOI, arXiv ID, normalised title (D8).
Topic tagging - `tagging.build_tags` applies priority D6.
Database storage - one `with conn:` transaction: `papers`, `authors`/`paper_authors`, `topics`/`paper_topics`, `paper_references`, citation matching (`citations`), `activity_log`.
Search/filter - `GET /api/papers` with `q`, `author`, `topic`, `year`.
Graph generation - `GET /api/graph` → `graph.build_graph` reads the stored tables, derives `CO_AUTHOR` and `RELATED_TOPIC`, returns Cytoscape `elements`; the Graph view always requests fresh data, so it reflects new uploads and deletions.
C.3 Layering rule
`routes_*` → `pipeline` / `repo_*` / `graph` / `citations` → `db` / `text_utils` / `config`. Parsers (`pdf_text`, `parse_*`, `references`) and API code (`http_utils`, `clients_*`, `enrichment`) do not import the routes. A later prompt never edits a file produced by an earlier prompt (see Section H preface).
C.4 Shared data shapes (used by several prompts)
```text
ExtractResult (pdf_text.extract_pdf):
  {"page_count": int, "raw_text": str, "first_page_raw_text": str,
   "body_text": str, "first_page_body_text": str,
   "first_page_lines": [{"text": str, "size": float, "x0": float, "y0": float, "x1": float, "y1": float}],
   "page_width": float, "page_height": float,
   "doc_metadata": {"title": str, "author": str, "keywords": str}}

ParsedMetadata (built by pipeline from parsers):
  {"title": str|None, "authors": [str], "abstract": str|None, "year": int|None, "venue": None,
   "keywords": [str]}

ApiResult (every client returns this dict or None):
  {"source": "crossref"|"openalex"|"semantic_scholar"|"arxiv",
   "title": str|None, "authors": [str], "year": int|None, "venue": str|None,
   "abstract": str|None, "doi": str|None, "arxiv_id": str|None, "topics": [str]}

ReferenceDict (references.extract_references items):
  {"raw_text": str, "text_key": str, "doi": str|None, "arxiv_id": str|None, "year": int|None}

TagDict (tagging.build_tags items):
  {"name": str, "source": "author"|"api"|"yake", "api_name": str|None, "confidence": "verified"|"estimated"}
```
---
D. Database schema
All statements are executable SQLite and are the exact text stored in `SCHEMA_SQL` by Prompt 2. `PRAGMA foreign_keys = ON` is set per connection in `db.get_conn` (SQLite does not persist it). Timestamps are UTC ISO-8601 text produced by SQLite itself. Nine tables are created.
```sql
CREATE TABLE IF NOT EXISTS papers (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    title             TEXT    NOT NULL CHECK (length(trim(title)) > 0),
    title_key         TEXT    NOT NULL,
    abstract          TEXT,
    year              INTEGER CHECK (year IS NULL OR (year BETWEEN 1800 AND 2100)),
    venue             TEXT,
    doi               TEXT,
    arxiv_id          TEXT,
    file_sha256       TEXT    NOT NULL,
    stored_filename   TEXT    NOT NULL,
    original_filename TEXT    NOT NULL,
    page_count        INTEGER,
    enriched_from     TEXT,
    uploaded_by       TEXT    NOT NULL,
    uploaded_at       TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    updated_at        TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_papers_file_sha256 ON papers (file_sha256);
CREATE UNIQUE INDEX IF NOT EXISTS ux_papers_doi         ON papers (doi)      WHERE doi IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS ux_papers_arxiv_id    ON papers (arxiv_id) WHERE arxiv_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_papers_title_key ON papers (title_key);
CREATE INDEX IF NOT EXISTS ix_papers_year      ON papers (year);

CREATE TABLE IF NOT EXISTS authors (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL CHECK (length(trim(name)) > 0),
    name_key TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS paper_authors (          -- stored edge AUTHORED_BY (paper -> author)
    paper_id  INTEGER NOT NULL REFERENCES papers  (id) ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES authors (id) ON DELETE CASCADE,
    position  INTEGER NOT NULL CHECK (position >= 1),
    PRIMARY KEY (paper_id, author_id),
    UNIQUE (paper_id, position)
);
CREATE INDEX IF NOT EXISTS ix_paper_authors_author ON paper_authors (author_id);

CREATE TABLE IF NOT EXISTS topics (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL CHECK (length(trim(name)) > 0),
    name_key TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS paper_topics (           -- stored edge HAS_TOPIC (paper -> topic)
    paper_id   INTEGER NOT NULL REFERENCES papers (id) ON DELETE CASCADE,
    topic_id   INTEGER NOT NULL REFERENCES topics (id) ON DELETE CASCADE,
    source     TEXT NOT NULL CHECK (source IN ('author', 'api', 'yake', 'manual')),
    api_name   TEXT,
    confidence TEXT NOT NULL CHECK (confidence IN ('verified', 'estimated')),
    PRIMARY KEY (paper_id, topic_id)
);
CREATE INDEX IF NOT EXISTS ix_paper_topics_topic ON paper_topics (topic_id);

CREATE TABLE IF NOT EXISTS paper_references (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id  INTEGER NOT NULL REFERENCES papers (id) ON DELETE CASCADE,
    position  INTEGER NOT NULL CHECK (position >= 1),
    raw_text  TEXT    NOT NULL,
    text_key  TEXT    NOT NULL,
    doi       TEXT,
    arxiv_id  TEXT,
    year      INTEGER,
    UNIQUE (paper_id, position)
);
CREATE INDEX IF NOT EXISTS ix_refs_paper ON paper_references (paper_id);
CREATE INDEX IF NOT EXISTS ix_refs_doi   ON paper_references (doi)      WHERE doi IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_refs_arxiv ON paper_references (arxiv_id) WHERE arxiv_id IS NOT NULL;

CREATE TABLE IF NOT EXISTS citations (              -- stored edge CITES (citing paper -> cited paper)
    citing_paper_id INTEGER NOT NULL REFERENCES papers (id) ON DELETE CASCADE,
    cited_paper_id  INTEGER NOT NULL REFERENCES papers (id) ON DELETE CASCADE,
    reference_id    INTEGER REFERENCES paper_references (id) ON DELETE SET NULL,
    match_method    TEXT NOT NULL CHECK (match_method IN ('doi', 'arxiv_id', 'title')),
    PRIMARY KEY (citing_paper_id, cited_paper_id),
    CHECK (citing_paper_id <> cited_paper_id)
);
CREATE INDEX IF NOT EXISTS ix_citations_cited ON citations (cited_paper_id);

CREATE TABLE IF NOT EXISTS activity_log (           -- no foreign key: log survives deletions
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT NOT NULL,
    action      TEXT NOT NULL CHECK (action IN ('upload', 'edit', 'tag_add', 'tag_remove', 'delete')),
    paper_id    INTEGER,
    paper_title TEXT,
    details     TEXT,
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);
CREATE INDEX IF NOT EXISTS ix_activity_created ON activity_log (created_at);
CREATE INDEX IF NOT EXISTS ix_activity_user    ON activity_log (username);

CREATE TABLE IF NOT EXISTS api_cache (              -- successful API responses only
    cache_key  TEXT PRIMARY KEY,
    payload    TEXT NOT NULL,
    fetched_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);
```
Stored versus derived relationships
Relationship	Meaning	Where it lives	Stored or derived
`AUTHORED_BY`	paper → author	`paper_authors`	stored
`HAS_TOPIC`	paper → topic (with source and confidence)	`paper_topics`	stored
`CITES`	citing paper → cited paper that is also in the library (D9)	`citations`	stored
`CO_AUTHOR`	author – author, both listed on ≥1 common paper; `weight` = number of shared papers; skipped for papers with more than 15 authors	computed in `graph.build_graph`	derived
`RELATED_TOPIC`	topic – topic, both attached to ≥1 common paper; `weight` = number of shared papers	computed in `graph.build_graph`	derived
Duplicates. Keys: `file_sha256` (exact file), `doi` and `arxiv_id` (lower-cased, `NULL` when absent, so many papers may lack them), `title_key` (title lower-cased, accents stripped, punctuation removed, whitespace collapsed). `find_duplicate` checks sha256 → doi → arxiv_id (kind `duplicate_paper`) and then `title_key` (kind `possible_duplicate`). The partial unique indexes enforce the exact kinds even under a race (the insert raises `sqlite3.IntegrityError`, reported as `duplicate_paper`).
Delete consistency (F11). Deleting a paper cascades to `paper_authors`, `paper_topics`, `paper_references` and `citations`; the data-access layer then deletes `authors` and `topics` rows that no longer belong to any paper; the stored PDF is removed by the route; the log row is kept.
Known limits. Author identity is the normalised name only (no ORCID/disambiguation). `activity_log.details` is free text. Tags are not language-aware.
---
E. API contract
Base URL: `http://127.0.0.1:8000`. All endpoints are under `/api`. Responses are JSON. Write requests (`POST`, `PATCH`, `DELETE`) require the header `X-Username` (1-50 characters after trimming). Example payloads below are illustrative, not recorded results.
E.1 Endpoint table
Method	Path	Purpose	Request	Success response	Error responses
GET	`/api/health`	Liveness and environment info	-	`200` `{"status":"ok","sqlite_version":"3.x.y","paper_count":0,"offline_mode":false}`	-
POST	`/api/papers`	Upload and ingest one PDF (F1-F4)	`multipart/form-data`: `file` (PDF, required), `allow_duplicate` (bool form field, default false); header `X-Username`	`201` `{"paper": PaperDetail, "warnings": [str]}`	`400 missing_username`, `400 empty_file`, `400 not_pdf`, `400 unreadable_pdf`, `413 file_too_large`, `422 no_text_layer`, `409 duplicate_paper`, `409 possible_duplicate`, `500 internal_error`
GET	`/api/papers`	List/search/filter (F7)	query: `q` (substring of title, author or topic), `author` (substring), `topic` (substring), `year` (int), `limit` (1-200, default 50), `offset` (≥0, default 0)	`200` `{"total":int,"items":[PaperSummary]}` newest first	`422 validation_error`
GET	`/api/papers/{id}`	Paper detail (F8)	-	`200` PaperDetail	`404 not_found`
PATCH	`/api/papers/{id}`	Correct metadata (F8)	JSON, any subset of `title`, `abstract`, `year`, `venue`, `doi`, `arxiv_id`, `authors` (list of names); header `X-Username`	`200` PaperDetail	`400 missing_username`, `404 not_found`, `409 duplicate_paper`, `422 invalid_doi`, `422 invalid_arxiv_id`, `422 validation_error`
DELETE	`/api/papers/{id}`	Delete paper + file (F11)	header `X-Username`	`200` `{"deleted": id}`	`400 missing_username`, `404 not_found`
POST	`/api/papers/{id}/topics`	Add a manual tag	JSON `{"name": str (1-60 chars)}`; header `X-Username`	`200` PaperDetail	`400 missing_username`, `404 not_found`, `422 validation_error`
DELETE	`/api/papers/{id}/topics/{topic_id}`	Remove a tag from a paper	header `X-Username`	`200` PaperDetail	`400 missing_username`, `404 not_found`
GET	`/api/topics`	All topics with usage count	-	`200` `[{"id":int,"name":str,"paper_count":int}]`	-
GET	`/api/graph`	Knowledge graph (F9)	query: `include_derived` (bool, default true)	`200` GraphResponse	-
GET	`/api/activity`	Activity log (F10)	query: `user` (exact name), `limit` (1-200, default 50), `offset`	`200` `{"total":int,"items":[ActivityItem]}` newest first	`422 validation_error`
E.2 Response shapes
```json
PaperSummary = {
  "id": 1, "title": "Attention Is All You Need", "year": 2017, "venue": "NeurIPS",
  "doi": null, "arxiv_id": "1706.03762",
  "authors": ["Ashish Vaswani", "Noam Shazeer"],
  "tags": [{"id": 3, "name": "attention", "source": "author", "confidence": "verified"}],
  "uploaded_by": "alice", "uploaded_at": "2026-10-22T10:00:00Z"
}

PaperDetail = PaperSummary fields plus {
  "abstract": "text or null", "page_count": 15, "enriched_from": ["arxiv", "semantic_scholar"],
  "original_filename": "1706.03762.pdf", "updated_at": "2026-10-22T10:00:05Z",
  "authors": [{"id": 1, "name": "Ashish Vaswani"}],            // objects instead of strings
  "tags": [{"id": 3, "name": "attention", "source": "author", "api_name": null, "confidence": "verified"}],
  "references": [{"id": 10, "position": 1, "raw_text": "[1] ...", "doi": null, "arxiv_id": null,
                  "year": 2014, "cited_paper_id": null}],
  "cites":    [{"paper_id": 2, "title": "..."}],
  "cited_by": [{"paper_id": 5, "title": "..."}]
}

ActivityItem = {"id": 7, "username": "alice", "action": "upload", "paper_id": 1,
                "paper_title": "Attention Is All You Need", "details": "optional text",
                "created_at": "2026-10-22T10:00:05Z"}

GraphResponse = {
  "elements": {
    "nodes": [
      {"data": {"id": "paper:1",  "type": "paper",  "label": "Attention Is All You Need", "paper_id": 1, "year": 2017}},
      {"data": {"id": "author:1", "type": "author", "label": "Ashish Vaswani", "author_id": 1, "paper_count": 1}},
      {"data": {"id": "topic:3",  "type": "topic",  "label": "attention", "topic_id": 3, "paper_count": 1}}
    ],
    "edges": [
      {"data": {"id": "AUTHORED_BY:paper:1:author:1", "type": "AUTHORED_BY", "source": "paper:1", "target": "author:1"}},
      {"data": {"id": "HAS_TOPIC:paper:1:topic:3", "type": "HAS_TOPIC", "source": "paper:1", "target": "topic:3",
                "tag_source": "author", "confidence": "verified"}},
      {"data": {"id": "CITES:paper:2:paper:1", "type": "CITES", "source": "paper:2", "target": "paper:1"}},
      {"data": {"id": "CO_AUTHOR:author:1:author:2", "type": "CO_AUTHOR", "source": "author:1", "target": "author:2", "weight": 1}},
      {"data": {"id": "RELATED_TOPIC:topic:3:topic:4", "type": "RELATED_TOPIC", "source": "topic:3", "target": "topic:4", "weight": 2}}
    ]
  },
  "stats": {"papers": 1, "authors": 1, "topics": 1,
            "edges": {"AUTHORED_BY": 1, "HAS_TOPIC": 1, "CITES": 0, "CO_AUTHOR": 0, "RELATED_TOPIC": 0}}
}
```
Directions: `AUTHORED_BY` paper→author, `HAS_TOPIC` paper→topic, `CITES` citing→cited (the only edge drawn with an arrow). `CO_AUTHOR` and `RELATED_TOPIC` are undirected; their `source` has the smaller numeric id. When `include_derived=false` the last two types are omitted.
E.3 Error format
Every error returns the HTTP status above and this body (`existing_paper_id` appears only on the two `409` codes):
```json
{"error": {"code": "duplicate_paper", "message": "This paper is already in the library.", "existing_paper_id": 3}}
```
Code	Status	Meaning
`missing_username`	400	`X-Username` header absent or blank
`empty_file` / `not_pdf` / `unreadable_pdf`	400	zero bytes / does not start with `%PDF-` / PyMuPDF cannot open it or it is password-protected
`file_too_large`	413	larger than 25 MB
`no_text_layer`	422	scanned or image-only PDF (fewer than 200 extractable characters)
`duplicate_paper`	409	same file hash, DOI or arXiv ID already stored
`possible_duplicate`	409	same normalised title; repeat with `allow_duplicate=true` to keep both
`not_found`	404	no paper or tag link with that id
`invalid_doi` / `invalid_arxiv_id`	422	supplied value does not parse
`validation_error`	422	request body/query failed validation
`internal_error`	500	unexpected failure (details only in the server log)
The upload `warnings` array contains plain strings such as `"Crossref lookup returned no data."`, `"No DOI or arXiv ID found; metadata comes from the PDF only."`, `"Title could not be detected; the file name was used."`, `"Offline mode: scholarly APIs skipped."`.
---
F. Frontend specification
Delivery. `frontend/index.html` plus `css/` and `js/` files, served by FastAPI at `/` (or opened directly from disk; see D1). Plain `<script>` tags (no modules), no `package.json`, no framework, no build step. In `file://` mode `API_BASE` is `http://127.0.0.1:8000`; otherwise it is the empty string (same origin).
Pinned CDN tag (only third-party script):
```html
<script src="https://cdn.jsdelivr.net/npm/cytoscape@3.34.4/dist/cytoscape.min.js"></script>
```
It is placed before the project scripts. Script order in `index.html`: Cytoscape, `js/api.js`, `js/library.js`, `js/detail.js`, `js/graph.js`, `js/activity.js`, `js/app.js` (last).
High-level DOM
```text
<body>
  <header id="app-header"> title · <nav> links #/library #/graph #/activity </nav> · #user-box (name input + Save) </header>
  <main id="view"></main>          <- the active view renders here
  <div id="toast" hidden></div>    <- transient messages
</body>
```
Views (hash routes)
Route	Function (global)	Behaviour
`#/library` (default)	`renderLibraryView(container)`	Upload form (PDF file input + button); search form (`q`, `author`, `topic`, `year`); results list with title link to `#/paper/{id}`, authors, year, tag badges; pagination (20 per page); upload warnings and errors shown in plain language; on `possible_duplicate` the user is asked to confirm and the upload is repeated with `allow_duplicate=true`.
`#/paper/{id}`	`renderDetailView(container, paperId)`	Shows metadata, abstract, authors, tag badges with a remove button, add-tag input, references (with a link when `cited_paper_id` is set), "Cites" and "Cited by" lists; Edit form (title, year, venue, DOI, arXiv ID, abstract, authors one per line) sending `PATCH`; Delete with confirmation.
`#/graph`	`renderGraphView(container)`	Toolbar (show derived edges checkbox, node-type checkboxes, Refresh, Fit); Cytoscape canvas; legend; click a node to highlight its neighbourhood; double-click a paper node to open its detail view; empty-library message.
`#/activity`	`renderActivityView(container)`	Optional user filter; table of time, user, action, paper (link if the paper still exists), details; pagination.
Tag badge classes: `tag tag-author`, `tag tag-api`, `tag tag-yake`, `tag tag-manual`; confidence `estimated` additionally gets `tag-estimated` (dashed border, per Phase 1 §7 distinction between verified and machine-generated).
Graph JSON → Cytoscape. The `elements` object of the response is passed unchanged: `cytoscape({container, elements: response.elements, style: [...], layout: {name: "cose", animate: false}})`. `data.type` drives styling via selectors:
Selector	Style
`node[type = "paper"]`	round-rectangle, `#4e79a7`, label = `data(label)`
`node[type = "author"]`	ellipse, `#59a14f`
`node[type = "topic"]`	diamond, `#f28e2b`
`edge[type = "AUTHORED_BY"]`	thin grey line
`edge[type = "HAS_TOPIC"]`	thin orange dotted line
`edge[type = "CITES"]`	red, `target-arrow-shape: triangle`, `curve-style: bezier`
`edge[type = "CO_AUTHOR"]`	green dashed, width from `data(weight)`
`edge[type = "RELATED_TOPIC"]`	orange dashed, width from `data(weight)`
`.faded`	opacity 0.15 (used for neighbourhood highlight)
Node-type checkboxes hide/show nodes with `cy.nodes('[type = "author"]').style('display', ...)`.
Username. Stored in `localStorage` key `rpl_username`; `api.js` adds it as `X-Username` on write requests. If it is empty, write actions are blocked with a toast.
---
G. Build order and dependencies
Numbers are Prompt numbers from Section H; a prompt is built only after everything in "Depends on" passes its acceptance test.
Step	Prompt(s)	File(s)	Depends on	Checked by
0	manual	folders, venv, `requirements.txt`, placeholder `frontend/index.html`, sample PDFs	B.2	`pip install -r requirements.txt` succeeds
1	0	`config.py`	-	`python -m backend.config`
2	1	`text_utils.py`	-	`python -m backend.text_utils`
3	2	`db.py`	0	`python -m backend.db` (9 tables)
4	3	`repo_aux.py`	2	`python -m backend.repo_aux`
5	4	`repo_write.py`	1, 2	`python -m backend.repo_write`
6	5	`repo_read.py`	1, 2, 4	`python -m backend.repo_read`
7	6	`pdf_text.py`	0	run on a sample PDF
8	7, 8	`parse_title_authors.py`, `parse_abstract_keywords.py`	0, 6	run on sample PDFs
9	9	`references.py`	0, 1, 6	run on sample PDFs
10	10	`http_utils.py`	0	`python -m backend.http_utils`
11	11, 12	`clients_json.py`, `client_arxiv.py`	0, 1, 10	live lookup (network)
12	13	`enrichment.py`	0, 1, 2, 3, 11, 12	offline and online runs
13	14	`tagging.py`	0, 1	`python -m backend.tagging`
14	15, 16	`citations.py`, `graph.py`	0, 1, 2, 4	`python -m backend.citations`, `python -m backend.graph`
15	17	`pipeline.py`	0-9, 13-16	ingest a sample PDF from the command line
16	18	`tests/test_core.py`	1-5, 9, 14-16	`python -m unittest tests.test_core -v`
17	19, 20, 21	`api_errors.py`, `routes_papers.py`, `routes_misc.py`	0, 2-5, 15-17	import check, then full test after step 18
18	22	`main.py`	19-21	server start + `curl` checks
19	23, 24, 25, 26	`index.html`, `styles.css`, `api.js`, `app.js`	22	page loads, router shows placeholders
20	27, 28, 29, 30	`library.js`, `detail.js`, `graph.js`, `activity.js`	22, 25, 26	browser checks in each prompt
21	31	`README.md`	all	follow it on a clean venv
22	manual	integration test with ≥3 real PDFs; error cases (text file, scanned PDF, duplicate); Section F/G self-check commands from assignment §5.3; zip	all	checklist in assignment §7.2
---
H. Prompts for Qwen 2.5 Coder 7B
How to use these prompts
Start a fresh chat for every prompt. Paste only the text inside the code block (everything between the fences). Each block is self-contained: it restates the constraints and contains the interface and context it needs.
Save the answer into the file named in the prompt, run the acceptance test shown under the block, and do not continue until it passes. Record attempts in Section I and any manual change in Section J.
No prompt edits a file created by an earlier prompt. If a file is wrong, fix the cause in that prompt's own text (assignment §6.4.2) and regenerate that file in a fresh chat. Order in Section G already puts every file after the files it imports, and `main.py` is written after the route files for that reason.
Backend modules are run as `python -m backend.<module>` from the project root (virtual environment active) because they use absolute imports. Qwen is also told to add a small `if __name__ == "__main__":` self-test where practical.
The prompts use the exact names from Sections C-E. If you change a name in the plan, change it in every prompt that mentions it.
Qwen model/route used (fill in during Phase 4): ______________________
Prompt 0 - `backend/config.py`
Depends on: nothing · Modifies existing files: no
```text
ROLE: You are a senior Python backend engineer.
OBJECTIVE: Write ONE file, backend/config.py, holding the shared constants and environment helpers of a research-paper library web app.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.

INTERFACE (names must match exactly; other files import them):
  from pathlib import Path
  BASE_DIR: Path        # project root = parent of the backend folder
  DATA_DIR = BASE_DIR / "data"
  UPLOAD_DIR = BASE_DIR / "uploads"
  FRONTEND_DIR = BASE_DIR / "frontend"
  DB_PATH = DATA_DIR / "library.db"
  MAX_UPLOAD_BYTES = 25 * 1024 * 1024
  MIN_TEXT_CHARS = 200
  MAX_AUTHORS = 100
  MAX_TAGS_PER_PAPER = 10
  MAX_REFERENCES = 500
  MAX_COAUTHOR_FANOUT = 15
  HTTP_TIMEOUT_SECONDS = 10.0
  HTTP_MAX_RETRIES = 2
  CACHE_TTL_DAYS = 30
  USER_AGENT_BASE = "ResearchPaperLibrary/1.0"
  CROSSREF_URL = "https://api.crossref.org/works/"
  OPENALEX_URL = "https://api.openalex.org/works/"
  S2_URL = "https://api.semanticscholar.org/graph/v1/paper/"
  ARXIV_URL = "http://export.arxiv.org/api/query"
  MIN_INTERVAL_SECONDS = {"api.crossref.org": 0.25, "api.openalex.org": 0.15, "api.semanticscholar.org": 1.1, "export.arxiv.org": 3.1}
  def ensure_dirs() -> None            # create DATA_DIR and UPLOAD_DIR if missing (parents ok, exist_ok)
  def is_offline() -> bool             # True if env var OFFLINE_MODE is "1", "true" or "yes" (case-insensitive)
  def get_crossref_mailto() -> str | None   # env var CROSSREF_MAILTO, stripped; None if unset or empty
  def get_openalex_key() -> str | None      # env var OPENALEX_API_KEY, same rule
  def get_s2_key() -> str | None            # env var S2_API_KEY, same rule

CONTEXT: Never hard-code keys or e-mail addresses; they come only from environment variables.

STEPS:
1. Define BASE_DIR with Path(__file__).resolve().parent.parent.
2. Define all constants exactly as listed.
3. Implement the five functions.
4. Add an if __name__ == "__main__": block that calls ensure_dirs() and prints BASE_DIR, DB_PATH and is_offline().

OUTPUT FORMAT: Only the complete contents of config.py in a single Python code block. No explanation before or after.
REMINDER: one file only; names and values exactly as listed; no extra features.
```
Acceptance test: `python -m backend.config` prints the project root path, `.../data/library.db` and `False`; folders `data/` and `uploads/` exist. Running with `OFFLINE_MODE=1` (Windows: `set OFFLINE_MODE=1`) prints `True`.
---
Prompt 1 - `backend/text_utils.py`
Depends on: nothing · Modifies existing files: no
```text
ROLE: You are a senior Python backend engineer.
OBJECTIVE: Write ONE file, backend/text_utils.py, with pure text-normalisation helpers and DOI / arXiv-ID detection. Standard library only (re, unicodedata).
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.

INTERFACE (must match exactly):
  def clean_whitespace(text: str) -> str
      # replace every run of whitespace (including newlines) by one space and strip
  def normalize_title(text: str) -> str
      # key used for duplicate and citation matching: unicodedata NFKD, drop combining marks,
      # casefold, replace every character that is not a letter or digit by a space, collapse spaces, strip
  def normalize_name(name: str) -> str       # same behaviour as normalize_title
  def normalize_topic(name: str) -> str
      # casefold, collapse whitespace, strip spaces and the characters .,;:"'()[]
  def normalize_doi(raw: str) -> str | None
  def find_doi(text: str) -> str | None
  def normalize_arxiv_id(raw: str) -> str | None
  def find_arxiv_id(text: str) -> str | None

CONTEXT:
- A DOI looks like 10.1109/CVPR.2016.90 : prefix "10.", 4 to 9 digits, a slash, then a suffix without spaces. DOIs are case-insensitive: always return them lower-case, without the prefixes "https://doi.org/", "http://dx.doi.org/", "doi:", and without trailing punctuation . , ; : ] } > ' " . A trailing ")" is removed only if the DOI contains more ")" than "(".
- Regex for a DOI candidate: r"10\.\d{4,9}/[^\s\"<>]+"
- normalize_doi returns None if, after cleaning, the result does not match r"^10\.\d{4,9}/\S+$".
- find_doi returns the FIRST DOI found in text (after normalising it), or None.
- arXiv IDs: new style 1706.03762 (four digits, dot, four or five digits, optional version v5); old style cs.CL/0501001 or hep-th/9901001 (letters, optional .XX, slash, seven digits). find_arxiv_id ONLY accepts an ID that is preceded by "arXiv:" (case-insensitive, optional spaces after the colon) or by "arxiv.org/abs/" or "arxiv.org/pdf/". A bare number such as 2024.12345 without such a prefix must return None.
- Returned arXiv IDs are lower-case and have NO version suffix: "arXiv:1706.03762v5 [cs.CL]" -> "1706.03762".
- normalize_arxiv_id(raw) strips an optional "arxiv:" prefix and version suffix, returns None if the rest is not a valid new-style or old-style ID.

STEPS:
1. Compile the regular expressions once at module level.
2. Implement the eight functions.
3. Add an if __name__ == "__main__": block with these asserts, then print "text_utils OK":
   find_doi("see doi: 10.1109/CVPR.2016.90.") == "10.1109/cvpr.2016.90"
   normalize_doi("https://doi.org/10.1109/CVPR.2016.90") == "10.1109/cvpr.2016.90"
   normalize_doi("not a doi") is None
   find_arxiv_id("arXiv:1706.03762v5 [cs.CL] 6 Dec 2017") == "1706.03762"
   find_arxiv_id("number 1706.03762 appears alone") is None
   normalize_title("Attention Is All You Need!") == "attention is all you need"
   normalize_name("Ashish   Vaswani") == "ashish vaswani"
   normalize_topic(" Machine  Learning. ") == "machine learning"

OUTPUT FORMAT: Only the complete contents of text_utils.py in a single Python code block. No explanation before or after.
REMINDER: one file only; standard library only; no extra functions except underscore helpers.
```
Acceptance test: `python -m backend.text_utils` prints `text_utils OK`.
---
Prompt 2 - `backend/db.py`
Depends on: Prompt 0 · Modifies existing files: no
```text
ROLE: You are a senior Python backend engineer.
OBJECTIVE: Write ONE file, backend/db.py: the SQLite schema string, a connection helper and a schema initialiser.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.

INTERFACE (must match exactly):
  from pathlib import Path
  import sqlite3
  SCHEMA_SQL: str      # the exact SQL given below
  def get_conn(db_path: str | Path | None = None) -> sqlite3.Connection
  def init_db(conn: sqlite3.Connection | None = None) -> None
  def db_session(db_path: str | Path | None = None)      # @contextlib.contextmanager; yields a connection, always closes it
  def list_tables(conn: sqlite3.Connection) -> list[str] # user table names, sorted

CONTEXT: SCHEMA_SQL must be exactly the following text, copied character for character into one triple-quoted Python string (nine tables):
CREATE TABLE IF NOT EXISTS papers (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    title             TEXT    NOT NULL CHECK (length(trim(title)) > 0),
    title_key         TEXT    NOT NULL,
    abstract          TEXT,
    year              INTEGER CHECK (year IS NULL OR (year BETWEEN 1800 AND 2100)),
    venue             TEXT,
    doi               TEXT,
    arxiv_id          TEXT,
    file_sha256       TEXT    NOT NULL,
    stored_filename   TEXT    NOT NULL,
    original_filename TEXT    NOT NULL,
    page_count        INTEGER,
    enriched_from     TEXT,
    uploaded_by       TEXT    NOT NULL,
    uploaded_at       TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    updated_at        TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_papers_file_sha256 ON papers (file_sha256);
CREATE UNIQUE INDEX IF NOT EXISTS ux_papers_doi         ON papers (doi)      WHERE doi IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS ux_papers_arxiv_id    ON papers (arxiv_id) WHERE arxiv_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_papers_title_key ON papers (title_key);
CREATE INDEX IF NOT EXISTS ix_papers_year      ON papers (year);

CREATE TABLE IF NOT EXISTS authors (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL CHECK (length(trim(name)) > 0),
    name_key TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS paper_authors (          -- stored edge AUTHORED_BY (paper -> author)
    paper_id  INTEGER NOT NULL REFERENCES papers  (id) ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES authors (id) ON DELETE CASCADE,
    position  INTEGER NOT NULL CHECK (position >= 1),
    PRIMARY KEY (paper_id, author_id),
    UNIQUE (paper_id, position)
);
CREATE INDEX IF NOT EXISTS ix_paper_authors_author ON paper_authors (author_id);

CREATE TABLE IF NOT EXISTS topics (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL CHECK (length(trim(name)) > 0),
    name_key TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS paper_topics (           -- stored edge HAS_TOPIC (paper -> topic)
    paper_id   INTEGER NOT NULL REFERENCES papers (id) ON DELETE CASCADE,
    topic_id   INTEGER NOT NULL REFERENCES topics (id) ON DELETE CASCADE,
    source     TEXT NOT NULL CHECK (source IN ('author', 'api', 'yake', 'manual')),
    api_name   TEXT,
    confidence TEXT NOT NULL CHECK (confidence IN ('verified', 'estimated')),
    PRIMARY KEY (paper_id, topic_id)
);
CREATE INDEX IF NOT EXISTS ix_paper_topics_topic ON paper_topics (topic_id);

CREATE TABLE IF NOT EXISTS paper_references (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id  INTEGER NOT NULL REFERENCES papers (id) ON DELETE CASCADE,
    position  INTEGER NOT NULL CHECK (position >= 1),
    raw_text  TEXT    NOT NULL,
    text_key  TEXT    NOT NULL,
    doi       TEXT,
    arxiv_id  TEXT,
    year      INTEGER,
    UNIQUE (paper_id, position)
);
CREATE INDEX IF NOT EXISTS ix_refs_paper ON paper_references (paper_id);
CREATE INDEX IF NOT EXISTS ix_refs_doi   ON paper_references (doi)      WHERE doi IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_refs_arxiv ON paper_references (arxiv_id) WHERE arxiv_id IS NOT NULL;

CREATE TABLE IF NOT EXISTS citations (              -- stored edge CITES (citing paper -> cited paper)
    citing_paper_id INTEGER NOT NULL REFERENCES papers (id) ON DELETE CASCADE,
    cited_paper_id  INTEGER NOT NULL REFERENCES papers (id) ON DELETE CASCADE,
    reference_id    INTEGER REFERENCES paper_references (id) ON DELETE SET NULL,
    match_method    TEXT NOT NULL CHECK (match_method IN ('doi', 'arxiv_id', 'title')),
    PRIMARY KEY (citing_paper_id, cited_paper_id),
    CHECK (citing_paper_id <> cited_paper_id)
);
CREATE INDEX IF NOT EXISTS ix_citations_cited ON citations (cited_paper_id);

CREATE TABLE IF NOT EXISTS activity_log (           -- no foreign key: log survives deletions
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT NOT NULL,
    action      TEXT NOT NULL CHECK (action IN ('upload', 'edit', 'tag_add', 'tag_remove', 'delete')),
    paper_id    INTEGER,
    paper_title TEXT,
    details     TEXT,
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);
CREATE INDEX IF NOT EXISTS ix_activity_created ON activity_log (created_at);
CREATE INDEX IF NOT EXISTS ix_activity_user    ON activity_log (username);

CREATE TABLE IF NOT EXISTS api_cache (              -- successful API responses only
    cache_key  TEXT PRIMARY KEY,
    payload    TEXT NOT NULL,
    fetched_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

STEPS:
1. Import DB_PATH and ensure_dirs from backend.config.
2. get_conn: if db_path is None, call ensure_dirs() and use DB_PATH. Connect with sqlite3.connect(str(path), check_same_thread=False, timeout=10). Set conn.row_factory = sqlite3.Row. Execute "PRAGMA foreign_keys = ON". Return the connection. (db_path may be ":" + "memory:" for tests.)
3. init_db: if conn is None, open get_conn(), run executescript(SCHEMA_SQL), commit, close. Otherwise run executescript(SCHEMA_SQL) on the given connection and commit.
4. db_session: open get_conn(db_path), yield it, close it in a finally block.
5. list_tables: SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name; return the names as a list of str.
6. Add an if __name__ == "__main__": block: call init_db(); open a connection with get_conn(); assert PRAGMA foreign_keys returns 1; print the table names and their count.

OUTPUT FORMAT: Only the complete contents of db.py in a single Python code block. No explanation before or after.
REMINDER: one file only; SCHEMA_SQL must be identical to the text above; no extra tables or columns.
```
Acceptance test: `python -m backend.db` prints nine table names (`activity_log, api_cache, authors, citations, paper_authors, paper_references, paper_topics, papers, topics`) and `9`; `data/library.db` exists. Run it twice - no error.
---
Prompt 3 - `backend/repo_aux.py`
Depends on: Prompt 2 · Modifies existing files: no
```text
ROLE: You are a senior Python backend engineer.
OBJECTIVE: Write ONE file, backend/repo_aux.py: data-access functions for the activity log and the API cache.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.

INTERFACE (must match exactly; conn is an sqlite3.Connection with row_factory sqlite3.Row):
  def log_activity(conn, username: str, action: str, paper_id: int | None, paper_title: str | None, details: str | None = None) -> int
      # inserts one row, returns its id
  def list_activity(conn, limit: int = 50, offset: int = 0, username: str | None = None) -> dict
      # returns {"total": int, "items": [dict, ...]} newest first (ORDER BY created_at DESC, id DESC)
      # item keys: id, username, action, paper_id, paper_title, details, created_at
      # if username is given, only rows with that exact username
  def cache_get(conn, cache_key: str, max_age_days: int) -> dict | None
      # parsed JSON payload if the row exists and is not older than max_age_days, else None
  def cache_put(conn, cache_key: str, payload: dict) -> None
      # INSERT OR REPLACE with the payload as JSON text

CONTEXT - tables (already created, do not create them):
  activity_log(id INTEGER PK, username TEXT, action TEXT IN ('upload','edit','tag_add','tag_remove','delete'), paper_id INTEGER, paper_title TEXT, details TEXT, created_at TEXT default current UTC)
  api_cache(cache_key TEXT PK, payload TEXT, fetched_at TEXT default current UTC in format %Y-%m-%dT%H:%M:%SZ)
Timestamps use SQLite: strftime('%Y-%m-%dT%H:%M:%SZ', 'now'). For the age check use: fetched_at >= strftime('%Y-%m-%dT%H:%M:%SZ', 'now', ?) with the parameter f"-{max_age_days} days".

STEPS:
1. Implement the four functions with ? placeholders. None of them calls commit.
2. Convert sqlite3.Row objects to dict with dict(row).
3. Add an if __name__ == "__main__": block that opens get_conn(":memory:") from backend.db, calls init_db(conn), logs two activities, checks list_activity totals and the username filter, puts and gets a cache payload (max_age_days=30), asserts the results, and prints "repo_aux OK".

OUTPUT FORMAT: Only the complete contents of repo_aux.py in a single Python code block. No explanation before or after.
REMINDER: one file only; no commit() calls; only the four listed functions.
```
Acceptance test: `python -m backend.repo_aux` prints `repo_aux OK`.
---
Prompt 4 - `backend/repo_write.py`
Depends on: Prompts 1, 2 · Modifies existing files: no
```text
ROLE: You are a senior Python backend engineer.
OBJECTIVE: Write ONE file, backend/repo_write.py: all INSERT / UPDATE / DELETE data-access functions for papers, authors, topics and references.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.

INTERFACE (must match exactly; conn is an sqlite3.Connection):
  def insert_paper(conn, *, title: str, abstract: str | None, year: int | None, venue: str | None,
                   doi: str | None, arxiv_id: str | None, file_sha256: str, stored_filename: str,
                   original_filename: str, page_count: int | None, enriched_from: list[str],
                   uploaded_by: str) -> int
  def set_paper_authors(conn, paper_id: int, author_names: list[str]) -> None
  def add_paper_topic(conn, paper_id: int, name: str, source: str, confidence: str, api_name: str | None = None) -> int | None
  def remove_paper_topic(conn, paper_id: int, topic_id: int) -> bool
  def insert_references(conn, paper_id: int, refs: list[dict]) -> int
  def update_paper_fields(conn, paper_id: int, fields: dict) -> bool
  def delete_paper(conn, paper_id: int) -> str | None

CONTEXT - tables (already created, do not create them):
  papers(id, title, title_key, abstract, year, venue, doi, arxiv_id, file_sha256, stored_filename, original_filename, page_count, enriched_from, uploaded_by, uploaded_at, updated_at)
  authors(id, name, name_key UNIQUE)
  paper_authors(paper_id, author_id, position)  PRIMARY KEY(paper_id, author_id), UNIQUE(paper_id, position)
  topics(id, name, name_key UNIQUE)
  paper_topics(paper_id, topic_id, source IN ('author','api','yake','manual'), api_name, confidence IN ('verified','estimated'))
  paper_references(id, paper_id, position, raw_text, text_key, doi, arxiv_id, year)
Foreign keys use ON DELETE CASCADE, so deleting a paper automatically deletes its rows in paper_authors, paper_topics, paper_references and citations (foreign keys are switched on by the connection).
Helpers available: from backend.text_utils import normalize_title, normalize_name, normalize_topic, normalize_doi, normalize_arxiv_id

STEPS (per function):
- insert_paper: title_key = normalize_title(title); doi = normalize_doi(doi) if doi else None; arxiv_id = normalize_arxiv_id(arxiv_id) if arxiv_id else None; enriched_from stored as ",".join(list) or None. INSERT; return cursor.lastrowid. Let sqlite3.IntegrityError propagate.
- set_paper_authors: DELETE FROM paper_authors WHERE paper_id = ?. Walk the names in order, skip blank names, skip names whose normalize_name key was already seen, keep at most backend.config.MAX_AUTHORS. For each: INSERT OR IGNORE INTO authors(name, name_key); SELECT id by name_key; INSERT INTO paper_authors(paper_id, author_id, position) with position starting at 1. Finally delete orphans: DELETE FROM authors WHERE id NOT IN (SELECT author_id FROM paper_authors).
- add_paper_topic: key = normalize_topic(name); if the stripped name has fewer than 2 or more than 60 characters or the key is empty return None. INSERT OR IGNORE INTO topics(name, name_key); SELECT id; INSERT OR IGNORE INTO paper_topics(paper_id, topic_id, source, api_name, confidence). Return the topic id.
- remove_paper_topic: DELETE the paper_topics row; if no row was deleted return False; otherwise delete orphan topics (DELETE FROM topics WHERE id NOT IN (SELECT topic_id FROM paper_topics)) and return True.
- insert_references: refs items have keys raw_text, text_key, doi, arxiv_id, year. Insert each non-blank raw_text with position 1, 2, 3 ... in order. Return the number inserted.
- update_paper_fields: only these keys are allowed, others are ignored: title, abstract, year, venue, doi, arxiv_id. If title is present and blank after strip, raise ValueError. If title is present also set title_key = normalize_title(title). doi goes through normalize_doi and arxiv_id through normalize_arxiv_id (a blank value becomes None). Always set updated_at = strftime('%Y-%m-%dT%H:%M:%SZ','now'). Build the SET clause only from the fixed list of allowed column names; values are passed with ?. Return True if a row was updated.
- delete_paper: SELECT stored_filename FROM papers WHERE id = ?; if missing return None. DELETE FROM papers WHERE id = ?. Delete orphan authors and orphan topics as above. Return the stored_filename.
- Add an if __name__ == "__main__": block using get_conn(":memory:") and init_db(conn) from backend.db: insert one paper, set two authors, add one topic, insert two references, update the title, remove the topic, delete the paper; assert that the authors table is empty at the end; print "repo_write OK".

OUTPUT FORMAT: Only the complete contents of repo_write.py in a single Python code block. No explanation before or after.
REMINDER: one file only; never call commit(); no reads other than those described; only the listed functions.
```
Acceptance test: `python -m backend.repo_write` prints `repo_write OK`.
---
Prompt 5 - `backend/repo_read.py`
Depends on: Prompts 1, 2, 4 (tables must exist) · Modifies existing files: no
```text
ROLE: You are a senior Python backend engineer.
OBJECTIVE: Write ONE file, backend/repo_read.py: read-only data-access functions (detail, list/search, topics, duplicate lookup).
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.

INTERFACE (must match exactly; conn is an sqlite3.Connection with row_factory sqlite3.Row):
  def get_paper_detail(conn, paper_id: int) -> dict | None
  def list_papers(conn, q: str | None = None, author: str | None = None, topic: str | None = None,
                  year: int | None = None, limit: int = 50, offset: int = 0) -> dict
  def list_topics(conn) -> list[dict]
  def find_duplicate(conn, *, file_sha256: str | None = None, doi: str | None = None,
                     arxiv_id: str | None = None, title_key: str | None = None) -> dict | None
  def count_papers(conn) -> int

CONTEXT - tables (already created):
  papers(id, title, title_key, abstract, year, venue, doi, arxiv_id, file_sha256, stored_filename, original_filename, page_count, enriched_from, uploaded_by, uploaded_at, updated_at)
  authors(id, name, name_key); paper_authors(paper_id, author_id, position)
  topics(id, name, name_key); paper_topics(paper_id, topic_id, source, api_name, confidence)
  paper_references(id, paper_id, position, raw_text, text_key, doi, arxiv_id, year)
  citations(citing_paper_id, cited_paper_id, reference_id, match_method)

RETURN SHAPES:
  get_paper_detail -> None if the paper does not exist, else a dict with keys:
    id, title, abstract, year, venue, doi, arxiv_id, page_count, enriched_from (list of str: split the stored text on "," ; empty or NULL -> []),
    original_filename, uploaded_by, uploaded_at, updated_at,
    authors: [{"id", "name"}] ordered by paper_authors.position,
    tags: [{"id", "name", "source", "api_name", "confidence"}] ordered by topic name,
    references: [{"id", "position", "raw_text", "doi", "arxiv_id", "year", "cited_paper_id"}] ordered by position;
       cited_paper_id comes from LEFT JOIN citations c ON c.reference_id = paper_references.id (None if no match),
    cites: [{"paper_id", "title"}]    papers this paper cites (citations.citing_paper_id = id), ordered by title,
    cited_by: [{"paper_id", "title"}] papers citing this paper (citations.cited_paper_id = id), ordered by title
  list_papers -> {"total": int, "items": [summary, ...]} ordered by uploaded_at DESC, id DESC.
    summary keys: id, title, year, venue, doi, arxiv_id, authors (list of name strings in position order),
    tags (list of {"id","name","source","confidence"}), uploaded_by, uploaded_at.
    Filters (all optional, combined with AND, all substring matches that ignore case):
      q: matches papers.title OR any author name OR any topic name of the paper
      author: matches any author name of the paper
      topic: matches any topic name of the paper
      year: papers.year equals the integer
    limit is clamped to 1..200 and offset to >= 0. total counts all matches before limit/offset.
  list_topics -> [{"id", "name", "paper_count"}] ordered by paper_count DESC then name.
  find_duplicate -> None or {"kind": "duplicate_paper" | "possible_duplicate", "paper_id": int, "title": str, "matched_on": "sha256" | "doi" | "arxiv_id" | "title"}.
    Check in this order and return the first hit: file_sha256 = papers.file_sha256; doi = papers.doi (compare lower-case);
    arxiv_id = papers.arxiv_id; these three give kind "duplicate_paper". Then title_key = papers.title_key gives kind "possible_duplicate".
    Skip any argument that is None or empty.

STEPS:
1. Write a private helper _like(term: str) -> str that escapes the characters \ % _ with a backslash and wraps the result in % ... %. Use it in SQL as: column LIKE ? ESCAPE '\'.
2. list_papers: build the WHERE conditions as a list of fixed SQL strings and a list of parameter values. For author/topic/q use EXISTS (SELECT 1 FROM paper_authors pa JOIN authors a ON a.id = pa.author_id WHERE pa.paper_id = p.id AND a.name LIKE ? ESCAPE '\') and the equivalent EXISTS for topics. Run one COUNT(*) query for total and one SELECT with LIMIT ? OFFSET ?. Then load authors and tags for the page's paper ids with one query each, using an IN (...) clause whose placeholders are generated as ",".join("?" * n) (only the placeholder string is built dynamically, never the values). Return an empty items list when the page has no rows.
3. Implement get_paper_detail, list_topics, find_duplicate and count_papers as described.
4. Add an if __name__ == "__main__": block: open get_conn(":memory:") from backend.db, init_db(conn), insert two papers with insert_paper, set_paper_authors, add_paper_topic (all from backend.repo_write, called inside "with conn:"), then assert: list_papers filters by q/author/topic/year work, get_paper_detail returns the authors and tags, find_duplicate finds a stored doi and a stored title_key, list_topics counts correctly. Print "repo_read OK".

OUTPUT FORMAT: Only the complete contents of repo_read.py in a single Python code block. No explanation before or after.
REMINDER: one file only; read-only functions; never build SQL values with string formatting; only the listed functions.
```
Acceptance test: `python -m backend.repo_read` prints `repo_read OK`.
---
Prompt 6 - `backend/pdf_text.py`
Depends on: Prompt 0 · Modifies existing files: no
```text
ROLE: You are a senior Python engineer who knows the PyMuPDF library.
OBJECTIVE: Write ONE file, backend/pdf_text.py, that reads a text-based research-paper PDF and returns text in reading order plus page-1 line data.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.
Use only: import pymupdf (the PyMuPDF package, version 2.0), re, pathlib, sys.

INTERFACE (must match exactly):
  class PdfReadError(Exception): ...        # file cannot be opened, is corrupt or password-protected
  class NoTextLayerError(Exception): ...    # fewer than MIN_TEXT_CHARS non-whitespace characters in the whole document
  def extract_pdf(path: str | Path) -> dict
Returned dict (exact keys):
  {"page_count": int,
   "raw_text": str,                 # all pages joined with "\n", from page.get_text("text"), nothing removed
   "first_page_raw_text": str,      # page 1 only, same method
   "body_text": str,                # reading-order text of all pages, margins removed, pages joined with "\n\n"
   "first_page_body_text": str,     # same, page 1 only
   "first_page_lines": [{"text": str, "size": float, "x0": float, "y0": float, "x1": float, "y1": float}, ...],
   "page_width": float, "page_height": float,           # of page 1
   "doc_metadata": {"title": str, "author": str, "keywords": str}}   # from doc.metadata, "" when missing or None
Also a private helper:
  def _order_blocks(blocks: list[dict], page_width: float) -> list[dict]
      # blocks are dicts with keys x0, y0, x1, y1 (and possibly more); returns the same dict objects in reading order

CONTEXT:
- Many papers have two columns. Reading order rule for _order_blocks (implement exactly):
  a block is "full" if x0 < 0.45 * page_width and x1 > 0.55 * page_width;
  otherwise it is "left" if x1 <= 0.55 * page_width, otherwise "right" if x0 >= 0.45 * page_width, otherwise "full".
  Sort all blocks by (y0, x0). Walk them in that order keeping two buffers left_buf and right_buf.
  A left block goes into left_buf, a right block into right_buf. When a full block is met: output left_buf (sorted by y0), then right_buf (sorted by y0), then the full block, then empty both buffers. After the last block output left_buf then right_buf.
- PyMuPDF calls: doc = pymupdf.open(str(path)); doc.needs_pass; len(doc); doc[i]; page.rect.width; page.rect.height; page.get_text("text"); page.get_text("blocks") returns tuples (x0, y0, x1, y1, text, block_no, block_type) where block_type 0 means text; page.get_text("dict")["blocks"] gives blocks with "type" (0 = text), "bbox" and "lines"; each line has "bbox" and "spans"; each span has "text" and "size". doc.metadata is a dict or None. Close the document with doc.close().
- Margins: for body text ignore text blocks with y1 < 0.05 * page_height or y0 > 0.95 * page_height (headers, footers, page numbers).
- Ligatures: replace these characters in all returned text: "\ufb01"->"fi", "\ufb02"->"fl", "\ufb00"->"ff", "\ufb03"->"ffi", "\ufb04"->"ffl".
- Hyphenation: in body text join a word split at a line end with a hyphen when the next line starts with a lower-case letter: re.sub(r"([a-z])-\n([a-z])", r"\1\2", text).

STEPS:
1. Open the PDF inside try/except; any exception -> raise PdfReadError with a short message. If doc.needs_pass is true, close and raise PdfReadError("PDF is password-protected").
2. Build raw_text and first_page_raw_text (apply the ligature replacement). Count characters that are not whitespace in raw_text; if the count is below MIN_TEXT_CHARS (backend.config) close the document and raise NoTextLayerError.
3. For every page: take page.get_text("blocks"), keep block_type 0, convert each to a dict {x0, y0, x1, y1, text}, drop margin blocks, order with _order_blocks, join the stripped block texts with "\n", apply the ligature and hyphenation fixes. body_text joins pages with "\n\n"; first_page_body_text is page 1.
4. For page 1 only: take page.get_text("dict")["blocks"], keep type 0, make dicts with x0, y0, x1, y1 from "bbox" plus the "lines" list, order them with _order_blocks, then flatten their lines in that order. For each line: text = "".join(span["text"]) stripped (skip empty), size = max span size, x0..y1 from the line bbox. Apply the ligature replacement to the text. Do NOT drop margin lines here.
5. Read page_width and page_height from page 1; read doc_metadata; close the document; return the dict.
6. Add an if __name__ == "__main__": block: read a PDF path from sys.argv[1]; call extract_pdf; print page_count, the first 400 characters of first_page_body_text, and the number of first_page_lines with the three largest font sizes. Catch PdfReadError and NoTextLayerError and print their message.

OUTPUT FORMAT: Only the complete contents of pdf_text.py in a single Python code block. No explanation before or after.
REMINDER: one file only; use pymupdf only; no OCR; keep the dict keys exactly as listed.
```
Acceptance test: put a two-column open-access PDF in `sample_papers/`; `python -m backend.pdf_text sample_papers/<file>.pdf` prints the page count, readable paragraph text (not interleaved columns) and the largest font sizes. A plain text file renamed to `.pdf` prints the PdfReadError message.
---
Prompt 7 - `backend/parse_title_authors.py`
Depends on: Prompts 0, 6 · Modifies existing files: no
```text
ROLE: You are a senior Python engineer.
OBJECTIVE: Write ONE file, backend/parse_title_authors.py, with heuristics that find the title and the author names on page 1 of a research paper. Standard library only.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.

INTERFACE (must match exactly):
  def extract_title(lines: list[dict], page_height: float, doc_title: str = "") -> str | None
  def extract_authors(lines: list[dict], title: str | None) -> list[str]
Input "lines" is the list first_page_lines in reading order; each item is {"text": str, "size": float, "x0": float, "y0": float, "x1": float, "y1": float}.

CONTEXT - rules to implement exactly:
extract_title:
 1. Candidates = lines with y0 < 0.5 * page_height and at least 3 non-space characters whose lower-cased text does NOT start with any of: "arxiv", "preprint", "accepted", "published", "proceedings", "journal", "copyright", "doi", "http", "www", "vol", "under review", "©".
 2. If there are candidates: max_size = largest size among them. Title lines = the first candidate whose size >= max_size - 0.6, plus the directly following candidates (consecutive in the candidate list) whose size >= max_size - 0.6 and whose vertical gap (y0 of next minus y1 of previous) is at most 1.5 * the size. Stop at the first line that breaks this chain.
 3. Join the title lines with single spaces, repair "- " line-break hyphens only when the next piece starts with a lower-case letter, collapse whitespace, strip. Return it if it has at least 5 characters.
 4. Otherwise (or when nothing qualifies) fall back to doc_title if, after strip, it has at least 10 characters, does not end with ".pdf", ".doc" or ".docx", and its lower-case form is not one of "untitled", "microsoft word"; else return None.
extract_authors:
 1. If title is None return [].
 2. Find the index of the last title line (the last line whose text, lower-cased, is contained in the lower-cased title); take the lines AFTER it, at most 15 lines, stopping before the first line whose lower-case text starts with "abstract", "keywords", "index terms" or "introduction", or whose y0 is greater than 0.6 * page height (use the largest y1 among the input lines as the page height proxy).
 3. Skip a line if it contains "@" or any of these words (case-insensitive): university, universit, institute, department, school, laboratory, lab, college, centre, center, corporation, inc., ltd, research, faculty, hospital, academy, technology, google, microsoft, facebook, openai.
 4. In the remaining lines remove footnote markers with re.sub(r"[\d*\u2020\u2021\u00a7\u00b6]+", "", line). Split on commas, semicolons, the middle dot, the bullet, "&" and the word "and" (r",|;|\u00b7|\u2022|&|\band\b").
 5. Accept a piece after strip if it has 2 to 5 whitespace-separated words, each word starts with an upper-case letter (initials like "J." and particles like "van" are fine only if at least two words start upper-case), has at most 60 characters and contains no digit.
 6. Remove duplicates keeping order and return at most backend.config.MAX_AUTHORS names. Return [] if nothing is accepted.

STEPS:
1. Implement the two functions with small private helpers where useful.
2. Add an if __name__ == "__main__": block that reads a PDF path from sys.argv[1], calls backend.pdf_text.extract_pdf, then extract_title and extract_authors, and prints the title and the authors list.
3. In the same block also assert on this synthetic input: lines = [{"text":"Deep Learning for Everyone","size":20.0,"x0":50,"y0":60,"x1":400,"y1":80},{"text":"Jane Doe1, John Smith2","size":11.0,"x0":50,"y0":100,"x1":300,"y1":112},{"text":"1 Example University","size":9.0,"x0":50,"y0":115,"x1":300,"y1":124},{"text":"Abstract","size":10.0,"x0":50,"y0":150,"x1":100,"y1":160}] gives title "Deep Learning for Everyone" and authors ["Jane Doe", "John Smith"] (run the asserts only when no sys.argv[1] is given).

OUTPUT FORMAT: Only the complete contents of parse_title_authors.py in a single Python code block. No explanation before or after.
REMINDER: one file only; standard library plus backend.config and backend.pdf_text imports only inside the main block; no extra functions except underscore helpers.
```
Acceptance test: `python -m backend.parse_title_authors` (no argument) passes the synthetic asserts; then on three sample PDFs it prints a plausible title and author list (note failures for Section I).
---
Prompt 8 - `backend/parse_abstract_keywords.py`
Depends on: Prompt 6 · Modifies existing files: no
```text
ROLE: You are a senior Python engineer.
OBJECTIVE: Write ONE file, backend/parse_abstract_keywords.py, with heuristics that find the abstract, the author keywords and the publication year of a research paper. Standard library only (re, datetime).
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.

INTERFACE (must match exactly):
  def extract_abstract(first_page_body_text: str) -> str | None
  def extract_keywords(first_page_body_text: str, doc_keywords: str = "") -> list[str]
  def extract_year(first_page_raw_text: str, arxiv_id: str | None = None) -> int | None

CONTEXT - rules to implement exactly:
extract_abstract:
 - Find the heading with re.search(r"(?im)^\s*abstract\b[\s:.\-\u2014\u2013]*", text). The abstract starts right after the match (it may continue on the same line).
 - It ends at the earliest of these, searched after the start: r"(?im)^\s*(index terms|key\s*words?|keywords?)\b", r"(?im)^\s*(\d+|[ivx]+)[.\s]+\s*introduction\b", r"(?im)^\s*introduction\s*$". If none is found, take at most 3000 characters.
 - Join lines with single spaces, repair a line-end hyphen only when the next character is lower-case, collapse whitespace. Return None if the result has fewer than 50 characters or if no heading was found.
extract_keywords:
 - Find r"(?im)^\s*(index terms|key\s*words?|keywords?)\s*[:\-\u2014\u2013.]*\s*". Take the text after it up to the first blank line (r"\n\s*\n") or up to the next heading matching r"(?im)^\s*(\d+|[ivx]+)[.\s]+\s*introduction\b" or r"(?im)^\s*introduction\s*$", at most 400 characters; join lines with spaces.
 - Split on r"[,;\u00b7\u2022]", strip spaces and a final ".", keep items with 2 to 60 characters, remove duplicates (case-insensitive, keep the first), at most 10 items.
 - If the text has no keywords line or the result is empty, split doc_keywords the same way (only on "," and ";") and return that result (also at most 10). Otherwise return [].
extract_year:
 - Look at lines of first_page_raw_text whose lower-case text contains one of: "©", "copyright", "published", "accepted", "received", "revised", "available online", "proceedings". In those lines find all four-digit numbers matching r"\b(19[5-9]\d|20\d\d)\b". Let limit = datetime.date.today().year + 1. Return the largest number that is <= limit.
 - If none and arxiv_id matches r"^(\d{2})(\d{2})\.\d{4,5}$" return 2000 + int(first group). Otherwise return None.

STEPS:
1. Implement the three functions.
2. Add an if __name__ == "__main__": block with asserts, then print "parse_abstract_keywords OK":
   text = "Title line\nJane Doe\nAbstract\u2014We study deep nets and show\nthat they work well in many settings of interest to us all.\nKeywords: deep learning, optimisation; vision.\n1. Introduction\nBody."
   extract_abstract(text) starts with "We study deep nets" and contains "work well"
   extract_keywords(text) == ["deep learning", "optimisation", "vision"]
   extract_keywords("no keywords here", "a, b; c") == ["a", "b", "c"]
   extract_year("\u00a9 2019 IEEE\nSomething 2031") == 2019
   extract_year("nothing", "1706.03762") == 2017
   extract_abstract("no heading at all") is None

OUTPUT FORMAT: Only the complete contents of parse_abstract_keywords.py in a single Python code block. No explanation before or after.
REMINDER: one file only; standard library only; no extra functions except underscore helpers.
```
Acceptance test: `python -m backend.parse_abstract_keywords` prints `parse_abstract_keywords OK` (the year test must return 2019 because only the line containing "©" is examined).
---
Prompt 9 - `backend/references.py`
Depends on: Prompts 0, 1, 6 · Modifies existing files: no
```text
ROLE: You are a senior Python engineer.
OBJECTIVE: Write ONE file, backend/references.py, that finds the reference list in the body text of a research paper, splits it into separate references and extracts identifiers from each. Standard library only (re).
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.

INTERFACE (must match exactly):
  def find_reference_section(body_text: str) -> str | None
  def split_references(section_text: str) -> list[str]
  def parse_reference(raw_text: str) -> dict
  def extract_references(body_text: str) -> list[dict]
parse_reference returns {"raw_text": str, "text_key": str, "doi": str | None, "arxiv_id": str | None, "year": int | None}.
Import: from backend.text_utils import find_doi, find_arxiv_id, normalize_title, clean_whitespace ; from backend.config import MAX_REFERENCES

CONTEXT - rules to implement exactly:
find_reference_section:
 - A heading is a line matching r"(?im)^\s*(?:\d+\.?\s+|[IVX]+\.?\s+)?(references|bibliography|literature cited|works cited)\s*$".
 - Use the LAST heading in the text. The section is everything after it, stopped before the first later line matching r"(?im)^\s*(appendix|appendices|supplementary material)\b". Return the stripped section, or None if no heading exists or the section has fewer than 50 characters.
split_references:
 - Work on lines. Style A (numbered brackets): if at least 3 lines start with r"^\s*\[\d+\]", a new reference begins at every such line.
 - Style B (numbered list): else if at least 3 lines start with r"^\s*\d{1,3}[.)]\s+", a new reference begins at every such line.
 - Style C (author-year): else a new reference begins at a line that matches r"^[A-Z][A-Za-z'\u2019\-]+,\s+(?:[A-Z]\.|[A-Z][a-z]+)" AND the reference collected so far ends with "." or ")".
 - Style D: if styles A to C produce fewer than 2 references, split on blank lines instead.
 - Join the continuation lines of a reference with single spaces (collapse whitespace). Drop references shorter than 20 characters. Return at most MAX_REFERENCES items. Keep the leading "[1]" or "1." markers in the text.
parse_reference:
 - raw_text = clean_whitespace(raw_text); doi = find_doi(raw_text); arxiv_id = find_arxiv_id(raw_text); text_key = normalize_title(raw_text).
 - year: first match of r"\((19[5-9]\d|20\d\d)[a-z]?\)" if any; otherwise the LAST match of r"\b(19[5-9]\d|20\d\d)\b"; otherwise None. Return the year as int.
extract_references(body_text): find_reference_section, then split_references, then parse_reference for each item; return [] when there is no section.

STEPS:
1. Implement the four functions.
2. Add an if __name__ == "__main__": block that reads a PDF path from sys.argv[1] when given, calls backend.pdf_text.extract_pdf and prints the number of references and the first three raw_text values; when no argument is given run these asserts and print "references OK":
   sample = "Intro text.\n\nReferences\n[1] A. Author, B. Writer, Deep nets, in Proc. CVPR, 2016, doi: 10.1109/CVPR.2016.90.\n[2] C. Person, Learning to learn, arXiv:1706.03762v5, 2017.\n[3] D. Third, A very long title that\ncontinues on the next line, Journal X, 2015."
   refs = extract_references(sample); len(refs) == 3; refs[0]["doi"] == "10.1109/cvpr.2016.90"; refs[1]["arxiv_id"] == "1706.03762"; refs[2]["year"] == 2015 and "continues on the next line" in refs[2]["raw_text"]

OUTPUT FORMAT: Only the complete contents of references.py in a single Python code block. No explanation before or after.
REMINDER: one file only; standard library only; exact function names and dict keys.
```
Acceptance test: `python -m backend.references` prints `references OK`; on a sample PDF (`python -m backend.references sample_papers/<file>.pdf`) the count is close to the paper's real reference count.
---
Prompt 10 - `backend/http_utils.py`
Depends on: Prompt 0 · Modifies existing files: no
```text
ROLE: You are a senior Python engineer who knows httpx.
OBJECTIVE: Write ONE file, backend/http_utils.py: a polite async GET helper with per-host throttling and bounded retries.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.
Use only: httpx (version 0.28.1), asyncio, time, urllib.parse.

INTERFACE (must match exactly):
  def build_headers(extra: dict | None = None) -> dict
  async def get_with_retry(client: httpx.AsyncClient, url: str, params: dict | None = None, headers: dict | None = None) -> httpx.Response | None
Imports: from backend.config import HTTP_MAX_RETRIES, MIN_INTERVAL_SECONDS, USER_AGENT_BASE, get_crossref_mailto

CONTEXT:
- Requests are made one at a time (never concurrently), so a plain module-level dict is enough: _last_request: dict[str, float] mapping host name -> time.monotonic() of the last request to that host.
- Public API limits we must respect: Crossref 5 requests/second, arXiv 1 request every 3 seconds, Semantic Scholar 1 request/second, OpenAlex 10 requests/second. The minimum gaps are in MIN_INTERVAL_SECONDS (host -> seconds); hosts that are not in the dict get 0.
- Retry only on HTTP 429, 500, 502, 503, 504 and on httpx.RequestError (timeouts, connection errors).

STEPS:
1. build_headers: start with {"User-Agent": USER_AGENT_BASE}; if get_crossref_mailto() returns a value, set the User-Agent to f"{USER_AGENT_BASE} (mailto:{mailto})". Update with extra when given. Return the dict.
2. get_with_retry: host = urllib.parse.urlparse(url).netloc. For attempt in range(HTTP_MAX_RETRIES + 1):
   a. Throttle: wait = MIN_INTERVAL_SECONDS.get(host, 0.0) - (time.monotonic() - _last_request.get(host, -1e9)); if wait > 0: await asyncio.sleep(wait). Then record _last_request[host] = time.monotonic().
   b. Try resp = await client.get(url, params=params, headers=build_headers(headers)); on httpx.RequestError set resp = None.
   c. If resp is not None and resp.status_code not in (429, 500, 502, 503, 504): return resp (this includes 200 and 404).
   d. If this was the last attempt return None.
   e. Delay before the next attempt: if resp has a numeric Retry-After header use min(float(value), 10.0); otherwise 2 ** attempt seconds (1 then 2). await asyncio.sleep(delay).
3. Never raise to the caller; never log secrets.
4. Add an if __name__ == "__main__": block (no network) that asserts build_headers() contains "User-Agent" and build_headers({"x-api-key": "k"})["x-api-key"] == "k", then prints "http_utils OK".

OUTPUT FORMAT: Only the complete contents of http_utils.py in a single Python code block. No explanation before or after.
REMINDER: one file only; httpx and standard library only; exact signatures.
```
Acceptance test: `python -m backend.http_utils` prints `http_utils OK`.
---
Prompt 11 - `backend/clients_json.py`
Depends on: Prompts 0, 1, 10 · Modifies existing files: no
```text
ROLE: You are a senior Python engineer who knows httpx and REST APIs.
OBJECTIVE: Write ONE file, backend/clients_json.py: three async clients that look up one paper in Crossref, OpenAlex and Semantic Scholar and return a normalised dict.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.
Use only: httpx, urllib.parse, re, and the project modules named below.

INTERFACE (must match exactly):
  async def fetch_crossref(client: httpx.AsyncClient, doi: str) -> dict | None
  async def fetch_openalex(client: httpx.AsyncClient, doi: str) -> dict | None
  async def fetch_semantic_scholar(client: httpx.AsyncClient, paper_id: str) -> dict | None   # paper_id like "DOI:10.1109/cvpr.2016.90" or "ARXIV:1706.03762"
Every function returns None when the response is missing, not HTTP 200, or not valid JSON; otherwise a dict with EXACTLY these keys:
  {"source": "crossref" | "openalex" | "semantic_scholar", "title": str | None, "authors": [str], "year": int | None,
   "venue": str | None, "abstract": str | None, "doi": str | None, "arxiv_id": str | None, "topics": [str]}
Imports: from backend.http_utils import get_with_retry ; from backend.config import CROSSREF_URL, OPENALEX_URL, S2_URL, get_crossref_mailto, get_openalex_key, get_s2_key ; from backend.text_utils import normalize_doi, normalize_arxiv_id, clean_whitespace

CONTEXT - requests and field mapping:
Crossref: GET CROSSREF_URL + urllib.parse.quote(doi, safe="/"); params {"mailto": mailto} only if get_crossref_mailto() is set. JSON: data["message"]. Mapping: title = message["title"][0] if the list is non-empty; authors = for each item in message.get("author", []): "given family" joined (skip missing parts) or item["name"]; year = message["issued"]["date-parts"][0][0] if present; venue = message["container-title"][0] if non-empty; abstract = message.get("abstract") with XML tags removed (re.sub(r"<[^>]+>", " ", text)) and whitespace cleaned; doi = normalize_doi(message["DOI"]); arxiv_id None; topics = message.get("subject", []).
OpenAlex: GET OPENALEX_URL + "https://doi.org/" + doi ; params {"api_key": key} only if get_openalex_key() is set. JSON is the work object. Mapping: title = work.get("title") or work.get("display_name"); authors = [a["author"]["display_name"] for a in work.get("authorships", [])]; year = work.get("publication_year"); venue = work["primary_location"]["source"]["display_name"] when primary_location and its source are not None; abstract rebuilt from work["abstract_inverted_index"] (a dict word -> list of positions): create a list with one slot per position, put each word at its positions, join the filled slots with spaces; None if the index is missing; doi = normalize_doi(work["doi"]) if present (value looks like "https://doi.org/10..."); arxiv_id None; topics = display_name of every item of work.get("topics", []) plus every item of work.get("keywords", []) (each item is a dict with "display_name"), without duplicates, at most 15.
Semantic Scholar: GET S2_URL + urllib.parse.quote(paper_id, safe=":/") ; params {"fields": "title,abstract,year,venue,authors,externalIds,fieldsOfStudy"}; headers {"x-api-key": key} only if get_s2_key() is set. Mapping: title, abstract, year as given; venue = data["venue"] or None when empty; authors = [a["name"] for a in data.get("authors", [])]; doi = normalize_doi(data["externalIds"]["DOI"]) if present; arxiv_id = normalize_arxiv_id(data["externalIds"]["ArXiv"]) if present; topics = data.get("fieldsOfStudy") or [].
General rules: strip titles with clean_whitespace; convert empty strings to None; year must be an int or None; never raise (wrap parsing in try/except Exception and return None); use only .get() access for optional fields.

STEPS:
1. Implement a private helper _to_result(...) if useful so that all three functions return the same keys.
2. Implement the three functions with get_with_retry(client, url, params=..., headers=...).
3. Add an if __name__ == "__main__": block that uses httpx.AsyncClient(timeout=10.0, follow_redirects=True) inside asyncio.run to look up the DOI 10.1109/cvpr.2016.90 in all three services and print for each service either the title, first author and year, or "no data". No asserts (it needs the network).

OUTPUT FORMAT: Only the complete contents of clients_json.py in a single Python code block. No explanation before or after.
REMINDER: one file only; exact signatures and dict keys; no keys or e-mail addresses in the code.
```
Acceptance test (needs internet): `python -m backend.clients_json` prints a title/author/year line for Crossref, OpenAlex and Semantic Scholar (or `no data` for a service that is down or rate-limited - wait and retry). If a field is always empty, note it in Section I and improve the field mapping in this prompt.
---
Prompt 12 - `backend/client_arxiv.py`
Depends on: Prompts 0, 1, 10 · Modifies existing files: no
```text
ROLE: You are a senior Python engineer who knows httpx and XML parsing.
OBJECTIVE: Write ONE file, backend/client_arxiv.py: an async client that looks up one paper in the arXiv API and returns a normalised dict.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.
Use only: httpx, xml.etree.ElementTree, and the project modules named below.

INTERFACE (must match exactly):
  async def fetch_arxiv(client: httpx.AsyncClient, arxiv_id: str) -> dict | None
Returns None when the response is missing, not HTTP 200, not valid XML, or the feed contains no real entry; otherwise exactly:
  {"source": "arxiv", "title": str | None, "authors": [str], "year": int | None, "venue": None,
   "abstract": str | None, "doi": str | None, "arxiv_id": str | None, "topics": []}
Imports: from backend.http_utils import get_with_retry ; from backend.config import ARXIV_URL ; from backend.text_utils import clean_whitespace, normalize_doi, normalize_arxiv_id

CONTEXT:
- Request: GET ARXIV_URL with params {"id_list": arxiv_id, "max_results": 1}. The response is an Atom XML feed.
- Namespaces: atom = "http://www.w3.org/2005/Atom", arxiv = "http://arxiv.org/schemas/atom".
- Take the first {atom}entry. If there is none, or its {atom}title text is "Error", return None.
- Mapping: title = clean_whitespace of {atom}title; abstract = clean_whitespace of {atom}summary; authors = text of {atom}author/{atom}name for every author, in order; year = int of the first four characters of {atom}published; doi = normalize_doi of {arxiv}doi if that element exists else None; arxiv_id = normalize_arxiv_id(arxiv_id argument); venue None; topics [] (arXiv category codes are NOT used as topics).
- Empty strings become None. Never raise: wrap parsing in try/except Exception and return None.

STEPS:
1. Implement fetch_arxiv.
2. Add an if __name__ == "__main__": block that uses httpx.AsyncClient(timeout=10.0, follow_redirects=True) inside asyncio.run to look up "1706.03762" and prints the title, number of authors and year, or "no data". No asserts.

OUTPUT FORMAT: Only the complete contents of client_arxiv.py in a single Python code block. No explanation before or after.
REMINDER: one file only; exact signature and dict keys.
```
Acceptance test (needs internet): `python -m backend.client_arxiv` prints a title, an author count greater than 1 and a year (or `no data`; retry after a few seconds - arXiv allows one request every three seconds).
---
Prompt 13 - `backend/enrichment.py`
Depends on: Prompts 0, 1, 2, 3, 11, 12 · Modifies existing files: no
```text
ROLE: You are a senior Python engineer.
OBJECTIVE: Write ONE file, backend/enrichment.py: look up a paper in the scholarly APIs (with cache and safe fallback) and merge the results with the metadata parsed from the PDF.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.
Use only: httpx, asyncio, and the project modules named below.

INTERFACE (must match exactly):
  async def enrich_metadata(conn, parsed: dict, doi: str | None, arxiv_id: str | None) -> dict
Input parsed (from the PDF parser): {"title": str | None, "authors": [str], "abstract": str | None, "year": int | None, "venue": str | None}
Returns exactly:
  {"title": str | None, "authors": [str], "abstract": str | None, "year": int | None, "venue": str | None,
   "doi": str | None, "arxiv_id": str | None,
   "api_topics": [{"name": str, "api_name": str}],
   "enriched_from": [str],      # source names that returned data, in lookup order
   "warnings": [str]}
Imports: from backend.config import is_offline, CACHE_TTL_DAYS, HTTP_TIMEOUT_SECONDS ; from backend.repo_aux import cache_get, cache_put ; from backend.clients_json import fetch_crossref, fetch_openalex, fetch_semantic_scholar ; from backend.client_arxiv import fetch_arxiv ; from backend.text_utils import normalize_topic
Every client returns None or a dict {"source","title","authors","year","venue","abstract","doi","arxiv_id","topics"}.

STEPS:
1. Start from a copy of parsed values plus doi, arxiv_id, api_topics = [], enriched_from = [], warnings = [].
2. If is_offline(): add the warning "Offline mode: scholarly APIs skipped." and return.
3. If doi is None and arxiv_id is None: add the warning "No DOI or arXiv ID found; metadata comes from the PDF only." and return.
4. Build the lookup list in this order, each item (source_name, cache_key, async callable):
   if doi: ("crossref", f"crossref:{doi}", fetch_crossref(client, doi))
   if arxiv_id: ("arxiv", f"arxiv:{arxiv_id}", fetch_arxiv(client, arxiv_id))
   if doi: ("openalex", f"openalex:{doi}", fetch_openalex(client, doi))
   if doi: ("semantic_scholar", f"s2:DOI:{doi}", fetch_semantic_scholar(client, "DOI:" + doi))
   elif arxiv_id: ("semantic_scholar", f"s2:ARXIV:{arxiv_id}", fetch_semantic_scholar(client, "ARXIV:" + arxiv_id))
5. Create ONE httpx.AsyncClient(timeout=HTTP_TIMEOUT_SECONDS, follow_redirects=True) with "async with". Run the lookups one after another (never in parallel). For each: first try cache_get(conn, cache_key, CACHE_TTL_DAYS); if there is no cached dict, call the client inside try/except Exception; if the result is a dict, store it with "with conn: cache_put(conn, cache_key, result)". If the result is None add the warning f"{source_name} lookup returned no data." If an exception occurs add f"{source_name} lookup failed." Collect successful results in a dict by source name and append the source name to enriched_from.
6. Merge:
   - title, year, venue: the first non-empty value in the order crossref, arxiv, openalex, semantic_scholar; else keep the parsed value.
   - authors: the first non-empty list in the same order; else keep the parsed authors.
   - abstract: keep the parsed abstract if it has at least 50 characters; else the first non-empty abstract in the order arxiv, semantic_scholar, openalex, crossref; else None.
   - doi: the given doi, else the first doi found in any result. arxiv_id: the given arxiv_id, else the first arxiv_id found in any result.
   - api_topics: from crossref, openalex and semantic_scholar results only (in that order): every topic string as {"name": topic, "api_name": source_name}; skip duplicates by normalize_topic(topic).
7. Return the result dict. The function never raises.
8. Add an if __name__ == "__main__": block (using get_conn(":memory:") and init_db(conn) from backend.db and asyncio.run) that calls enrich_metadata with parsed = {"title": "PDF title", "authors": ["A. Person"], "abstract": None, "year": None, "venue": None}, doi "10.1109/cvpr.2016.90", arxiv_id None, and prints title, authors, year, enriched_from, api_topics and warnings. If is_offline() is true it just prints the offline result.

OUTPUT FORMAT: Only the complete contents of enrichment.py in a single Python code block. No explanation before or after.
REMINDER: one file only; sequential lookups; never raise; exact return keys.
```
Acceptance test: `OFFLINE_MODE=1 python -m backend.enrichment` (Windows: `set OFFLINE_MODE=1`) prints the offline warning and the unchanged title `PDF title`. Without `OFFLINE_MODE`, with internet, it prints the API title and a non-empty `enriched_from`.
---
Prompt 14 - `backend/tagging.py`
Depends on: Prompts 0, 1 · Modifies existing files: no
```text
ROLE: You are a senior Python engineer.
OBJECTIVE: Write ONE file, backend/tagging.py, that chooses topic tags for a paper with a strict priority order: author keywords, then scholarly-API topics, then YAKE keyword extraction.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.
Use only: yake (version 0.7.3) and the standard library.

INTERFACE (must match exactly):
  def build_tags(author_keywords: list[str], api_topics: list[dict], text: str, max_tags: int = MAX_TAGS_PER_PAPER) -> list[dict]
Each returned tag: {"name": str, "source": "author" | "api" | "yake", "api_name": str | None, "confidence": "verified" | "estimated"}
Imports: from backend.config import MAX_TAGS_PER_PAPER ; from backend.text_utils import normalize_topic, clean_whitespace
api_topics items look like {"name": "Computer vision", "api_name": "openalex"}.

CONTEXT - priority rules (implement exactly; ONE source group is used per paper):
 1. Clean author_keywords: clean_whitespace each, drop items shorter than 2 or longer than 60 characters, drop items that are only digits, drop duplicates by normalize_topic key (keep the first), keep at most max_tags. If at least one item remains, return them with source "author", api_name None, confidence "verified". STOP here.
 2. Otherwise clean api_topics the same way (use item["name"]; keep item["api_name"]). If at least one remains, return them with source "api", the item's api_name, confidence "verified". STOP here.
 3. Otherwise, if text has at least 200 characters, run YAKE: kw = yake.KeywordExtractor(lan="en", n=2, dedupLim=0.9, top=max_tags * 2); pairs = kw.extract_keywords(text[:20000]); each pair is (keyword, score) and a LOWER score is better. Sort by score ascending, clean like above (also drop keywords containing "@" or "http"), keep at most max_tags. Return them with source "yake", api_name None, confidence "estimated".
 4. Otherwise return [].
 - If importing yake fails (ImportError), step 3 returns [] instead of crashing: import yake inside a try/except at module level and keep a flag.

STEPS:
1. Implement a private helper _clean_names(names: list[str], max_tags: int) -> list[str] used by all three steps.
2. Implement build_tags.
3. Add an if __name__ == "__main__": block with asserts, then print "tagging OK":
   build_tags(["Deep Learning", "deep learning", "Vision"], [{"name": "X", "api_name": "openalex"}], "")  -> two tags, both source "author", confidence "verified"
   build_tags([], [{"name": "Computer vision", "api_name": "openalex"}], "")  -> one tag, source "api", api_name "openalex"
   build_tags([], [], "short")  == []
   a longer English text (at least 400 characters of your own, about neural networks and image classification) with no keywords -> non-empty list whose items all have source "yake" and confidence "estimated" (skip this assert if YAKE could not be imported).

OUTPUT FORMAT: Only the complete contents of tagging.py in a single Python code block. No explanation before or after.
REMINDER: one file only; the priority order is author keywords, API topics, YAKE; never mix groups.
```
Acceptance test: `python -m backend.tagging` prints `tagging OK`.
---
Prompt 15 - `backend/citations.py`
Depends on: Prompts 2, 4 (tables and data) · Modifies existing files: no
```text
ROLE: You are a senior Python backend engineer.
OBJECTIVE: Write ONE file, backend/citations.py: recompute the stored CITES links (citation matches between papers that are both in the library) for one paper, in both directions.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.

INTERFACE (must match exactly; conn is an sqlite3.Connection with row_factory sqlite3.Row):
  def rematch_paper_citations(conn, paper_id: int) -> int      # returns the number of citation rows that now involve paper_id

CONTEXT - tables (already created):
  papers(id, title, title_key, doi, arxiv_id, ...)
  paper_references(id, paper_id, position, raw_text, text_key, doi, arxiv_id, year)
  citations(citing_paper_id, cited_paper_id, reference_id, match_method)   PRIMARY KEY (citing_paper_id, cited_paper_id); match_method IN ('doi','arxiv_id','title')
A reference matches a library paper ONLY by: (1) equal doi, (2) equal arxiv_id, (3) the library paper's title_key has at least 20 characters and appears inside the reference's text_key (SQL: instr(text_key, title_key) > 0). Nothing else may create a match. A paper never cites itself. At most one citations row exists per (citing, cited) pair: use INSERT OR IGNORE and try doi first, then arxiv_id, then title.

STEPS:
1. Load the paper row; if it does not exist return 0.
2. DELETE FROM citations WHERE citing_paper_id = ? OR cited_paper_id = ?  (parameters: paper_id twice).
3. OUTGOING: for every reference of this paper (id, doi, arxiv_id, text_key): look for another paper (id <> paper_id) with the same doi (when the reference doi is not NULL) -> method "doi"; else with the same arxiv_id (when not NULL) -> "arxiv_id"; else a paper with length(title_key) >= 20 and instr(?, title_key) > 0 where ? is the reference text_key (lowest id first) -> "title". If found INSERT OR IGNORE INTO citations(citing_paper_id, cited_paper_id, reference_id, match_method) VALUES (this paper, found paper, reference id, method).
4. INCOMING: for every reference of any OTHER paper (paper_id <> this paper): it cites this paper if (this paper's doi is not NULL and reference.doi = this doi) -> "doi"; elif (this paper's arxiv_id is not NULL and reference.arxiv_id = this arxiv_id) -> "arxiv_id"; elif (length(this title_key) >= 20 and instr(reference.text_key, this title_key) > 0) -> "title". Do this with up to three SELECT queries over paper_references and INSERT OR IGNORE INTO citations(citing_paper_id = the reference's paper_id, cited_paper_id = this paper, reference_id, method). Run the doi query first, then arxiv, then title, so the strongest method is inserted first.
5. Return SELECT COUNT(*) FROM citations WHERE citing_paper_id = ? OR cited_paper_id = ?.
6. Add an if __name__ == "__main__": block with get_conn(":memory:") and init_db(conn) from backend.db: insert paper A (title "Attention Is All You Need", doi "10.1/a") and paper B whose single reference text_key contains "attention is all you need" (insert rows directly with SQL in the test, including title_key via backend.text_utils.normalize_title and text_key), call rematch_paper_citations(conn, A) and assert exactly one citations row (B cites A, method "title"); delete and re-run for B and assert the same row count; print "citations OK".

OUTPUT FORMAT: Only the complete contents of citations.py in a single Python code block. No explanation before or after.
REMINDER: one file only; no fuzzy matching; no commit() inside rematch_paper_citations; exact function name.
```
Acceptance test: `python -m backend.citations` prints `citations OK`.
---
Prompt 16 - `backend/graph.py`
Depends on: Prompts 0, 2, 4 · Modifies existing files: no
```text
ROLE: You are a senior Python backend engineer.
OBJECTIVE: Write ONE file, backend/graph.py: build the knowledge-graph JSON (Cytoscape.js elements) from the SQLite tables, including two derived edge types.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.

INTERFACE (must match exactly; conn is an sqlite3.Connection with row_factory sqlite3.Row):
  def build_graph(conn, include_derived: bool = True) -> dict
Imports: from backend.config import MAX_COAUTHOR_FANOUT

CONTEXT - tables (already created):
  papers(id, title, year); authors(id, name); paper_authors(paper_id, author_id, position)
  topics(id, name); paper_topics(paper_id, topic_id, source, api_name, confidence)
  citations(citing_paper_id, cited_paper_id, reference_id, match_method)
RETURN SHAPE (exact):
  {"elements": {"nodes": [ {"data": {...}}, ... ], "edges": [ {"data": {...}}, ... ]},
   "stats": {"papers": int, "authors": int, "topics": int,
             "edges": {"AUTHORED_BY": int, "HAS_TOPIC": int, "CITES": int, "CO_AUTHOR": int, "RELATED_TOPIC": int}}}
Nodes (data dicts):
  paper:  {"id": "paper:<id>", "type": "paper", "label": <title>, "paper_id": <id>, "year": <year or None>}
  author: {"id": "author:<id>", "type": "author", "label": <name>, "author_id": <id>, "paper_count": <number of papers>}
  topic:  {"id": "topic:<id>", "type": "topic", "label": <name>, "topic_id": <id>, "paper_count": <number of papers>}
  Include every paper; include only authors that appear in paper_authors and topics that appear in paper_topics.
Edges (data dicts, every edge also has "id": f"{type}:{source}:{target}", "type", "source", "target"):
  AUTHORED_BY  stored  source "paper:<id>"  target "author:<id>"      (one per paper_authors row)
  HAS_TOPIC    stored  source "paper:<id>"  target "topic:<id>"       plus "tag_source": <paper_topics.source>, "confidence": <paper_topics.confidence>
  CITES        stored  source "paper:<citing id>" target "paper:<cited id>"   (one per citations row)
  CO_AUTHOR    derived (only when include_derived): for every paper with between 2 and MAX_COAUTHOR_FANOUT authors, every unordered pair of its authors; source = author with the smaller numeric id; "weight" = number of papers in which the pair occurs together. One edge per pair.
  RELATED_TOPIC derived (only when include_derived): for every paper with at least 2 topics, every unordered pair of its topics; source = topic with the smaller numeric id; "weight" = number of papers in which the pair occurs together. One edge per pair.
When include_derived is False the stats counts for CO_AUTHOR and RELATED_TOPIC are 0 and no such edges are returned.

STEPS:
1. Run plain SELECT queries to load papers, authors per paper, topics per paper, citations and the paper counts.
2. Build the node list and the stored edges.
3. Build the derived edges with itertools.combinations over sorted id lists and a dict that counts pairs.
4. Compute stats from the lists you built and return the dict.
5. Add an if __name__ == "__main__": block using get_conn(":memory:") and init_db(conn) from backend.db and insert_paper, set_paper_authors, add_paper_topic from backend.repo_write: two papers share one author and one topic; assert the graph has 2 paper nodes, the expected AUTHORED_BY/HAS_TOPIC counts, one CO_AUTHOR edge with weight 1 (give paper 1 the authors A and B, paper 2 the authors B and C, plus a second shared pair so that weight 2 is tested for RELATED_TOPIC: give both papers the topics "x" and "y"), RELATED_TOPIC weight 2, and that include_derived=False removes both derived types. Print "graph OK".

OUTPUT FORMAT: Only the complete contents of graph.py in a single Python code block. No explanation before or after.
REMINDER: one file only; read-only; exact keys; edge type names are written exactly AUTHORED_BY, HAS_TOPIC, CITES, CO_AUTHOR, RELATED_TOPIC.
```
Acceptance test: `python -m backend.graph` prints `graph OK`.
---
Prompt 17 - `backend/pipeline.py`
Depends on: Prompts 0-9, 13-16 · Modifies existing files: no
```text
ROLE: You are a senior Python backend engineer.
OBJECTIVE: Write ONE file, backend/pipeline.py: the upload pipeline that turns the bytes of a PDF into stored database records.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.

INTERFACE (must match exactly):
  class IngestError(Exception):
      def __init__(self, code: str, message: str, existing_paper_id: int | None = None)   # stores .code, .message, .existing_paper_id
  async def ingest_pdf(conn, file_bytes: bytes, original_filename: str, username: str, allow_duplicate: bool = False) -> dict
      # returns {"paper_id": int, "warnings": [str]}
Allowed codes for IngestError: "empty_file", "not_pdf", "file_too_large", "unreadable_pdf", "no_text_layer", "duplicate_paper", "possible_duplicate".

IMPORTS AVAILABLE (already written; use exactly these names):
  backend.config: MAX_UPLOAD_BYTES, UPLOAD_DIR, ensure_dirs
  backend.text_utils: find_doi, find_arxiv_id, normalize_title
  backend.pdf_text: extract_pdf(path) -> dict with keys page_count, raw_text, first_page_raw_text, body_text, first_page_body_text, first_page_lines, page_width, page_height, doc_metadata{title,author,keywords}; exceptions PdfReadError, NoTextLayerError
  backend.parse_title_authors: extract_title(lines, page_height, doc_title) -> str|None ; extract_authors(lines, title) -> list[str]
  backend.parse_abstract_keywords: extract_abstract(first_page_body_text) -> str|None ; extract_keywords(first_page_body_text, doc_keywords) -> list[str] ; extract_year(first_page_raw_text, arxiv_id) -> int|None
  backend.references: extract_references(body_text) -> list[dict]
  backend.enrichment: async enrich_metadata(conn, parsed, doi, arxiv_id) -> dict with keys title, authors, abstract, year, venue, doi, arxiv_id, api_topics, enriched_from, warnings
  backend.tagging: build_tags(author_keywords, api_topics, text) -> list of {"name","source","api_name","confidence"}
  backend.repo_read: find_duplicate(conn, *, file_sha256=None, doi=None, arxiv_id=None, title_key=None) -> None or {"kind","paper_id","title","matched_on"} ; get_paper_detail(conn, paper_id)
  backend.repo_write: insert_paper(conn, *, title, abstract, year, venue, doi, arxiv_id, file_sha256, stored_filename, original_filename, page_count, enriched_from, uploaded_by) -> int ; set_paper_authors(conn, paper_id, names) ; insert_references(conn, paper_id, refs) -> int ; add_paper_topic(conn, paper_id, name, source, confidence, api_name=None)
  backend.citations: rematch_paper_citations(conn, paper_id) -> int
  backend.repo_aux: log_activity(conn, username, action, paper_id, paper_title, details=None) -> int
  backend.db: init_db, db_session

STEPS for ingest_pdf:
1. warnings = []. If len(file_bytes) == 0 raise IngestError("empty_file", "The uploaded file is empty."). If len(file_bytes) > MAX_UPLOAD_BYTES raise IngestError("file_too_large", "The file is larger than 25 MB."). If not file_bytes.startswith(b"%PDF-") raise IngestError("not_pdf", "Only PDF files are accepted.").
2. sha = hashlib.sha256(file_bytes).hexdigest(). dup = find_duplicate(conn, file_sha256=sha); if dup raise IngestError("duplicate_paper", "This file is already in the library.", dup["paper_id"]).
3. ensure_dirs(); stored_filename = f"{sha}.pdf"; path = UPLOAD_DIR / stored_filename; write the bytes to path.
4. Put ALL remaining steps inside one try block. In an except BaseException handler delete the file (path.unlink(missing_ok=True)) and re-raise.
5. try extract_pdf(path); on PdfReadError raise IngestError("unreadable_pdf", str(error)); on NoTextLayerError raise IngestError("no_text_layer", "This PDF has no extractable text (it may be a scanned image). OCR is not supported.").
6. Page 1 identifiers: doi = find_doi(first_page_raw_text); arxiv_id = find_arxiv_id(first_page_raw_text).
7. Parse: title = extract_title(first_page_lines, page_height, doc_metadata["title"]); authors = extract_authors(first_page_lines, title); abstract = extract_abstract(first_page_body_text); keywords = extract_keywords(first_page_body_text, doc_metadata["keywords"]); year = extract_year(first_page_raw_text, arxiv_id); references = extract_references(body_text). Add a warning when there are no authors ("No authors could be detected."), no abstract ("No abstract could be detected.") or no references ("No reference list could be detected.").
8. enriched = await enrich_metadata(conn, {"title": title, "authors": authors, "abstract": abstract, "year": year, "venue": None}, doi, arxiv_id); extend warnings with enriched["warnings"].
9. final_title = enriched["title"] or the file name without extension (Path(original_filename).stem); if enriched["title"] is empty add the warning "Title could not be detected; the file name was used.". title_key = normalize_title(final_title).
10. dup = find_duplicate(conn, doi=enriched["doi"], arxiv_id=enriched["arxiv_id"], title_key=title_key). If dup: if dup["kind"] == "possible_duplicate" and allow_duplicate is True, continue; otherwise raise IngestError(dup["kind"], "This paper appears to be in the library already.", dup["paper_id"]).
11. tags = build_tags(keywords, enriched["api_topics"], final_title + ". " + (enriched["abstract"] or "") + "\n" + body_text[:8000]).
12. Store everything inside ONE transaction: "with conn:" then insert_paper(...) using enriched values, enriched_from = enriched["enriched_from"], uploaded_by = username, page_count from the extraction; set_paper_authors(conn, id, enriched["authors"]); insert_references(conn, id, references); for each tag add_paper_topic(conn, id, tag["name"], tag["source"], tag["confidence"], tag["api_name"]); rematch_paper_citations(conn, id); log_activity(conn, username, "upload", id, final_title, "file: " + original_filename). Catch sqlite3.IntegrityError around this block and raise IngestError("duplicate_paper", "This paper is already in the library.").
13. Return {"paper_id": id, "warnings": warnings}.
14. Add an if __name__ == "__main__": block: read sys.argv[1] (a PDF path) and sys.argv[2] (a user name); init_db(); with db_session() as conn: run asyncio.run(ingest_pdf(...)); print the warnings and then the title, authors and tags from get_paper_detail; print the IngestError code and message if one is raised.

OUTPUT FORMAT: Only the complete contents of pipeline.py in a single Python code block. No explanation before or after.
REMINDER: one file only; use only the imports listed; no new endpoints, tables or fields; always delete the stored PDF when ingestion fails.
```
Acceptance test: `OFFLINE_MODE=1 python -m backend.pipeline sample_papers/<file>.pdf alice` prints a title, authors and tags; running it again prints `duplicate_paper`; running it on a text file renamed to `.pdf` prints `unreadable_pdf` or `not_pdf` and leaves `uploads/` unchanged; without `OFFLINE_MODE` (and with internet) a paper with a DOI or arXiv ID shows a non-empty enriched source in the detail output.
---
Prompt 18 - `tests/test_core.py`
Depends on: Prompts 1-5, 9, 14-16 · Modifies existing files: no
```text
ROLE: You are a senior Python test engineer.
OBJECTIVE: Write ONE file, tests/test_core.py, a unittest suite (standard library only, no pytest) for the pure-logic modules of a research-paper library.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.

INTERFACE: class CoreTests(unittest.TestCase) with the test methods listed below; module ends with: if __name__ == "__main__": unittest.main()
IMPORTS AVAILABLE (already written):
  backend.text_utils: find_doi, normalize_doi, find_arxiv_id, normalize_title
  backend.references: extract_references(body_text) -> list of dicts with keys raw_text, text_key, doi, arxiv_id, year
  backend.tagging: build_tags(author_keywords, api_topics, text) -> list of dicts with keys name, source, api_name, confidence
  backend.db: get_conn(":memory:"), init_db(conn)
  backend.repo_write: insert_paper(conn, *, title, abstract, year, venue, doi, arxiv_id, file_sha256, stored_filename, original_filename, page_count, enriched_from, uploaded_by) -> int ; set_paper_authors(conn, paper_id, names) ; add_paper_topic(conn, paper_id, name, source, confidence, api_name=None) ; insert_references(conn, paper_id, refs) ; delete_paper(conn, paper_id) -> str | None
  backend.repo_read: find_duplicate(conn, *, file_sha256=None, doi=None, arxiv_id=None, title_key=None) ; list_papers(conn, q=None, author=None, topic=None, year=None, limit=50, offset=0) -> {"total", "items"}
  backend.citations: rematch_paper_citations(conn, paper_id) -> int
  backend.graph: build_graph(conn, include_derived=True) -> {"elements": {"nodes": [...], "edges": [...]}, "stats": {...}}; every edge is {"data": {"type": ..., ...}}

TESTS (each method name starts with test_):
  test_find_doi: find_doi("doi: 10.1109/CVPR.2016.90.") == "10.1109/cvpr.2016.90"; find_doi("no identifier") is None.
  test_arxiv_requires_prefix: find_arxiv_id("arXiv:1706.03762v5") == "1706.03762"; find_arxiv_id("1706.03762") is None.
  test_references_split: body text "Intro\n\nReferences\n[1] A. Author, Deep nets, CVPR, 2016, doi: 10.1109/CVPR.2016.90.\n[2] B. Writer, Learning to learn, 2017, a long enough reference line.\n[3] C. Third, Another reference entry with enough text, 2015." gives 3 references and the first has doi "10.1109/cvpr.2016.90".
  test_tag_priority: author keywords win over api topics; api topics win when there are no author keywords; with no keywords or topics and a short text the result is [].
  test_duplicate_and_search: in a fresh in-memory database insert two papers with different titles, DOIs and file hashes; find_duplicate by doi returns kind "duplicate_paper"; find_duplicate by the normalised title returns kind "possible_duplicate"; list_papers(q="<part of the first title>") has total 1.
  test_graph_derived_edges: two papers: paper 1 authors ["Ann One", "Bob Two"], paper 2 authors ["Bob Two", "Cy Three"]; both get topics "graphs" and "networks" (source "author", confidence "verified"). Then build_graph: the nodes include 2 papers, 3 authors, 2 topics; exactly one CO_AUTHOR edge pair per author pair (3 CO_AUTHOR edges); exactly one RELATED_TOPIC edge with weight 2; with include_derived=False there are zero CO_AUTHOR and RELATED_TOPIC edges.
  test_citation_match_and_delete: paper A titled "A Study of Graph Neural Networks" and paper B whose single stored reference has raw_text and text_key (use normalize_title) containing that title; after rematch_paper_citations(conn, B_id) the graph has exactly one CITES edge from B to A; after delete_paper(conn, A_id) the graph has no CITES edge, and the author rows that belonged only to A are gone.
Use a new in-memory database in each database test (create it in the test body or setUp).

OUTPUT FORMAT: Only the complete contents of test_core.py in a single Python code block. No explanation before or after.
REMINDER: one file only; unittest only; tests must not use the network or the real data folder.
```
Acceptance test: `python -m unittest tests.test_core -v` from the project root shows 7 tests, all `ok`.
---
Prompt 19 - `backend/api_errors.py`
Depends on: nothing · Modifies existing files: no
```text
ROLE: You are a senior Python engineer who knows FastAPI.
OBJECTIVE: Write ONE file, backend/api_errors.py: a small exception class for API errors and a FastAPI dependency that reads the user name header.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.
Use only: fastapi and the standard library.

INTERFACE (must match exactly):
  class ApiError(Exception):
      def __init__(self, status_code: int, code: str, message: str, extra: dict | None = None)   # stores .status_code, .code, .message, .extra (dict, {} if None)
  def require_username(x_username: str | None = Header(default=None)) -> str
      # returns the stripped header value; raises ApiError(400, "missing_username", "The X-Username header is required.") if the header is missing, blank, or longer than 50 characters after strip
Import: from fastapi import Header

STEPS:
1. Implement the class and the function.
2. Add an if __name__ == "__main__": block that asserts require_username("  alice ") == "alice" and that require_username(None) and require_username("   ") raise ApiError with status_code 400 and code "missing_username"; print "api_errors OK".

OUTPUT FORMAT: Only the complete contents of api_errors.py in a single Python code block. No explanation before or after.
REMINDER: one file only; exact names; nothing else.
```
Acceptance test: `python -m backend.api_errors` prints `api_errors OK`.
---
Prompt 20 - `backend/routes_papers.py`
Depends on: Prompts 2-5, 15, 17, 19 · Modifies existing files: no
```text
ROLE: You are a senior Python engineer who knows FastAPI.
OBJECTIVE: Write ONE file, backend/routes_papers.py: the /api/papers endpoints (upload, list, detail, patch, delete, add/remove tag) as a FastAPI APIRouter.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.
Use only: fastapi, pydantic (installed with fastapi), json, sqlite3, and the project modules named below.

INTERFACE (must match exactly):
  router = APIRouter(prefix="/api")
  POST   /api/papers                              async def upload_paper(...)
  GET    /api/papers                              def list_papers_route(...)
  GET    /api/papers/{paper_id}                   def get_paper_route(...)
  PATCH  /api/papers/{paper_id}                   def patch_paper_route(...)
  DELETE /api/papers/{paper_id}                   def delete_paper_route(...)
  POST   /api/papers/{paper_id}/topics            def add_topic_route(...)
  DELETE /api/papers/{paper_id}/topics/{topic_id} def remove_topic_route(...)

IMPORTS AVAILABLE (already written):
  backend.api_errors: ApiError(status_code, code, message, extra=None), require_username (FastAPI dependency returning the user name)
  backend.db: db_session() context manager yielding an sqlite3 connection
  backend.config: MAX_UPLOAD_BYTES, UPLOAD_DIR
  backend.pipeline: IngestError (attributes .code, .message, .existing_paper_id), async ingest_pdf(conn, file_bytes, original_filename, username, allow_duplicate) -> {"paper_id", "warnings"}
  backend.repo_read: get_paper_detail(conn, paper_id) -> dict | None ; list_papers(conn, q, author, topic, year, limit, offset) -> dict
  backend.repo_write: update_paper_fields(conn, paper_id, fields) -> bool ; set_paper_authors(conn, paper_id, names) ; add_paper_topic(conn, paper_id, name, source, confidence, api_name=None) -> int | None ; remove_paper_topic(conn, paper_id, topic_id) -> bool ; delete_paper(conn, paper_id) -> str | None
  backend.citations: rematch_paper_citations(conn, paper_id)
  backend.repo_aux: log_activity(conn, username, action, paper_id, paper_title, details=None)
  backend.text_utils: normalize_doi, normalize_arxiv_id

ENDPOINT RULES:
- Every write endpoint has a parameter username: str = Depends(require_username).
- POST /api/papers: parameters file: UploadFile = File(...), allow_duplicate: bool = Form(False). data = await file.read(MAX_UPLOAD_BYTES + 1). Inside "with db_session() as conn:" call result = await ingest_pdf(conn, data, file.filename or "upload.pdf", username, allow_duplicate). Convert IngestError to ApiError with this status map: empty_file 400, not_pdf 400, unreadable_pdf 400, file_too_large 413, no_text_layer 422, duplicate_paper 409, possible_duplicate 409; for the two 409 codes pass extra={"existing_paper_id": error.existing_paper_id}. Return JSONResponse(status_code=201, content={"paper": get_paper_detail(conn, result["paper_id"]), "warnings": result["warnings"]}).
- GET /api/papers: query parameters q, author, topic (str | None), year (int | None), limit (int = Query(50, ge=1, le=200)), offset (int = Query(0, ge=0)); return list_papers(...).
- GET /api/papers/{paper_id}: return get_paper_detail or raise ApiError(404, "not_found", "Paper not found.").
- PATCH: body model PaperPatch(BaseModel) with optional fields title: str | None, abstract: str | None, year: int | None, venue: str | None, doi: str | None, arxiv_id: str | None, authors: list[str] | None. Use payload.model_dump(exclude_unset=True). 404 if the paper does not exist. If "title" is given and blank raise ApiError(422, "validation_error", "Title must not be empty."). If "doi" is given and non-blank but normalize_doi returns None raise ApiError(422, "invalid_doi", "Invalid DOI."); same for arxiv_id with code "invalid_arxiv_id". Take "authors" out of the dict, call update_paper_fields with the rest (inside "with conn:"), then set_paper_authors if authors was given, then rematch_paper_citations, then log_activity(conn, username, "edit", paper_id, new title, ", ".join(sorted changed field names)). Catch sqlite3.IntegrityError and raise ApiError(409, "duplicate_paper", "Another paper already has this DOI or arXiv ID."). Return the updated detail.
- DELETE: with db_session: detail = get_paper_detail (404 if None); inside "with conn:" stored = delete_paper(conn, paper_id) and log_activity(conn, username, "delete", paper_id, detail["title"], None). Then remove the file UPLOAD_DIR / stored with unlink(missing_ok=True). Return {"deleted": paper_id}.
- POST topics: body model TopicIn(BaseModel) with name: str (strip it; length 1 to 60 else ApiError 422 "validation_error"). 404 if no paper. "with conn:" add_paper_topic(conn, paper_id, name, "manual", "verified") and, when it returned an id, log_activity(conn, username, "tag_add", paper_id, title, name). Return the new detail.
- DELETE topics: 404 if no paper; "with conn:" removed = remove_paper_topic(...); if not removed raise ApiError(404, "not_found", "Tag not found on this paper."); else log_activity(conn, username, "tag_remove", paper_id, title, str(topic_id)). Return the new detail.
- Never return stack traces; unexpected exceptions are handled elsewhere.

STEPS:
1. Write the models and the seven endpoints.
2. Add no main block.

OUTPUT FORMAT: Only the complete contents of routes_papers.py in a single Python code block. No explanation before or after.
REMINDER: one file only; exactly these seven endpoints; every SQL access goes through the imported functions.
```
Acceptance test (import only, the server comes in Prompt 22): `python -c "import backend.routes_papers as r; print(len(r.router.routes))"` prints `7`.
---
Prompt 21 - `backend/routes_misc.py`
Depends on: Prompts 2, 3, 5, 16 · Modifies existing files: no
```text
ROLE: You are a senior Python engineer who knows FastAPI.
OBJECTIVE: Write ONE file, backend/routes_misc.py: the /api/health, /api/topics, /api/graph and /api/activity endpoints as a FastAPI APIRouter.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.
Use only: fastapi, sqlite3 and the project modules named below.

INTERFACE (must match exactly):
  router = APIRouter(prefix="/api")
  GET /api/health     def health_route()
  GET /api/topics     def topics_route()
  GET /api/graph      def graph_route(include_derived: bool = True)
  GET /api/activity   def activity_route(user: str | None = None, limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0))

IMPORTS AVAILABLE (already written):
  backend.db: db_session() context manager yielding an sqlite3 connection
  backend.config: is_offline()
  backend.repo_read: count_papers(conn) -> int ; list_topics(conn) -> list[dict]
  backend.repo_aux: list_activity(conn, limit, offset, username) -> {"total", "items"}
  backend.graph: build_graph(conn, include_derived) -> dict

ENDPOINT RULES:
- health: return {"status": "ok", "sqlite_version": sqlite3.sqlite_version, "paper_count": count_papers(conn), "offline_mode": is_offline()}.
- topics: return list_topics(conn).
- graph: return build_graph(conn, include_derived).
- activity: return list_activity(conn, limit, offset, user).
- Each endpoint opens "with db_session() as conn:" and returns plain dicts/lists (FastAPI converts them to JSON).

STEPS:
1. Write the router and the four endpoints.
2. Add no main block.

OUTPUT FORMAT: Only the complete contents of routes_misc.py in a single Python code block. No explanation before or after.
REMINDER: one file only; exactly these four endpoints.
```
Acceptance test (import only): `python -c "import backend.routes_misc as r; print(len(r.router.routes))"` prints `4`.
---
Prompt 22 - `backend/main.py`
Depends on: Prompts 0, 2, 19, 20, 21 and a (placeholder) `frontend/index.html` · Modifies existing files: no
```text
ROLE: You are a senior Python engineer who knows FastAPI.
OBJECTIVE: Write ONE file, backend/main.py: create the FastAPI application, wire the routers, CORS, error handlers and serve the static frontend.
HARD CONSTRAINTS: Python 3.12 backend. SQLite only through the standard-library sqlite3 module; every SQL value is passed with ? placeholders (never f-strings or + in SQL). Third-party packages allowed ONLY: fastapi, uvicorn, python-multipart, pymupdf, httpx, yake. FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular, TypeScript, any build step. Use absolute imports (from backend.config import X). Do not call conn.commit() inside repository functions. Do not invent files, functions, tables, columns, endpoints, packages or features. Private helpers whose names start with an underscore are allowed.
Use only: fastapi, starlette (installed with fastapi), uvicorn, contextlib.

INTERFACE (must match exactly):
  app = FastAPI(title="Research Paper Library", lifespan=lifespan)
Imports: from backend.config import FRONTEND_DIR, ensure_dirs ; from backend.db import init_db ; from backend.api_errors import ApiError ; from backend.routes_papers import router as papers_router ; from backend.routes_misc import router as misc_router

STEPS:
1. lifespan: an @asynccontextmanager async function that calls ensure_dirs() and init_db() before "yield".
2. Add CORSMiddleware with allow_origins=["*"], allow_methods=["*"], allow_headers=["*"] (the app is local, without cookies).
3. Exception handlers returning JSONResponse with the body {"error": {"code": ..., "message": ...}}:
   - ApiError -> status error.status_code, code error.code, message error.message, and the keys of error.extra merged into the "error" object.
   - fastapi.exceptions.RequestValidationError -> status 422, code "validation_error", message "The request was not valid." 
   - Exception (any other) -> status 500, code "internal_error", message "Unexpected server error." (print the exception to the console with traceback.print_exc()).
4. app.include_router(papers_router) and app.include_router(misc_router).
5. LAST of all: app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend") (from fastapi.staticfiles import StaticFiles). It must come after the routers so that /api/... is not shadowed.
6. Add an if __name__ == "__main__": block that runs uvicorn.run("backend.main:app", host="127.0.0.1", port=8000).

OUTPUT FORMAT: Only the complete contents of main.py in a single Python code block. No explanation before or after.
REMINDER: one file only; the documented start command is: python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
Acceptance test: from the project root run `python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`, then in a second terminal:
`curl http://127.0.0.1:8000/api/health` → `{"status":"ok","sqlite_version":"...","paper_count":0,"offline_mode":false}`
`curl -X POST -F "file=@sample_papers/<file>.pdf" http://127.0.0.1:8000/api/papers` → `400` with `missing_username`
same with `-H "X-Username: alice"` → `201` with a `paper` object and `warnings`; repeating it → `409 duplicate_paper`
`curl "http://127.0.0.1:8000/api/papers?q=<word>"`, `curl http://127.0.0.1:8000/api/graph`, `curl http://127.0.0.1:8000/api/activity` return the shapes in Section E.
Uploading a `.txt` file renamed `.pdf` returns `400`; `GET /api/papers/9999` returns `404 not_found`.
---
Prompt 23 - `frontend/index.html`
Depends on: Prompt 22 (server running) · Modifies existing files: no (replaces the empty placeholder)
```text
ROLE: You are a senior front-end engineer who writes plain HTML.
OBJECTIVE: Write ONE file, frontend/index.html: the page shell of a research-paper library single-page app.
HARD CONSTRAINTS: browser-native HTML5, CSS3 and vanilla ES6 JavaScript only, loaded with plain <script> tags (no import/export, no modules). FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular/JSX, TypeScript, bundlers, any build step, and any CDN library other than the pinned Cytoscape tag. Do not invent features, endpoints or fields.
The ONLY external script allowed is exactly this tag (pinned version, do not change it):
<script src="https://cdn.jsdelivr.net/npm/cytoscape@3.34.4/dist/cytoscape.min.js"></script>

REQUIRED CONTENT (exact ids and order):
<!DOCTYPE html>, <html lang="en">, head with meta charset UTF-8, meta viewport, <title>Research Paper Library</title>, and <link rel="stylesheet" href="css/styles.css">.
Body:
  <header id="app-header">
    <h1>Research Paper Library</h1>
    <nav id="main-nav">
      <a href="#/library" data-nav="library">Library</a>
      <a href="#/graph" data-nav="graph">Graph</a>
      <a href="#/activity" data-nav="activity">Activity</a>
    </nav>
    <div id="user-box">
      <label for="username-input">Your name</label>
      <input id="username-input" type="text" maxlength="50" placeholder="e.g. alice">
      <button id="username-save" type="button" class="btn">Save</button>
    </div>
  </header>
  <main id="view"></main>
  <div id="toast" hidden></div>
Then, at the end of the body, in this exact order: the Cytoscape script tag above, then <script src="js/api.js"></script>, <script src="js/library.js"></script>, <script src="js/detail.js"></script>, <script src="js/graph.js"></script>, <script src="js/activity.js"></script>, <script src="js/app.js"></script>.

STEPS: write the file exactly as described; add no inline JavaScript and no inline styles; add no other scripts, links or libraries.

OUTPUT FORMAT: Only the complete contents of index.html in a single HTML code block. No explanation before or after.
REMINDER: one file only; vanilla HTML; the Cytoscape tag must stay exactly as given.
```
Acceptance test: open `http://127.0.0.1:8000/` - an unstyled header with three links, a name box and an empty page; the browser console shows 404 errors only for the JS/CSS files not yet created, and no errors for Cytoscape (type `cytoscape` in the console: it is a function).
---
Prompt 24 - `frontend/css/styles.css`
Depends on: Prompt 23 · Modifies existing files: no
```text
ROLE: You are a senior front-end engineer who writes plain CSS.
OBJECTIVE: Write ONE file, frontend/css/styles.css: clean, readable styling for a research-paper library app.
HARD CONSTRAINTS: browser-native HTML5, CSS3 and vanilla ES6 JavaScript only, loaded with plain <script> tags (no import/export, no modules). FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular/JSX, TypeScript, bundlers, any build step, and any CDN library other than the pinned Cytoscape tag. Do not invent features, endpoints or fields.

REQUIRED SELECTORS (the JavaScript files use exactly these names; style every one):
  body, #app-header (flex row, wraps on small screens), #main-nav a and #main-nav a.active, #user-box, #view (max-width 1100px, centred, padding),
  .card, .toolbar (flex, gap, wraps), .form-row, .muted, .info-box, .warning-box, .error-box,
  .btn, .btn-secondary, .btn-danger (also style plain button, input, select, textarea consistently),
  .paper-item, .paper-title, .paper-meta, .tags, .pagination,
  .tag (small rounded badge), .tag-author, .tag-api, .tag-yake, .tag-manual, .tag-estimated (dashed border), .tag-remove (small button inside a tag),
  .detail-grid (two columns on wide screens, one on narrow), .ref-list (ordered list, small text), .data-table (full-width table with header row and zebra rows),
  .graph-wrap, #cy (width 100%, height 70vh, light border, background white), .legend, .legend-item, .swatch (small coloured square),
  #toast (fixed bottom-right, hidden attribute respected), #toast.toast-success, #toast.toast-error.
Use a neutral font stack (system-ui, sans-serif), a light background, dark text with sufficient contrast, visible focus outlines. Colours for tags: author = green, api = blue, yake = grey, manual = purple. No external fonts, no @import, no frameworks.

STEPS: write the stylesheet; keep it under 250 lines; use plain CSS only (no preprocessors).

OUTPUT FORMAT: Only the complete contents of styles.css in a single CSS code block. No explanation before or after.
REMINDER: one file only; plain CSS3; every listed selector must exist.
```
Acceptance test: reload the page - header is styled, the active nav link style exists, no console errors from CSS.
---
Prompt 25 - `frontend/js/api.js`
Depends on: Prompt 22 · Modifies existing files: no
```text
ROLE: You are a senior front-end engineer who writes vanilla JavaScript.
OBJECTIVE: Write ONE file, frontend/js/api.js: fetch wrappers for the backend API plus small helpers shared by all views.
HARD CONSTRAINTS: browser-native HTML5, CSS3 and vanilla ES6 JavaScript only, loaded with plain <script> tags (no import/export, no modules). FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular/JSX, TypeScript, bundlers, any build step, and any CDN library other than the pinned Cytoscape tag. Do not invent features, endpoints or fields.
This file is loaded with a plain script tag, so every function below is a global function.

INTERFACE (names must match exactly):
  const API_BASE = (window.location.protocol === "file:") ? "http://127.0.0.1:8000" : "";
  function getUsername()                 // localStorage key "rpl_username", "" if missing
  function setUsername(name)             // stores the trimmed name
  function escapeHtml(text)              // escapes & < > " ' ; returns "" for null/undefined
  function formatDate(iso)               // "2026-10-22T10:00:05Z" -> local date and time string; "" if empty
  class ApiRequestError extends Error    // constructor(status, code, message, extra) ; properties status, code, message, extra
  async function apiRequest(method, path, options = {})   // options: {query: object, json: object, formData: FormData}
  async function apiListPapers(params)            // GET /api/papers  params: {q, author, topic, year, limit, offset}; skip empty values
  async function apiGetPaper(id)                  // GET /api/papers/{id}
  async function apiUploadPaper(file, allowDuplicate)   // POST /api/papers  multipart fields "file" and "allow_duplicate" ("true"/"false")
  async function apiPatchPaper(id, fields)        // PATCH /api/papers/{id}  JSON body
  async function apiDeletePaper(id)               // DELETE /api/papers/{id}
  async function apiAddTopic(id, name)            // POST /api/papers/{id}/topics  JSON {"name": name}
  async function apiRemoveTopic(id, topicId)      // DELETE /api/papers/{id}/topics/{topicId}
  async function apiListTopics()                  // GET /api/topics
  async function apiGetGraph(includeDerived)     // GET /api/graph?include_derived=true|false
  async function apiListActivity(params)          // GET /api/activity  params: {user, limit, offset}; skip empty values

CONTEXT - backend behaviour:
- Errors come back with a non-2xx status and the JSON body {"error": {"code": "...", "message": "...", "existing_paper_id": 3 (only sometimes)}}.
- Every request whose method is not GET must send the header "X-Username" with getUsername(). If getUsername() is empty, do not send the request: throw new ApiRequestError(400, "missing_username", "Enter your name at the top of the page first.", {}).
- For JSON bodies set Content-Type "application/json". For FormData do NOT set Content-Type (the browser does it).

STEPS:
1. Implement apiRequest with fetch(API_BASE + path + query string). Parse the JSON response. If response.ok is false throw ApiRequestError built from the error body (fall back to status text and code "http_error" if the body is not JSON). If fetch itself fails (network error) throw ApiRequestError(0, "network_error", "Cannot reach the server.", {}).
2. Implement the wrappers using apiRequest.
3. Implement the helpers.

OUTPUT FORMAT: Only the complete contents of api.js in a single JavaScript code block. No explanation before or after.
REMINDER: one file only; no import/export; no libraries; exact function names.
```
Acceptance test: reload; in the browser console `await apiListPapers({})` returns `{total, items}`; `await apiDeletePaper(1)` with an empty name rejects with `missing_username`; `getUsername()` returns `""` before a name is saved.
---
Prompt 26 - `frontend/js/app.js`
Depends on: Prompts 23, 25 · Modifies existing files: no
```text
ROLE: You are a senior front-end engineer who writes vanilla JavaScript.
OBJECTIVE: Write ONE file, frontend/js/app.js: the hash router, the toast messages and the user-name box of a single-page app.
HARD CONSTRAINTS: browser-native HTML5, CSS3 and vanilla ES6 JavaScript only, loaded with plain <script> tags (no import/export, no modules). FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular/JSX, TypeScript, bundlers, any build step, and any CDN library other than the pinned Cytoscape tag. Do not invent features, endpoints or fields.
This file is the LAST script on the page. It uses these globals that already exist from other files: getUsername(), setUsername(name), escapeHtml(text) (from api.js), and - possibly not yet built - renderLibraryView(container), renderDetailView(container, paperId), renderGraphView(container), renderActivityView(container).

INTERFACE (names must match exactly):
  function showToast(message, kind)       // kind "success" or "error"; shows #toast (remove its hidden attribute, set class "toast-success" or "toast-error"), hides it after 4 seconds
  function showError(container, message)  // puts <div class="error-box"> with the escaped message into container
  async function route()                  // renders the view for location.hash into #view

CONTEXT - routes:
  "" or "#/" or "#/library"  -> renderLibraryView(container)
  "#/paper/<number>"         -> renderDetailView(container, <number as integer>)
  "#/graph"                  -> renderGraphView(container)
  "#/activity"               -> renderActivityView(container)
  anything else              -> show a short "Page not found" message with a link to #/library
If the needed render function is not defined (typeof ... !== "function") show the message "This view is not available yet." instead of failing.

STEPS:
1. Clear #view (container.innerHTML = "") before rendering; wrap the call in try/catch and show the error with showError; call await on the render function (it may be async).
2. Mark the matching nav link with class "active" (links in #main-nav have data-nav="library", "graph" or "activity"; a paper detail route keeps "library" active).
3. User box: on DOMContentLoaded fill #username-input with getUsername(); on click of #username-save call setUsername with the input value; if the value is blank show an error toast "Please enter a name.", otherwise show a success toast "Name saved.".
4. Listen to window "hashchange" and to "DOMContentLoaded" and call route(). If location.hash is empty set it to "#/library".

OUTPUT FORMAT: Only the complete contents of app.js in a single JavaScript code block. No explanation before or after.
REMINDER: one file only; no import/export; do not redefine functions that live in other files.
```
Acceptance test: reload `http://127.0.0.1:8000/` - URL becomes `#/library` and shows "This view is not available yet."; enter a name, click Save - green toast appears and disappears; the name is still there after reload; `#/nonsense` shows the not-found message.
---
Prompt 27 - `frontend/js/library.js`
Depends on: Prompts 24-26 · Modifies existing files: no
```text
ROLE: You are a senior front-end engineer who writes vanilla JavaScript.
OBJECTIVE: Write ONE file, frontend/js/library.js: the library view with PDF upload, search filters, paper list and pagination.
HARD CONSTRAINTS: browser-native HTML5, CSS3 and vanilla ES6 JavaScript only, loaded with plain <script> tags (no import/export, no modules). FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular/JSX, TypeScript, bundlers, any build step, and any CDN library other than the pinned Cytoscape tag. Do not invent features, endpoints or fields.
Globals that already exist: apiListPapers(params), apiUploadPaper(file, allowDuplicate), showToast(message, kind), escapeHtml(text), formatDate(iso), class ApiRequestError (properties status, code, message, extra).

INTERFACE (name must match exactly):
  async function renderLibraryView(container)

CONTEXT - API data:
  apiListPapers({q, author, topic, year, limit, offset}) resolves to {"total": 12, "items": [ {"id": 1, "title": "...", "year": 2017, "venue": null, "doi": null, "arxiv_id": "1706.03762", "authors": ["A B", "C D"], "tags": [{"id": 3, "name": "attention", "source": "author", "confidence": "verified"}], "uploaded_by": "alice", "uploaded_at": "2026-10-22T10:00:00Z"} ]}.
  apiUploadPaper(file, allowDuplicate) resolves to {"paper": {"id": 1, "title": "..."}, "warnings": ["..."]}. On failure it throws ApiRequestError; important codes: "no_text_layer", "not_pdf", "empty_file", "unreadable_pdf", "file_too_large", "duplicate_paper", "possible_duplicate", "missing_username". The two 409 codes carry error.extra.existing_paper_id.

STEPS:
1. Render into container (innerHTML with escaped values) three blocks:
   a) <section class="card"> "Upload a paper": <input type="file" id="upload-file" accept="application/pdf,.pdf"> and <button id="upload-btn" class="btn">Upload</button>, plus an empty <div id="upload-result"></div>.
   b) <section class="card"> a filter form (class "toolbar") with inputs id="f-q" (placeholder "Search title, author or topic"), id="f-author", id="f-topic", id="f-year" (type number), a Search button and a Clear button.
   c) <div id="paper-list"></div> and <div class="pagination" id="pager"></div>.
2. State: page size 20, current offset 0. A function loadPapers() calls apiListPapers with the filter values and the offset, then renders each item as <div class="paper-item"> with a title link <a class="paper-title" href="#/paper/ID">, a <div class="paper-meta"> with authors joined by ", ", year, and uploader/date (formatDate), and a <div class="tags"> with one <span class="tag tag-SOURCE"> per tag (add class "tag-estimated" when confidence is "estimated"). Show a <p class="muted"> "No papers found." for an empty list and "Showing X-Y of TOTAL" in the pager with Previous / Next buttons (disabled at the ends). Show errors with an <div class="error-box">.
3. Search button and Enter key reset the offset to 0 and call loadPapers(); Clear empties the inputs and reloads.
4. Upload: if no file is selected show an error toast. Otherwise disable the button, call apiUploadPaper(file, false) and on success show a success toast, list any warnings in <div class="warning-box"> inside #upload-result with a link to the new paper (#/paper/ID), clear the file input and reload the list. On ApiRequestError: if code is "possible_duplicate" ask window.confirm("A paper with the same title already exists. Add it anyway?"); if confirmed call apiUploadPaper(file, true) once more and handle its result the same way; for every other error put the message in <div class="error-box"> inside #upload-result (for "duplicate_paper" add a link to #/paper/EXISTING_ID) and show an error toast. Re-enable the button at the end.
5. Call loadPapers() once at the end of renderLibraryView.

OUTPUT FORMAT: Only the complete contents of library.js in a single JavaScript code block. No explanation before or after.
REMINDER: one file only; no import/export; escape every value with escapeHtml before putting it in innerHTML; define only renderLibraryView and private helpers whose names start with an underscore.
```
Acceptance test (browser): with a name saved, upload a sample PDF → success toast, the paper appears in the list with authors and tags; upload it again → "already in the library" message with a link; upload a `.txt` renamed `.pdf` → readable error; search by an author word filters the list; Clear restores it; pagination buttons are disabled when there is one page.
---
Prompt 28 - `frontend/js/detail.js`
Depends on: Prompts 24-26 · Modifies existing files: no
```text
ROLE: You are a senior front-end engineer who writes vanilla JavaScript.
OBJECTIVE: Write ONE file, frontend/js/detail.js: the paper detail view with metadata correction, tag management and deletion.
HARD CONSTRAINTS: browser-native HTML5, CSS3 and vanilla ES6 JavaScript only, loaded with plain <script> tags (no import/export, no modules). FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular/JSX, TypeScript, bundlers, any build step, and any CDN library other than the pinned Cytoscape tag. Do not invent features, endpoints or fields.
Globals that already exist: apiGetPaper(id), apiPatchPaper(id, fields), apiDeletePaper(id), apiAddTopic(id, name), apiRemoveTopic(id, topicId), showToast(message, kind), showError(container, message), escapeHtml(text), formatDate(iso), class ApiRequestError (property message).

INTERFACE (name must match exactly):
  async function renderDetailView(container, paperId)

CONTEXT - apiGetPaper(id) resolves to (and apiPatchPaper, apiAddTopic, apiRemoveTopic resolve to the updated version of) this object; a missing paper throws ApiRequestError with status 404:
  {"id": 1, "title": "...", "abstract": "... or null", "year": 2017, "venue": null, "doi": null, "arxiv_id": "1706.03762", "page_count": 15,
   "enriched_from": ["arxiv"], "original_filename": "x.pdf", "uploaded_by": "alice", "uploaded_at": "...", "updated_at": "...",
   "authors": [{"id": 1, "name": "A B"}],
   "tags": [{"id": 3, "name": "attention", "source": "author", "api_name": null, "confidence": "verified"}],
   "references": [{"id": 10, "position": 1, "raw_text": "...", "doi": null, "arxiv_id": null, "year": 2014, "cited_paper_id": null}],
   "cites": [{"paper_id": 2, "title": "..."}], "cited_by": [{"paper_id": 5, "title": "..."}]}

STEPS:
1. Load the paper with apiGetPaper(paperId); on error call showError(container, error.message) and return. Keep the loaded object in a local variable and re-render the page from it after every successful change (a private function _draw(paper)).
2. _draw renders (all values escaped): a link "Back to library" (#/library); the title as <h2>; a <div class="detail-grid"> showing authors (joined), year, venue, DOI (link https://doi.org/DOI when present), arXiv ID (link https://arxiv.org/abs/ID when present), pages, uploaded by/at (formatDate), "Metadata sources" (enriched_from joined or "PDF only"); an "Abstract" section (or <p class="muted">No abstract.</p>).
3. Tags section: each tag is <span class="tag tag-SOURCE"> (plus "tag-estimated" when confidence is "estimated") with the name and a <button class="tag-remove" data-topic="ID" title="Remove tag">x</button>; below it a small form with <input id="new-tag" maxlength="60"> and <button id="add-tag" class="btn">Add tag</button>. Remove calls apiRemoveTopic; add calls apiAddTopic with the trimmed value (ignore blanks). Success -> _draw(updated) and a success toast; failure -> error toast with the message.
4. "Cites" and "Cited by" lists with links to #/paper/ID (show "None in the library." when empty).
5. References: heading "References (N)" and <ol class="ref-list"> of raw_text; when cited_paper_id is not null append a link "[in library]" to #/paper/ID. Show <p class="muted">No references were detected.</p> when empty.
6. Edit: a button "Edit metadata" (class "btn btn-secondary") toggles a form (inside <section class="card">) with inputs id="e-title", id="e-year" (number), id="e-venue", id="e-doi", id="e-arxiv", textarea id="e-abstract", textarea id="e-authors" (one author per line), and Save / Cancel buttons. Save builds an object with only the fields that changed (year as a number or null when blank; authors as an array of non-blank lines), calls apiPatchPaper and then _draw(updated) with a success toast; on ApiRequestError show the message in an error toast (this includes invalid_doi and duplicate_paper).
7. Delete: a button "Delete paper" (class "btn btn-danger"); window.confirm("Delete this paper permanently?") then apiDeletePaper(paperId), success toast, and set location.hash = "#/library".

OUTPUT FORMAT: Only the complete contents of detail.js in a single JavaScript code block. No explanation before or after.
REMINDER: one file only; no import/export; escape every value with escapeHtml; define only renderDetailView and underscore helpers.
```
Acceptance test (browser): open a paper from the library: metadata, abstract, tags and references show; edit the title and year → shown after Save, and the Activity view lists an `edit` entry; add a tag and remove it; enter an invalid DOI (`abc`) → error toast; delete the paper → returns to the library and the paper is gone.
---
Prompt 29 - `frontend/js/graph.js`
Depends on: Prompts 23-26 (Cytoscape tag in `index.html`) · Modifies existing files: no
```text
ROLE: You are a senior front-end engineer who knows the Cytoscape.js library (version 3.34.4, loaded from a CDN as the global function cytoscape).
OBJECTIVE: Write ONE file, frontend/js/graph.js: the interactive knowledge-graph view.
HARD CONSTRAINTS: browser-native HTML5, CSS3 and vanilla ES6 JavaScript only, loaded with plain <script> tags (no import/export, no modules). FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular/JSX, TypeScript, bundlers, any build step, and any CDN library other than the pinned Cytoscape tag. Do not invent features, endpoints or fields.
Globals that already exist: cytoscape (from the CDN script tag), apiGetGraph(includeDerived), showError(container, message), escapeHtml(text), class ApiRequestError (property message).

INTERFACE (name must match exactly):
  async function renderGraphView(container)

CONTEXT - apiGetGraph(includeDerived) resolves to:
  {"elements": {"nodes": [{"data": {"id": "paper:1", "type": "paper", "label": "Title", "paper_id": 1, "year": 2017}},
                          {"data": {"id": "author:1", "type": "author", "label": "Name", "author_id": 1, "paper_count": 1}},
                          {"data": {"id": "topic:3", "type": "topic", "label": "attention", "topic_id": 3, "paper_count": 1}}],
                "edges": [{"data": {"id": "AUTHORED_BY:paper:1:author:1", "type": "AUTHORED_BY", "source": "paper:1", "target": "author:1"}},
                          {"data": {"id": "...", "type": "HAS_TOPIC" | "CITES" | "CO_AUTHOR" | "RELATED_TOPIC", "source": "...", "target": "...", "weight": 2}}]},
   "stats": {"papers": 1, "authors": 1, "topics": 1, "edges": {"AUTHORED_BY": 1, "HAS_TOPIC": 1, "CITES": 0, "CO_AUTHOR": 0, "RELATED_TOPIC": 0}}}
  Pass response.elements to Cytoscape unchanged. CITES is directed (citing -> cited); the other edge types are drawn without arrows.

STEPS:
1. Render into container: a <section class="card"> toolbar (class "toolbar") with <label><input type="checkbox" id="g-derived" checked> Show co-author and related-topic edges</label>, checkboxes id="g-papers", id="g-authors", id="g-topics" (all checked, labels Papers / Authors / Topics), buttons id="g-refresh" and id="g-fit" (class "btn btn-secondary"), and <span id="g-stats" class="muted"></span>; then <div class="graph-wrap"><div id="cy"></div></div>; then a <div class="legend"> with <span class="legend-item"><span class="swatch" style="background:#4e79a7"></span> Paper</span>, author #59a14f, topic #f28e2b, and one text item for each edge type.
2. A private async function _load() calls apiGetGraph(checkbox state); on error call showError(container, error.message). If there are no nodes show <p class="muted">The library is empty - upload a paper to see the graph.</p> inside #cy's parent instead of the graph. Show the stats text in #g-stats ("3 papers, 5 authors, 8 topics").
3. Create the graph with cytoscape({container: document.getElementById("cy"), elements: data.elements, layout: {name: "cose", animate: false}, style: [...]}). Destroy the previous instance first (keep it in a variable window.__rplCy and call destroy() if it exists).
4. Style array: node {label: "data(label)", font-size: 10, text-wrap: "ellipsis", text-max-width: 90, text-valign: "bottom"}; node[type = "paper"] {shape: "round-rectangle", background-color: "#4e79a7"}; node[type = "author"] {shape: "ellipse", background-color: "#59a14f"}; node[type = "topic"] {shape: "diamond", background-color: "#f28e2b"}; edge {width: 1, line-color: "#aaaaaa", curve-style: "bezier"}; edge[type = "HAS_TOPIC"] {line-color: "#f28e2b", line-style: "dotted"}; edge[type = "CITES"] {line-color: "#e15759", width: 2, target-arrow-shape: "triangle", target-arrow-color: "#e15759"}; edge[type = "CO_AUTHOR"] {line-color: "#59a14f", line-style: "dashed", width: "mapData(weight, 1, 5, 1, 5)"}; edge[type = "RELATED_TOPIC"] {line-color: "#f28e2b", line-style: "dashed", width: "mapData(weight, 1, 5, 1, 5)"}; .faded {opacity: 0.15}.
5. Interactions: on cy "tap" of a node: cy.elements().addClass("faded"); node.closedNeighborhood().removeClass("faded"). On "tap" of the background (event.target === cy): cy.elements().removeClass("faded"). On "dbltap" of a node whose data("type") is "paper": location.hash = "#/paper/" + node.data("paper_id").
6. Checkboxes #g-papers, #g-authors, #g-topics show or hide nodes of that type: for each type, cy.nodes('[type = "paper"]').style("display", checked ? "element" : "none") (similarly for author and topic). #g-derived and #g-refresh call _load() again; #g-fit calls cy.fit().
7. Call _load() once at the end of renderGraphView.

OUTPUT FORMAT: Only the complete contents of graph.js in a single JavaScript code block. No explanation before or after.
REMINDER: one file only; no import/export; do not load any other library; define only renderGraphView and underscore helpers.
```
Acceptance test (browser): after at least three papers are uploaded, `#/graph` shows green author, blue paper and orange topic nodes joined by edges; clicking a node fades everything outside its neighbourhood; double-clicking a paper opens its detail view; unticking "Authors" hides author nodes; unticking the derived-edges box removes dashed edges; uploading another paper and pressing Refresh adds it; deleting a paper removes its node after Refresh; an empty library shows the empty message.
---
Prompt 30 - `frontend/js/activity.js`
Depends on: Prompts 24-26 · Modifies existing files: no
```text
ROLE: You are a senior front-end engineer who writes vanilla JavaScript.
OBJECTIVE: Write ONE file, frontend/js/activity.js: the activity-log view.
HARD CONSTRAINTS: browser-native HTML5, CSS3 and vanilla ES6 JavaScript only, loaded with plain <script> tags (no import/export, no modules). FORBIDDEN: Node.js, npm, package.json, React/Vue/Angular/JSX, TypeScript, bundlers, any build step, and any CDN library other than the pinned Cytoscape tag. Do not invent features, endpoints or fields.
Globals that already exist: apiListActivity(params), showError(container, message), escapeHtml(text), formatDate(iso), class ApiRequestError (property message).

INTERFACE (name must match exactly):
  async function renderActivityView(container)

CONTEXT - apiListActivity({user, limit, offset}) resolves to:
  {"total": 7, "items": [{"id": 7, "username": "alice", "action": "upload", "paper_id": 1, "paper_title": "Title", "details": "file: x.pdf", "created_at": "2026-10-22T10:00:05Z"}]}
  action is one of "upload", "edit", "tag_add", "tag_remove", "delete". Newest entries come first. The log keeps entries of deleted papers.

STEPS:
1. Render into container: a <section class="card"> with a <div class="toolbar"> containing <input id="a-user" placeholder="Filter by user name">, a Filter button and a Clear button; then <div id="a-table"></div> and <div class="pagination" id="a-pager"></div>.
2. State: page size 25, offset 0. A private async function _load() calls apiListActivity({user, limit: 25, offset}) and renders <table class="data-table"> with columns Time (formatDate), User, Action, Paper, Details. Paper shows the paper_title; make it a link <a href="#/paper/ID"> only when action is not "delete" (deleted papers no longer exist). Show <p class="muted">No activity yet.</p> for an empty list. The pager shows "Showing X-Y of TOTAL" with Previous / Next buttons disabled at the ends.
3. Filter and Enter reset the offset to 0 and reload; Clear empties the input and reloads. Errors go to showError(container, error.message).
4. Call _load() once at the end of renderActivityView.

OUTPUT FORMAT: Only the complete contents of activity.js in a single JavaScript code block. No explanation before or after.
REMINDER: one file only; no import/export; escape every value with escapeHtml; define only renderActivityView and underscore helpers.
```
Acceptance test (browser): after uploading, editing, tagging and deleting a paper, `#/activity` lists each action with the user name and time (newest first); filtering by the user name narrows the list; the entry for the deleted paper has no link.
---
Prompt 31 - `README.md`
Depends on: all earlier prompts working · Modifies existing files: no
```text
ROLE: You are a technical writer who documents Python web projects.
OBJECTIVE: Write ONE file, README.md, for the project "Research Paper Library & Knowledge Graph". Plain Markdown; do not write any code other than the shell commands given below.

Include these seven sections in this order, with these exact facts:
1. Description (one paragraph): a web app to upload research-paper PDFs, extract title, authors, abstract, keywords, DOI/arXiv ID and references, enrich metadata through Crossref, arXiv, OpenAlex and Semantic Scholar when an identifier is found, assign topic tags (author keywords first, then API topics, then YAKE), store everything in SQLite, log every change with a user name, and show an interactive knowledge graph of papers, authors and topics. Backend: Python and FastAPI. Frontend: plain HTML, CSS and JavaScript with Cytoscape.js 3.34.4 from the jsDelivr CDN (internet needed for the graph library). No Node.js, npm or build step.
2. Python version: 3.12.
3. Install, exactly:
   python -m venv .venv
   Linux/macOS: source .venv/bin/activate      Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   Optional environment variables (never put them in files): CROSSREF_MAILTO (your e-mail, for Crossref's polite pool), OPENALEX_API_KEY, S2_API_KEY, OFFLINE_MODE=1 (skip all external lookups).
4. Start, exactly: python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000   then open http://127.0.0.1:8000 in a browser. Run it from the project root folder.
5. How to use: enter your name at the top and click Save; Library (upload a PDF, search by title/author/topic, year filter); click a paper to see details, correct metadata, add or remove tags, delete; Graph (node colours, click to highlight, double-click a paper to open it, toggle derived edges); Activity (who did what and when). Run the tests with: python -m unittest tests.test_core -v
6. Known limitations: scanned PDFs without a text layer are rejected (no OCR); title/author/abstract/reference detection uses heuristics and can fail on unusual layouts; two-column ordering is approximate; papers without a DOI or arXiv ID get no online metadata; author identity is the normalised name only; citation links only appear between papers that are both in the library; YAKE tags are English-only and estimated; online services have rate limits and may be unavailable (the app then keeps the PDF-derived data and shows a warning); uploaded PDFs are stored in the uploads folder.
7. AI statement: "All application code in this project was generated by Qwen 2.5 Coder 7B Instruct (route used: [FILL IN: hosted provider or local runtime and exact model name]). Planning was done with Claude, research with Gemini/DeepSeek, library lookups with Perplexity. Manual edits are listed in the project's plan document."

OUTPUT FORMAT: Only the complete contents of README.md in a single Markdown code block. No explanation before or after.
REMINDER: one file only; keep every command exactly as given; keep the placeholder [FILL IN: ...] literally.
```
Acceptance test: on a fresh virtual environment, follow the README line by line: install, start, open the page, upload a sample PDF, see it in the library and in the graph. Then replace the `[FILL IN: ...]` placeholder by hand (log this in Section J).
---
I. Build log
To be completed during Phase 4. One row per prompt actually run (add rows for repeated attempts). Nothing below has happened yet.
Prompt #	Attempts	Result	What I changed in the prompt
0			
1			
2			
3			
4			
5			
6			
7			
8			
9			
10			
11			
12			
13			
14			
15			
16			
17			
18			
19			
20			
21			
22			
23			
24			
25			
26			
27			
28			
29			
30			
31			
---
J. Manual-edit log
To be completed during Phase 4. Every manual change (assignment §6.4.3) is listed here: allowed changes are folders/empty files, copy-paste of generated code, renames, package installation, configuration values, and trivial typo/path fixes of a few lines per file. The skeleton work in Section C.1 (empty `__init__.py` files, `requirements.txt`, placeholder `frontend/index.html`, virtual environment, sample PDFs) is recorded here too once it is done.
File	What was changed	Why
		



## B)TECHNOLOGY STACK

1) PYTHON WEB FRAMEWORK
What I choose : FASTAPI
Version : fastapi 0.157.0
Purpose : Serves the app and handles requests/uploads
Why I choose this : Native PDF uploads: UploadFile handles files efficiently without loading the entire PDF into memory.
Built-in API features: Type-validated endpoints, JSON APIs, and automatic OpenAPI/Swagger documentation.
Built-in static-file serving: Mount your HTML/CSS/JS frontend with StaticFiles.
Built-in CORS: CORSMiddleware avoids needing a separate CORS package.
Better long-term fit than Flask: Flask works well, but needs Flask-CORS and lacks automatic validation/OpenAPI.
More convenient than Bottle: Bottle is very lightweight but requires manual static-file routing and has no built-in CORS.
Source URL :
FastAPI static files: 
https://fastapi.tiangolo.com/tutorial/static-files/
FastAPI file uploads: 
https://fastapi.tiangolo.com/tutorial/request-files/
FastAPI CORS: 
https://fastapi.tiangolo.com/tutorial/cors/
FastAPI on PyPI: 
https://pypi.org/project/fastapi/


2) PDF Text and Layout Extraction
What I chose : PyMuPDF
Version :PyMuPDF (Not PyPDF2 as it is deprecated)
Purpose : Extracts text and layout information
Why I choose this : Rich positional data: It returns text as blocks, lines, spans, words, and characters with bounding boxes, which is essential for detecting and processing columns.
Better two-column handling: Its block/word coordinates let you implement column-aware reading order; it does not magically solve two-column PDFs, but it gives you the tools to do so reliably.
Fast and actively maintained: PyMuPDF is a high-performance PDF extraction and manipulation library, with current stable version 2.0 released October 19, 2026.
OCR support: It can integrate OCR for scanned papers, unlike pdfplumber or pypdf.
More suitable than pypdf: pypdf is good for PDF manipulation but is weaker for structured, position-aware extraction.
More practical than pdfplumber as the default: pdfplumber is excellent for detailed character-level geometry and debugging, but it is slower and its layout mode is experimental; use it as a fallback for difficult PDFs.
Source URL : 
PyMuPDF documentation — 
https://pymupdf.readthedocs.io/en/latest/
PyMuPDF text-extraction details — 
https://pymupdf.readthedocs.io/en/latest/app1.html
PyMuPDF FAQ, including multi-column guidance — 
https://pymupdf.readthedocs.io/en/latest/faq/index.html
PyMuPDF TextPage reference — 
https://pymupdf.readthedocs.io/en/latest/textpage.html
PyMuPDF on PyPI — 
https://pypi.org/project/pymupdf/
pdfplumber on PyPI — 
https://pypi.org/project/pdfplumber/
pdfplumber README — 
https://github.com/jsvine/pdfplumber/blob/v0.7.1/README.md
pypdf on PyPI — 
https://pypi.org/project/pypdf/
pypdf history and PyPDF2 deprecation/merge — 
https://github.com/py-pdf/pypdf/blob/main/docs/meta/history.md
https://artifex.com/licensing?utm_source=github&utm_medium=referral&utm_campaign=pymupdf_github&utm_content=footer&utm_term=licensing

3) Metadata APIs and HTTP client
What I chose : httpx and Crossref, OpenAlex, Semantic Scholar, arXiv
Version : httpx 0.28.1
Purpose : Calls metadata APIs
Why I choose this : Choose httpx because your app uses FastAPI, which is asynchronous; httpx.AsyncClient lets metadata requests run without blocking the server’s event loop.
It supports both sync and async code, so you can use it in API routes, background jobs, or scripts.
It supports HTTP/1.1 and HTTP/2; HTTP/2 requires the optional http2 extra.
Its API is familiar to requests users, making migration and testing straightforward.
Current stable version is 0.28.1, released December 6, 2024.
Crossref: Primary source when you have a DOI; best for authoritative bibliographic metadata and deposited references.
OpenAlex: Best broad enrichment source for works, authors, citations, open-access information, and graph-friendly IDs.
Semantic Scholar: Best for abstracts, citation/reference graphs, recommendations, and lookup by DOI or arXiv ID.
arXiv: Best for arXiv preprints—titles, authors, abstracts, versions, categories, and arXiv IDs; it does not provide structured references.
Package
Uvicorn : Runs the FastAPI application as an ASGI server. (uvicorn 0.54.0)
python-multipart : Supports handling uploaded files through FastAPI's form and file-upload mechanisms. (python-multipart 0.0.32)
Source URL : 
httpx on PyPI — 
https://pypi.org/project/httpx/
requests on PyPI — 
https://pypi.org/project/requests/
Crossref access/authentication — 
https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/
Crossref metadata retrieval — 
https://www.crossref.org/documentation/retrieve-metadata/
OpenAlex authentication — 
https://help.openalex.org/api/authentication/
OpenAlex endpoints — 
https://help.openalex.org/api/endpoints/
Semantic Scholar API reference — 
https://api.semanticscholar.org/api-docs
Semantic Scholar tutorial — 
https://www.semanticscholar.org/product/api/tutorial
arXiv API User’s Manual — 
https://info.arxiv.org/help/api/user-manual.html
https://pypi.org/project/httpx/

4) Automatic keyword extraction and tagging
What I chose : Author-provided keywords
Version : (YAKE (yake 0.7.3))

Purpose : Assigns topic tags
Why I choose this :
They are usually the most accurate and meaningful tags because authors deliberately selected them to describe the paper.
They require no machine-learning model, training data, or large downloads.
They are simple to implement: normalize casing, split delimiters, remove duplicates, and store them as tags.
Their main limitation is availability—many papers do not include them—so use them as the preferred source when present.
Use author keywords first when available.
Let users accept, edit, or reject suggested tags; record whether a tag came from the author, YAKE, or an API.
The application will generate topic tags using the following priority order:
Author-provided keywords: Use keywords extracted from the paper's metadata when available.
Scholarly API topics: If author-provided keywords are unavailable, use relevant topics returned by a scholarly metadata API, when available.
YAKE fallback: If neither source provides usable keywords or topics, use YAKE (Yet Another Keyword Extractor) to extract candidate keywords from the paper's extracted text.
YAKE will run locally and will not require an external API request. The application will record the source of the generated tags so users can distinguish author-provided keywords, API-supplied topics, and automatically extracted keywords.
Purpose: To provide useful topic tags for searching, filtering, and visualising research papers, including papers for which external metadata is incomplete.
Source: https://pypi.org/project/yake/
Source URL : 
YAKE on PyPI — 
https://pypi.org/project/yake/
OpenAlex API endpoints — https://help.openalex.org/api/endpoints/
Semantic Scholar API reference — 
https://api.semanticscholar.org/api-docs

5) SQLite database access and SQL injection
What I chose : Python's built in sqlite3 (Python 3.13)
Version :  Python's built in sqlite3 (Python 3.13)
Purpose : Reads and writes database
Why I choose this :
No extra installation: It is part of Python’s standard library, so you avoid adding a database dependency.
Simple for a small app: It directly supports SQLite files, SQL queries, cursors, transactions, commits, rollbacks, and parameterized queries.
Good fit for the schema: A small Research Paper Library with papers, authors, tags, references, and knowledge-graph links fits naturally into relational tables.
Safe queries: Use ? placeholders and pass values separately; this is the documented way to bind user input without building SQL strings by concatenation.
Reliable transactions: Use with con: to commit on success and roll back after an uncaught exception; explicitly call commit() or rollback() when managing transactions manually.
Foreign keys: Define foreign keys in the schema and enable enforcement per connection with PRAGMA foreign_keys = ON.
Source URL : 
Python sqlite3 documentation — 
https://docs.python.org/3/library/sqlite3.html
Python 3.14 sqlite3 documentation — 
https://docs.python.org/3.14/library/sqlite3.html
Python 3.10 sqlite3 documentation — 
https://docs.python.org/3.10/library/sqlite3.html
SQLAlchemy download and release status — 
https://www.sqlalchemy.org/download.html
SQLAlchemy homepage — https://www.sqlalchemy.org/
SQLAlchemy transactions and connection management — 
https://docs.sqlalchemy.org/en/20/orm/session_transaction.html
SQLAlchemy Session basics — 
https://docs.sqlalchemy.org/en/20/orm/session_basics.html




6) Browser based graph visualization 
What I chose : Cytoscape.js
Version : v3.34.4
Purpose : Displays graph in browser
Why I choose this :
Best fit for a knowledge graph: It is designed for graph-theory networks, including directed edges, relationships, styling, and graph queries—ideal for papers, authors, topics, and citation links.
Works without npm or a build step: Load it directly in plain HTML with a pinned jsDelivr <script> tag.
No separate CSS file: Cytoscape.js needs only JavaScript; you add your own CSS to size the graph container.
Strong interaction and styling: It supports node/edge styling, selectors, events, layouts, neighborhood highlighting, and dynamic graph updates.
Source URL : 
Cytoscape.js releases — 
https://github.com/cytoscape/cytoscape.js/releases
Cytoscape.js documentation — https://js.cytoscape.org/
Cytoscape.js getting-started tutorial — 
https://blog.js.cytoscape.org/2016/05/24/getting-started/
Cytoscape.js layouts guide — 
https://blog.js.cytoscape.org/2020/05/11/layouts/
Cytoscape.js on jsDelivr — 
https://www.jsdelivr.com/package/npm/cytoscape
vis-network documentation — 
https://visjs.github.io/vis-network/docs/network/
https://www.jsdelivr.com/package/npm/cytoscape
https://www.jsdelivr.com/package/npm/cytoscape
