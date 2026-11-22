# CONTEXT - Research Paper Library \& Knowledge Graph

## 1\. Project in one paragraph
The Research Paper Library & Knowledge Graph is a web-based application designed to help users organise, manage, and explore research papers. Users can upload research-paper PDFs, from which the application extracts information such as titles, authors, abstracts, keywords, publication years, identifiers, and references. It enriches this information using external scholarly APIs, assigns topic tags, and stores the data in an SQLite database. Users can search and filter their library, edit paper metadata, manage topic tags, and view an interactive knowledge graph showing connections between papers, authors, and topics. The application also supports duplicate detection, citation linking, and an activity log to help users manage their research collection.

## 2\. Anatomy of a research paper (sections, order, what each contains)

The macro-structure of an academic research paper follows a continuous, predictable narrative progression designed to communicate experimental rationale, methodology, empirical findings, and contextual integration within the scientific literature.. While minor structural adaptations occur across sub-disciplines, empirical scholarly publications adhere to a standardized structural tripartite format comprising Front Matter, Core Body Text, and Back Matter.

1. Common Research-Paper Sections and Contents
Front Matter : Title, authors, affiliations, abstract (150–300 words), keywords, and publication metadata (DOI, dates) establishing paper identity.
Core Body (IMRaD) : Introduction (context, gaps, related work), Methods (setup), Results (findings, tables), and Discussion (interpretation).  
Back Matter : Conclusions, Acknowledgments (funding/grants), References (graph edges), and Appendices.  
Pattern vs. Rule : IMRaD is a standard convention for empirical papers, not an absolute rule across all disciplines.
2. Geolocation of Key Metadata Elements
Titles, Authors, \& Affiliations : Top third of page 1; Affiliations appear directly below authors or in page 1 footnotes.  
Abstract \& Keywords : Page 1 preceding body text, often full-width or indented.  
DOIs \& Publication Info : Page 1 headers, footers, side margins, or embedded XMP streams.  
References : Itemized list at the document tail.  
Pattern vs. Rule : Top-page titles and terminal reference lists are near-universal invariants, whereas exact spatial coordinates ($X, Y$) vary by template.
(Structural Parsing and Challenges :
-Multi-line titles accidentally merging with running journal headers or sub-titles.
-Disambiguating individual author names from interleaved institution strings or emails.
-Parsing complexM-to-NMappings between authors and institutions.
-Distinguishing abstract body text from executive summaries or introductory paragraphs.
-Parsing non-standard delimiter formats (commas, semicolons, bullet points)
-DOIs split across line wraps with inserted hyphens; missing DOIs in preprints.
-Column wrapping, split citation records across page boundaries, varied citation styles.)
3. Differences Across Venues (Conference, Journal, Preprint)
IEEE : Two-column layout, author header grid, page 1 footer DOIs/copyright, numeric citations\[1].  
ACM : Single/two-column ( acmart); Includes CCS taxonomy, copyright blocks, and explicit reference callouts.  
Springer LNCS : Single-column; Compressed author/affiliation block on page 1, numeric citations.  
arXiv Preprints : Variable LaTeX templates; lack formal publisher DOIs; feature a vertical margin watermark stamp.
4. Variations in Paper Structure and Formatting
Invariant Structural Elements :
Across scientific disciplines, several structural and geometric principles remain consistent. The logical narrative flow strictly moves top-to-bottom, with title and primary author metadata situationalized in the upper third of the first page. Visual hierarchy is encoded through typographic font size scaling; title text size strictly exceeds section heading size, which exceeds body text size, which exceeds footnote and reference text size. Key structural sections are marked by explicit string anchors such as "Abstract", "Introduction", "References", and "Acknowledgments". The bibliographic reference list is positioned at the terminal tail of the document text stream, immediately preceding optional appendices.

Highly Variable Structural Elements :
Citation Styles : Numeric ( \[1]), Author-Date ( (Smith, 2020)), or footnote systems vary by venue/discipline.  
Author-Affiliation Mapping : Mapped via superscripts (1, \*), shared address strings, or footnotes.  
Layout Grids : Single vs. multi-column layouts and line-wrapped metadata fields.

5. Implications for Automated PDF Metadata Extractor Design
Reading Order \& Column Segmentation : PDF streams lack reading order; Multi-column layouts require spatial gutter detection to prevent text interleaving.  
Unreliable Native Metadata : DocInfo fields are often inaccurate and XMP is frequently missing in preprints, requiring visual parsing.  
Pipeline Architecture : Requires spatial layout analysis, cascaded ML models (header, author, reference parsing), hyphenation repair, and watermark filtering.

## 3\. The PDF problem (how text is stored; two-column, scanned, etc.)

1. Text-Based vs. Scanned PDFs
Text-Based (Digital-Native) PDFs (Common):\*\* Contain explicit text streams, font data, and ToUnicode maps (ISO 32000-1 / Adobe PDF Reference), allowing direct character extraction.
Scanned PDFs (Specific):\*\* Consist entirely of compressed raster images with no underlying text layer, requiring fallback OCR pipelines to interpret characters.
2. Structural Extraction Problems
Two-Column Layouts (Common): Content streams are recorded by compilation order rather than visual layout, causing naive parsers to extract text horizontally across columns.
Headers, Footers, Hyphenation, \& Ligatures (Common): Top and bottom margins introduce running titles; line breaks create hyphenated splits (e.g., "infor-mation"); missing ToUnicode maps corrupt character ligatures (e.g., "fi").
Footnotes \& Equations (Specific): Floating notes inject themselves mid-paragraph; math formulas rely on fragmented glyph coordinates or unmapped private-use symbols.
3. Impact on Metadata Extraction
Titles \& Authors: Vulnerable to top-margin artifacts, stray header text, and multi-column alignment errors on the first page.
Abstracts \& Keywords: Frequently scrambled by two-column boundary misinterpretations or interrupted by misplaced footnote injections.
References: Column flow errors, hyphenation, and broken ligatures corrupt bibliographic strings, author names, and DOIs.
4. Practical Ways to Handle Limitations
Layout-Aware Parsing: Use Python libraries (`pdfplumber`, `PyMuPDF`) to access bounding box coordinates (x, y) and programmatically group text into proper columns.
Margin Filtering: Discard text falling within designated top and bottom y-coordinate ranges to eliminate headers and footers.
Post-Processing: Apply regular expressions to automatically rejoin hyphenated line breaks.
Scope Management: Defer complex mathematical equation parsing and handle image-only scanned files with OCR tools.

## 4\. Citation styles (IEEE / APA / MLA / BibTeX) - one REAL example each

Designing a robust Research Paper Library and Knowledge Graph application requires understanding the structural and syntactical nuances of various citation formats. Different academic communities adhere to distinct standards, posing significant challenges for PDF ingestion engines and citation parsers.

IEEE
In-Text Citation: Uses bracketed numbers corresponding to a sequentially ordered bibliography list (e.g., [1]`).
Reference Entry:[#] Initials. Last Name, "Title of paper," *Abbreviated Journal/Proceedings Name*, vol. Vol, no. Issue, pp. Pages, Year.`
Example:
[1] A. Vaswani *et al.*, "Attention Is All You Need," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 30, 2017, pp. 5998–6008.

APA
In-Text Citation: Uses an author-date parenthetical system (e.g., `(Vaswani et al., 2017)`).
Reference Entry: `Author, A. A., et al. (Year). Title. *Periodical*, *Volume*(Issue), pages. DOI
Example:
Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., \& Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, *30*, 5998–6008. [https://doi.org/10.48550/arXiv.1706.03762](https://doi.org/10.48550/arXiv.1706.03762)

MLA
In-Text Citation: Uses an author-page parenthetical system without punctuation (e.g., `(Vaswani et al. 5999)`).
Reference Entry: `Author Last, First, et al. "Title." *Container*, vol. Vol, no. Issue, Year, pp. Pages.`
Example:
Vaswani, Ashish, et al. "Attention Is All You Need." *Advances in Neural Information Processing Systems*, vol. 30, 2017, pp. 5998–6008.

BibTeX
What it is: A plain-text, machine-readable data format utilizing key-value pairs to store bibliographic metadata. Unlike conventional formatted in-text citations or printed reference lists, BibTeX separates structural data from layout styling, leaving formatting to $\\LaTeX$ compilation styles.
Example:
bibtex
@inproceedings{vaswani2017attention,
author    = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N. and Kaiser, {\\L}ukasz and Polosukhin, Illia},
title     = {Attention is all you need},
booktitle = {Advances in Neural Information Processing Systems},
volume    = {30},
pages     = {5998--6008},
year      = {2017}

Knowledge graph and library ingestion engines process unstructured PDFs from diverse academic disciplines. Because citation formats vary widely in author positioning, date placement, and typography (e.g., IEEE vs. APA vs. MLA), PDF parsers cannot rely on a single parsing rule. Understanding these variations is essential for robust reference extraction, normalization, and graph linking.

## 5\. Identifiers and metadata APIs

1. DOI and arXiv ID Patterns

-Digital Object Identifier (DOI):

Pattern: Starts with 10. followed by a prefix and a suffix separated by a slash (e.g., 10.1038/s41586-021-03819-2 or formatted as a URL \[https://doi.org/10.1038/](https://doi.org/10.1038/)...).

Locations in PDF: Publisher landing links, headers/footers, first-page footnotes, reference sections, and embedded PDF XMP metadata.

-arXiv ID:

Pattern: Modern format is YYMM.NNNNN (e.g., 2103.12345), optionally with a version suffix (v1). Older format uses subject class classifications (e.g., cs.AI/0501001).

Locations in PDF: Top-right corner of the first page, page footer banners, repository submission manifests, and PDF metadata fields.



2. Metadata APIs Comparison

Crossref REST API

Purpose: Authoritative metadata registry for journal articles and books linked via DOIs.

Endpoint: `[https://api.crossref.org/works/](https://api.crossref.org/works/){doi}`

Authentication: Optional polite pool (include `mailto=` parameter in user-agent header).

Rate Limits / Restrictions: Up to 50 requests/second.

Returned Fields: Title, authors, publication date, identifiers (DOI, ISSN, ISBN), references, and partial abstracts (publisher-dependent).



OpenAlex API

Purpose: Open catalog mapping scholarly works, authors, institutions, and citations.

Endpoint: `[https://api.openalex.org/works/](https://api.openalex.org/works/){id}`

Authentication: Free API key via account registration (`api_key` parameter).

Rate Limits / Restrictions: Freemium model: $1/day free usage with key ($0.10/day without key).

Returned Fields: Title, authors, abstract (via inverted index), publication year, identifiers (DOI, PMID, arXiv, OpenAlex ID), and reference links.



Semantic Scholar API

Purpose: Academic graph providing paper details, citation metrics, and embeddings.

Endpoint: `[https://api.semanticscholar.org/graph/v1/paper/](https://api.semanticscholar.org/graph/v1/paper/){paper_id}`

Authentication: Optional API key for guaranteed throughput.

Rate Limits / Restrictions: Unauthenticated shared pool; API key grants dedicated 1 request/second.

Returned Fields: Title, authors, abstract, publication year, identifiers (DOI, arXiv, CorpusId, MAG ID), and references (inbound/outbound).



arXiv API

Purpose: Official interface for querying arXiv preprint metadata.

Endpoint: `[http://export.arxiv.org/api/query](http://export.arxiv.org/api/query)?...`

Authentication: None required.

Rate Limits / Restrictions: Max 1 request every 3 seconds; single connection at a time.

Returned Fields: Title, authors, abstract/summary, published date, identifiers (arXiv ID, optional DOI if published).References: Not provided.



Response examples :



Crossref REST API :

{ "status": "ok",

     ; "message-type": "work",

     ; "message": {

     ;   "DOI": "10.1016/j.jbiotec.2010.08.003",

     ;   "title": \["Example article title from Crossref registry"],

     ;   "author": \[{"given": "Jane", "family": "Doe", "sequence": "first"}],

     ;   "issued": {"date-parts": \[\[2010, 9]]}

     ;  }

}



OpenAlex API :

{ "id": "https://openalex.org/W2741809807",

     ; "doi": "https://doi.org/10.1016/j.neuroimage.2017.11.040",

     ; "title": "Example OpenAlex work title",

     ; "publication\_year": 2018,

     ; "authorships": \[{"author": {"id": "https://openalex.org/A5023880200", "display\_name": "Sample Author"}}]

}



Semantic Scholar API :

{

     ; "paperId": "649def34f8be52c8b66281af98ae884c09aef38b",

     ; "externalIds": {"DOI": "10.18653/v1/N18-3011", "ArXiv": "1802.05365"},

     ; "title": "Example paper title from Semantic Scholar graph",

     ; "abstract": "This is an example abstract string returned by the API.",

     ; "year": 2018

}



arXiv API (Note: Illustrative JSON mapping; actual arXiv API natively returns Atom XML) :

{

     ; "feed": {

     ;   "entry": {

     ;     "id": "http://arxiv.org/abs/2103.12345v1",

     ;     "title": "Example arXiv preprint title",

     ;     "summary": "This is a sample abstract extracted from the official arXiv API Atom feed schema.",

     ;     "published": "2021-03-22T00:00:00Z",

     ;     "author": \[{"name": "Preprint Author"}]

     ;   }

     ; }

}

3. Relevance to Application

When a user uploads a PDF, extracted text or metadata streams can be parsed for a DOI or arXiv ID pattern. Querying these APIs using a verified identifier eliminates keyword search ambiguity and author name collisions. Programmatically querying these endpoints allows the application to automatically auto-fill missing fields—such as structured author lists, publication dates, canonical titles, abstracts, and reference/citation graphs—into the Knowledge Graph without requiring manual user input.



4. Confirmed Capabilities vs. Known Limitations

Confirmed Capabilities:

DOIs and arXiv IDs provide globally unique resolution across databases.

All APIs return core metadata (titles, authors, publication dates, identifiers).

Limitations & Unverified Details:

Crossref: Abstracts are dependent on publisher deposit and may be missing for older or niche records.

OpenAlex: Uses automated disambiguation, which can occasionally introduce entity matching errors.

Semantic Scholar: Enforces strict pagination caps on citation/reference lists and rate-limits unauthenticated pools.

arXiv API: Limited strictly to preprints, does not natively return reference lists.

External Scholarly API Rate Limits, Terms of Use and Data Licensing

The application uses Crossref, arXiv, Semantic Scholar and OpenAlex to enrich research-paper metadata. Each service has its own request limits and reuse conditions. The application must respect these limits, handle rate-limit responses without crashing, and avoid assuming that all retrieved content is free to redistribute.

1. Crossref REST API

-Rate limits: The public pool allows up to 5 requests per second, with 1 concurrent request. The polite pool allows up to 10 requests per second, with 3 concurrent requests for single-record lookups. The polite pool is accessed by including a valid email address in the `mailto` parameter. Limits can differ for list/search requests.
-Terms of use: Use the API responsibly, identify the application with a contact email, cache responses where appropriate, and respect rate-limit responses such as HTTP 429.
-Data licensing: Crossref states that almost none of its deposited metadata is subject to copyright and that it may be used for any purpose. However, some abstracts contained in metadata may be copyrighted by publishers or authors. The copyright status of individual content fields must not be assumed to be identical.
-Official sources:
  - https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/
  - https://www.crossref.org/documentation/retrieve-metadata/rest-api/

2. arXiv API

-Rate limits: The legacy arXiv API permits no more than one request every 3 seconds, with only one connection at a time across the machines controlled by the same user.
-Terms of use: Requests must respect the rate limits and must not circumvent access restrictions. The API may be used to build research-discovery tools and citation visualisations.
-Data licensing: Descriptive metadata, including titles, abstracts, authors, identifiers and classification terms, may be used under the Creative Commons CC0 1.0 Public Domain Declaration. Full-text papers are different: their copyright and redistribution permissions depend on the applicable rights and licence for each paper. The application must not redistribute arXiv PDFs unless it has permission or the applicable licence allows it.
-Official sources:
  - https://info.arxiv.org/help/api/user-manual.html
  - https://info.arxiv.org/help/api/tou.html
  - https://arxiv.org/help/license

3. Semantic Scholar Academic Graph API

-Rate limits: Semantic Scholar recommends using an API key. Its introductory API-key rate limit is 1 request per second across endpoints. Unauthenticated requests share a common pool and may be throttled further during periods of high demand.
-Terms of use: Requests must comply with the API documentation and licence agreement. API keys must be kept confidential, and rate limits must not be bypassed.
-Data licensing and attribution: The API licence agreement sets conditions on how its data may be used. It describes permitted use in terms of internal, non-commercial research and educational purposes, including specified data-transformation activities. Public displays of data require attribution, a link back to Semantic Scholar with the specified `utm_source=api` parameter, and the Semantic Scholar name and logo. Uses outside the stated licence scope may require an expanded licence. The intended use should therefore be checked against the agreement before implementation or public deployment.
-Official sources:
  - https://www.semanticscholar.org/product/api
  - https://api.semanticscholar.org/api-docs/
  - https://api.semanticscholar.org/license/

4. OpenAlex API

- Rate limits and usage budget: OpenAlex permits up to 10 requests per second without an API key and up to 30 requests per second with a free API key. A free account receives a daily API usage budget of $1, which is separate from the per-second request limit. Different request types consume different amounts of that budget.
- Terms of use: Requests must remain within the applicable rate limits and usage budget. The application should monitor usage, handle HTTP 429 responses, and retry with backoff rather than repeatedly sending requests.
- Data licensing: OpenAlex states that its scholarly metadata is released under the CC0 public-domain licence. This applies to the OpenAlex dataset; it does not automatically change the licence of the underlying research papers or full-text files that OpenAlex describes.
- Official sources:
  - https://help.openalex.org/api/authentication/
  - https://help.openalex.org/access/pricing/
  - https://help.openalex.org/data/how-its-built/

Implementation implications

1. Use conservative request limits, especially for arXiv and Semantic Scholar.
2. Cache successful metadata responses to reduce unnecessary requests.
3. Handle HTTP 429 and server errors with a delay and a limited retry policy.
4. Keep API keys in environment variables rather than hard-coding them into source files.
5. Store and display metadata separately from full-text papers, and respect the relevant content licences.
6. Recheck the official documentation during implementation because API limits and terms may change.

Research note: The limits above are taken from the official documentation consulted for this project. They should be rechecked before deployment. API access does not itself grant permission to redistribute every piece of content returned by that API.





##6). Extraction techniques considered -> which one I chose and why

   1) Python PDF extraction libraries

pypdf: A pure-Python library optimized for document-level tasks like splitting, merging, and rotating. It uses sequential stream reading, which scrambles multi-column academic layouts into interleaved text and is unsuitable for structured extraction.

PyMuPDF (`pymupdf`): Built on the C-based MuPDF engine. It offers high execution speed and block-level extraction (`get_text("blocks")`) that uses spatial sorting to preserve multi-column reading order. Its primary constraint is the copyleft AGPL-3.0 license.

pdfplumber: Built on `pdfminer.six`, providing fine-grained, character-level coordinate, font, and bounding-box data. While slower in execution speed, it enables precise spatial filtering and layout debugging.



  2) Metadata extraction techniques

External Metadata APIs (CrossRef / Semantic Scholar): Programmatically queries academic databases using detected digital identifiers (DOIs or arXiv IDs) to fetch verified titles, authors, affiliations, and abstracts.

Font-Size and Position Heuristics: Targets layout zones by assuming titles appear in the largest font within the top 20% of the first page, authors sit between the title and abstract, and abstracts are positioned near the top-left or centered blocks.

Regular Expressions (Regex): Matches predictable string structures such as DOIs, emails, publication years, and bracketed citation tokens (e.g., `[1]`).

Section-Heading Detection: Tracks heading text patterns and layout markers to segment monolithic text streams into logical research sections (such as Introduction, Methodology, and References).

LLM-Based Extraction: Passes messy, irregular text chunks (like complex multi-institution author lists or reference bibliographies) to language models using strict schema prompts to extract clean structure.



  3) Comparison and limitations

Accuracy and Reliability: Heuristics and regex are fast and offline-capable, but fail easily against non-standard templates, custom styling, or hyphenated line wraps. Metadata APIs achieve high accuracy for indexed papers, but fail completely if a paper lacks an identifier or is an unindexed preprint.

Difficulty and Performance: Linear text extraction tools fail entirely on multi-column formats. Spatial layout parsers (`PyMuPDF`, `pdfplumber`) successfully handle multi-column flows. LLMs handle varied phrasing well, but introduce compute/token costs and potential structural hallucinations.



  4) Recommended approach

Recommended Strategy:The original report recommends a multi-layered, fallback-driven strategy to avoid relying on a single fragile assumption:

1. Extract layout-aware text using PyMuPDF or pdfplumber, and scan for a DOI or arXiv ID.

2. Query external metadata APIs (CrossRef or Semantic Scholar) to retrieve authoritative metadata if an identifier is found.

3. Fall back to font-size/position heuristics and section-heading detection if no identifier exists.

4. Use targeted LLM parsing for unstructured edge cases like complex affiliation blocks or messy reference sections.



Limitations Requiring Verification: While this hybrid architecture minimizes single points of failure, the reliability of its heuristic and LLM fallback layers still requires empirical validation against your specific local collection of research PDFs.

Scope clarification — researched alternatives not included in the implementation
GROBID, AnyStyle, OCR tools, LLM-based extraction, and text embeddings were considered during the research phase as possible ways to improve PDF processing, reference extraction, and paper discovery. However, these features are not included in the current implementation scope. The project will instead use PyMuPDF for PDF text extraction, heuristic methods for identifying metadata and references, scholarly APIs for metadata enrichment, and YAKE as a fallback for topic-tag extraction. Scanned PDFs without an extractable text layer will be rejected with a clear error message rather than processed using OCR. Semantic search using embeddings and LLM-based extraction will not be implemented.



## 7\. Tagging / topic assignment techniques -> chosen approach

1. Available techniques

Author-provided Keywords: Extracted directly from PDF metadata or header sections.
RAKE: Splits text using stop-word lists and delimiters for co-occurrence scoring
(Rose et al., 2010; CRAN rapidraker Documentation: `[https://www.icesi.edu.co/CRAN/web/packages/rapidraker/rapidraker.pdf]
(https://www.icesi.edu.co/CRAN/web/packages/rapidraker/rapidraker.pdf)`).
YAKE: Unsupervised, graph-free statistical extraction evaluating local document features (Campos et al., 2020; YAKE GitHub: `[https://github.com/INESCTEC/yake](https://github.com/INESCTEC/yake)`; YAKE Documentation Portal: `[https://oss.inesctec.pt/yake/docs/--home](https://oss.inesctec.pt/yake/docs/--home)`).
TF-IDF: Evaluates term specificity across a local document corpus (Sparck Jones, 1972; *Journal of Documentation*, 28(1), 11–21).
Controlled Vocabulary: Curated local lists and taxonomies aligned with ISO 25964 guidelines.
Scholarly Metadata APIs: Queries OpenAlex (`[https://help.openalex.org/data/topics/](https://help.openalex.org/data/topics/)`) and Crossref using document identifiers.

2. Advantages and limitations

Author Keywords: High precision and zero compute overhead; limited by inconsistent availability in older or pre-print documents.
RAKE: Fast and lightweight; sensitive to stop-word quality and layout noise.
YAKE: Robust multi-word phrase extraction without training data or large models; vulnerable to irregular document capitalization.
TF-IDF: Excellent for surfacing terms unique to the local library; fails on isolated single documents without a multi-document corpus.
Controlled Vocabulary: Enforces taxonomy consistency; inflexible to novel or interdisciplinary terms.Scholarly APIs: Yields rich publisher classifications without local compute; failsoffline or when DOIs are missing.

3. Recommended approach

Recommendation: A Hybrid Fallback Pipeline is recommended.
Why: It first attempts high-trust metadata lookups and API queries, falls back to unsupervised YAKE extraction for papers with missing keywords, and normalizes all terms through a controlled vocabulary to prevent tag fragmentation.

4. Practical considerations

Missing Keywords & Inconsistent Terminology: Handled through API fallbacks, YAKE extraction, and controlled vocabulary mapping to prevent duplicate tags.
Storage & Display: Store provenance tracking attributes (`"author"`, `"crossref_api"`, `"openalex_api"`, `"yake_extracted"`, `"controlled_vocab"`) alongside categorical confidence levels (`verified` versus `estimated`). Visually separate them in the UI using solid badges for verified publisher tags and distinct icons or dashed borders for machine-generated suggestions.

## 8\. Knowledge-graph model (nodes, edges, direction, derived edges)

1. Knowledge-graph basics
Nodes: Represent distinct entities or objects within the application domain, such as research papers, authors, topics, and publication venues.
Edges: Represent connections or relationships linking two nodes together.

2. Node types
Paper: Represents a research article, preprint, or publication (attributes include title, abstract, publication year, and DOI).
Author: Represents an individual researcher (attributes include name, institution, and ORCID identifier).
Topic: Represents a subject area, keyword, or field of study (attributes include name and category).
Venue: Represents a journal, workshop, or conference proceedings name.

3. Edge types and direction
Edge name	Meaning
AUTHORED_BY	A paper was written by an author.
HAS_TOPIC	A paper is associated with a topic or tag.
CITES	A paper cites another paper.
CO_AUTHOR	Two authors co-authored a paper.
RELATED_TOPIC	Two topics are related because they occur in the same paper.

4. Derived relationships
Stored and Derived Graph Relationships
The knowledge graph uses three stored relationships: `AUTHORED_BY` connects papers to their authors, `HAS_TOPIC` connects papers to their topics, and `CITES` connects papers to other papers in the library that they cite.
Two additional relationships are derived dynamically when the knowledge graph is generated:
CO_AUTHOR — connects two authors who have co-authored at least one paper in the library. This relationship is derived from the stored paper-author relationships.
RELATED_TOPIC — connects two topics that appear together in at least one paper. This relationship is derived from the stored paper-topic relationships.
The derived relationships are calculated when generating the graph rather than stored separately in the database. This avoids duplicating relationship data and ensures that the graph 
reflects the current library contents.

5. Database representation

Stored in a standard relational database (such as PostgreSQL or SQLite) using two core tables:
nodes Table: Stores `id`, `type`, and a `properties` JSON/JSONB column for attributes like titles, names, and years.
edges Table: Stores `id`, `source_id`, `target_id`, and `relationship_type`.

6. Visualization and data format

Cytoscape.js: Offers layout algorithms and flexible styling; documented at [Cytoscape.js Documentation](https://js.cytoscape.org/) (Cytoscape.js) and [Cytoscape.js Introductory Tutorial](https://blog.js.cytoscape.org/2016/05/24/getting-started/) (Cytoscape.js Blog).
vis-network (Vis.js): Beginner-friendly with built-in interactive physics simulation; documented at [vis-network Documentation](https://visjs.github.io/vis-network/docs/) (Vis.js).
Data format: Expected JSON structure centers on an `elements` object containing separate `nodes` and `edges` arrays using `data` blocks for identifiers, types, labels, sources, and targets.

What I chose : Author provided keywords and YAKE as a fall back option.

## 9\. Edge cases and failure modes the app must handle

1. PDF and Text-Extraction Problems
Multi-line titles: Basic script extractors treat wrapped lines as separate paragraphs, fracturing title strings in the library UI and knowledge graph.
Two-column papers: Standard text dumpers read horizontally across page widths instead of column by column, interweaving sentences into unreadable text.
Scanned PDFs: Image-only historic documents yield zero extracted text, breaking automated metadata extraction and graph generation.
Non-English text: Non-Latin scripts or legacy encodings cause character garbling (mojibake) or tokenization failures.

2. Metadata Problems
Missing abstracts or keywords: Short, editorial, or older papers often omit formal abstract sections or keyword lists, rendering auto-tagging ineffective.
Missing DOIs: Preprints, thesis submissions, and grey literature lack DOIs, breaking API-based metadata lookups.
Missing or incorrect metadata: Embedded PDF file properties often contain placeholder text like "Microsoft Word" or "Admin" rather than true academic metadata (Stack Overflow, *Extracting information from PDFs of research papers*, 2009).
Papers with many authors: Large consortium papers list dozens or hundreds of authors, breaking rigid string fields or UI rendering limits.

3. References and Citations
References split across columns or pages: Bibliographies breaking across page footers or multi-column boundaries interrupt sequential text parsing.
Inconsistent citation formats: Publishers enforce conflicting style guidelines (APA, IEEE, Chicago), causing extreme variance in inline callouts and bibliography entries (Tkaczyk et al., *Machine Learning for Bibliographic Data Extraction*).

4. Duplicate Papers and Uploads
Duplicate uploads: Users import multiple iterations of the same manuscript (e.g., an early arXiv preprint alongside the final published version), cluttering the UI and fracturing
graph connections.

5. Tagging and Knowledge-Graph Problems
Graph fragmentation: Unhandled multi-line titles, author list overflows, and missing abstracts/keywords lead to broken graph nodes, missing edges, and ineffective topic modeling.

6. Recommended Handling
Layout & Extraction: Use GROBID (`[https://grobid.org/](https://grobid.org/)` - GROBID) for machine learning layout analysis (Lopez, *GROBID*, 2008–2026). Employ column-aware tools (`pdfplumber` or `PyMuPDF`) and OCR fallbacks (Tesseract or OCRmyPDF) for scanned documents.
Metadata & References: Disregard raw PDF file properties. Verify metadata using Crossref (`[https://www.crossref.org/](https://www.crossref.org/)` - Crossref) and parse references using specialized tools like AnyStyle (`[https://anystyle.io/](https://anystyle.io/)` - AnyStyle) (Tkaczyk et al.).
Database & Duplicates: Implement nullable schema fields, normalized relational junction tables (`PaperAuthors`), UTF-8 encoding, and content-based duplicate detection (title-author hashes or DOI/arXiv matching). Use exponential backoff for scholarly API rate limits.

## 10\. Sample-paper findings (bonus, if done)
None done

## 11\. What I discarded and why (sifting log)

For Anatomy of a research paper :
-Downstream Knowledge Graph \& Database Ingestion Details :
What was discarded : Node definitions ( Paper, Author, Venue), directed edge schemas ( AUTHORED\_BY, CITES), entity resolution/deduplication workflows, Crossref/OpenAlex API merging, and administrative quarantine queues.  
Reason : Scope limited to Section 2 ("Anatomy of a research paper"), which covers paper structure and PDF extraction rather than downstream database modeling.
-Tool-Specific Implementations \& Deep Model Details :
What was discarded : Specific tool-by-tool comparisons (eg, GROBID vs. CERMINE benchmark scores, TEI XML schema details) and specific machine learning model architectures (Conditional Random Fields, BiLSTM-CRFs, Transformer sequence-labeling configurations).  
Reason : To avoid code/implementation-heavy details while focusing on general extraction principles.
-PDF History \& Low-Level Format Mechanics :
What was discarded : Introductory history on why PDFs were created, internal PDF stream object graphs, character glyph coordinate rendering, and explanations of PDF DocInfovs. XMP metadata layers.  
Reason : Removal of historical background, repetition, and unrelated details.
-Extended Granular Variations :
What was discarded : Exhaustive lists of sub-disciplinary citation formats (eg, Chicago footnotes, MHRA notes, ACS standards) and granular section breakdowns.  
Reason : Compressed into high-level categories (Numeric vs. Author-Date) to maintain brevity while clearly distinguishing typical patterns from universal rules.

For PDF problem :

##12\. Sources (URLs)

For Anatomy of a research paper :
GROBID Guide: https://grobid.org/guides/pdf-metadata-extraction\[cite: 1]
CERMINE Architecture: https://www.researchgate.net/publication/282495770\_CERMINE\_automatic\_extraction\_of\_structured\_metadata\_from\_scientific\_literature\[cite: 9]
Accuracy Study: https://peer.asee.org/examining-accuracy-in-ai-powered-metadata-extraction-for-engineering-education-research.pdf\[cite: 13]
ACS GROBID Study: https://www.acspublisher.com/journals/index.php/lt/article/download/22256/19259/38874\[cite: 2]
IMRaD Guide: https://studypedia.au.dk/en/formal-requirements/imrad-structure\[cite: 3]
Templates: https://trybibby.com/latex/templates\&https://letx.app/templates/journal-articles/  
Reference Extraction: https://arxiv.org/html/2605.08583v2\[cite: 10]
Referencing Styles: https://www.researchgate.net/publication/387754071\_REFERENCING\_AND\_REFERENCING\_STYLES\[cite: 15]
Column Layout: https://blog.jztan.com/multi-column-pdf-reading-order/\[cite: 19]
GROBID Documentation \& Repo: https://grobid.readthedocs.io/en/latest/Training-the-models-of-Grobid/,https://github.com/grobidOrg/grobid  
arXiv Watermarking: https://hongsong-wang.github.io/Watermarking/\[cite: 14]

For the PDF problem :
Primary Technical Documentation \& Specifications
ISO 32000-1 (Adobe PDF Reference):The international standard specification governing PDF architecture, content streams, text positioning operators, and ToUnicode Character Mapping (CMaps).
Official Reference/Access: [PDF Association ISO 32000-1 Resource Guide](https://pdfa.org/resource/iso-32000-1/) or [Adobe PDF Specification Overview](https://www.adobe.com/accessibility/pdf.html).

Python-Based Parsing Libraries
pdfplumber:A Python library built on `pdfminer.six` that extracts detailed spatial metrics, word bounding boxes (`x0, y0, x1, y1`), and layout geometry.
Documentation \& Source: [pdfplumber GitHub Repository](https://github.com/jsvine/pdfplumber).

PyMuPDF (`fitz`): A high-performance Python binding for the MuPDF rendering engine, utilized for rapid text extraction, coordinate inspection, and structure analysis.
Documentation \& Source: [PyMuPDF Official ReadTheDocs](https://pymupdf.readthedocs.io/).

For Citation styles :
Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., \& Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 30, 5998–6008. [https://doi.org/10.48550/arXiv.1706.03762](https://doi.org/10.48550/arXiv.1706.03762)

For Identifiers and metadata APIs:

Crossref REST API: \[Crossref Documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)

OpenAlex API: \[OpenAlex Help Center \& Pricing](https://help.openalex.org/access/pricing/)

Semantic Scholar API: \[Semantic Scholar API Reference](https://api.semanticscholar.org/)

arXiv API: \[arXiv API Terms of Use \& User Manual](https://info.arxiv.org/help/api/tou.html)

For Extraction techniques considered :

\[https://pypi.org/project/pypdf/](https://pypi.org/project/pypdf/)

\[https://pymupdf.readthedocs.io/](https://pymupdf.readthedocs.io/)

\[https://github.com/eriston/PDFPlumber-data-extraction](https://github.com/eriston/PDFPlumber-data-extraction)

\[https://www.crossref.org/documentation/](https://www.crossref.org/documentation/)

\[https://www.semanticscholar.org/product/api%2Ftutorial](https://www.semanticscholar.org/product/api%2Ftutorial)

For Tagging : 
CRAN rapidraker Documentation [https://www.icesi.edu.co/CRAN/web/packages/rapidraker/rapidraker.pdf](https://www.icesi.edu.co/CRAN/web/packages/rapidraker/rapidraker.pdf)
OpenAlex Topics Help [https://help.openalex.org/data/topics/](https://help.openalex.org/data/topics/)
YAKE Documentation Portal [https://oss.inesctec.pt/yake/docs/--home](https://oss.inesctec.pt/yake/docs/--home)
YAKE GitHub Repository [https://github.com/INESCTEC/yake](https://github.com/INESCTEC/yake)
For Knowledge graphs : 
[https://js.cytoscape.org/](https://js.cytoscape.org/) (Cytoscape.js)
[https://blog.js.cytoscape.org/2016/05/24/getting-started/](https://blog.js.cytoscape.org/2016/05/24/getting-started/) (Cytoscape.js Blog)
[https://visjs.github.io/vis-network/docs/](https://visjs.github.io/vis-network/docs/) (Vis.js)

For edge cases :
GROBID (`[https://grobid.org/](https://grobid.org/)`)
Stack Overflow (*Extracting information from PDFs of research papers*, 2009)
Crossref (`[https://www.crossref.org/](https://www.crossref.org/)`)
AnyStyle (`[https://anystyle.io/](https://anystyle.io/)`)
Tkaczyk et al. (*Machine Learning for Bibliographic Data Extraction*)