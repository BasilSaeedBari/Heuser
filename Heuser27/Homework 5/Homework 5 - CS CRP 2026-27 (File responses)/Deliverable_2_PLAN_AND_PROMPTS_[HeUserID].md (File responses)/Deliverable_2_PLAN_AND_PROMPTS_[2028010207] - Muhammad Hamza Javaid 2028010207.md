&#32;

# Technology-Stack Lookup Table

| **Need** | **Library** | **Exact Version** | **Purpose** | **Why Chosen** | **Source URL** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Web framework | Flask | 3.1.3 | Build the app, serve static files, handle the PDF upload endpoint | Current stable Flask release; supports Python 3 and includes the documented upload/static-file patterns | \[<https://pypi.org/project/Flask/>\] |
| PDF extraction | **PyMuPDF** | **2.0** (current stable PyPI release, Oct 19, 2026) | Extract text blocks, lines, spans, fonts, and bounding boxes via `page.get_text("dict")`; supports multi-column layouts, natural reading order, clipping, search coordinates, and JSON/Markdown export | It provides precise low-level text-position metadata (`bbox`) and is much faster than pdfplumber/pdfminer.six; pdfplumber is better for tables/visual debugging but slower, while pypdf is primarily for PDF manipulation and offers only basic text extraction. Its AGPL/commercial dual license is the main tradeoff. | <https://pypi.org/project/pymupdf/> [pypi](https://pypi.org/project/pymupdf/) |
| HTTP client | requests | 2.34.2 | Send GET requests, pass query parameters, parse JSON responses, enforce timeouts, and handle HTTP/network failures | It is the de facto standard Python HTTP client, has a simple API for `params` and `.json()`, and supports explicit connect/read timeouts; `httpx` is preferable mainly when you need async requests or HTTP/2, while `urllib3` is lower-level and `aiohttp` is async-first. | <https://pypi.org/project/requests/> |
| Keyword extraction | YAKE | 0.7.3 | Unsupervised, local keyword extraction from a single document using statistical text features; returns ranked keywords and scores | It is actively maintained, requires no model download, external corpus, dictionary, or training data, and is designed to work across text lengths, domains, and languages; RAKE-NLTK is simpler but stale, while transformer-based extractors require substantially larger models and more compute. | <https://pypi.org/project/yake/> |
| SQLite access | sqlite3 | Bundled with Python 3.11; no separate install | Execute parameterized SQL, manage transactions, and store application data in a local SQLite database | It has zero extra dependency, directly supports SQLite’s `?` and named-parameter binding, and is sufficient for a small schema; SQLAlchemy adds an ORM/query abstraction and dependency/maintenance overhead that may not pay off for a small app. | <https://docs.python.org/3/library/sqlite3.html> |
| Graph visualization | vis-network | 10.1.2 | Display and interact with networks made of nodes and edges; supports dynamic `DataSet` updates, layouts, clustering, and event handling | It is purpose-built for interactive network visualization, accepts plain node/edge arrays or DataSets, and has first-class built-in physics/layout options; Cytoscape.js is stronger for graph-analysis-oriented styling and selectors but has a more verbose element schema. | <https://www.jsdelivr.com/package/npm/vis-network> |
| CSS framework | Water.css | 2.1.1 | Provide sensible default typography, spacing, form styling, and automatic light/dark theme support using semantic HTML | It is a drop-in, class-less stylesheet with no JavaScript or build process; Pico CSS is stronger for semantic-HTML UI components but has ended maintenance at v2.1.1, while Water.css remains the smaller, simpler baseline choice. | \[<https://cdn.jsdelivr.net/gh/kognise/water.css@2.1.1/README.md>\] |

&#32;

# Claude Provided Plan:

## PaperLib: Architecture Plan and Qwen Prompt Series

&#32;I read both files. Three things to know before you start:

- **Version conflicts are marked \[VERIFY\].** Your Phase 1 says PyMuPDF 1.28.2 and YAKE 0.6.0. Your Phase 2 table says PyMuPDF 2.0 and YAKE 0.7.3. I could not settle these. Run `pip index versions <pkg>` for each before the first install.
- **`references` is an SQL reserved word.** The table is named `paper_references` to prevent a class of bugs a 7B model would hit.
- **Scope calls I made:**
  - Link tables (F5 “links”) are `paper_authors` and `paper_topics`.
  - “Tags” and “topics” are the same entity.
  - OCR, SimHash, and LLM or GROBID reference fallbacks are out of scope.

---

### A. Overview and key design decisions

PaperLib is a single-process Flask app that serves a JSON API and a static vanilla-JS single-page frontend. Uploading a PDF runs a pipeline: parse, extract metadata, extract references, enrich, tag, store, then the graph is computed on demand.

| \# | Decision | Justification |
| --- | --- | --- |
| 1 | **Graph edges are computed on request, not stored.** | `/api/graph` builds nodes and edges with SQL joins over `paper_authors`, `paper_topics` and `paper_references`. |
|  |  | A stored `edges` table must be kept in sync on upload, edit, tag change and delete. That is four places where a 7B model can leave stale edges, and it would break F9 and F11. |
|  |  | Computed edges are always consistent. Deleting a paper (F11) automatically removes its edges. |
|  |  | At personal-library scale (hundreds of papers) the joins are milliseconds. A `max_papers` cap guards the worst case. |
|  |  | If the library ever exceeds about 1,000 papers, add a cache. That is a later change that touches only `graph.py`. |
| 2 | Identity is a typed user name, with no login. | The name is stored in browser `localStorage` and sent as the `X-User-Name` header. Every mutating call is rejected without it (F6). |
| 3 | Tags and topics are one concept: `topics`. | `paper_topics.source` is `author`, `yake` or `manual`. The UI calls them “tags”. |
| 4 | Tagging is layered, per your Phase 1 research. | Author keywords come first, then a YAKE fallback on title and abstract. OpenAlex `/text` is skipped so the app works offline. |
| 5 | Metadata enrichment is best-effort. | Crossref (by DOI) and arXiv (by ID) fill only the fields that are still empty. Enrichment never raises. Offline, the app still works. |
| 6 | Duplicate detection uses three keys. | SHA-256 of the file bytes, then DOI, then arXiv ID. All three are `UNIQUE`. A duplicate returns HTTP 409. |
| 7 | Scanned PDFs are rejected with a clear error. | The test is average extracted characters per page below 100. OCR is out of scope. |
| 8 | The activity log has no foreign key to `papers`. | Log rows survive deletion and keep the paper title. |
| 9 | Transaction rule. | Repository functions never commit. Callers wrap work in `with conn:`. |
| 10 | Timestamps are UTC ISO-8601 strings. | Example: `2026-10-23T09:00:00Z`. |
| 11 | Uploaded files are stored as `uploads/<sha256>.pdf`. | This avoids filename collisions and path tricks. |
| 12 | Frontend uses classic `<script>` files with global namespaces. | Namespaces are `Api`, `App`, `Library`, `PaperView`, `GraphView`, `ActivityView`. This is simpler for a weak model than ES-module import and export wiring. |
| 13 | All data-derived text is inserted with `textContent`, never `innerHTML`. | Prevents XSS from malicious PDF text. |

---

### B. Technology stack

| Name | Exact version | Purpose | Why chosen | Source URL |
| --- | --- | --- | --- | --- |
| Python | 3.11 | Runtime | Hard constraint. | <https://www.python.org/downloads/> |
| Flask | 3.1.3 \[VERIFY\] | Web app, static files, upload endpoint | Minimal, well documented. | <https://pypi.org/project/Flask/> |
| PyMuPDF | 2.0 \[VERIFY: Phase 1 says 1.28.2\] | Text blocks, fonts and bounding boxes via `get_text("dict")` | Gives the layout metadata needed for titles and two-column order. It is fast. AGPL or commercial license is the tradeoff. | <https://pypi.org/project/pymupdf/> |
| requests | 2.34.2 \[VERIFY\] | Crossref and arXiv calls with timeouts | Simple standard HTTP client. | <https://pypi.org/project/requests/> |
| YAKE | 0.7.3 \[VERIFY: Phase 1 says 0.6.0\] | Local keyword fallback | Single-document, no corpus or model download. | <https://pypi.org/project/yake/> |
| sqlite3 | Bundled with Python 3.11 | Database | No install, and enough for this schema. | <https://docs.python.org/3/library/sqlite3.html> |
| vis-network | 10.1.2 (matches Phase 1) | Interactive graph | Takes plain `nodes` and `edges` arrays and ships with physics. | <https://www.jsdelivr.com/package/npm/vis-network> |
| Water.css | 2.1.1 | Class-less styling with light/dark theme | No JS and no build step. | <https://cdn.jsdelivr.net/gh/kognise/water.css@2.1.1/README.md> |

`requirements.txt` content (pins copied from your Phase 2 table; fix the \[VERIFY\] lines first):

```
Flask==3.1.3        # [VERIFY]
PyMuPDF==2.0        # [VERIFY] Phase 1 said 1.28.2
requests==2.34.2    # [VERIFY]
yake==0.7.3         # [VERIFY] Phase 1 said 0.6.0
```

Standard-library modules used: `sqlite3`, `hashlib`, `re`, `json`, `pathlib`, `xml.etree.ElementTree`, `unicodedata`, `datetime`, `contextlib`, `os`. Use `import pymupdf`, not the deprecated `import fitz`.

---

### C. Architecture

#### File tree

```
paperlib/
├── requirements.txt          # pinned deps (Section B)
├── README.md                 # setup + run command
├── run.py                    # starts Flask on 127.0.0.1:5000
├── data/                     # (runtime) paperlib.db
├── uploads/                  # (runtime) <sha256>.pdf files
├── tests/sample.pdf          # YOU supply: one of your 3 sample papers
└── app/
    ├── __init__.py           # create_app(): blueprints, error handlers, "/" route
    ├── common.py             # constants, AppError, now_iso, norm_text, get_user_name
    ├── schema.sql            # Section D, pasted verbatim (no Qwen needed)
    ├── db.py                 # get_conn(), init_db()
    ├── repo_papers.py        # SQL for papers/authors/topics/references
    ├── repo_activity.py      # log_action(), list_activity()
    ├── pdf_text.py           # PyMuPDF: ordered text, first-page lines, scan detection
    ├── meta_ids.py           # regex: DOI, arXiv ID, year, venue, author keywords
    ├── meta_layout.py        # layout heuristics: title, authors, abstract
    ├── references.py         # locate + split the reference list
    ├── enrich.py             # Crossref / arXiv lookup (best-effort)
    ├── tagging.py            # author keywords, then YAKE fallback
    ├── pipeline.py           # ingest_pdf(): orchestrates all of the above
    ├── graph.py              # build_graph(): computed nodes/edges
    ├── api_upload.py         # POST /api/papers
    ├── api_papers.py         # list/detail/patch/topics/delete/file/topics list
    ├── api_misc.py           # GET /api/graph, GET /api/activity
    └── static/
        ├── index.html        # shell, CDN tags, nav, user-name box
        └── js/
            ├── api.js        # fetch wrapper `Api`
            ├── app.js        # `App` helpers + hash router
            ├── library.js    # library + upload + filters view
            ├── paper.js      # paper detail + edit + tags + delete
            ├── graph.js      # vis-network graph view
            └── activity.js   # activity log view
```

#### Data flow

1. **Upload.** The browser POSTs a multipart `file` with the `X-User-Name` header to `/api/papers`.
1. **Validate.** The route checks the user name, the `.pdf` extension and the `%PDF-` magic bytes. It computes the SHA-256 and rejects an exact duplicate with 409.
1. **Store.** The file is saved to `uploads/<sha256>.pdf`.
1. **Parse.** `pdf`_`text.extract`_`pdf` returns ordered page text, first-page lines with font sizes, and `is_scanned`. A scanned PDF is rejected with 422.
1. **Extract.** `meta_ids` and `meta_layout` produce title, authors, abstract, DOI, arXiv ID, year, venue and keywords. `references.extract_references` splits the reference list.
1. **Enrich.** `enrich.enrich_metadata` fills only missing fields. It is best-effort and never raises.
1. **Tag.** `tagging.assign_topics` uses author keywords first, then YAKE.
1. **Dedupe.** A second duplicate check runs on DOI and arXiv ID, giving 409 on a match.
1. **Store records.** In one transaction, `pipeline.ingest_pdf` inserts the paper, authors, topics and references, and writes the `upload` log row.
1. **Graph.** Nothing is written. `/api/graph` recomputes from the tables, so the new paper appears on the next load.
1. **Failure.** If anything fails after step 3, the saved file is deleted and a JSON error is returned.

---

### D. Database schema

Save as `app/schema.sql`, copied verbatim. `db.get_conn()` must also run `PRAGMA foreign_keys = ON` on every connection.

sql

```
CREATE TABLE IF NOT EXISTS papers (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  title           TEXT    NOT NULL,
  abstract        TEXT    NOT NULL DEFAULT '',
  abstract_source TEXT    NOT NULL DEFAULT 'missing'
                  CHECK (abstract_source IN ('extracted','fallback_intro','missing')),
  doi             TEXT    UNIQUE,            -- lowercase, NULL if absent
  arxiv_id        TEXT    UNIQUE,            -- no prefix, no version, NULL if absent
  year            INTEGER,
  venue           TEXT,
  file_name       TEXT    NOT NULL,          -- original upload name
  file_path       TEXT    NOT NULL,          -- uploads/<sha256>.pdf
  file_sha256     TEXT    NOT NULL UNIQUE,
  page_count      INTEGER NOT NULL DEFAULT 0,
  uploaded_by     TEXT    NOT NULL,
  created_at      TEXT    NOT NULL,
  updated_at      TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_papers_title ON papers(title);
CREATE INDEX IF NOT EXISTS idx_papers_year  ON papers(year);

CREATE TABLE IF NOT EXISTS authors (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  name      TEXT NOT NULL,
  name_norm TEXT NOT NULL UNIQUE             -- norm_text(name)
);

CREATE TABLE IF NOT EXISTS paper_authors (
  paper_id  INTEGER NOT NULL REFERENCES papers(id)  ON DELETE CASCADE,
  author_id INTEGER NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
  position  INTEGER NOT NULL,
  PRIMARY KEY (paper_id, author_id)
);
CREATE INDEX IF NOT EXISTS idx_pa_author ON paper_authors(author_id);

CREATE TABLE IF NOT EXISTS topics (
  id   INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE                  -- stored lowercase
);

CREATE TABLE IF NOT EXISTS paper_topics (
  paper_id INTEGER NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
  topic_id INTEGER NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
  source   TEXT    NOT NULL CHECK (source IN ('author','yake','manual')),
  score    REAL    NOT NULL DEFAULT 1.0,
  PRIMARY KEY (paper_id, topic_id)
);
CREATE INDEX IF NOT EXISTS idx_pt_topic ON paper_topics(topic_id);

CREATE TABLE IF NOT EXISTS paper_references (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  paper_id INTEGER NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
  position INTEGER NOT NULL,                 -- 1-based order in the list
  raw_text TEXT    NOT NULL,                 -- always kept
  doi      TEXT,                             -- lowercase, if found in raw_text
  year     INTEGER,
  title    TEXT,
  UNIQUE (paper_id, position)
);
CREATE INDEX IF NOT EXISTS idx_ref_paper ON paper_references(paper_id);
CREATE INDEX IF NOT EXISTS idx_ref_doi   ON paper_references(doi);

CREATE TABLE IF NOT EXISTS activity_log (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  ts           TEXT    NOT NULL,
  user_name    TEXT    NOT NULL,
  action       TEXT    NOT NULL CHECK (action IN ('upload','edit','tag_change','delete')),
  entity_type  TEXT    NOT NULL DEFAULT 'paper',
  entity_id    INTEGER,                      -- NO foreign key: survives deletion
  paper_title  TEXT,
  details_json TEXT    NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_log_ts     ON activity_log(ts DESC);
CREATE INDEX IF NOT EXISTS idx_log_entity ON activity_log(entity_id);
```

**Orphan rule.** After any change to `paper_authors` or `paper_topics`, and after a delete, `repo`_`papers.cleanup`_`orphans(conn)` deletes authors and topics that have no links. This keeps the graph clean (F11).

---

### E. API contract

All errors use this JSON shape: `{"error": {"code": "DUPLICATE", "message": "Already in library as paper 3."}}`.

All mutating requests (POST, PATCH, PUT, DELETE) require the `X-User-Name` header. Without it they return 400 `NO_USER`.

**Shared shapes**

- **PaperSummary:** `{"id":3,"title":"JaxMARL-BC: Multi-Agent Reinforcement Learning for Macroeconomic Modelling, in Seconds","authors":["Daniele Montagnani","Andrea Coletta"],"year":2026,"venue":"ACM ICAIF","doi":null,"arxiv`_`id":"2610.28907","topics":["multi-agent reinforcement learning"],"created`_`at":"2026-10-23T09:00:00Z"}`
- **PaperDetail:** PaperSummary plus these fields, with `topics` becoming a list of objects:
  - `abstract`
  - `abstract_source`
  - `file_name`
  - `page_count`
  - `uploaded_by`
  - `updated_at`
  - `topics: [{"name":"macroeconomics","source":"author"}]`
  - `references: [{"id":1,"position":1,"raw_text":"[1] Stéphane Adjemian ...","doi":null,"year":2011,"title":null}]`

| Method | Path | Request | Success | Errors |
| --- | --- | --- | --- | --- |
| POST | `/api/papers` | multipart, field `file` | 201 `{"paper": PaperDetail}` | 400 NO_USER, NO_FILE, NOT_PDF; 409 DUPLICATE; 413 TOO_LARGE; 422 SCANNED_PDF, PARSE_FAILED |
| GET | `/api/papers` | query: `q`, `author`, `topic`, `year`, `limit` (default 20, max 100), `offset` | 200 `{"papers":[PaperSummary],"total":42}` | 400 BAD_REQUEST |
| GET | `/api/papers/<id>` | none | 200 `{"paper": PaperDetail}` | 404 NOT_FOUND |
| PATCH | `/api/papers/<id>` | JSON with any of `title, abstract, year, venue, doi, arxiv_id, authors` (list of names) | 200 `{"paper": PaperDetail}` | 400 NO_USER, BAD_REQUEST; 404; 409 DUPLICATE |
| PUT | `/api/papers/<id>/topics` | JSON `{"topics":["a","b"]}` (full replacement, max 30) | 200 `{"paper": PaperDetail}` | 400 NO_USER, BAD_REQUEST; 404 |
| DELETE | `/api/papers/<id>` | none | 200 `{"deleted":true,"id":3}` | 400 NO_USER; 404 |
| GET | `/api/papers/<id>/file` | none | 200 `application/pdf` | 404 |
| GET | `/api/topics` | none | 200 `{"topics":[{"id":1,"name":"macroeconomics","paper_count":2}]}` | none |
| GET | `/api/graph` | query: `min_weight` (int, default 1) | 200 graph JSON (below) | 400 BAD_REQUEST |
| GET | `/api/activity` | query: `limit` (default 50, max 200), `offset`, `user`, `paper_id` | 200 (below) | 400 BAD_REQUEST |

**Graph response:**

json

```
{"nodes":[{"id":"paper:3","type":"paper","label":"JaxMARL-BC: Multi-Agent Reinf..."},
          {"id":"author:7","type":"author","label":"Andrea Coletta"},
          {"id":"topic:2","type":"topic","label":"macroeconomics"}],
 "edges":[{"from":"author:7","to":"paper:3","type":"AUTHORED","weight":1},
          {"from":"paper:3","to":"topic:2","type":"HAS_TOPIC","weight":1},
          {"from":"author:7","to":"author:9","type":"CO_AUTHOR","weight":2},
          {"from":"topic:2","to":"topic:5","type":"CO_TOPIC","weight":3},
          {"from":"paper:3","to":"paper:1","type":"CITES","weight":1}]}
```

**Activity response:**

json

```
{"entries":[{"id":12,"ts":"2026-10-23T09:00:00Z","user_name":"Sam","action":"tag_change","entity_type":"paper","entity_id":3,"paper_title":"JaxMARL-BC ...","details":{"added":["jax"],"removed":[]}}],"total":12}
```

**Error examples**

- `{"error":{"code":"SCANNED_PDF","message":"This PDF has no extractable text (scanned?). OCR is not supported."}}`
- `{"error":{"code":"NOT_PDF","message":"Only PDF files are accepted."}}`

**Activity details by action**

- `upload`: `{"file`_`name","page`_`count","reference`_`count","topic`_`count"}`
- `edit`: `{"changed":{"title":["old","new"]}}`
- `tag_change`: `{"added":[],"removed":[]}`
- `delete`: `{}`

---

### F. Frontend specification

**Views**, hash-routed in one page:

- `#/library`, the default. It has the upload form, filters and the paper table.
- `#/paper/<id>`
- `#/graph`
- `#/activity`

**DOM skeleton (`index.html`)**

```
<header>
  <h1>PaperLib</h1>
  <nav> a#nav-library  a#nav-graph  a#nav-activity </nav>
  <label>Your name <input id="user-name" maxlength="80"></label>
</header>
<main id="view"></main>
<div id="toast" role="status"></div>
```

**Exact CDN tags** (head, before app scripts):

html

```
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2.1.1/out/water.min.css"> <!-- [VERIFY] file path -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/vis-network@10.1.2/styles/vis-network.min.css">
<script src="https://cdn.jsdelivr.net/npm/vis-network@10.1.2/standalone/umd/vis-network.min.js"></script>
```

**Local scripts**, at the end of body, in this exact order:

html

```
<script src="/static/js/api.js"></script>
<script src="/static/js/library.js"></script>
<script src="/static/js/paper.js"></script>
<script src="/static/js/graph.js"></script>
<script src="/static/js/activity.js"></script>
<script src="/static/js/app.js"></script>
```

**Library view layout**

- An upload form (`input type=file accept=.pdf` plus a button).
- A filter row: title text, author text, topic `<select>` filled from `/api/topics`, and year.
- A table with columns Title (link), Authors, Year, Topics, Added.
- A pager (20 per page).

**Paper view layout**

- Metadata block (title, authors, year, venue, DOI, arXiv ID, abstract). A note appears when `abstract_source` is not `extracted`.
- Edit toggle with Save.
- Tag chips with remove and add.
- Ordered reference list. A DOI becomes a [`https://doi.org/`](https://doi.org/)`<doi>` link.
- “Open PDF” link and a Delete button with `confirm()`.

**Graph JSON to vis-network mapping** (applied in `graph.js`)

| API field | vis-network field |
| --- | --- |
| node `id` | `id` (string, used as is) |
| node `label` | `label` |
| node `type` | `group`, plus these per-type shapes |
| `paper` | `shape:"box"`, colour `#4f8cff` |
| `author` | `shape:"dot"`, colour `#f5a623` |
| `topic` | `shape:"diamond"`, colour `#50c878` |
| edge `from`, `to` | `from`, `to` |
| edge `type` AUTHORED, HAS_TOPIC, CITES | `arrows:"to"` |
| edge `type` CO_AUTHOR, CO_TOPIC | `dashes:true`, no arrows |
| edge `weight` | `width: Math.min(1 + weight, 6)`; `label` only when weight > 1 |

- Wrap nodes and edges in `new vis.DataSet(...)`, and create `new vis.Network(container, {nodes, edges}, options)`.
- Clicking a `paper:` node sets `location.hash = "#/paper/" + id`.
- Checkboxes toggle edge types client-side. The view re-fetches `/api/graph` on every render, so new papers appear (F9).

---

### G. Build order and dependencies

| Step | Module | Depends on |
| --- | --- | --- |
| 0 | Create folders, an empty `app/_`_`init`_`_.py`, `requirements.txt`, `schema.sql`; `pip install -r requirements.txt` | none |
| 1 | P0 `common.py` | none |
| 2 | P1 `db.py` | common, schema.sql |
| 3 | P2 `repo_papers.py`, P3 `repo_activity.py` | db, common |
| 4 | P4 `pdf_text.py` | common |
| 5 | P5 `meta_ids.py`, P6 `meta_layout.py`, P7 `references.py` | none (pure functions) |
| 6 | P8 `enrich.py`, P9 `tagging.py` | common |
| 7 | P10 `pipeline.py` | everything above |
| 8 | P11 `graph.py` | db |
| 9 | P12–P14 API modules, P15 **`_`_`init`_`_`**`.py`, P16 `run.py` | pipeline, repos, graph |
| 10 | P17 `index.html`, then P18–P23 JS in order | API running |
| 11 | P24 `README.md` | all |

**Checkpoints.**

- After P10, run an end-to-end ingest from the command line.
- After P16, run `curl` against the API.
- After P23, do the full browser test.

---

### H. Prompts for Qwen 2.5 Coder 7B Instruct

Paste each prompt on its own, in order. Do not combine prompts. If a module fails its acceptance test, fix the prompt, not the output. Then log the change in Section I.

#### Prompt 0: `app/common.py`

text

```
ROLE: You are a careful Python 3.11 developer. OBJECTIVE: write the shared constants and helpers module for a Flask + SQLite app.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/common.py
IMPORTS ALLOWED: pathlib, datetime, re, unicodedata.

CONSTANTS (exact names and values):
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "paperlib.db"
UPLOAD_DIR = BASE_DIR / "uploads"
MAX_UPLOAD_BYTES = 25 * 1024 * 1024
MIN_CHARS_PER_PAGE = 100
MAX_TOPICS = 10
MAX_REFERENCES = 500
ENRICH_ENABLED = True
HTTP_TIMEOUT = (3, 8)
CROSSREF_URL = "https://api.crossref.org/works/"
ARXIV_URL = "http://export.arxiv.org/api/query"
CROSSREF_MAILTO = ""
ACTIONS = ("upload", "edit", "tag_change", "delete")
TOPIC_SOURCES = ("author", "yake", "manual")

CLASS: class AppError(Exception) with __init__(self, code: str, message: str, status: int = 400); store them as attributes code, message, status; call super().__init__(message).

FUNCTIONS:
now_iso() -> str : current UTC time like "2026-10-23T09:00:00Z".
norm_text(s: str) -> str : lowercase, strip accents (unicodedata NFKD, drop combining marks), replace every run of non-alphanumeric characters with one space, strip.
truncate(s: str, n: int) -> str : s if len(s) <= n else s[:n-3] + "...".
get_user_name() -> str : import flask.request INSIDE the function; read header "X-User-Name", strip it, cut to 80 chars; if empty raise AppError("NO_USER", "Enter your name first.", 400); else return it.

STEPS: 1) imports 2) constants 3) AppError 4) the four functions.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: python -c "from app.common import *; print(now_iso(), '|', norm_text('Éé  Foo-Bar!'), '|', DB_PATH)"  -> second field is exactly: ee foo bar
```

#### Prompt 1: `app/db.py`

text

```
ROLE: You are a careful Python 3.11 developer. OBJECTIVE: write the SQLite connection helper.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/db.py
IMPORTS ALLOWED: sqlite3, pathlib.Path, and from app.common import DB_PATH, UPLOAD_DIR.

INTERFACE:
get_conn() -> sqlite3.Connection : connect to str(DB_PATH) with timeout=10; set conn.row_factory = sqlite3.Row; run conn.execute("PRAGMA foreign_keys = ON"); return conn.
init_db() -> None : create the parent folder of DB_PATH and UPLOAD_DIR (parents=True, exist_ok=True); read the text file app/schema.sql (located next to this file, utf-8); open a connection; conn.executescript(schema); conn.commit(); conn.close().

CONTEXT: schema.sql already exists and creates 7 tables: papers, authors, paper_authors, topics, paper_topics, paper_references, activity_log.

STEPS: 1) imports 2) get_conn 3) init_db.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: python -c "from app.db import init_db,get_conn; init_db(); c=get_conn(); print([r[0] for r in c.execute(\"select name from sqlite_master where type='table'\")])"  -> list contains all 7 table names.
```

#### Prompt 2: `app/repo_papers.py`

text

```
ROLE: You are a careful Python 3.11 developer. OBJECTIVE: write the data-access functions for papers, authors, topics and references.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/repo_papers.py
IMPORTS ALLOWED: sqlite3, and from app.common import now_iso, norm_text.
RULES: every function takes an open sqlite3 connection `conn` (row_factory=sqlite3.Row) as first argument and NEVER calls commit. Always use ? placeholders, never string-format values into SQL. Tables: papers(id,title,abstract,abstract_source,doi,arxiv_id,year,venue,file_name,file_path,file_sha256,page_count,uploaded_by,created_at,updated_at); authors(id,name,name_norm UNIQUE); paper_authors(paper_id,author_id,position); topics(id,name UNIQUE lowercase); paper_topics(paper_id,topic_id,source,score); paper_references(id,paper_id,position,raw_text,doi,year,title).

INTERFACE:
insert_paper(conn, fields: dict) -> int : fields has title, abstract, abstract_source, doi, arxiv_id, year, venue, file_name, file_path, file_sha256, page_count, uploaded_by. Set created_at and updated_at to now_iso(). Return new id.
set_paper_authors(conn, paper_id: int, names: list[str]) -> None : delete this paper's paper_authors rows; for each non-empty name (dedupe by norm_text) upsert into authors by name_norm, insert link with position starting at 1; then call cleanup_orphans(conn).
replace_topics(conn, paper_id: int, items: list[dict]) -> None : items are {"name","source","score"}; name lowercased+stripped, skip empty and duplicates; delete this paper's paper_topics rows; upsert topics; insert links; then cleanup_orphans(conn).
insert_references(conn, paper_id: int, refs: list[dict]) -> int : refs are {"position","raw_text","doi","year","title"}; insert all; return count.
get_paper(conn, paper_id: int) -> dict | None : returns PaperDetail: id,title,abstract,abstract_source,doi,arxiv_id,year,venue,file_name,page_count,uploaded_by,created_at,updated_at, authors: list[str] ordered by position, topics: list[{"name","source"}] ordered by name, references: list[{"id","position","raw_text","doi","year","title"}] ordered by position. Do NOT return file_path or file_sha256.
list_papers(conn, q=None, author=None, topic=None, year=None, limit=20, offset=0) -> tuple[list[dict], int] : returns (PaperSummary list, total). PaperSummary: id,title,authors:list[str],year,venue,doi,arxiv_id,topics:list[str],created_at. Filters (AND): q -> title LIKE %q%; author -> EXISTS author whose name_norm LIKE %norm_text(author)%; topic -> EXISTS topic whose name = topic.lower(); year -> year = int. Order by created_at DESC, id DESC. total = count with same filters.
update_paper_fields(conn, paper_id: int, fields: dict) -> None : only these keys allowed: title, abstract, year, venue, doi, arxiv_id; ignore others. If "abstract" is in fields also set abstract_source to 'extracted' when abstract is non-empty else 'missing'. Always set updated_at.
find_duplicate(conn, sha256: str, doi: str | None, arxiv_id: str | None) -> dict | None : return {"id","title","reason"} with reason one of "same_file","same_doi","same_arxiv" (check in that order; skip doi/arxiv when None) or None.
delete_paper(conn, paper_id: int) -> dict | None : return {"title","file_path"} of the deleted paper (None if it does not exist); delete the papers row (links cascade); call cleanup_orphans(conn).
cleanup_orphans(conn) -> None : delete authors with no paper_authors rows; delete topics with no paper_topics rows.
list_topics(conn) -> list[dict] : [{"id","name","paper_count"}] ordered by paper_count DESC, name.

STEPS: 1) imports 2) helper to build summaries 3) each function in the order above 4) at the end add an `if __name__ == "__main__":` self-test: call app.db.init_db(), open a connection, inside `with conn:` insert a paper (file_sha256 "selftest"), set authors ["Ada Lovelace","Alan Turing"], topics, one reference; assert get_paper(...)["authors"] == ["Ada Lovelace","Alan Turing"]; then delete_paper; assert get_paper is None; print("SELFTEST OK").
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: python -m app.repo_papers  -> prints SELFTEST OK
```

#### Prompt 3: `app/repo_activity.py`

text

```
ROLE: You are a careful Python 3.11 developer. OBJECTIVE: write the activity-log data access.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/repo_activity.py
IMPORTS ALLOWED: json, and from app.common import now_iso, ACTIONS, AppError.
TABLE: activity_log(id, ts, user_name, action, entity_type, entity_id, paper_title, details_json).
RULES: functions take an open sqlite3 connection `conn` (row_factory=sqlite3.Row) first; NEVER commit; use ? placeholders.

INTERFACE:
log_action(conn, user_name: str, action: str, entity_type: str, entity_id: int | None, paper_title: str | None, details: dict | None = None) -> int : raise AppError("BAD_REQUEST", "Unknown action", 400) if action not in ACTIONS; insert with ts=now_iso() and details_json=json.dumps(details or {}); return new id.
list_activity(conn, limit: int = 50, offset: int = 0, user: str | None = None, paper_id: int | None = None) -> tuple[list[dict], int] : filters (AND): user -> user_name = user (exact); paper_id -> entity_id = paper_id. Order by id DESC. Each entry dict: id, ts, user_name, action, entity_type, entity_id, paper_title, details (json.loads of details_json). Return (entries, total_matching).

STEPS: 1) imports 2) log_action 3) list_activity 4) `if __name__ == "__main__":` self-test using app.db.init_db()/get_conn(): inside `with conn:` log an "upload" entry for user "selftest", entity_id 999999; read it back with list_activity(conn, user="selftest"); assert the first entry's action == "upload"; then delete rows where user_name='selftest'; print("SELFTEST OK").
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: python -m app.repo_activity  -> prints SELFTEST OK
```

#### Prompt 4: `app/pdf_text.py`

text

```
ROLE: You are a careful Python 3.11 developer. OBJECTIVE: extract ordered text from a PDF with PyMuPDF and detect scanned PDFs.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/pdf_text.py
IMPORTS ALLOWED: re, pymupdf (use `import pymupdf`, NOT fitz), and from app.common import AppError, MIN_CHARS_PER_PAGE.

INTERFACE:
extract_pdf(path: str) -> dict with keys:
 "page_count": int (pages in the document),
 "pages": list[str] (ordered text of each processed page; process at most the first 60 pages),
 "first_page_lines": list[dict] each {"text": str, "size": float, "bold": bool, "x0": float, "y0": float, "x1": float, "y1": float},
 "total_chars": int,
 "is_scanned": bool.
Raises AppError("PARSE_FAILED", "<message>", 422) if the file cannot be opened, is password protected (doc.needs_pass), or has 0 pages.

STEPS:
1. Open with pymupdf.open(path) inside try/except Exception -> AppError PARSE_FAILED. Close the doc at the end.
2. For each page: d = page.get_text("dict"); keep only blocks where block["type"] == 0.
3. Order the blocks with helper _order_blocks(blocks, page_width): mid = page_width/2; a block is LEFT if bbox x1 <= mid+10, RIGHT if bbox x0 >= mid-10, else FULL. If there are >=3 LEFT and >=3 RIGHT blocks: result = FULL blocks whose y1 <= the smallest y0 among LEFT+RIGHT blocks (sorted by y0) + LEFT sorted by y0 + RIGHT sorted by y0 + remaining FULL blocks sorted by y0. Otherwise sort all blocks by (y0, x0).
4. A block's lines: for each line, text = "".join(span["text"] for span in line["spans"]).strip(); size = max span size; bold = any(span["flags"] & 16); bbox = line["bbox"]. Skip empty lines.
5. Page text = lines joined by "\n" in block order. Then clean it: replace ligatures (ﬁ->fi, ﬂ->fl, ﬀ->ff, ﬃ->ffi, ﬄ->ffl); remove hyphenation at line ends with re.sub(r"(\w)-\n(\w)", r"\1\2", text).
6. first_page_lines = the line dicts of page 0 in the ordered-block order.
7. total_chars = sum(len(p.strip()) for p in pages); is_scanned = (len(pages) == 0) or (total_chars / len(pages) < MIN_CHARS_PER_PAGE).
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: python -c "from app.pdf_text import extract_pdf; d=extract_pdf('tests/sample.pdf'); print(d['page_count'], d['is_scanned'], d['first_page_lines'][0])"  -> a page count, False, and a dict with text/size/bold/x0/y0/x1/y1. A non-PDF file renamed to .pdf raises AppError PARSE_FAILED.
```

#### Prompt 5: `app/meta_ids.py`

text

```
ROLE: You are a careful Python 3.11 developer. OBJECTIVE: write regex-based extractors for DOI, arXiv ID, year, venue and author keywords.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/meta_ids.py
IMPORTS ALLOWED: re, collections.Counter. Pure functions; no file or network access; never raise on bad input (return None or []).

INTERFACE (all take `text: str`, the text of page 1 unless noted):
extract_doi(text) -> str | None : regex 10\.\d{4,9}/[-._;()/:A-Za-z0-9]+ ; take the first match; strip trailing characters . , ; ) ; return lowercase.
extract_arxiv_id(text) -> str | None : case-insensitive; modern pattern arXiv:\s*(\d{4}\.\d{4,5})(v\d+)? ; legacy pattern arXiv:\s*([a-z\-]+(?:\.[A-Z]{2})?/\d{7})(v\d+)? ; return only the id group (no "arXiv:", no version).
extract_year(text) -> int | None : years are 4-digit numbers 1950-2035 (regex \b(19[5-9]\d|20[0-3]\d)\b). Priority 1: among lines containing (case-insensitive) "arxiv", "copyright", "©", "published", "accepted", "received", return the largest year found in those lines. Priority 2: the most frequent year in the whole text. Else None.
extract_venue(text) -> str | None : look at the first 40 lines; return the first stripped line of length 10-200 matching (case-insensitive) one of: proceedings of, journal of, transactions on, conference on, workshop, accepted at, published in. Else None.
extract_author_keywords(text) -> list[str] : find a line starting (case-insensitive, after whitespace) with "keywords", "key words" or "index terms". Take the rest of that line after an optional ":" or dash, plus up to 2 following non-empty lines; stop early at a blank line or a line starting with a digit/roman numeral heading such as "1 Introduction" or "I. INTRODUCTION". Join, split on "," ";" "·" "•", strip spaces and trailing periods, drop empty items and items longer than 60 chars, return at most 10.

STEPS: 1) imports 2) one function at a time in the order above.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: python -c "from app.meta_ids import *; print(extract_doi('see https://doi.org/10.1145/3768292.3770348.'), extract_arxiv_id('arXiv:2610.28907v1 [cs.MA] 20 Oct 2026'), extract_year('arXiv:2610.28907v1 [cs.MA] 20 Oct 2026'), extract_author_keywords('Keywords: graph, rag; llm.\n\n1 Introduction'))"  -> 10.1145/3768292.3770348 2610.28907 2026 ['graph', 'rag', 'llm']
```

#### Prompt 6: `app/meta_layout.py`

text

```
ROLE: You are a careful Python 3.11 developer. OBJECTIVE: write layout-based extractors for title, authors and abstract.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/meta_layout.py
IMPORTS ALLOWED: re. Pure functions; never raise (return empty values).

INPUT SHAPE: `lines` is a list of dicts {"text": str, "size": float, "bold": bool, "x0": float, "y0": float, "x1": float, "y1": float} in reading order (from page 1).

INTERFACE:
extract_title(lines: list[dict]) -> tuple[str, int] : returns (title, end_index) where end_index is the index of the line AFTER the last title line (0 if no title found).
 Steps: ignore lines that are empty, shorter than 4 chars, or match arXiv stamps (case-insensitive "arxiv:"). Among the first 25 remaining lines find max size. The title is the FIRST run of consecutive lines (consecutive in the original list) whose size >= max_size - 0.5, up to 8 lines. Join with single spaces, collapse whitespace. If shorter than 5 chars return ("", 0).
extract_authors(lines: list[dict], start_index: int) -> list[str] :
 Steps: scan lines from start_index, at most 15 lines; stop at a line whose lowercase text starts with "abstract", "keywords", "key words", "index terms" or matches ^\d+\.?\s+introduction. Skip lines longer than 200 chars, lines containing "@", and lines containing (case-insensitive) any of: university, universit, institute, department, laboratory, school of, college, research, inc., corp, gmbh, centre, center. For each kept line: remove parenthesised text (...), remove digits and the symbols * † ‡ ∗ ¹ ² ³; split on ",", ";", " and ", "&"; strip each piece; keep pieces of 2-5 words where each word starts with an uppercase letter and total length is 3-60 chars. Deduplicate keeping order; return at most 30.
extract_abstract(pages: list[str]) -> tuple[str, str] : returns (abstract, source) with source in "extracted", "fallback_intro", "missing".
 Steps: text = "\n".join(pages[:2]). Find a line starting (case-insensitive, multiline) with "abstract" and take everything after it (also after an optional ":" "." or dash). Cut at the next line that starts (case-insensitive) with keywords, key words, index terms, "1 introduction", "1. introduction", "i. introduction" or "introduction". Limit to 3000 chars; collapse whitespace. If the result has >= 50 chars return (result, "extracted"). Else find a line starting with "introduction" (optionally numbered), take the next 300 chars, collapse whitespace; if >= 50 chars return (that, "fallback_intro"). Else return ("", "missing").

STEPS: 1) imports 2) three functions in the order above.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: python -c "from app.pdf_text import extract_pdf; from app.meta_layout import *; d=extract_pdf('tests/sample.pdf'); t,i=extract_title(d['first_page_lines']); print(t); print(extract_authors(d['first_page_lines'],i)); print(extract_abstract(d['pages'])[1])"  -> the real title, a plausible author list, and "extracted".
```

#### Prompt 7: `app/references.py`

text

```
ROLE: You are a careful Python 3.11 developer. OBJECTIVE: locate and split the reference list of a paper into separate records.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/references.py
IMPORTS ALLOWED: re, and from app.common import MAX_REFERENCES. Pure function; never raise.

INTERFACE:
extract_references(pages: list[str]) -> list[dict] : each dict is {"position": int (1-based), "raw_text": str, "doi": str | None, "year": int | None, "title": None}.

STEPS:
1. full = "\n".join(pages). Find ALL lines that, stripped, equal (case-insensitive) "references", "bibliography", "reference", or "literature cited" (an optional leading number like "7" or "7." is allowed). Use the LAST such line. Text after it is the reference block. If none found return [].
2. Split into entries. Strategy A (numbered): if the block contains at least 3 occurrences of a line-start marker like "[1]" (regex ^\s*\[\d+\]), split before every such marker. Strategy B: if at least 3 line starts like "1." or "2." (regex ^\s*\d{1,3}\.\s), split before each. Strategy C (fallback): split on blank lines.
3. For each entry: join its lines with single spaces, collapse whitespace; drop entries shorter than 20 chars; stop after MAX_REFERENCES entries.
4. doi = first match of 10\.\d{4,9}/[-._;()/:A-Za-z0-9]+ with trailing . , ; ) stripped, lowercased, else None. year = the last 4-digit number between 1950 and 2035 in the entry (regex \b(19[5-9]\d|20[0-3]\d)\b), else None.
5. position = 1-based order of kept entries.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: python -c "from app.references import extract_references as e; r=e(['intro','References\n[1] A. Smith. 2011. A paper title. J. X.\n[2] B. Jones. 2020. Another title. doi 10.1000/abc.123.\n[3] C. Lee. 2019. Third title here. Venue.']); print(len(r), r[1]['doi'], r[0]['year'])"  -> 3 10.1000/abc.123 2011
```

#### Prompt 8: `app/enrich.py`

text

```
ROLE: You are a careful Python 3.11 developer. OBJECTIVE: write best-effort metadata lookups against Crossref and arXiv.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/enrich.py
IMPORTS ALLOWED: re, requests, xml.etree.ElementTree as ET, and from app.common import CROSSREF_URL, ARXIV_URL, CROSSREF_MAILTO, HTTP_TIMEOUT.

INTERFACE:
enrich_metadata(doi: str | None, arxiv_id: str | None) -> dict : returns a dict that may contain these keys (only non-empty values): "title": str, "authors": list[str], "year": int, "venue": str, "abstract": str. It must NEVER raise: wrap everything in try/except Exception and return {} on any failure (offline, timeout, bad JSON, bad XML). Send header User-Agent "PaperLib/1.0".

STEPS:
1. If doi: GET CROSSREF_URL + doi with timeout=HTTP_TIMEOUT (add params {"mailto": CROSSREF_MAILTO} only if CROSSREF_MAILTO is non-empty). If status 200: m = response.json()["message"]. title = m["title"][0]; authors = [f"{a.get('given','')} {a.get('family','')}".strip() for a in m.get("author", [])]; year = m["issued"]["date-parts"][0][0]; venue = m["container-title"][0]; abstract = m.get("abstract","") with XML tags removed via re.sub(r"<[^>]+>", " ", ...) and whitespace collapsed. Return the non-empty values.
2. Else if arxiv_id: GET ARXIV_URL with params {"id_list": arxiv_id}, same timeout. Parse response.text with ET.fromstring; namespace {"a": "http://www.w3.org/2005/Atom"}; entry = root.find("a:entry", ns); title = a:title text (collapse whitespace); abstract = a:summary text (collapse whitespace); authors = [a:name text for each a:author]; year = int(a:published text[:4]). Return the non-empty values.
3. Else return {}.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: python -c "from app.enrich import enrich_metadata as e; print(e('10.1038/s41586-021-03819-2', None)); print(e(None, None))"  -> online: a dict with title/authors/year/venue; offline: {} with NO traceback. Second call prints {}.
```

#### Prompt 9: `app/tagging.py`

text

```
ROLE: You are a careful Python 3.11 developer. OBJECTIVE: assign topic tags to a paper from author keywords, falling back to YAKE.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/tagging.py
IMPORTS ALLOWED: re, yake, and from app.common import MAX_TOPICS. Never raise.

INTERFACE:
assign_topics(keywords: list[str], title: str, abstract: str) -> list[dict] : each dict {"name": str, "source": "author" | "yake", "score": float}. At most MAX_TOPICS items, unique names.

STEPS:
1. Helper _clean(s): lowercase, collapse whitespace, strip spaces and the characters . , ; : ; return "" unless 3 <= len <= 60 and it contains at least one letter.
2. Author keywords: for each keyword in `keywords`, c = _clean(k); if c and not seen: add {"name": c, "source": "author", "score": 1.0}. If at least 1 was added, return the list cut to MAX_TOPICS.
3. Fallback: text = (title + ". " + abstract).strip(). If len(text) < 20 return []. Inside try/except Exception (return [] on error): extractor = yake.KeywordExtractor(lan="en", n=3, top=MAX_TOPICS); for kw, raw in extractor.extract_keywords(text): c = _clean(kw); skip empty/duplicate; score = round(1.0 / (1.0 + raw), 4) (YAKE: lower raw is better); append {"name": c, "source": "yake", "score": score}.
4. Return the list cut to MAX_TOPICS.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: python -c "from app.tagging import assign_topics as a; print(a(['Graph Neural Networks','RAG.'],'t','')); print(a([],'Deep learning for protein folding','We train a deep neural network to predict protein structures from sequences using attention.'))"  -> first call: 2 author items; second: up to 10 yake items.
```

#### Prompt 10: `app/pipeline.py`

text

```
ROLE: You are a careful Python 3.11 developer. OBJECTIVE: write the ingest pipeline that turns a stored PDF into database records.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/pipeline.py
IMPORTS ALLOWED: sqlite3, pathlib.Path, and: from app.common import AppError, ENRICH_ENABLED; from app.pdf_text import extract_pdf; from app.meta_ids import extract_doi, extract_arxiv_id, extract_year, extract_venue, extract_author_keywords; from app.meta_layout import extract_title, extract_authors, extract_abstract; from app.references import extract_references; from app.enrich import enrich_metadata; from app.tagging import assign_topics; from app.repo_papers import insert_paper, set_paper_authors, replace_topics, insert_references, find_duplicate; from app.repo_activity import log_action.

INTERFACE:
ingest_pdf(conn, pdf_path: str, original_name: str, sha256: str, user_name: str) -> int : returns the new paper id. Raises AppError on failure. The caller has already checked the file hash for exact duplicates but you must still handle it.

STEPS:
1. parsed = extract_pdf(pdf_path). If parsed["is_scanned"]: raise AppError("SCANNED_PDF", "This PDF has no extractable text (scanned?). OCR is not supported.", 422).
2. page1 = parsed["pages"][0]; head = page1 + "\n" + (parsed["pages"][1] if len(parsed["pages"]) > 1 else "").
3. doi = extract_doi(page1); arxiv_id = extract_arxiv_id(page1); year = extract_year(page1); venue = extract_venue(page1); keywords = extract_author_keywords(head).
4. title, end = extract_title(parsed["first_page_lines"]); authors = extract_authors(parsed["first_page_lines"], end); abstract, abs_source = extract_abstract(parsed["pages"]).
5. If ENRICH_ENABLED and (doi or arxiv_id): extra = enrich_metadata(doi, arxiv_id). Fill ONLY empty fields: title if empty; authors if empty list; year if None; venue if empty; abstract if empty (then abs_source = "extracted").
6. If title is still empty: title = Path(original_name).stem.
7. dup = find_duplicate(conn, sha256, doi, arxiv_id). If dup: raise AppError("DUPLICATE", f"Already in library as paper {dup['id']}: {dup['title']}", 409).
8. refs = extract_references(parsed["pages"]); topics = assign_topics(keywords, title, abstract).
9. Inside `with conn:` do: paper_id = insert_paper(conn, {title, abstract, abstract_source: abs_source, doi, arxiv_id, year, venue, file_name: original_name, file_path: pdf_path, file_sha256: sha256, page_count: parsed["page_count"], uploaded_by: user_name}); set_paper_authors; replace_topics; insert_references; log_action(conn, user_name, "upload", "paper", paper_id, title, {"file_name": original_name, "page_count": parsed["page_count"], "reference_count": len(refs), "topic_count": len(topics)}).
10. Wrap step 9 in try/except sqlite3.IntegrityError -> raise AppError("DUPLICATE", "This paper is already in the library.", 409). Return paper_id.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: python -c "import hashlib; from app.db import init_db,get_conn; from app.pipeline import ingest_pdf; init_db(); p='tests/sample.pdf'; h=hashlib.sha256(open(p,'rb').read()).hexdigest(); c=get_conn(); print(ingest_pdf(c,p,'sample.pdf',h,'tester'))"  -> prints an integer id. Running it a second time raises AppError DUPLICATE. Then: python -c "from app.db import get_conn; from app.repo_papers import get_paper; p=get_paper(get_conn(),1); print(p['title'], p['authors'], len(p['references']), p['topics'])"
```

#### Prompt 11: `app/graph.py`

text

```
ROLE: You are a careful Python 3.11 developer. OBJECTIVE: compute the knowledge graph from the database on every request (no stored edges).

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/graph.py
IMPORTS ALLOWED: sqlite3, and from app.common import truncate.
TABLES: papers(id,title,doi), authors(id,name), paper_authors(paper_id,author_id), topics(id,name), paper_topics(paper_id,topic_id), paper_references(paper_id,doi).

INTERFACE:
build_graph(conn, min_weight: int = 1, max_papers: int = 300) -> dict : returns {"nodes": [...], "edges": [...]}.
 Node: {"id": "paper:<id>" | "author:<id>" | "topic:<id>", "type": "paper" | "author" | "topic", "label": str}. Paper label = truncate(title, 60).
 Edge: {"from": str, "to": str, "type": str, "weight": int}.

STEPS (each is a separate SQL query; use ? placeholders; no commit):
1. Papers: the newest max_papers papers (ORDER BY id DESC LIMIT ?). Remember their ids as the allowed set; emit paper nodes.
2. AUTHORED: for rows in paper_authors whose paper_id is allowed: emit author node (once per author) and edge from "author:<aid>" to "paper:<pid>", weight 1.
3. HAS_TOPIC: for rows in paper_topics whose paper_id is allowed: emit topic node (once) and edge from "paper:<pid>" to "topic:<tid>", weight 1.
4. CO_AUTHOR: self-join paper_authors a1, a2 on same paper_id with a1.author_id < a2.author_id (allowed papers only); GROUP BY the pair; weight = COUNT(*); keep weight >= min_weight; edge from "author:<a1>" to "author:<a2>".
5. CO_TOPIC: same idea with paper_topics (topic_id < topic_id); keep weight >= min_weight.
6. CITES: join paper_references r to papers p2 on lower(r.doi) = lower(p2.doi) where r.doi IS NOT NULL and r.paper_id != p2.id and both papers are allowed; DISTINCT pairs; edge from "paper:<r.paper_id>" to "paper:<p2.id>", weight 1.
7. Return the dict. An empty database returns {"nodes": [], "edges": []}.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: python -c "from app.db import get_conn; from app.graph import build_graph; g=build_graph(get_conn()); print(len(g['nodes']), len(g['edges']), {n['type'] for n in g['nodes']})"  -> after ingesting 1+ papers: node types include paper, author, topic.
```

#### Prompt 12: `app/api_upload.py`

text

```
ROLE: You are a careful Python 3.11 + Flask developer. OBJECTIVE: write the PDF upload endpoint.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/api_upload.py
IMPORTS ALLOWED: hashlib, os, contextlib.closing, pathlib.Path, flask (Blueprint, request, jsonify), and: from app.common import AppError, UPLOAD_DIR, get_user_name; from app.db import get_conn; from app.pipeline import ingest_pdf; from app.repo_papers import find_duplicate, get_paper.

INTERFACE: bp_upload = Blueprint("upload", __name__); route POST /api/papers.
Success: HTTP 201, JSON {"paper": <PaperDetail from get_paper>}.
Errors are raised as AppError (a global handler turns them into {"error":{"code","message"}}).

STEPS:
1. user = get_user_name() (raises NO_USER).
2. f = request.files.get("file"); if missing or f.filename == "": raise AppError("NO_FILE", "No file was uploaded.", 400).
3. If not f.filename.lower().endswith(".pdf"): raise AppError("NOT_PDF", "Only PDF files are accepted.", 400).
4. data = f.read(); if not data.startswith(b"%PDF-"): raise AppError("NOT_PDF", "Only PDF files are accepted.", 400).
5. sha = hashlib.sha256(data).hexdigest(). With closing(get_conn()) as conn: dup = find_duplicate(conn, sha, None, None); if dup: raise AppError("DUPLICATE", f"Already in library as paper {dup['id']}: {dup['title']}", 409).
6. UPLOAD_DIR.mkdir(parents=True, exist_ok=True); path = UPLOAD_DIR / f"{sha}.pdf"; write data to path.
7. try: pid = ingest_pdf(conn, str(path), f.filename, sha, user) except Exception: delete the file at path (os.remove inside try/except OSError) and re-raise.
8. Return jsonify({"paper": get_paper(conn, pid)}), 201. Always close the connection (use closing()).
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST (after Prompts 13-16 exist): curl -i -F "file=@tests/sample.pdf" -H "X-User-Name: tester" http://127.0.0.1:5000/api/papers -> 201 with JSON paper. Same command again -> 409 DUPLICATE. curl -i -F "file=@README.md" -H "X-User-Name: tester" ... -> 400 NOT_PDF. Without the header -> 400 NO_USER.
```

#### Prompt 13: `app/api_papers.py`

text

```
ROLE: You are a careful Python 3.11 + Flask developer. OBJECTIVE: write list, detail, edit, tag, delete, file and topic-list endpoints.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/api_papers.py
IMPORTS ALLOWED: os, re, sqlite3, contextlib.closing, flask (Blueprint, request, jsonify, send_file), and: from app.common import AppError, get_user_name, truncate; from app.db import get_conn; from app.repo_papers import get_paper, list_papers, update_paper_fields, set_paper_authors, replace_topics, delete_paper, list_topics, find_duplicate; from app.repo_activity import log_action.
INTERFACE: bp_papers = Blueprint("papers", __name__). Use `with closing(get_conn()) as conn:` in every route. Writes happen inside `with conn:`. Errors: raise AppError(code, message, status).

ROUTES:
GET /api/papers : params q, author, topic, year (int or 400 BAD_REQUEST), limit (default 20, clamp 1..100), offset (default 0, >=0). Return {"papers": [...], "total": n} from list_papers.
GET /api/papers/<int:pid> : get_paper or AppError("NOT_FOUND","Paper not found.",404). Return {"paper": ...}.
PATCH /api/papers/<int:pid> : user = get_user_name(). body = request.get_json(silent=True) or {}; allowed keys: title, abstract, year, venue, doi, arxiv_id, authors. Validate: title non-empty str <= 500 chars; year int 1500..2100 or null; doi null or lowercase-able string matching 10\.\d{4,9}/\S+ (store lowercase; empty string -> None); arxiv_id str or null; authors list of str (max 100). If no allowed key present: 400 BAD_REQUEST. Load old = get_paper (404 if none). Build changed = {field: [truncate(str(old), 200), truncate(str(new), 200)]} only for fields whose value differs (authors compared as lists). If nothing changed, return the paper without logging. Else inside `with conn:` call update_paper_fields for the scalar fields, set_paper_authors if authors changed, and log_action(conn, user, "edit", "paper", pid, new title, {"changed": changed}). Catch sqlite3.IntegrityError -> AppError("DUPLICATE","Another paper already has this DOI or arXiv ID.",409). Return {"paper": get_paper(...)}.
PUT /api/papers/<int:pid>/topics : user = get_user_name(); body {"topics": [str,...]} (list required, max 30, else 400 BAD_REQUEST). Names lowercased/stripped, empties and duplicates removed. Existing topics keep their stored source; new names get source "manual", score 1.0. added/removed = differences versus the old names. If no difference, return the paper without logging. Else in `with conn:` call replace_topics and log_action(conn, user, "tag_change", "paper", pid, title, {"added": [...], "removed": [...]}). Return {"paper": ...}.
DELETE /api/papers/<int:pid> : user = get_user_name(). In `with conn:` info = delete_paper(conn, pid) (None -> 404) and log_action(conn, user, "delete", "paper", pid, info["title"], {}). AFTER the transaction remove the file at info["file_path"] with os.remove inside try/except OSError. Return {"deleted": true, "id": pid}.
GET /api/papers/<int:pid>/file : look up file_path with SELECT file_path, file_name FROM papers WHERE id=?; 404 if none or file missing; return send_file(path, mimetype="application/pdf", download_name=file_name).
GET /api/topics : return {"topics": list_topics(conn)}.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST (server running): curl -X PATCH -H "X-User-Name: tester" -H "Content-Type: application/json" -d '{"year":2025}' http://127.0.0.1:5000/api/papers/1 -> JSON with year 2025; curl -X PUT ... -d '{"topics":["a","b"]}' .../api/papers/1/topics -> topics a,b; curl -X DELETE -H "X-User-Name: tester" .../api/papers/1 -> {"deleted":true,"id":1}; GET .../api/papers/1 -> 404 NOT_FOUND.
```

#### Prompt 14: `app/api_misc.py`

text

```
ROLE: You are a careful Python 3.11 + Flask developer. OBJECTIVE: write the graph and activity endpoints.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/api_misc.py
IMPORTS ALLOWED: contextlib.closing, flask (Blueprint, request, jsonify), and: from app.common import AppError; from app.db import get_conn; from app.graph import build_graph; from app.repo_activity import list_activity.
INTERFACE: bp_misc = Blueprint("misc", __name__). Use `with closing(get_conn()) as conn:`.

ROUTES:
GET /api/graph : min_weight from query (default 1; non-integer or < 1 -> AppError("BAD_REQUEST","min_weight must be a positive integer.",400)). Return jsonify(build_graph(conn, min_weight)).
GET /api/activity : limit (default 50, clamp 1..200), offset (default 0, >=0), optional user (string), optional paper_id (int, else 400 BAD_REQUEST). Return {"entries": [...], "total": n} from list_activity.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST (server running): curl http://127.0.0.1:5000/api/graph -> {"nodes":[...],"edges":[...]}; curl "http://127.0.0.1:5000/api/activity?limit=5" -> {"entries":[...],"total":N}; curl "http://127.0.0.1:5000/api/graph?min_weight=abc" -> 400 BAD_REQUEST.
```

#### Prompt 15: `app/_`_`init`_`_.py`

text

```
ROLE: You are a careful Python 3.11 + Flask developer. OBJECTIVE: write the Flask application factory.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: app/__init__.py
IMPORTS ALLOWED: flask (Flask, jsonify, send_from_directory), werkzeug.exceptions.HTTPException, logging, and: from app.common import AppError, MAX_UPLOAD_BYTES; from app.db import init_db; from app.api_upload import bp_upload; from app.api_papers import bp_papers; from app.api_misc import bp_misc.

INTERFACE: create_app() -> Flask.

STEPS:
1. app = Flask(__name__, static_folder="static", static_url_path="/static"); app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES.
2. Call init_db().
3. Register bp_upload, bp_papers, bp_misc.
4. Route GET "/" -> send_from_directory(app.static_folder, "index.html").
5. Error handlers, all returning jsonify({"error": {"code": ..., "message": ...}}) with the status:
 - AppError -> (e.code, e.message, e.status)
 - HTTPException: 404 -> NOT_FOUND; 405 -> BAD_REQUEST "Method not allowed"; 413 -> TOO_LARGE "File is too large (max 25 MB)."; other -> BAD_REQUEST with e.description.
 - Exception -> log with logging.exception, return 500 SERVER_ERROR "Unexpected server error."
6. Return app.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: python -c "from app import create_app; a=create_app(); c=a.test_client(); print(c.get('/api/graph').status_code, c.get('/api/papers/999').get_json())"  -> 200 and {'error': {'code': 'NOT_FOUND', 'message': 'Paper not found.'}}
```

#### Prompt 16: `run.py`

text

```
ROLE: You are a careful Python 3.11 developer. OBJECTIVE: write the tiny launcher script.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Import only the modules named below.

FILE: run.py (project root)
IMPORTS ALLOWED: from app import create_app.
STEPS: 1) app = create_app() 2) under `if __name__ == "__main__":` call app.run(host="127.0.0.1", port=5000, debug=False) and print "PaperLib running at http://127.0.0.1:5000" first.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: pip install -r requirements.txt && python run.py ; then open http://127.0.0.1:5000/api/graph in a browser -> JSON.
```

#### Prompt 17: `app/static/index.html`

text

```
ROLE: You are a careful front-end developer. OBJECTIVE: write the single HTML shell page for a vanilla-JS app.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Do not add any other libraries.

FILE: app/static/index.html
REQUIRED HEAD TAGS (copy exactly, in this order): <meta charset="utf-8">; <meta name="viewport" content="width=device-width, initial-scale=1">; <title>PaperLib</title>;
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2.1.1/out/water.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/vis-network@10.1.2/styles/vis-network.min.css">
<script src="https://cdn.jsdelivr.net/npm/vis-network@10.1.2/standalone/umd/vis-network.min.js"></script>
Then one <style> block with: body max-width 1100px; .chip (inline-block, small padding, border-radius 1em, background #8884, margin-right 0.3em); #toast (fixed, bottom 1em, right 1em, display none, padding 0.6em 1em, border-radius 6px, background #333, color #fff) with #toast.error {background:#b00020}; #graph-box {height: 70vh; border: 1px solid #8886}; nav a {margin-right: 1em}; nav a.active {font-weight: bold}.
BODY (exact structure): <header><h1>PaperLib</h1><nav><a id="nav-library" href="#/library">Library</a><a id="nav-graph" href="#/graph">Graph</a><a id="nav-activity" href="#/activity">Activity</a></nav><label>Your name <input id="user-name" maxlength="80" placeholder="required to upload/edit"></label></header><main id="view"></main><div id="toast" role="status"></div>
Then these scripts at the END of body, in this exact order: /static/js/api.js, /static/js/library.js, /static/js/paper.js, /static/js/graph.js, /static/js/activity.js, /static/js/app.js (each as <script src="..."></script>).
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: open http://127.0.0.1:5000/ -> page shows the header, nav and name box (JS errors about missing files are expected until Prompts 18-23 are done).
```

#### Prompt 18: `app/static/js/api.js`

text

```
ROLE: You are a careful JavaScript developer. OBJECTIVE: write a fetch wrapper object named Api.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. This is a classic script (no import/export); define a global `const Api = {...}`.

FILE: app/static/js/api.js
INTERFACE (every method returns a Promise of the parsed JSON object; on a non-2xx response it throws an Error whose .message is the server's error.message, .code is error.code and .status is the HTTP status; on network failure it throws Error("Cannot reach the server.")):
Api.listPapers(params)  // params {q,author,topic,year,limit,offset}; omit empty values; GET /api/papers?...
Api.getPaper(id)        // GET /api/papers/<id>
Api.uploadPaper(file)   // POST /api/papers, FormData with field "file"; do NOT set Content-Type
Api.updatePaper(id, patch) // PATCH, JSON body
Api.setTopics(id, names)   // PUT /api/papers/<id>/topics, body {"topics": names}
Api.deletePaper(id)     // DELETE
Api.listTopics()        // GET /api/topics
Api.getGraph(minWeight = 1) // GET /api/graph?min_weight=
Api.listActivity(params)    // params {limit,offset,user,paper_id}
Api.fileUrl(id)         // returns the string "/api/papers/<id>/file" (no fetch)
SHARED: a private helper request(method, url, body, isForm) adds header "X-User-Name" with localStorage.getItem("paperlib_user") || "" (wrap localStorage in try/catch); for JSON bodies sets Content-Type application/json and JSON.stringify.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: in the browser console on http://127.0.0.1:5000/ run: await Api.listPapers({}) -> {papers: [...], total: N}; await Api.getPaper(99999) -> throws Error with code "NOT_FOUND".
```

#### Prompt 19: `app/static/js/app.js`

text

```
ROLE: You are a careful JavaScript developer. OBJECTIVE: write shared UI helpers (object App) and the hash router.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Classic script (no import/export); define a global `const App = {...}`. NEVER use innerHTML with data; use textContent.

FILE: app/static/js/app.js (loaded LAST; other globals already exist: Api, Library, PaperView, GraphView, ActivityView)
INTERFACE:
App.getUser() -> string : localStorage "paperlib_user" or "" (try/catch).
App.setUser(name) : store trimmed name (try/catch).
App.requireUser() -> string : returns the name, or if empty calls App.toast("Enter your name in the header first.", true), focuses #user-name and returns "".
App.toast(message, isError = false) : show #toast with the text (class "error" if isError) for 3.5 seconds.
App.el(tag, props = {}, ...children) -> HTMLElement : create element; props: "class" -> className, "text" -> textContent, "href"/"type"/"value"/"placeholder"/"title"/"colSpan"/"target"/"rel"/"accept"/"rows" assigned as properties, keys starting with "on" (e.g. onclick) assigned as handlers; children are strings (appended as text nodes) or Nodes; skip null/undefined children.
App.clear(node) : remove all children.
ROUTER: function route() reads location.hash (default "#/library"); first call GraphView.destroy() if it exists; clear #view; then: "#/library" -> Library.render(view); "#/paper/<id>" -> PaperView.render(view, Number(id)); "#/graph" -> GraphView.render(view); "#/activity" -> ActivityView.render(view); anything else -> go to "#/library". Wrap the render call in try/catch (and handle a returned promise with .catch) -> App.toast(err.message, true). Set class "active" on the matching nav link (ids nav-library, nav-graph, nav-activity; a paper route highlights nav-library).
STARTUP: on DOMContentLoaded: fill #user-name from App.getUser(); on its "change" event call App.setUser(value); add window "hashchange" listener = route; call route().
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: reload http://127.0.0.1:5000/ -> URL becomes/stays #/library with no console errors once all views exist; type a name in the header, reload -> the name is still there.
```

#### Prompt 20: `app/static/js/library.js`

text

```
ROLE: You are a careful JavaScript developer. OBJECTIVE: write the library view (upload, filters, paper table).

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Classic script; define a global `const Library = {...}`. NEVER use innerHTML with data; build DOM with App.el(tag, props, ...children) and textContent.

FILE: app/static/js/library.js
AVAILABLE GLOBALS: Api.listPapers({q,author,topic,year,limit,offset}) -> {papers,total}; Api.uploadPaper(file); Api.listTopics() -> {topics:[{id,name,paper_count}]}; App.el, App.clear, App.toast(msg,isError), App.requireUser() (returns "" if no name).
A paper in the list: {id,title,authors:[str],year,venue,doi,arxiv_id,topics:[str],created_at}.
INTERFACE: Library.render(container) -> Promise.
LAYOUT (top to bottom): 1) h2 "Library". 2) Upload row: <input type=file accept=".pdf"> + button "Upload PDF". On click: if !App.requireUser() return; require a chosen file; disable the button; await Api.uploadPaper(file); on success App.toast("Uploaded: "+title) and reload the list; on error App.toast(err.message, true); always re-enable the button. 3) Filter row: text inputs for title (q), author, year; a <select> of topics (first option "All topics", value ""), filled from Api.listTopics(); a "Search" button; Enter in any input also searches. 4) Summary text "N papers". 5) Table with header Title | Authors | Year | Topics | Added; title cell is a link href="#/paper/<id>"; authors joined with ", "; topics as <span class="chip">; Added = created_at.slice(0,10). If no papers: show a paragraph "No papers yet. Upload a PDF to begin." 6) Pager: buttons "Previous"/"Next" with 20 per page, disabled at the ends.
STEPS: keep state {q,author,topic,year,offset} in a local object; a function load() calls Api.listPapers and redraws only the table, summary and pager.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: browser at #/library: uploading tests/sample.pdf with a name set shows a toast and a new row; uploading it again shows a red toast "Already in library..."; uploading a .txt renamed .pdf shows a red toast; filtering by a title word narrows the table.
```

#### Prompt 21: `app/static/js/paper.js`

text

```
ROLE: You are a careful JavaScript developer. OBJECTIVE: write the paper detail view with editing, tags and delete.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Classic script; define a global `const PaperView = {...}`. NEVER use innerHTML with data; build DOM with App.el and textContent.

FILE: app/static/js/paper.js
AVAILABLE GLOBALS: Api.getPaper(id) -> {paper}; Api.updatePaper(id, patch) -> {paper}; Api.setTopics(id, names) -> {paper}; Api.deletePaper(id); Api.fileUrl(id); App.el, App.clear, App.toast(msg,isError), App.requireUser().
PaperDetail shape: {id,title,abstract,abstract_source,doi,arxiv_id,year,venue,file_name,page_count,uploaded_by,created_at,updated_at, authors:[str], topics:[{name,source}], references:[{id,position,raw_text,doi,year,title}]}.
INTERFACE: PaperView.render(container, id) -> Promise. Keep the current paper in a local variable; a function draw() clears the container and rebuilds everything from it.
LAYOUT: 1) link "← Back to library" (href "#/library"). 2) h2 title. 3) Metadata list: Authors (joined ", "), Year, Venue, DOI (link https://doi.org/<doi>, target _blank, rel noopener), arXiv ID, Pages, Uploaded by + date, link "Open PDF" (href Api.fileUrl(id), target _blank). 4) h3 Abstract + paragraph; if abstract_source != "extracted" add a small note: "Abstract source: <value>". 5) Button "Edit": swaps the metadata/abstract for a form with inputs: title, authors (textarea, one name per line), year (number), venue, doi, arxiv_id, abstract (textarea rows 8), plus "Save" and "Cancel". Save: if !App.requireUser() return; build a patch (year "" -> null; authors split on newlines, trimmed, empties removed); await Api.updatePaper; on success replace the local paper, App.toast("Saved"), draw(); on error App.toast(err.message, true). 6) h3 Tags: each topic as <span class="chip"> showing the name, a small "×" button that calls Api.setTopics(id, names without that one), and an input + "Add tag" button that calls Api.setTopics(id, [...current names, new name]). Require the user name for both. 7) h3 "References (N)": an <ol> with raw_text per item; if the reference has a doi append a link "DOI" to https://doi.org/<doi>. 8) Button "Delete paper": if !App.requireUser() return; confirm("Delete this paper?"); await Api.deletePaper(id); set location.hash = "#/library".
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: open #/paper/1: metadata and references show; Edit -> change year -> Save -> value updates; add tag "test" -> chip appears; remove it; Delete -> returns to library and the row is gone.
```

#### Prompt 22: `app/static/js/graph.js`

text

```
ROLE: You are a careful JavaScript developer. OBJECTIVE: write the interactive knowledge-graph view using vis-network.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link> (vis-network is already loaded by index.html: global `vis`). App runs via: pip install -r requirements.txt && python run.py. Classic script; define a global `const GraphView = {...}`. NEVER use innerHTML with data.

FILE: app/static/js/graph.js
AVAILABLE GLOBALS: Api.getGraph(minWeight) -> {nodes,edges}; App.el, App.clear, App.toast; vis.Network, vis.DataSet.
API shape: node {id:"paper:3"|"author:7"|"topic:2", type:"paper"|"author"|"topic", label}; edge {from,to,type:"AUTHORED"|"HAS_TOPIC"|"CO_AUTHOR"|"CO_TOPIC"|"CITES", weight:int}.
INTERFACE: GraphView.render(container) -> Promise; GraphView.destroy() -> destroys the vis network if one exists (call network.destroy(), set to null).
STEPS:
1. Build UI: h2 "Knowledge graph"; a legend line (Paper = blue box, Author = orange dot, Topic = green diamond); checkboxes (all checked by default) for edge types AUTHORED, HAS_TOPIC, CO_AUTHOR, CO_TOPIC, CITES; a "Refresh" button; a div with id "graph-box".
2. Fetch data = await Api.getGraph(1). If data.nodes is empty: put the paragraph "The graph is empty. Upload papers first." in graph-box and return.
3. Map nodes: {id, label, group: type, shape: box|dot|diamond for paper|author|topic, color: "#4f8cff" | "#f5a623" | "#50c878"}.
4. Map edges: {from, to, width: Math.min(1 + weight, 6), label: weight > 1 ? String(weight) : undefined, arrows: "to" for AUTHORED/HAS_TOPIC/CITES else "", dashes: true for CO_AUTHOR/CO_TOPIC}. Only include edges whose type checkbox is checked. A function draw() rebuilds the DataSets from the stored data and the checkboxes.
5. Create `new vis.Network(box, {nodes: new vis.DataSet(...), edges: new vis.DataSet(...)}, {physics: {stabilization: {iterations: 150}}, interaction: {hover: true}})`.
6. network.on("click", params): if params.nodes.length and the id starts with "paper:", set location.hash = "#/paper/" + id.slice(6).
7. Checkbox change -> draw(); Refresh -> refetch and draw(). Destroy any previous network before creating a new one.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: open #/graph after uploading 2+ papers: boxes, dots and diamonds appear connected; unticking CO_AUTHOR removes the dashed lines; clicking a paper box opens its detail page; deleting a paper and reopening the graph shows it gone.
```

#### Prompt 23: `app/static/js/activity.js`

text

```
ROLE: You are a careful JavaScript developer. OBJECTIVE: write the activity history view.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. External libs only via CDN <script>/<link>. App runs via: pip install -r requirements.txt && python run.py. Classic script; define a global `const ActivityView = {...}`. NEVER use innerHTML with data; build DOM with App.el.

FILE: app/static/js/activity.js
AVAILABLE GLOBALS: Api.listActivity({limit,offset,user,paper_id}) -> {entries,total}; App.el, App.clear, App.toast.
Entry shape: {id, ts, user_name, action: "upload"|"edit"|"tag_change"|"delete", entity_id, paper_title, details: object}.
INTERFACE: ActivityView.render(container) -> Promise.
LAYOUT: h2 "Activity"; a filter row with a text input "User" and a "Filter" button; a table with columns When | User | Action | Paper | Details; a pager (50 per page, Previous/Next buttons disabled at the ends); "N entries" summary; if none: paragraph "No activity yet.".
RULES: When = new Date(ts).toLocaleString(). Paper cell: if action is not "delete" and entity_id is set, a link to "#/paper/<entity_id>" with paper_title as text; for "delete" plain text paper_title. Details cell text: for edit -> "Changed: " + the keys of details.changed joined ", "; for tag_change -> "Added: a, b | Removed: c" (omit an empty side); for upload -> details.file_name + " (" + details.reference_count + " references, " + details.topic_count + " tags)"; for delete -> "". Action cell shows the action word in a <span class="chip">.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: open #/activity after upload, edit, tag change and delete -> four rows with your name, correct action words, and the deleted paper's title still visible.
```

#### Prompt 24: `README.md`

text

```
ROLE: You are a technical writer. OBJECTIVE: write a short README for a Python + SQLite + vanilla JS web app.

HARD CONSTRAINTS: Python 3.11 backend; SQLite (stdlib sqlite3); vanilla HTML5/CSS3/ES6+ JS frontend only. No Node.js/Bun/Deno/npm/yarn/package.json/node_modules. No React/Vue/Angular/JSX/TypeScript/Vite/Webpack/Babel. No build step. Do NOT mention Node, npm, or any build tool anywhere in the file.

FILE: README.md (project root)
CONTENT (use exactly these sections): 
# PaperLib - one sentence description (personal research-paper library with a knowledge graph).
## Requirements - Python 3.11; internet only for optional metadata lookups and for the CDN libraries (Water.css, vis-network).
## Run - a code block with exactly: python -m venv .venv  /  source .venv/bin/activate  (Windows: .venv\Scripts\activate)  /  pip install -r requirements.txt && python run.py  ; then "Open http://127.0.0.1:5000".
## Using the app - 5 short bullets: enter your name in the header; upload a PDF; browse/search the library; open a paper to correct metadata and tags; Graph and Activity pages.
## Limits - 4 bullets: scanned PDFs (no text layer) are rejected, OCR is not supported; metadata extraction is heuristic, so correct it manually on the paper page; duplicates are detected by file hash, DOI and arXiv ID; uploads are limited to 25 MB.
## Licence note - PyMuPDF is AGPL-3.0 (or commercial); keep that in mind before distributing the app.
OUTPUT: Only the complete file in a single code block, no explanation.
ACCEPTANCE TEST: follow the Run section literally on a clean machine/virtualenv -> the app starts and the page loads.
```

### I. Build log

&#32;

| Prompt # | Attempts | Result | What I changed in the prompt |
| --- | --- | --- | --- |
| 0 |  |  |  |
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |
| 6 |  |  |  |
| 7 |  |  |  |
| 8 |  |  |  |
| 9 |  |  |  |
| 10 |  |  |  |
| 11 |  |  |  |
| 12 |  |  |  |
| 13 |  |  |  |
| 14 |  |  |  |
| 15 |  |  |  |
| 16 |  |  |  |
| 17 |  |  |  |
| 18 |  |  |  |
| 19 |  |  |  |
| 20 |  |  |  |
| 21 |  |  |  |
| 22 |  |  |  |
| 23 |  |  |  |
| 24 |  |  |  |

### J. Manual edit log

| File | What was changed | Why |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |