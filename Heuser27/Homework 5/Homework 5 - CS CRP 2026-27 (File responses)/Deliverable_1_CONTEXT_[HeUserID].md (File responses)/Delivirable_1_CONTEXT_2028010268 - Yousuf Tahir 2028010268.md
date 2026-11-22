# Deliverable 1: Academic Research Paper & PDF Extraction Pipeline Context Pack

## 1. What I Discarded and Why

To ensure maximum information density within the 1,500–3,500 word constraint, specific categories of redundant or non-essential content were pruned:

* **Decorative Layout Elements & Promotional Boilerplates:** Removed visual callout styling, institutional blurb text, subscription links, and social media footers from briefing papers to focus strictly on structural text streams.
* **Full Programmatic Scripts:** Omitted boilerplate code snippets for PDF extraction, API wrappers, and DOM rendering. Replaced them with exact data schemas, regex patterns, and architectural trade-off comparisons to optimize LLM instruction context.
* **Historical Development & Broad Theory:** Excluded the historical evolution of PostScript, broad theoretical proofs of human agency, and non-actionable background history. Retained only functional mechanics of PDF layout streams, metadata protocols, and parsing heuristics.
* **Non-Essential API Methods:** Omitted secondary API endpoints (e.g., user profiles, search autocompletions) to focus exclusively on identifier lookup endpoints, field mapping schemas, and rate-limit constraints.

---

## 2. Structural Anatomy of Academic Papers & Observed Real-World Patterns

### Canonical Section Sequence

```
[Title Block] ➔ [Authors & Affiliations] ➔ [Abstract / Key Points] ➔ [Keywords]
       │
       ▼
[Introduction / Problem] ➔ [Methods / Action Research] ➔ [Results / Findings]
       │
       ▼
[Discussion / Recommendations] ➔ [Conclusion] ➔ [Acknowledgements / Funders] ➔ [Notes / References]
```

1. **Title Block:** Concise statement of research scope and focus.
2. **Authors and Affiliations:** Names, academic degrees, institutional addresses, ORCID IDs, and primary contact details.
3. **Abstract / In Brief Summary:** A 150–300 word self-contained summary detailing problem statement, methodology, primary results, and key recommendations.
4. **Keywords:** 4–6 standardized terms for library and database indexing.
5. **Introduction:** Problem context, research gap, hypothesis, and core contributions.
6. **Related Work / Literature Review:** Contextualization of research within existing literature.
7. **Methodology / Methods:** Experimental design, algorithms, field study protocols, and data collection methods.
8. **Results / Key Findings:** Empirical findings, metric evaluations, tables, and analytical figures.
9. **Discussion / Policy Recommendations:** Critical evaluation of findings, practical applications, and limitations.
10. **Conclusion & Future Work:** Summary of contributions and open research directions.
11. **Acknowledgements & Funding:** Disclosures of granting agencies, grant numbers, and institutional support.
12. **References / Notes:** Bibliographic inventory of all cited literature.

### Real-World Evidence & Observed Structural Patterns

Analysis of real research briefing documents (`22761iied.pdf` and `22665iied.pdf`) reveals specific recurring structural patterns that parser heuristics must account for:

#### Title & Metadata Block Patterns
* **Multi-Column Sidebar Placement:** Titles frequently share horizontal space with institutional logos, sidebar summaries ("In brief", "Key findings"), and metadata blocks rather than occupying a full-width header block.
* **Exemplar Title:** `Promoting youth participation in urban governance in Nepal`
* **Exemplar Metadata:** Keywords explicitly tagged (`Keywords: Nature finance, climate change economics, natural resource investment...`) or embedded as document properties (`ISBN: 978-1-83759-222-7`).

#### Abstract & Executive Summary Patterns
* Appears as an italicized lead-in paragraph or a dedicated "In brief" section directly beneath the main title.
* **Exemplar Abstract Stream:**  
  > *"Inclusive urban governance fosters youth participation, yet a gap persists between policy commitments and everyday realities in Dharan, Nepal. Despite inclusive constitutional and policy frameworks, young people face multiple barriers to participation, including unemployment, economic insecurity, migration pressure and exclusion from adult-dominated decision-making spaces..."*

#### Reference & Notes Section Patterns
* **Heading Variant:** Frequently titled `Notes` rather than `References` or `Bibliography`.
* **Numbering Schema:** Arabic numerals followed directly by author names without enclosing square brackets or parentheses (`1 UNDP (2023)...`).
* **Exemplar Reference List Stream:**  
  > **Notes**  
  > 1 National Statistics Office (2025) Urbanization and Development in Nepal. National Planning and Housing Census 2021. Kathmandu.  
  > 2 Pandey, CL (2023) Capturing the Role of Civil Society for Urban Sustainability in Nepal, International Journal of Politics, Culture and Society, 36(3), pp.349-365.

### Publication Venue Comparison

| Feature | Conference Papers | Journal Papers | arXiv Preprints |
| :--- | :--- | :--- | :--- |
| **Length** | 4–10 pages (strict limit) | 10–30+ pages | Unrestricted |
| **Review Process** | Peer-reviewed (fixed deadlines) | Multi-round rigorous peer review | None (Light moderation/sanity check) |
| **Publication Speed** | Fixed conference timeline | 6–18 months | Immediate (24–48 hours) |
| **Archival Status** | Proceedings (IEEE, ACM, Springer) | Volume/Issue bound | Non-archival prior to formal acceptance |
| **Versioning** | Final camera-ready only | Revisions handled internally | Public version history (`v1`, `v2`, etc.) |

---

## 3. The PDF Format & Extraction Mechanics

### Underlying Storage Architecture
PDF is a layout description language based on PostScript. Rather than storing structured text (paragraphs, headings), a PDF content stream contains absolute positional drawing commands on a 2D Cartesian plane:

```postscript
BT
  /F1 12 Tf
  72 712 Td
  (Hello World) Tj
ET
```

Text characters are stored as visual glyphs positioned using absolute coordinates (`x`, `y`), font dictionaries, and scaling matrices.

### Common Parsing Failure Modes
* **Two-Column / Multi-Column Layouts:** Naive horizontal scrapers read stream bytes across the entire page width, interleaving left and right column text into incoherent sentences.
* **Headers, Footers, and Marginalia:** Repeating headers, running titles, and sidebars interrupt continuous body paragraphs across page boundaries.
* **Footnotes & Callouts:** Positioned at page bottoms or in floating side boxes, causing abrupt injection into main narrative streams.
* **Mathematical Equations:** Multi-line formulas, fractions, and symbols use disparate layout bounding boxes and custom font maps that collapse into broken string fragments.
* **Ligatures:** Combined glyphs (e.g., `fi` $\rightarrow$ `ﬁ`, `fl` $\rightarrow$ `ﬂ`) lack standard ASCII representation unless correctly mapped via explicit `/ToUnicode` mapping tables.
* **Hyphenation:** Words split across line ends (`com-` / `putation`) require coordinate-aware string reconstruction.

### Document Type Distinction
* **Text PDF:** Contains vector text layout streams, readable font dictionaries, and `/ToUnicode` mapping tables.
* **Scanned PDF:** Pure raster bitmap images encapsulated inside a PDF container; contains zero text streams and requires Optical Character Recognition (OCR) to recover readable text.

---

## 4. Citation and Reference Styles

### In-Text Citations vs. Bibliography
* **In-Text Citation:** Pointers positioned within body text linking to full citations.
* **Bibliography:** Comprehensive list at the end of the paper providing complete metadata for every cited source.

### Standard Citation Formats

#### IEEE Style (Numbered)
* **In-Text:** `[1]`
* **Reference List:**  
  `[1] A. Vaswani et al., "Attention is all you need," in Advances in Neural Information Processing Systems, vol. 30, 2017, pp. 5998–6008.`

#### APA 7th Edition (Author-Date)
* **In-Text:** `(Vaswani et al., 2017)`
* **Reference List (Edited Book / Proceedings Chapter Standardized Format):**  
  `Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need. In I. Guyon, U. Von Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, & R. Garnett (Eds.), Advances in Neural Information Processing Systems 30 (NeurIPS 2017) (pp. 5998–6008). Curran Associates, Inc. https://proceedings.neurips.cc/paper/2017/file/3f5edd2435479d70ce3d08a1dce5fbb4-Paper.pdf`

#### MLA 9th Edition (Author-Page)
* **In-Text:** `(Vaswani et al. 5998)`
* **Reference List:**  
  `Vaswani, Ashish, et al. "Attention Is All You Need." Advances in Neural Information Processing Systems, vol. 30, 2017, pp. 5998–6008.`

#### Chicago Style (Author-Date)
* **In-Text:** `(Vaswani et al. 2017)`
* **Reference List:**  
  `Vaswani, Ashish, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. "Attention Is All You Need." In Advances in Neural Information Processing Systems, 30:5998–6008.`

#### BibTeX Entry
```bibtex
@inproceedings{vaswani2017attention,
  author    = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and Kaiser, {\textnormal{\'{L}}}ukasz and Polosukhin, Illia},
  title     = {Attention is All You Need},
  booktitle = {Advances in Neural Information Processing Systems},
  volume    = {30},
  pages     = {5998--6008},
  year      = {2017}
}
```

---

## 5. Persistent Identifiers & Metadata Services

### Persistent Identifiers

#### DOI (Digital Object Identifier)
* **Regex Pattern:** `^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$`
* **Example:** `10.1145/3318464.3389700`
* **Location in PDF:** Headers, footers, first-page margin, or document `/Metadata` streams.

#### arXiv ID & arXiv DOI
* **ArXiv ID Regex:** `^\d{4}\.\d{4,5}(v\d+)?$` (e.g., `1706.03762`)
* **ArXiv DOI Format:** `10.48550/arXiv.1706.03762`
* **Location in PDF:** Top margin stamp on every page generated during arXiv ingestion.

### Free Scholarly Metadata APIs

| Service | Identifier | Primary Returned Fields | Rate Limits & Rules |
| :--- | :--- | :--- | :--- |
| **Crossref API** | DOI | Title, Authors, Venue, Year, Volume, Issue, Citation Count, Funders, References | **Polite Pool:** Up to 50 requests/sec with mandatory `mailto:` header. Exceeding yields `429` / `503` codes. Commercial tier requires Crossref Metadata Plus. |
| **Semantic Scholar API** | DOI, arXiv ID, S2ID | PaperId, Title, Abstract, Authors, Venue, Year, CitationCount, FieldsOfStudy, OpenAccessPdf | **Public Pool:** 100 requests per 5 minutes per IP. Higher throughput available via free developer API Keys. |
| **arXiv API** | arXiv ID, Search Terms | Entry Title, Summary (Abstract), Authors, Dates, Primary Category, DOI Link | **Public Pool:** XML Atom feed. Polite throttling at $\le 1$ request per 3 seconds expected. |

---

## 6. Python PDF Extraction Libraries & Techniques

### Parsing Libraries Matrix

| Library | Engine | Key Strengths | Weaknesses | License Note |
| :--- | :--- | :--- | :--- | :--- |
| **PyMuPDF (`fitz`)** | C (MuPDF) | Extremely fast execution speed; granular word/glyph coordinate access. | Lacks native multi-column reading order detection. | **GNU AGPLv3** (Requires full source code disclosure if exposed as a service; commercial license required for proprietary use). |
| **`pdfplumber`** | Python (`pdfminer.six`) | Exceptional table extraction algorithms; precise shape and line inspection. | Slower parsing performance on large batches. | **MIT License** (Permissive). |
| **`pypdf`** | Pure Python | Lightweight with zero external dependencies; good for metadata reading and splitting. | Poor layout analysis; breaks on complex/multi-column documents. | **BSD License** (Permissive). |
| **GROBID** | Java / ML | State-of-the-art parsing of academic PDFs directly into TEI XML schemas; excels at parsing titles, abstracts, and references. | Heavier infrastructure requirement (requires Java/Docker REST service hosting). | **Apache 2.0 License** (Permissive). |

### Structural Element Detection Strategies

```
                  ┌──────────────────────────────┐
                  │      PDF Text Input Stream   │
                  └──────────────┬───────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
     [Heuristic Extraction]            [Model / LLM Parsing]
  - Font Size & Style Rules         - Vision Transformers / VLM
  - Spatial Coordinate Thresholds   - Sequence Tagging (LayoutLM)
  - Regex Heading Identification    - Structural JSON Schema Prompt
```

* **Heuristic Strategies:**
  * *Title Detection:* Identify page 1 text blocks with highest `font_size` values exceeding baseline body text threshold ($\Delta > 4\text{pt}$).
  * *Section Headings:* Match regex patterns across text lines: `^(\d+\.|\b[I|V|X]+\.|\bNotes\b|\bReferences\b)`.
  * *Authors/Affiliations:* Map font size and vertical offset deviations directly below the title bounding box.
* **Machine Learning & LLM Strategies:**
  * Route page renderings to Vision-Language Models (VLMs) or layout-aware vision models (LayoutLMv3) to yield structured JSON bounding-box tags (`[TITLE]`, `[ABSTRACT]`, `[AUTHOR]`, `[SECTION]`, `[REFERENCES]`).

---

## 7. Tagging, Topic Assignment & Keyword Extraction

### Methodology Taxonomy

```
                         ┌─────────────────────────────┐
                         │      Document Content       │
                         └──────────────┬──────────────┘
                                        │
    ┌───────────────────────────┼───────────────────────────┐
    ▼                           ▼                           ▼
[Unsupervised Statistical]   [Vocabulary Matching]   [Scholarly API Lookup]
- TF-IDF                     - ACM CCS Taxonomy      - Semantic Scholar
- RAKE / YAKE                - String Matching       - Pre-computed Fields
```

#### Statistical & NLP Approaches
* **TF-IDF:** Evaluates term relevance across a document corpus:
  $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \log\left(\frac{|D|}{|\{d \in D : t \in d\}|}\right)$$
  *Strengths:* Fast, unsupervised, domain-agnostic.  
  *Limitations:* Cannot capture semantic synonyms or implicit topic relationships.
* **RAKE / YAKE:** Keyphrase extraction based on word co-occurrence scores and positional text features.  
  *Strengths:* Fully domain-independent; requires zero training corpus.  
  *Limitations:* Vulnerable to extraction noise (e.g., misparsed PDF sidebars).

#### Controlled Vocabulary Alignment
* Match candidate keyphrases against structured taxonomies (e.g., ACM Computing Classification System, MeSH).  
  *Strengths:* High precision and standardized subject terms.  
  *Limitations:* Incapable of tagging novel or emerging terminology absent from the dictionary.

#### Scholarly API Metadata Lookup
* Query pre-computed classification fields (`fieldsOfStudy`, `s2FieldsOfStudy`) directly from scholarly graph databases (e.g., Semantic Scholar API).  
  *Strengths:* Zero local compute overhead; reliable classification.  
  *Limitations:* Unavailable for unpublished manuscripts, early preprints, or unindexed papers.

---

## 8. Knowledge Graphs & Relational Mapping

### Graph Fundamentals
* **Graph Definition:** $G = (V, E)$ composed of Vertices/Nodes ($V$) and Edges ($E$).
* **Directed Graph:** Asymmetric directional edges ($u \rightarrow v$), representing relations like `CITES` or `AUTHORED_BY`.
* **Undirected Graph:** Symmetric bidirectional edges ($u \leftrightarrow v$), representing relations like `CO_AUTHORED_WITH`.

### Relational Database Schema Mapping

```
     ┌───────────────────┐               ┌───────────────────┐
     │    nodes Table    │               │    edges Table    │
     ├───────────────────┤               ├───────────────────┤
     │ PK  node_id       │◄──────────────┤ PK  edge_id       │
     │     label         │               │ FK  source_id     │
     │     properties    │◄──────────────┤ FK  target_id     │
     └───────────────────┘               │     relation_type │
                                         │     weight        │
                                         └───────────────────┘
```

#### Node Table (`nodes`)
```sql
CREATE TABLE nodes (
    node_id VARCHAR(255) PRIMARY KEY,
    label VARCHAR(50) NOT NULL, -- e.g., 'Paper', 'Author', 'Concept'
    properties JSONB -- Stores metadata (title, year, author_name)
);
```

#### Edge Table (`edges`)
```sql
CREATE TABLE edges (
    edge_id SERIAL PRIMARY KEY,
    source_id VARCHAR(255) REFERENCES nodes(node_id),
    target_id VARCHAR(255) REFERENCES nodes(node_id),
    relation_type VARCHAR(50) NOT NULL, -- e.g., 'CITES', 'AUTHORED'
    weight FLOAT DEFAULT 1.0
);
```

### Browser Interactive Graph Schemas

#### Vis.js (`vis-network`)
```json
{
  "nodes": [
    { "id": "p1", "label": "Paper A", "group": "paper" },
    { "id": "a1", "label": "Author B", "group": "author" }
  ],
  "edges": [
    { "from": "a1", "to": "p1", "label": "AUTHORED" }
  ]
}
```

#### D3.js (Force-Directed Graph)
```json
{
  "nodes": [
    { "id": "p1", "name": "Paper A", "group": 1 },
    { "id": "a1", "name": "Author B", "group": 2 }
  ],
  "links": [
    { "source": "a1", "target": "p1", "value": 1, "relation": "AUTHORED" }
  ]
}
```

---

## 9. Structural Edge Cases & Failure Mitigation Strategies

| Edge Case Scenario | Root Cause | Technical Mitigation Strategy |
| :--- | :--- | :--- |
| **Missing Abstract Section** | Briefing papers, short papers, or unconventional executive summary headings (`In Brief`). | Fall back to extracting the introductory section up to section `1.1` or generate an abstract summary using an LLM over the initial 1000 words. |
| **Multi-Line Titles** | Wrapping title strings split across multiple line objects in PDF streams. | Group top-of-page text blocks using physical vertical position thresholding ($y_1 - y_0 < \text{threshold}$) before concatenating strings. |
| **Complex Author/Affiliation Mapping** | Numeric/symbolic superscripts (`Doe¹`, `Smith²`) connecting authors to footnotes. | Use regex patterns to detach superscript markers and cross-reference them with footnote block spatial coordinates. |
| **Non-English / Multilingual Text** | Missing language tags or non-standard font character maps. | Detect character encodings using UTF-8 fallback decoders; route unmapped encodings to multilingual OCR pipelines. |
| **Missing DOI / arXiv ID** | Draft manuscripts, institutional briefing papers, or legacy non-indexed publications. | Execute fuzzy string matching (e.g., Levenshtein distance on title + lead author) against Crossref and Semantic Scholar APIs. |
| **Scanned Pages / Raster PDF** | Document lacks vector text objects (`/Text` object stream missing). | Check text stream byte counts; if character count per page is $< 50$, automatically route page image renderings to Tesseract OCR or PaddleOCR pipelines. |
| **References Split Across Columns** | Individual reference entries spanning column boundaries or page breaks. | Implement programmatic bounding-box sorting based on physical reading order columns (`column_index`, `y_coordinate`) prior to regex entry extraction. |
| **Duplicate Document Uploads** | Identical papers published as preprints, working papers, or camera-ready versions. | Generate SHA-256 hashes of raw PDF files, combined with soft deduplication using cosine similarity on normalized title embeddings. |
```

---

The context pack has been generated in the document editor. It covers all required topics concisely and includes real-world patterns observed from your samples.