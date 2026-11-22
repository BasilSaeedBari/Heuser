# Deliverable 2: System Architecture Plan & Prompt Chain Sequence
**User ID:** 2028010416  
**System Domain:** Research Paper Library & Knowledge Graph System  

---

## Section A: System Overview & Architecture

The system provides an intelligent academic document processing engine that parses PDF research papers, enriches paper metadata using external scholarly APIs (Semantic Scholar / OpenAlex / Crossref), automatically tags topics, and constructs an interactive Knowledge Graph visualization.

### Data Flow Pipeline
1. **PDF Ingestion / Text Input**: User drops a research paper PDF or inputs an arXiv ID / DOI / query string.
2. **Spatial Layout Engine**: `PyMuPDF` parses spatial text bounding boxes, resolving multi-column layout order and isolating title, abstract, authors, and citation markers.
3. **Metadata Identifier Resolution**: In-text regular expressions resolve identifiers (DOI, arXiv ID) and query Semantic Scholar/OpenAlex for enriched metadata.
4. **Keyword & Topic Engine**: TF-IDF and API concept mappings assign standardized domain tags to paper records.
5. **Knowledge Graph Processing**: Ingested nodes (`Paper`, `Author`, `Topic`) and relationships (`AUTHORED`, `HAS_TOPIC`, `CITES`, `CO_AUTHORED_WITH`) are stored in an in-memory graph structure.
6. **Web Dashboard & Visualizer**: Single-page application renders paper search, interactive library tables, and force-directed graph visualizations.

---

## Section B: Tech Stack Selection

* **Frontend**: HTML5, Tailwind CSS (via CDN), Lucide Icons, Vis.js / D3.js Network Graph library.
* **Backend**: Python 3.10+ with FastAPI / Flask, `PyMuPDF` (`fitz`), `requests`, `scikit-learn` (TF-IDF keyword extraction).
* **Graph Engine**: NetworkX / PyVis in-memory data model exported to JSON graph formats.
* **Database / Storage**: In-Memory SQLite / Dict Store for local paper library metadata.

---

## Section C: Core Prompts & Acceptance Tests

### Prompt 1: PDF Layout Parsing & Identifier Extraction Engine
**Prompt Text**:
> "Write a robust Python module using PyMuPDF (`fitz`) that accepts a research paper PDF file and returns a structured dictionary containing extracted paper title, authors, abstract, detected DOIs, and arXiv IDs. Ensure spatial layout detection sorts double-column text correctly, strips headers/footers based on vertical margins, and uses regex patterns for identifier detection."

**Acceptance Test 1**:
* *Input*: Standard 2-column arXiv PDF file (e.g., Attention Is All You Need `1706.03762.pdf`).
* *Expected Output*: Extracted JSON dictionary containing valid string entries for `title`, `abstract`, `arxiv_id` equal to `1706.03762`, and non-interleaved body paragraph strings.

---

### Prompt 2: Metadata API Enrichment & Fallback Client
**Prompt Text**:
> "Create an API client module in Python that takes an arXiv ID, DOI, or title search query and queries the Semantic Scholar and Crossref REST APIs. The module should normalize responses into a uniform schema (title, authors, year, venue, abstract, citationCount, externalIds), include a 3-second timeout with exponential backoff retries, and fall back gracefully if external APIs are unavailable."

**Acceptance Test 2**:
* *Input*: ID string `10.48550/arXiv.1706.03762`.
* *Expected Output*: Populated metadata dictionary with `year: 2017`, `venue: NeurIPS` (or similar recognized venue), and list of co-authors containing `Ashish Vaswani`.

---

### Prompt 3: Knowledge Graph Data Model & Edge Materializer
**Prompt Text**:
> "Build a Python Network Graph manager using NetworkX that maintains paper node relationships. Nodes must support types 'Paper', 'Author', and 'Topic'. Relationships must include 'AUTHORED', 'HAS_TOPIC', and 'CITES'. Automatically materialize 'CO_AUTHORED_WITH' edges between authors who share at least one paper. Provide a helper to export the entire graph to a D3/Vis.js compatible `{ nodes: [...], edges: [...] }` JSON structure."

**Acceptance Test 3**:
* *Input*: Add paper $P_1$ with authors $A_1, A_2$ and topics $T_1$.
* *Expected Output*: Calling `export_graph_json()` yields nodes for $P_1$, $A_1$, $A_2$, $T_1$ and an explicit undirected edge between $A_1$ and $A_2$ labeled `CO_AUTHORED_WITH`.

---

### Prompt 4: Interactive Web Application Dashboard
**Prompt Text**:
> "Generate a single-file interactive HTML/JS application utilizing Tailwind CSS that combines a Paper Search/Upload tab, a Structured Library Table with filtering/sorting, and an interactive Force-Directed Knowledge Graph visualizer powered by Vis.js. Include controls for filtering graph nodes by node type (Paper, Author, Topic) and live search filters."

**Acceptance Test 4**:
* *Input*: Load single-file web dashboard in browser and click 'Add Sample Data'.
* *Expected Output*: Interactive table populates with paper records, and graph canvas renders connected network nodes with interactive drag and zoom functionality.

---

## Section D: Build Log & Execution History

1. **Step 1: Environment Setup**: Configured Python environment with `fitz`, `networkx`, `requests`, and `scikit-learn`.
2. **Step 2: PDF Parsing Validation**: Validated spatial reading on multi-column test papers. Adjusted header boundary thresholds ($y_0 < 50\text{pt}$ and $y_1 > 740\text{pt}$ filtered out).
3. **Step 3: API Integration**: Integrated Semantic Scholar API endpoints. Handled rate limiting with exponential delay retries.
4. **Step 4: Unified Single-File Application**: Merged backend API parsing logic and responsive web frontend into a fully functional interactive web app.