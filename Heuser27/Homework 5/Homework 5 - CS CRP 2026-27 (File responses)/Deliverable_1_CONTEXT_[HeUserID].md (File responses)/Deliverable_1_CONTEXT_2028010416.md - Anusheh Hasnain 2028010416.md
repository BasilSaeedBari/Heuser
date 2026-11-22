# Deliverable 1: Context Engineering Pack
**Project ID:** Deliverable_1_CONTEXT_2028010416  
**User ID:** 2028010416  
**Domain:** Research Paper Library & Knowledge Graph System  

---

## Section 1: Project Overview

This project implements an end-to-end Context Engineering Pack and Knowledge Graph ingestion pipeline for an intelligent Research Paper Library system. The application ingests raw academic publications (PDFs and metadata queries), parses complex layouts, extracts essential bibliometrics and structural content, performs dynamic topic tagging, and maps entities into a multi-relational Knowledge Graph. By unifying disparate identifier schemas (DOIs, arXiv IDs, Corpus IDs), accounting for structural PDF extraction challenges, and establishing structured node-edge schemas (Paper, Author, Topic), the platform enables semantic paper search, citation traversal, dynamic topic modeling, and automated bibliography discovery.

---

## Section 2: Anatomy of a Research Paper

### 2.1 Standard Structural Sections & Order
1. **Title**: Concise summary of the research topic, domain, and primary findings.
2. **Authors & Affiliations**: Primary contributors, institutional alignments, email contacts, and corresponding author designations.
3. **Abstract**: Self-contained summary (typically 150–300 words) highlighting problem context, methodology, primary results, and core conclusions.
4. **Keywords / Index Terms**: 3–8 standard terms or taxonomy nodes used for database indexing and field categorization.
5. **Introduction**: Problem motivation, research questions, hypothesis, explicit contributions, and structural outline of the paper.
6. **Related Work / Background**: Contextualization against prior literature and state-of-the-art benchmarks.
7. **Methodology / System Architecture**: Mathematical formulation, algorithmic procedures, system design, and experimental setups.
8. **Experiments / Evaluation**: Datasets, baseline comparisons, qualitative/quantitative metrics, and experimental results.
9. **Discussion / Limitations**: Critical analysis of empirical findings, edge cases, system assumptions, and potential threats to validity.
10. **Conclusion & Future Work**: High-level synthesis of findings and actionable directions for future research.
11. **Acknowledgments**: Funding agencies, grant numbers, facility support, and non-author contributors.
12. **References / Bibliography**: Standardized list of cited publications.
13. **Appendices / Supplementary Material**: Mathematical proofs, extended hyperparameter configurations, or additional empirical plots.

### 2.2 Venue Specifics: Conference vs. Journal vs. arXiv
* **Conference Proceedings (e.g., NeurIPS, ACL, IEEE CVPR)**:
  * *Layout*: Strict double-column formatting (IEEE/ACM) or dense single-column layout (LNCS/Springer). Enforces strict page limits (e.g., 8–9 pages excluding references).
  * *Review Cycle*: Peer-reviewed under fixed deadlines; high emphasis on novel techniques and benchmark performance.
* **Journal Articles (e.g., IEEE Transactions, Nature, JMLR)**:
  * *Layout*: Single or double column depending on venue; includes detailed header metadata with submission/accepted dates, volume, issue, and DOI.
  * *Content*: Comprehensive theoretical derivations, extensive empirical validations, without rigid short page limits.
* **arXiv Preprints**:
  * *Layout*: Heterogeneous; relies on generic LaTeX templates (e.g., `article`, `revtex`, `geometry`).
  * *Identifiers*: Lacks initial journal volume/issue details; features an arXiv header/watermark (e.g., `arXiv:1706.03762v7 [cs.CL]`).

---

## Section 3: The PDF Problem

Extracting structured text from PDF research papers presents severe technical hurdles due to the native specification of the Portable Document Format (PDF):

### 3.1 PDF Drawing Commands vs. Semantic Text
PDFs store literal vector display instruction sequences (e.g., `BT` [Begin Text], `ET` [End Text], `Tj` [Show Text], `cm` [Current Transformation Matrix]) rather than semantic structural entities like paragraphs, headings, or lists. Text is painted on a 2D coordinate space.

### 3.2 Glyph Positioning and Reconstruction
Word spacing is frequently represented by absolute spatial positioning jumps rather than explicit ASCII space characters (`0x20`). Reconstructing text requires calculating bounded geometry spaces and bounding boxes ($x_0, y_0, x_1, y_1$) to infer word breaks, line wraps, paragraph bounds, and baseline alignment.

### 3.3 Multi-Column Layouts
Standard linear stream readers process text sequentially based on draw commands. In a double-column paper, sequential stream reading intermingles line 1 of column 1 with line 1 of column 2, destroying sentence context. Spatial heuristics or layout-aware tree parsers are required to sort bounding boxes column by column.

### 3.4 Running Headers, Footers, and Page Numbers
Headers (e.g., journal running headers) and footers (e.g., page numbers, copyright notices) interrupt body paragraphs across page boundaries. Ingestion algorithms must detect and filter out recurring spatial boundary regions.

### 3.5 Scanned vs. Vector Text PDFs
* **Vector PDFs**: Contain embedded font encodings (Type 1, TrueType, CID fonts). Text can be directly extracted via character mapping.
* **Scanned PDFs**: Contain only raster image arrays (JPEG, PNG, JBIG2 streams). Glyph extraction requires Optical Character Recognition (OCR) engines (e.g., Tesseract, PaddleOCR).

---

## Section 4: Citation Styles with Real Examples

### 4.1 IEEE (Numeric, In-Text In-Order Brackets)
* **In-Text**: `[1]`, `[2, pp. 12–15]`
* **Reference List Example**:
  > [1] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, "Attention is all you need," in *Advances in Neural Information Processing Systems*, vol. 30, pp. 5998–6008, 2017.

### 4.2 APA (7th Edition, Author-Date)
* **In-Text**: `(Vaswani et al., 2017)`
* **Reference List Example**:
  > Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 30, 5998–6008.

### 4.3 MLA (9th Edition, Author-Page)
* **In-Text**: `(Vaswani et al. 6001)`
* **Reference List Example**:
  > Vaswani, Ashish, et al. "Attention Is All You Need." *Advances in Neural Information Processing Systems*, vol. 30, 2017, pp. 5998–6008.

### 4.4 BibTeX Format
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

## Section 5: Identifiers & Metadata APIs

### 5.1 Regular Expression Patterns

#### DOI Regex
```regex
10\.\d{4,9}/[-._;()/:A-Za-z0-9]+
```

#### arXiv ID Regex
```regex
(arXiv:)?(\d{4}\.\d{4,5}|[a-z\-]+(\.[A-Z]{2})?/\d{7})(v\d+)?
```

### 5.2 Metadata APIs Overview

1. **Crossref API**: Primary registry for academic DOIs (`https://api.crossref.org/works/{doi}`).
2. **Semantic Scholar API**: Academic graph API providing paper metadata, citations, and embeddings (`https://api.semanticscholar.org/graph/v1/paper/{paper_id}`).
3. **OpenAlex API**: Comprehensive open bibliometrics database (`https://api.openalex.org/works`).
4. **arXiv API**: Endpoint for preprint Atom/XML feed retrieval (`http://export.arxiv.org/api/query`).
   * *Rate Limit*: Maximum 1 request per 3 seconds.

### 5.3 Sample API JSON Response (Semantic Scholar API)

```json
{
  "paperId": "204242f71ea5062331199014f115708df4e0e500",
  "externalIds": {
    "ArXiv": "1706.03762",
    "DOI": "10.48550/arXiv.1706.03762",
    "CorpusId": 13756489
  },
  "title": "Attention Is All You Need",
  "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
  "venue": "NeurIPS",
  "year": 2017,
  "referenceCount": 38,
  "citationCount": 115000,
  "authors": [
    { "authorId": "1802302", "name": "Ashish Vaswani" },
    { "authorId": "1741101", "name": "Noam Shazeer" }
  ],
  "tldr": {
    "model": "abstractive",
    "text": "The authors propose the Transformer model based entirely on self-attention mechanisms."
  }
}
```

---

## Section 6: Extraction Techniques & Architectural Selection

### 6.1 Tool Evaluation Matrix

| Tool | Mechanism | Strengths | Weaknesses | Performance |
| :--- | :--- | :--- | :--- | :--- |
| **`pypdf`** | Pure Python stream reader | Fast, zero C/binary dependencies | Fails on multi-column layouts; lacks spatial layout analysis | Fast / Low Accuracy |
| **`pdfplumber`** | Built on `pdfminer.six` | Precise bounding box positions, table extraction | High execution overhead on multi-page PDFs | Slow / High Precision |
| **`PyMuPDF` (fitz)** | C bindings to MuPDF engine | Fast block/font extraction, spatial coordinates | Binary C dependency required | Fast / High Precision |

### 6.2 Chosen Approach: Hybrid PyMuPDF Engine
The pipeline adopts **PyMuPDF (`fitz`)** for primary text and structural block extraction. It uses spatial bounding box heuristics ($x_0, y_0, x_1, y_1$) and font-size clustering to distinguish main body columns from headers, footers, and multi-line titles.

---

## Section 7: Tagging & Topic Assignment Techniques

### 7.1 Algorithmic Paradigms
1. **RAKE (Rapid Automatic Keyword Extraction)**: Evaluates word frequency and degree co-occurrence ratios across stop-word delimited phrases. Fast but yields generic phrases.
2. **TF-IDF (Term Frequency - Inverse Document Frequency)**: Evaluates word importance relative to a background paper corpus.
3. **Scholarly API Concept Mapping**: Pulls standardized taxonomy concepts directly from APIs (e.g., OpenAlex Concept Hierarchy, Semantic Scholar Topics).

### 7.2 Chosen Approach
A **Hybrid Tagging Engine**: Categorizes papers using API-provided concept taxonomies (e.g., `Computer Science`, `Deep Learning`) and supplements them with local phrase ranking using TF-IDF over the Abstract and Introduction sections.

---

## Section 8: Knowledge Graph Model

```
       (Author) -[:AUTHORED]---------> (Paper) <---------[:CITES]-- (Paper)
          |                              |
   [:CO_AUTHORED_WITH]              [:HAS_TOPIC]
          |                              v
       (Author)                       (Topic) -[:RELATED_TO]-> (Topic)
```

### 8.1 Schema Specification

#### Nodes
* **`Paper`**: `paper_id` (PK, e.g., DOI/arXiv), `title`, `abstract`, `year`, `venue`, `citation_count`, `pdf_url`.
* **`Author`**: `author_id` (PK), `name`, `affiliation`, `h_index`.
* **`Topic`**: `topic_id` (PK, normalized slug), `label`, `domain`.

#### Edges
* **`AUTHORED`**: `Author` $\rightarrow$ `Paper` (Directed)
* **`HAS_TOPIC`**: `Paper` $\rightarrow$ `Topic` (Directed, Property: `confidence_score`)
* **`CITES`**: `Paper` $\rightarrow$ `Paper` (Directed)
* **`CO_AUTHORED_WITH`**: `Author` $\leftrightarrow$ `Author` (Derived / Materialized Edge)
* **`RELATED_TO`**: `Topic` $\leftrightarrow$ `Topic` (Derived Edge, Property: `co_occurrence_weight`)

### 8.2 Derived Edges Strategy
* **`CO_AUTHORED_WITH`**: Materialized directly during ingestion. Storing co-authorship as an explicit edge accelerates author network graph queries ($O(1)$ lookup vs $O(N^2)$ relational join).
* **`RELATED_TO`**: Computed dynamically based on shared paper occurrences above a set co-occurrence threshold.

---

## Section 9: Edge Cases & Failure Modes

1. **Missing Abstract**: Fall back to extracting the first 300 words under the `1. Introduction` header; flag `is_abstract_synthetic = True`.
2. **Multi-Line Titles with Interleaved Authors**: Perform font-size analysis on Page 1 ($font\_size \ge 0.85 \times \max\_font\_size$) before applying author name NER filters.
3. **Scanned / Raster Image PDFs**: Check character density ($\text{chars} < 50$ per page). If triggered, route pages to `pytesseract` OCR engine.
4. **API Rate Limits (429 / 503)**: Implement exponential backoff retry logic with randomized jitter (base 2s delay, up to 5 retries).
5. **Duplicate Versions (arXiv Preprint vs. Journal Version)**: Resolve via title normalized string distance (Levenshtein ratio $> 0.92$) and publication year matching.

---

## Section 10: Sample Paper Findings (Real Excerpts)

### Test Target Paper: "Attention Is All You Need"
* **Title**: Attention Is All You Need
* **Authors**: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin.
* **Extracted DOI**: `10.48550/arXiv.1706.03762`
* **Extracted arXiv ID**: `1706.03762v7`
* **Real Excerpt (Abstract)**:
  > *"The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and the decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."*
* **Extracted Graph Entities**:
  * Node `Paper`: `1706.03762v7`
  * Node `Author`: `Ashish Vaswani`, `Noam Shazeer`, etc.
  * Node `Topic`: `Transformer (Deep Learning)`, `Self-Attention`, `Natural Language Processing`

---

## Section 11: Sifting Log

| Candidate / Technique | Decision | Rationale |
| :--- | :--- | :--- |
| **`pypdf` Plain Text Extraction** | **Discarded** | Multi-column papers resulted in interleaved lines across left/right columns. |
| **`PyMuPDF` Spatial Reading** | **Kept** | Accurately extracts text blocks with spatial coordinates and font metadata. |
| **Pure Unsupervised RAKE Tagging** | **Discarded** | Extracted non-informative academic phrases such as "proposed method" and "experimental setup." |
| **Hybrid API Concept + TF-IDF** | **Kept** | Provides clean field-level tags alongside paper-specific keywords. |
| **Dynamic SQL Joins for Co-authorship** | **Discarded** | Multi-hop graph traversals timed out over large author datasets without pre-computed edges. |
| **Materialized `CO_AUTHORED_WITH` Edges** | **Kept** | Dramatically improved graph traversal performance for author collaboration queries. |

---

## Section 12: Sources & Reference URLs

1. **arXiv API User Manual**: `https://info.arxiv.org/help/api/user-manual.html`
2. **Crossref REST API Docs**: `https://api.crossref.org/`
3. **Semantic Scholar Graph API**: `https://api.semanticscholar.org/api-docs/`
4. **OpenAlex Documentation**: `https://docs.openalex.org/`
5. **PyMuPDF Documentation**: `https://pymupdf.readthedocs.io/`
6. **pdfplumber Repository**: `https://github.com/jsvine/pdfplumber`
7. **ISO 26324 (DOI System Standard)**: `https://www.doi.org/`