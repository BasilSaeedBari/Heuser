# User Prompts Log

## PHASE 1

* Tool: Gemini
* Model or mode: Deep Research
* Date: 20 October 2026
* Research question: Research Paper Library & Knowledge Graph
* Exact prompt sent:
[PROMPT 1]
I am researching the domain requirements for a beginner's computer science project: a Research Paper Library and Knowledge Graph. The application will accept academic research papers as PDF files and attempt to extract structured information from them.

Research the typical anatomy of academic research papers.

Please explain:

1. The usual sections of a research paper, their typical order, and what each section contains.
2. Where the title, authors, institutional affiliations, abstract, keywords, publication information, DOI, and references commonly appear.
3. How conference papers, journal papers, and arXiv preprints differ in structure and formatting.
4. Which parts are relatively consistent across papers and which vary between publishers or disciplines.
5. What these variations mean for a program attempting to extract paper metadata automatically.

Use reliable sources and provide source URLs. Give concrete examples where useful. Focus on information that would change the design of a PDF metadata extractor. Avoid lengthy publishing history and unrelated information. Do not write application code.

\[PROMPT 2]
Condense your previous research report into a concise set of findings for Section 2, “Anatomy of a research paper (sections, order, what each contains),” in my Research Paper Library \& Knowledge Graph context document.
Keep ONLY:

1. Common research-paper sections and what they contain.
2. Where titles, authors, affiliations, abstracts, keywords, DOIs and references usually appear.
3. Relevant differences between conference papers, journal papers and arXiv preprints.
4. Important variations in paper structure or formatting.
5. What these findings mean for automatically extracting metadata from PDFs.
Requirements:
* Use clear bullet points under these five categories.
* Aim for approximately 200–300 words total.
* Preserve relevant citations and source URLs from the original report.
* Do not introduce new claims or sources.
* If the original report does not support a claim, leave it out.
* Remove repetition, historical background and unrelated details.
* Clearly distinguish typical patterns from rules that apply to every paper.

\[PROMPT 3]
For my Research Paper Library and Knowledge Graph project, research how academic research papers are represented in PDF files and why extracting their text can be difficult.
Explain:

1. How text and its position are represented in a PDF at a practical level.
2. The difference between a text-based PDF and a scanned PDF.
3. Why two-column layouts can cause text to be extracted in the wrong reading order.
4. How headers, footers, footnotes, equations, ligatures, and hyphenated words can cause extraction errors.
5. How text extraction differs from OCR.
6. Which of these problems a beginner's application should anticipate and how the limitations should be handled.
Give concrete examples of likely extraction errors. Cite reliable technical documentation or research sources. Focus on implications for a Python-based research-paper parser. Do not write application code. Focus on:
* Why PDFs can be difficult to parse.
* What causes incorrect reading order.
* The difference between scanned and text-based PDFs.
* Which problems your application should handle.
don't need a history of the PDF format or a long explanation of how PDF files were invented.

\[Prompt 4]
Condense  previous report for Section 3, “The PDF problem (how text is stored; two-column, scanned, etc.),” in my Research Paper Library \& Knowledge Graph context document.
Keep ONLY information relevant to extracting metadata from research-paper PDFs:

1. How text is stored in text-based PDFs versus scanned/image-based PDFs.
2. Problems caused by two-column layouts, headers and footers, footnotes, equations, ligatures, and words split across lines.
3. How these problems can affect extracting titles, authors, abstracts, keywords, and references.
4. Practical ways to handle or reduce these problems in my application.
Requirements:
* Use concise bullet points under these four categories.
* Aim for approximately 200–300 words total.
* Preserve relevant citations and source URLs from the original report.
* Do not introduce new claims or sources.
* Remove repetition, unrelated background, lengthy technical explanations, and details that are not useful for this project.
* Clearly distinguish common PDF problems from problems that occur only in some documents.

\[PROMPT 5]
For a Research Paper Library and Knowledge Graph application, research the following citation and reference formats: IEEE, APA, MLA, Chicago, and BibTeX.
For each format:

1. Explain how an in-text citation typically looks.
2. Explain how the corresponding bibliography or reference entry is structured.
3. Provide one real, verifiable example of a reference to an actual published work.
4. Identify which fields appear in the reference, such as authors, title, publication venue, year, pages, and DOI, where applicable.
5. Explain how the formats differ and why a PDF parser cannot safely assume every reference follows one format.
Distinguish BibTeX records from the formatted references printed in a paper. Cite reliable sources, including official style guidance where accessible. Verify that the example references correspond to real publications. Do not invent example citations or write application code.

\[PROMPT 6]
Condense your previous research report for Section 4, “Citation styles (IEEE / APA / MLA / BibTeX) - one REAL example each,” in my Research Paper Library \& Knowledge Graph context document.
Keep ONLY the following:

1. IEEE: How the citation style works, what its in-text citations look like, and how a reference-list entry is formatted.
2. APA: The same information.
3. MLA: The same information.
4. BibTeX: What it is, how a BibTeX entry is structured, and how it differs from conventional in-text citation styles.
5. Real examples: Include one genuine, correctly formatted example for each style. Use real sources from the original report, and preserve enough information to identify each source.
6. Relevance to my project: Briefly explain why these citation formats matter when extracting and storing references from research-paper PDFs.
Requirements:
* Use clear headings for IEEE, APA, MLA, BibTeX, and Relevance to the project.
* Aim for approximately 250–350 words total, excluding URLs if necessary.
* Preserve relevant citations and source URLs from the original report.
* Do not invent examples, sources, or bibliographic details.
* Do not introduce new claims or sources.
* Remove repetition, historical background, lengthy explanations, and unrelated details.
* Clearly distinguish in-text citations from bibliography/reference-list entries.
* If the original report does not contain enough information to provide a genuine example for any style, explicitly say what is missing instead of making one up.

\[PROMPT 7]
I am researching identifiers and metadata services for a Research Paper Library and Knowledge Graph application.
Investigate DOI identifiers, arXiv identifiers, and free scholarly metadata APIs.
Please cover:

1. What a DOI and an arXiv ID are, their usual patterns, and where they may appear in a research paper.
2. How DOI and arXiv identifiers can help identify a paper and retrieve metadata.
3. Relevant scholarly metadata APIs, considering Crossref, OpenAlex, Semantic Scholar, and the arXiv API.
4. For each suitable API, provide its official documentation URL, endpoint, authentication requirements, documented rate limits, and relevant terms or usage policies.
5. Explain which fields each service can return, including titles, authors, abstracts, publication dates, identifiers, and references where available.
6. Include a small, trimmed example of an actual or officially documented JSON response. Clearly identify any illustrative examples that are not actual API responses.
7. Explain the limitations of each service, including missing fields, rate limits, and cases where a paper may not be found.
Use official documentation wherever possible. Do not guess current rate limits or claim that every service returns every field. Clearly distinguish verified facts from uncertainty. Do not write application code.  Keep API Name, endpoint, authentication, rate limit, returned fields, limitations. Give a trimmed sample JSON response, should contain a real or officially documented example for the relevant API, with the source identified.

\[PROMPT 8]
Condense your previous research report for Section 5, “Identifiers and metadata APIs,” in my Research Paper Library \& Knowledge Graph context document.
Keep ONLY information relevant to identifying research papers and retrieving their metadata programmatically.
Organize the condensed report into these sections:

1. DOI and arXiv ID patterns: What they look like, how to recognize them, and where they may appear in a research-paper PDF.
2. Metadata APIs: Identify the useful APIs discussed in your original report. For each API, include:
* API/service name and purpose.
* Endpoint or URL template for retrieving paper metadata.
* Whether authentication or an API key is required.
* Rate limits or usage restrictions, if documented.
* The most useful returned metadata fields, such as title, authors, abstract, DOI, publication date, and references.
* A short, trimmed JSON response example, if supported by the original report.
3. Relevance to my application: Briefly explain how these identifiers and APIs could help extract or fill in missing metadata when a PDF is uploaded.
Requirements:
* Aim for approximately 300–450 words, excluding URLs and JSON examples if necessary.
* Use a compact table for comparing APIs where practical.
* Preserve relevant source URLs and citations from the original report.
* Do not introduce new claims, APIs, sources, or examples.
* Do not invent endpoints, authentication requirements, rate limits, JSON fields, or response examples.
* If any required detail was not covered in the original report, label it “Not specified in the original report.”
* Remove repetition, lengthy technical explanations, historical background, and unrelated information.
* Clearly distinguish confirmed API capabilities from limitations or details that still need verification.

\[PROMPT 9]
make metadata apis comparison into a concise bullet points without removing any important information in table

\[PROMPT 10]

For a beginner's Python Research Paper Library and Knowledge Graph project, research techniques for extracting structured information from academic research-paper PDFs.

Compare relevant Python PDF libraries, such as PyMuPDF, pdfplumber, and pypdf. Explain their trade-offs for text extraction, layout information, and two-column papers.

Then investigate approaches for identifying:

\- Paper titles.

\- Authors and affiliations.

\- Abstracts.

\- Keywords.

\- Reference sections and individual references.

Consider font size and position heuristics, regular expressions, section-heading detection, metadata lookup, and LLM-based extraction.

For each approach, explain its strengths, limitations, likely failure cases, and suitability for a small local application.

Recommend a practical strategy that does not depend entirely on one fragile assumption. Cite official library documentation and relevant research. Do not write application code.

\[PROMPT 11]

Condense your previous research report for Section 6, “Extraction techniques considered → which one I chose and why,” in my Research Paper Library \& Knowledge Graph context document.

Keep ONLY information relevant to extracting metadata and text from research-paper PDFs for my Research Paper Library \& Knowledge Graph application.

Organize the condensed report under these headings:

1\. Python PDF extraction libraries: Identify the relevant libraries discussed in your original report, what each can extract, and their main advantages and limitations.

2\. Metadata extraction techniques: Explain the methods discussed for identifying titles, authors, abstracts, keywords, and references. Include relevant approaches such as PDF metadata, font-size and position heuristics, regular expressions, section-heading detection, and external metadata APIs or LLMs, but only if they appeared in the original report.

3\. Comparison and limitations: Summarize the most important trade-offs, including accuracy, reliability, difficulty of implementation, and performance on differently formatted PDFs.

4\. Recommended approach: State which extraction approach the original report recommends, why it is suitable for my application, and any fallback methods or limitations mentioned.

Requirements:

\- Use clear headings and concise bullet points, not tables.

\- Aim for approximately 300–450 words.

\- Preserve relevant citations and source URLs from the original report.

\- Do not introduce new claims, libraries, techniques, or sources.

\- Do not invent performance figures, test results, or capabilities.

\- Remove repetition, historical background, lengthy code examples, and details unrelated to my application.

\- Focus on practical information that will help me decide how my app should extract paper metadata.

\- If the original report does not recommend a specific approach, explicitly state that instead of inventing a recommendation.

\- Clearly distinguish facts from the report's recommendations and any limitations that still need verification.

[PROMPT 12]
Research practical methods for automatically assigning keywords or topics to academic papers in a small Python-based Research Paper Library.
Compare:
1. Using keywords already provided by the paper.
2. RAKE keyword extraction.
3. YAKE keyword extraction.
4. TF-IDF-based keyword selection.
5. Matching against a small controlled vocabulary.
6. Using subject or topic information returned by scholarly metadata services.
For each method, explain how it works, what input it requires, its strengths, limitations, and whether it needs training data, external services, or large model downloads.
Recommend a practical approach for a small local application that must handle papers with missing keywords. Explain how to distinguish automatically extracted keywords from verified subject classifications. Cite reliable documentation or research. Do not write application code. Focus on how each method works, what it requires and what it does well, where it fails, which method and combination makes more sense. Mention sources and urls cited.

[PROMPT 13]
Condense your previous research report for Section 7, “Tagging / topic assignment techniques → chosen approach,” in my Research Paper Library & Knowledge Graph context document.
Keep ONLY information relevant to automatically assigning useful topic tags to research papers in my application.
Organize the condensed report under these headings:
1. Available techniques: Explain the relevant methods discussed in the original report, such as RAKE, YAKE, TF-IDF, keywords provided by the paper's authors, controlled vocabularies, and topics obtained from metadata APIs. Include only techniques covered in the original report.
2. Advantages and limitations: Briefly explain the strengths and weaknesses of each relevant technique, including accuracy, implementation difficulty, computational requirements, and whether it requires downloading a large model, if the original report addresses these points.
3. Recommended approach: State which tagging method or combination of methods the original report recommends for my Research Paper Library & Knowledge Graph application, and explain why.
4. Practical considerations: Include relevant issues such as missing author keywords, irrelevant tags, duplicate tags, inconsistent terminology, and how tags could be stored or displayed, but only if discussed in the original report.
Requirements:
- Use clear headings and concise bullet points. Do NOT use tables.
- Aim for approximately 250–350 words.
- Preserve the original report's citations and source URLs. Include the source name or organization alongside each relevant URL so I can identify where the information came from.
- Keep citations close to the claims they support. If multiple sources support a claim, include the relevant citations and URLs.
- Do not introduce new claims, techniques, sources, or URLs.
- Do not invent source names, citations, or links.
- Remove repetition, historical background, lengthy technical explanations, code examples, and information unrelated to my application.
- Clearly distinguish established findings from recommendations.
- If the original report does not support a specific claim or recommendation, state that the information was not provided rather than making it up.
- Ensure the condensed result retains enough evidence and source information for me to verify the important claims later.

[PROMPT 14]
Research knowledge-graph concepts relevant to a Research Paper Library and Knowledge Graph application.
Explain:
1. What nodes and edges are.
2. The difference between directed and undirected edges.
3. Useful node types for this project, including papers, authors, and topics.
4. Useful relationships, such as written-by, tagged-with, and cites.
5. Which relationships are directly available from paper metadata and which would need to be derived.
6. How these relationships could be represented using relational database tables.
7. JavaScript libraries suitable for displaying interactive graphs in a browser without a build step, considering libraries such as Cytoscape.js and vis-network.
8. The expected node-and-edge JSON structure for the chosen graph library, with a small documented example.
Cite official documentation. Explain the trade-offs and focus on a simple graph that a beginner's application can support. Do not write application code. Focus on definition of nodes, proposed node types, proposed relationship types, which relationships are directed, how relationships will be stored, what format the graph library expects. Mention sources, urls cited.

[PROMPT 15]
Condense your previous research report for Section 8, “Knowledge-graph model (nodes, edges, direction, derived edges),” in my Research Paper Library & Knowledge Graph context document.
Keep ONLY information relevant to designing a knowledge graph for a web application that stores research papers, their authors, topics, and relationships between them.
Organize the condensed report under these headings:
1. Knowledge-graph basics: Briefly explain what nodes and edges represent in this project.
2. Node types: Relevant node types, such as research papers, authors, and topics, including any useful attributes mentioned in the original report.
3. Edge types and direction: Explain the relationships between nodes, whether each relationship should be directed or undirected, and why, based only on the original report.
4. Derived relationships: Explain any relationships that can be inferred from existing data, such as papers sharing an author or topic, if discussed in the original report.
5. Database representation: Summarize how graph entities and relationships could be stored or retrieved using the proposed relational database, if covered.
6. Visualization and data format: Summarize relevant browser-based graph visualization libraries, their official documentation URLs, and the expected node/edge data format, but ONLY if these were discussed in the original report.
Accuracy and source requirements:
- Keep the result around 300–450 words.
- Use clear headings and concise bullet points. Do not use tables.
- Preserve the original report’s citations and all relevant source URLs. Include the source name or organization beside each URL and keep citations close to the claims they support.
- Prioritize official documentation and sources already cited in the original report.
- Do not invent, guess, shorten incorrectly, or fabricate URLs, citations, library features, data formats, or technical claims.
- Do not add new sources or outside knowledge. Base the condensed version strictly on the original report.
- Distinguish sourced facts from recommendations or interpretations.
- If a detail is not supported by the original report, omit it or explicitly write “Not specified in the original report.”
- Remove repetition, unrelated graph theory, lengthy examples, and background material that does not help design this application.
- Before finalizing, check that every retained technical claim is supported by the original report and that every cited URL is copied accurately.
Return ONLY the condensed report, ready to paste into my context document.

[PROMPT 16]
For a beginner's Research Paper Library and Knowledge Graph application, identify realistic edge cases that could cause PDF metadata extraction, tagging, metadata lookup, storage, or graph generation to fail.
Investigate:
- Missing abstracts or keywords.
- Multi-line titles.
- Papers with many authors.
- Non-English text.
- Papers without DOIs.
- Scanned PDFs.
- Two-column papers.
- References split across columns or pages.
- Inconsistent citation formats.
- Missing or incorrect metadata.
- Duplicate uploads.
- Scholarly APIs returning no result or an error.
For each case, explain what could go wrong, why it happens, and a reasonable way for a small application to handle it.
Prioritise realistic cases that affect the core requirements. Cite reliable sources where appropriate, distinguish documented behaviour from recommendations, and do not write application code. Mention URLS and sources cited.

[PROMPT 17]
Condense your previous research report for Section 9, “Edge cases and failure modes the app must handle,” in my Research Paper Library & Knowledge Graph context document.
Keep ONLY information relevant to potential problems when building a web-based Research Paper Library & Knowledge Graph that uploads research-paper PDFs, extracts metadata and references, assigns topic tags, stores papers in SQLite, and displays search results and a knowledge graph.
Organize the condensed report under these headings:
1. PDF and text-extraction problems: Missing or corrupted text, scanned PDFs, two-column layouts, unusual formatting, equations, ligatures, and broken or hyphenated words, but only where covered in the original report.
2. Metadata problems: Missing titles or abstracts, multiple or unusually formatted authors, missing DOI/arXiv identifiers, incomplete metadata, and inconsistent metadata from different sources.
3. References and citations: References that span multiple lines or columns, inconsistent citation formats, incomplete references, and difficulties identifying individual references, if discussed.
4. Duplicate papers and uploads: Duplicate detection, repeated uploads, different versions of the same paper, and related problems, if discussed.
5. Tagging and knowledge-graph problems: Missing or inconsistent keywords, duplicate tags, ambiguous relationships, missing graph connections, and incorrect or misleading edges, if discussed.
6. Recommended handling: Summarize the solutions, fallback strategies, or error-handling approaches suggested by the original report. Do not invent solutions if the report does not provide them.
Accuracy and source requirements:
- Keep the result around 300–450 words.
- Use clear headings and concise bullet points. Do not use tables.
- Preserve the original report’s citations and relevant source URLs. Include the source name or organization beside each URL, and keep citations close to the claims they support.
- Retain sources that directly support important failure modes or suggested handling strategies.
- Do not invent, guess, or fabricate technical claims, citations, source names, or URLs. Copy URLs accurately from the original report.
- Do not add outside sources or new information. Base the summary strictly on the original report.
- Clearly distinguish findings supported by sources from recommendations or interpretations.
- If a listed issue or solution was not covered in the original report, omit it or state “Not specified in the original report.”
- Remove repeated explanations, unrelated edge cases, lengthy examples, and background information that does not help identify or handle problems in this application.
- Before finalizing, verify that each retained technical claim is supported by the original report and that every cited source and URL is preserved accurately.
Return ONLY the condensed report, ready to paste into my context document.

### Summary of result

### What I kept

Core Anatomy \& Section Progression : The functional breakdown of Front Matter, Core Body (IMRaD framework), and Back Matter, along with explicit distinctions between standard layout patterns and universal rules.
Spatial Geolocation Rules : The standard physical locations of key fields on PDF pages—such as top-page placement for titles and authors, bottom margins/headers for DOIs, and terminal sections for bibliographies.
Venue \& Repository Characteristics : Key structural features across major publishers and preprint servers, including IEECondense your previous research report for Section 8, “Knowledge-graph model (nodes, edges, direction, derived edges),” in my Research Paper Library & Knowledge Graph context document.
E two-column grids, ACM taxonomy blocks, Springer LNCS single-column layouts, and arXiv margin watermark stamps.
Structural \& Typographical Variations : Critical layout variations, such as Numeric vs. Author-Date citation systems, multi-column grids, and complex author-to-institution mapping methods.  
PDF Metadata Extraction Implications : High-priority engineering requirements for PDF parsing, including spatial gutter detection for multi-column reading order, line-wrap repair, the unreliability of native PDF DocInfo/ XMPstreams, and cascaded machine learning extraction models.  
Grounding Citations \& Source URLs : All key citations and primary repository/documentation URLs directly backing these extraction rules.

Text vs. Scanned: Digital-native PDFs store structured text and ToUnicode maps (ISO 32000-1); scanned PDFs are unsearchable images requiring OCR.
Structural Problems:
Common: Two-column layouts (misordered text streams), running headers/footers, hyphenated line breaks, and font ligatures.
Specific: Floating footnotes and fragmented mathematical equations.
Metadata Impact: These anomalies corrupt first-page title/author blocks, scramble abstracts/keywords, and break bibliographic reference strings.
Practical Solutions: Use Python layout parsers (`pdfplumber`, `PyMuPDF`) to filter margins, track bounding-box coordinates (x, y) for column sorting, and apply regex for hyphen clean-up.

When condensing the section, I retained the core structural information and verifiable data, specifically:
Key Mechanics for IEEE, APA, and MLA: Kept each style operates, their specific in-text citation format, and the general template for reference entries.
BibTeX Core Definition: Retained the definition of BibTeX as a structured key-value data format and how it differs from static printed citation strings.
Verifiable Real Example: Preserved the single real publication example (*Vaswani et al., 2017*) formatted across IEEE, APA, MLA, and BibTeX, including its DOI.
Project Relevance: Summarized why citation format variability creates parsing challenges during PDF reference extraction and graph linking in your application.
All historical background, the Chicago style section, non-essential commentary, and detailed field-by-field lists were removed.

When condensing the API comparison from a table into bullet points, every core operational attribute for each service was fully retained without losing data. Specifically, the following five attributes were kept for all four APIs (Crossref, OpenAlex, Semantic Scholar, and arXiv):
Purpose: What the service provides.
Endpoint / URL Template: The exact API route for fetching metadata.
Authentication: Whether an API key or polite header is needed.
Rate Limits / Restrictions: Throttling rules and usage limits.
Returned Metadata Fields: Specific data points provided (such as titles, authors, abstracts, identifiers, and references).

Libraries: The comparison of `pypdf`, `PyMuPDF`, and `pdfplumber` focusing on layout handling, speed, and multi-column parsing.

Techniques: Core methods for extracting metadata (APIs, font/position heuristics, regex, section headers, and LLMs).

Trade-offs: Accuracy, reliability, and limitations of each method on academic documents.

Recommendation: The multi-layered hybrid strategy combining spatial parsing, metadata APIs, heuristic fallbacks, and targeted LLM extraction.

### What I discarded and why

\-Downstream Knowledge Graph \& Database Ingestion Details :
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

Source Citations/Attributions: The explicit parenthetical reference line at the bottom pointing to ISO 32000-1 and library docs was dropped to maximize brevity.
Common vs. Specific Classifications: The sub-categorization separating "common" issues (two-column layouts, hyphens) from "specific" ones (footnotes, equations) was streamlined into a single combined bullet point to save space.

Chicago Style Section: Omitted entirely because the prompt specifically requested coverage for IEEE, APA, MLA, and BibTeX only.
Granular Field-by-Field Breakdown (Section 4): Removed the standalone bulleted lists identifying individual fields (authors, title, volume, pages, etc.) to eliminate redundancy, as these components are already visible within the templates and real examples.
Expanded Comparison Table \& Multi-Section Analysis: Omitted the summary comparison table and multi-paragraph layout comparisons to stay strictly within the 250–350 word length constraint.
Detailed Parsing/Layout Edge Cases: Stripped out lengthy explanations regarding PDF multi-column layouts, font size shifts, and journal abbreviation ambiguities, summarizing the core challenge in a brief "Relevance to the project" section.
Background \& Formal Source List: Excluded general introductory text, domain descriptions, and the standalone list of official style manual references to focus purely on actionable style definitions and examples.

Lengthy Background \& Definitions: Explanations of IDF governance, historical arXiv naming pre-2007, and broad theoretical explanations of metadata seeding to focus strictly on actionable extraction rules.

Redundant Formatting \& Structural Text: Descriptive table headers, repetitive preamble/transitional phrasing, and redundant category labels to maximize scannability.

Non-Essential Metadata Fields: Secondary identifiers not core to basic paper identification (e.g., volume/issue numbers, publisher names, and broad topic taxonomies) to prioritize essential fields (titles, authors, abstracts, dates, core IDs, and references).

Application Code \& Detailed Architectural Specs: Step-by-step parsing pipelines and implementation logic (omitted per prompt constraints).

Why: To strip away conversational filler, historical background, and redundant metadata, delivering a streamlined reference tailored directly to automating metadata extraction and Knowledge Graph ingestion.

Granular element-by-element failure cases: Specific, individual challenges for each metadata field (e.g., exact failure scenarios for keywords or individual reference lines).

Markdown tables: Replaced the structured comparison matrices with concise bullet points.

Conversational framing and background narrative: Introductory remarks, closing encouragement, and general prose about the inherent difficulty of parsing PDFs.

Why: To eliminate redundancy, remove non-essential context, and fit the strict constraints of a concise, practical technical documentation section focused purely on decision-making.

### Sources returned:

https://www.researchgate.net/publication/282495770\_CERMINE\_automatic\_extraction\_of\_structured\_metadata\_from\_scientific\_literature
https://grobid.org/guides/pdf-metadata-extraction
https://www.editage.com/blog/imrad-paper-example-structure-outline/
https://www.researchgate.net/publication/342914436\_A\_Systematic\_Approach\_to\_Map\_the\_Research\_Articles'\_Sections\_to\_IMRAD
https://studypedia.au.dk/en/formal-requirements/imrad-structure

ISO 32000-1:2008. \*Document Management — Portable Document Format. [ISO 32000-1 Specification](https://cdn.standards.iteh.ai/samples/51502/a0f48fe34d5e43989cde77ca2e3e951d/ISO-32000-1-2008.pdf)
`pdfplumber` Python Library Documentation. [pdfplumber on PyPI](https://pypi.org/project/pdfplumber/)
`PyMuPDF` (`fitz`) Documentation. [PyMuPDF ReadTheDocs](https://pymupdf.readthedocs.io/)
Boukhers, Z., \& Bouabdallah, A. (2022). Vision and natural language for metadata extraction from scientific PDF documents. \*Proceedings of the 22nd ACM/IEEE Joint Conference on Digital Libraries. [DOI: 10.1145/3529372.3533295](https://doi.org/10.1145/3529372.3533295)
GROBID Community. (2026). *A Practical Guide to PDF Metadata Extraction*. [GROBID Guides](https://grobid.org/guides/pdf-metadata-extraction)

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., \& Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 30, 5998–6008. [https://doi.org/10.48550/arXiv.1706.03762](https://doi.org/10.48550/arXiv.1706.03762)

Crossref REST API: \[Crossref Documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)

OpenAlex API: \[OpenAlex Help Center \& Pricing](https://help.openalex.org/access/pricing/)

Semantic Scholar API: \[Semantic Scholar API Reference](https://api.semanticscholar.org/)

arXiv API: \[arXiv API Terms of Use \& User Manual](https://info.arxiv.org/help/api/tou.html)

\[https://pypi.org/project/pypdf/](https://pypi.org/project/pypdf/)

\[https://pymupdf.readthedocs.io/](https://pymupdf.readthedocs.io/)

\[https://github.com/eriston/PDFPlumber-data-extraction](https://github.com/eriston/PDFPlumber-data-extraction)

\[https://www.crossref.org/documentation/](https://www.crossref.org/documentation/)

\[https://www.semanticscholar.org/product/api%2Ftutorial](https://www.semanticscholar.org/product/api%2Ftutorial)
CRAN rapidraker Documentation [https://www.icesi.edu.co/CRAN/web/packages/rapidraker/rapidraker.pdf](https://www.icesi.edu.co/CRAN/web/packages/rapidraker/rapidraker.pdf)
OpenAlex Topics Help [https://help.openalex.org/data/topics/](https://help.openalex.org/data/topics/)
YAKE Documentation Portal [https://oss.inesctec.pt/yake/docs/--home](https://oss.inesctec.pt/yake/docs/--home)
YAKE GitHub Repository [https://github.com/INESCTEC/yake](https://github.com/INESCTEC/yake)
[https://js.cytoscape.org/](https://js.cytoscape.org/) (Cytoscape.js)
[https://blog.js.cytoscape.org/2016/05/24/getting-started/](https://blog.js.cytoscape.org/2016/05/24/getting-started/) (Cytoscape.js Blog)
[https://visjs.github.io/vis-network/docs/](https://visjs.github.io/vis-network/docs/) (Vis.js)
GROBID (`[https://grobid.org/](https://grobid.org/)`)
Stack Overflow (*Extracting information from PDFs of research papers*, 2009)
Crossref (`[https://www.crossref.org/](https://www.crossref.org/)`)
AnyStyle (`[https://anystyle.io/](https://anystyle.io/)`)
Tkaczyk et al. (*Machine Learning for Bibliographic Data Extraction*)

## PHASE 2

* Tool: Perplexity
* Model or mode: Model
* Date: 21 October 2026
* Research question: Research Paper Library & Knowledge Graph
* Exact prompt sent:

[PROMPT 1]
Research the current technology options for a small web application built with Python, SQLite, and a vanilla HTML/CSS/JavaScript frontend.

Compare Flask, FastAPI, and any other genuinely suitable lightweight Python web framework. Which is the best fit for this specific project: a small Research Paper Library & Knowledge Graph that serves static frontend files, accepts PDF file uploads, and exposes backend API endpoints?

Report:
1. The current stable version of each relevant framework and its release date, if available.
2. Whether it can serve static files, accept uploaded files, and provide API endpoints.
3. Any important upload-size, file-handling, or CORS considerations.
4. The advantages and disadvantages of the options for this project.
5. Your recommendation and why it is preferable to the alternatives.
Cite official documentation and official package-index pages. Include the exact source URLs. Do not invent version numbers or features; distinguish verified facts from recommendations.

[PROMPT 2]
why choose FAST API over other alternatives (summarise concisely and accurately and shortly), as well as give official url separately

What I kept :
Important information relevant to the library that I wish to create.


What I discarded and why :
Alternative options as they did not fit the library I wish to create, such as bottle and flask.



Sources returned :
FastAPI static files: 
https://fastapi.tiangolo.com/tutorial/static-files/
FastAPI file uploads: 
https://fastapi.tiangolo.com/tutorial/request-files/
FastAPI CORS: 
https://fastapi.tiangolo.com/tutorial/cors/
FastAPI on PyPI: 
https://pypi.org/project/fastapi/


[PROMPT 3]
Compare PyMuPDF, pdfplumber, and pypdf for extracting text from research-paper PDFs in Python.

This application needs to extract titles, authors, abstracts, and references from research papers, including papers with two-column layouts.

For each relevant library, report:
1. Its current stable version and whether it is actively maintained.
2. Its capabilities for text extraction, page layout, text blocks, and positional information.
3. How suitable it is for two-column research papers.
4. Important limitations and trade-offs.
5. Whether PyPDF2 is deprecated, renamed, or otherwise not recommended, with reliable evidence.
Recommend one primary library for this project and explain why. Use official documentation, release information, and official package-index pages. Include exact source URLs and do not guess versions or claim that any library perfectly handles two-column PDFs.

[PROMPT 4]
why choose PyMuPDF over other alternatives (summarise concisely and accurately and shortly), as well as list official url and sources cited and used separately

What I kept :
Important information relevant to the library that I wish to create.


What I discarded and why :
Alternative options as they did not fit the library I wish to create, such as pdfplumber and pypdf

Source urls : 
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

[PROMPT 5]
Research how a Python web application can retrieve research-paper metadata from Crossref, Semantic Scholar, OpenAlex, and arXiv.

Also compare suitable Python HTTP client libraries, such as requests and httpx, for making these API requests.

For each metadata service, provide:
1. The official API documentation URL and exact endpoint(s) relevant to searching for a paper or retrieving metadata by DOI or arXiv ID.
2. Whether authentication or an API key is required, and under what circumstances.
3. Current documented rate limits or usage restrictions.
4. The relevant response format and the fields available for title, authors, abstract, DOI/arXiv ID, publication date, and references, where supported.
5. A short, valid JSON response example based on official documentation or a real documented response. Clearly identify any fields that are unavailable or not consistently provided.
Compare requests and httpx, including current stable versions and relevant trade-offs. Recommend an appropriate HTTP client and explain which metadata sources would be useful for this project.

Cite official documentation and include exact URLs. Do not fabricate endpoints, API limits, JSON responses, or metadata fields. State when information is unavailable or could not be verified.

[PROMPT 6]
why choose httpx and which field would you recommend over other alternatives (summarise concisely and accurately and shortly), as well as list official url  and sources cited and used separately and no tables, explain briefy in bullet points

What I kept :
Important information relevant to the library that I wish to create.


What I discarded and why :
Alternative options as they did not fit the library I wish to create, such as requests.

source url :
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

[PROMPT 7]
Research Python libraries and approaches for automatically assigning topic tags to research papers in a small application.

Consider YAKE, RAKE, TF-IDF-based keyword extraction, author-provided keywords, and topic metadata from scholarly APIs, but only recommend approaches that are appropriate for this project.

For the relevant options, explain:
1. Whether a maintained Python library is available and its current stable version.
2. How the technique extracts or obtains keywords.
3. Its advantages, limitations, and implementation complexity.
4. Whether it requires downloading a large machine-learning model or additional data.
5. How it could handle papers without author-provided keywords.
Recommend a practical tagging approach for a small research-paper library, explaining the trade-offs. Cite official documentation or package-index pages and include exact URLs. Verify maintenance and version information. Do not invent benchmark results or claim that keyword extraction always produces accurate tags.

[PROMPT 8]
why choose author-provided keywords(model as well) (summarise concisely and accurately and shortly), as well as list official url  and sources cited and used separately and no tables, explain briefy in bullet points

What I kept :
Important information relevant to the library that I wish to create.


What I discarded and why :
Alternative options as they did not fit the library I wish to create, such as RAKE, YAKE ETC.


Source url :
YAKE on PyPI — 
https://pypi.org/project/yake/
OpenAlex API endpoints — https://help.openalex.org/api/endpoints/
Semantic Scholar API reference — 
https://api.semanticscholar.org/api-docs

[PROMPT 8]
Research the recommended way to access SQLite from Python for a small Research Paper Library & Knowledge Graph application.

Compare Python's standard-library sqlite3 module with a suitable ORM, such as SQLAlchemy, if relevant.

Report:
1. Whether sqlite3 requires an additional installation and what SQLite operations it supports.
2. The current stable version of the ORM you compare, if applicable, and its advantages and disadvantages.
3. How parameterized SQL queries prevent SQL injection, with a short example from official documentation if available.
4. How database connections, transactions, and foreign-key constraints should be handled, if covered by the documentation.
5. Which option is the simplest suitable choice for this project's small relational database, and why.
Prefer official Python documentation and official project documentation. Include exact source URLs. Clearly distinguish documented facts from your recommendation. Do not invent version numbers or security guarantees.

[PROMPT 9]
why choose Python's built in sqlite3 (model as well) (summarise concisely and accurately and shortly), as well as list official url  and sources cited and used separately and no tables, explain briefy in bullet points

What I kept :
Important information relevant to the library that I wish to create.


What I discarded and why :
Alternative options as they did not fit the library I wish to create, such as SQL Alchemy

Source urls :
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


[PROMPT 10]
Compare vis-network and Cytoscape.js for visualizing a knowledge graph in a frontend built with vanilla HTML, CSS, and JavaScript, without npm, Node.js, or a build step.

For each relevant option, report:
1. Its current stable version.
2. The exact pinned jsDelivr CDN URL for that version.
3. Whether a separate CSS file is required and the exact URL, if applicable.
4. The required JavaScript data format for nodes and edges, with a small example based on research papers, authors, and topics.
5. Relevant features, limitations, and trade-offs for an interactive graph.
6. Whether it can be used directly in a plain HTML page without a package manager.
Recommend one option for this project and explain why. Use official documentation and official release information where available. Include exact source URLs. Do not invent version numbers, CDN URLs, or data-format requirements. Verify that the proposed CDN URL corresponds to the stated version.

[PROMPT 11]
why choose Cytoscape.js (model as well) (summarise concisely and accurately and shortly), as well as list official url  and sources cited and used separately and no tables, explain briefy in bullet points

What I kept :
Important information relevant to the library that I wish to create.


What I discarded and why :
Alternative options as they did not fit the library I wish to create, such as vis-network.

Source urls :
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



## PHASE 3

* Tool: Claude
* Model or mode: Sonnet 5.5
* Date: 22 October 2026 (Time : 8:07 am)
* Research question: Planning
* Exact prompt sent:

[PROMPT 1]
The code will be written by Qwen 2.5 Coder 7B, a small model with a limited effective context. Each prompt must therefore be self-contained, produce one file or one small group of functions, and state all interfaces explicitly.” I need you to **revise and complete my Phase 3 deliverable for Homework 5**. I have attached three files:

1. **`Homework_5.pdf`** — the original assignment instructions. This is the authoritative source for what I must submit.
2. **`Deliverable_1_CONTEXT_[HeUserID].md`** — my Phase 1 research and context document. Use this as the source for my project requirements, research findings, and decisions.
3. **`Phase3_Planning_Sections_DRAFT.md`** — your previous draft. Use it as a starting point, but it is not automatically correct or complete.

## Main objective

Produce a complete, accurate, submission-ready **`Deliverable_2_PLAN_AND_PROMPTS_[HeUserID].md`** that satisfies the Phase 3 requirements in `Homework_5.pdf`.

Do not merely critique the draft or give me instructions for fixing it. **Actually revise and write the complete document.**

## Step 1 — Read and verify the sources first

Before writing, carefully inspect the relevant Phase 3 instructions in `Homework_5.pdf`, especially the requirements for Deliverable 2, and compare them with both Markdown files.

Follow these rules:

- The assignment PDF determines the required sections, deliverables, constraints, and expected level of detail.
- My Phase 1 document is the source of my actual research and project decisions.
- The previous draft is only a draft. Do not assume its claims about my Phase 1 document are correct.
- Do not claim that I researched, selected, rejected, or recommended a technology unless the source files support that claim.
- Do not silently invent project requirements, research findings, test results, or implementation decisions.
- Where information is missing, identify the gap and make a clearly labelled, conservative proposal only when necessary to complete the plan.
- Keep the implementation realistic for the assignment and the specified local coding model.

If you cannot access or read a file, tell me exactly which file or section is inaccessible. Do not pretend you inspected it.

## Step 2 — Correct the known issues

Check and resolve the following issues while revising the document:

**C1. PyMuPDF:** Use the correct package name and verify its exact version, purpose, licence information, and official source URL. Do not confuse it with PyPDF or PyPDF2.

**C2. FastAPI:** Supply a verified, exact version. A description of its architecture is not a version number.

**C3. Missing dependencies:** Account for Uvicorn, the ASGI server, and `python-multipart`, required for FastAPI file uploads. Include them in the technology stack and planned `requirements.txt` if the chosen implementation uses them.

**C4. YAKE:** Keep YAKE as a fallback keyword-extraction method unless the source material gives a compelling reason not to. Make the tagging priority explicit:
1. Keywords supplied by the paper's author, where available.
2. Topic information returned by a scholarly API, where available.
3. YAKE keyword extraction as a fallback when suitable keywords or topics are unavailable.

Ensure the actual implementation plan agrees with this priority.

**C5. Cytoscape.js:** Verify the exact version and use a version-pinned CDN URL. Do not use an unpinned `latest` URL or state an unverified release date.

**C6. HTTPX:** Verify the exact version and explain its purpose in the chosen architecture.

**C7. Python and SQLite:** Specify the intended Python version. Explain that SQLite is accessed through Python's standard-library `sqlite3` module and should not be listed as a separate pip dependency. Verify any SQLite runtime version you choose to state.

**C8. Graph relationship names:** Use consistent relationship names throughout the design, database, API, and graph mapping:
- `AUTHORED_BY`: a paper is associated with its author.
- `HAS_TOPIC`: a paper is associated with a topic.
- `CITES`: a paper references another paper that can be matched to a paper in the library.
- `CO_AUTHOR`: derived relationship between authors who co-authored at least one paper in the library.
- `RELATED_TOPIC`: derived relationship between topics that occur together in at least one paper.

Make clear which relationships are stored and which are derived. `CO_AUTHOR` and `RELATED_TOPIC` may be calculated when building the graph rather than stored as redundant database records, provided the design explains this consistently. Do not invent citation matches where none can be established.

**C9. Scholarly API limits, terms, and licensing:** Correct the discussion of Crossref, arXiv, Semantic Scholar, and OpenAlex using official documentation. Distinguish request-rate limits from usage budgets, explain any relevant API-key requirements, include caching and sensible handling of rate-limit responses, and discuss metadata reuse/licensing where relevant. Include direct source URLs. Do not present uncertain or outdated limits as verified facts.

**C10. Scope consistency:** Check my actual Phase 1 document before claiming that I proposed GROBID, AnyStyle, OCR, LLM-based extraction, embedding-based relationships, or other technologies. If these appear only as research alternatives, distinguish them from the technologies selected for implementation. If they do not appear in my document, do not attribute them to me. Keep Phase 3 consistent with the requirements and decisions actually supported by the files.

**C11. Empty project summaries:** Complete the project overview in Phase 1 only if that is within the scope of this task; otherwise, use the Phase 1 document's supported information to write the overview required in Phase 3 Section A. Describe planned functionality accurately without implying that the application has already been built.

## Step 3 — Follow the assignment's required Deliverable 2 structure

Use these sections, in this order, and satisfy the specific requirements stated in the PDF:

### A. Overview and key design decisions
Summarise the project, its intended users and functionality, the chosen architecture, and the main design decisions. Distinguish confirmed requirements from proposals.

### B. Technology stack
Provide a table containing:
- Technology/package
- Exact version
- Purpose
- Why it was selected
- Official source URL

Verify exact versions using official package pages, release pages, or documentation. Include all dependencies the implementation genuinely needs. Keep the technology stack and `requirements.txt` consistent.

### C. Architecture
Provide a complete file and folder tree, with a one-line purpose for every planned file. Explain the data flow:

**PDF upload → text extraction → metadata parsing → scholarly API enrichment → topic tagging → database storage → search/filtering and graph generation.**

Make sure the architecture agrees with the actual technology choices and does not include unplanned services or libraries.

### D. Database schema
Provide complete, executable SQLite `CREATE TABLE` statements, not merely descriptions or pseudocode. Include:
- Primary keys and foreign keys
- Appropriate uniqueness constraints
- Necessary indexes
- The activity log
- Consistent relationships between papers, authors, topics, citations, and any other entities required by the chosen design

Explain how duplicates are identified and handled. Ensure the schema is compatible with the planned backend and API.

### E. API contract
Define each planned endpoint with its HTTP method, path, purpose, request format, example response JSON, and relevant error responses. Include the endpoints needed for the required application features. Make sure the contracts match the database schema and frontend.

### F. Frontend specification
Describe the required views and their functionality, high-level DOM structure, and interaction flow. Include the exact version-pinned Cytoscape.js CDN script tag and explain how backend graph data maps to Cytoscape.js nodes and edges. Ensure the frontend can communicate with the planned backend.

### G. Build order and dependencies
Give a realistic, numbered implementation order. Identify which files or components depend on others, so the work can be built and tested incrementally.

### H. Prompts for Qwen 2.5 Coder 7B
This section is particularly important. Write the **actual, paste-ready prompts**, not advice about what the prompts should contain.

Assume I will use Qwen 2.5 Coder 7B, which has limited context. Therefore:

- Each prompt must be independently pasteable into a fresh conversation.
- Each prompt must include the context needed for its specific task; do not rely on Qwen remembering previous prompts.
- Give each prompt a number, objective, target file(s), and clear scope.
- Include the role, objective, relevant project context, constraints, interfaces, required steps, output format, and acceptance test.
- Ask Qwen to produce only the requested file or small, clearly defined group of functions.
- Tell Qwen not to invent additional requirements, dependencies, endpoints, schema fields, or features.
- Keep prompts small enough for a 7B model to handle reliably. Split complicated work into smaller prompts rather than asking it to build the entire application at once.
- Specify exact filenames and expected function signatures or endpoint contracts where applicable.
- Ensure prompts are ordered according to Section G and agree with Sections B–F.
- Include explicit instructions to use only the chosen dependencies and avoid Node.js, npm, React, or a frontend build step unless the assignment explicitly requires otherwise.
- Include an acceptance test or concrete verification checklist for each prompt.
- Avoid having different prompts generate conflicting versions of the same file. Explain when a later prompt is allowed to modify an existing file.
- Include prompts for the database, backend endpoints, PDF parsing, scholarly API enrichment, topic tagging, frontend, graph generation, and testing as appropriate to the final architecture.

Every prompt must contain enough relevant information to be used by itself. Do not replace the actual prompts with summaries, templates, or placeholders.

### I. Build log
Include a blank table to complete during Phase 4 with these columns:

`Prompt # | Attempts | Result | What I changed in the prompt`

Do not fabricate attempts or results.

### J. Manual-edit log
Include a blank table to complete during Phase 4 with these columns:

`File | What was changed | Why`

Do not invent manual edits that have not happened.

## Step 4 — Technical and factual verification

Research current official documentation where necessary, especially for exact package versions, API limits, licensing, and CDN URLs.

- Prefer official documentation, official package indexes, official repositories, and official release pages.
- Cite claims that depend on external research with direct source URLs.
- Make it clear when a fact is verified, when a design choice is a proposal, and when information remains uncertain.
- Do not invent citations or URLs.
- Do not use a version number merely because it appeared in your previous draft.
- Use exact pinned versions consistently in the technology table, dependency file, and frontend script tags.
- Do not add a separate pip dependency for Python's built-in `sqlite3` module.

## Step 5 — Final consistency audit

Before presenting the result, check that:

1. All required sections A–J exist in the correct order.
2. The document satisfies the actual assignment instructions.
3. The design, schema, API, frontend, build order, and Qwen prompts agree with one another.
4. Every dependency used in the plan appears in the stack and planned `requirements.txt`.
5. Every listed dependency has a justified purpose.
6. Database table and column names match the API and code-generation prompts.
7. All relationship names are consistent.
8. The Qwen prompts are genuinely paste-ready and independently understandable.
9. No build logs, implementation results, or manual edits have been fabricated.
10. No research or decisions have been falsely attributed to my Phase 1 document.
11. The output is a complete Markdown document that I can save as `Deliverable_2_PLAN_AND_PROMPTS_[HeUserID].md`.

**Deliver the revised Markdown document itself.** If you can create a downloadable Markdown file, do so. After the document, briefly list any unresolved decisions or facts you could not verify. Do not replace the deliverable with a general explanation of what I should do next.
(I sent deliverable context 1 and deliverable 2 plans and prompts alongside homework 5 file)



