# **Project: Research Paper Library and Knowledge Graph** 

## **1. Aim and Purpose:-** 

This project involves building a web application that allows users to upload, organize, search, and manage academic research papers. The application will extract information from PDFs, assign topic tags, store paper details in a database, and display connections between papers, authors, and topics in a knowledge graph. 

_The application will use Python for the backend, SQLite for the database, and HTML, CSS, and JavaScript for the frontend._ 

## **2. Anatomy of an Academic Research Paper** 

Academic research papers commonly include a title, author names, an abstract, keywords, the main body, and references. Many empirical science papers follow the IMRAD structure: Introduction, Methods, Results, and Discussion. Some papers also include affiliations, publication dates, journal or conference details, acknowledgements, funding information, and appendices. 

For this application, the initial metadata fields should include the paper title, authors, abstract, keywords or topics, DOI, publication date, and publication venue. These fields support searching, filtering, citation generation, and connections between papers, authors, and topics. 

Not every research paper follows the same structure, so extracted fields should be allowed to remain empty when information cannot be identified confidently. 

## **3. Problems with Extracting Information from PDFs** 

Extracting information from research-paper PDFs can be difficult because PDFs are designed to preserve page appearance rather than always store text in a simple reading order. 

Common problems include: 

- Two-column layouts: Text from the columns may be extracted in the wrong order. 

- Scanned PDFs: Some PDFs contain page images rather than selectable text, so Optical Character Recognition (OCR) may be needed. 

- Missing or incorrect text: Unusual fonts, mathematical symbols, tables, and encoding problems can affect extraction. 

- Reading order: Titles, headings, footnotes, and references may be mixed together. 

- Incomplete metadata: A PDF may not contain a DOI, publication date, or other useful information in an easily extractable form. 

For this project, the application should check whether text was extracted successfully and handle missing information without crashing. Scanned PDFs should be identified as a possible special case, rather than assuming every PDF can be processed in the same way. 

## **4. Citation Styles** 

Research papers use different citation styles depending on their subject area, publisher, or institution. The library should store a paper’s metadata separately from its formatted citation so that references can be generated in different styles. 

- APA: Commonly used in psychology and social sciences. It often uses author and year in in-text citations. 

- MLA: Commonly used in literature and the humanities. It commonly uses the author’s name and a page number for in-text citations when applicable. 

- IEEE: Commonly used in engineering and computing. It uses numbered citations in square brackets, linked to numbered references. 

- BibTeX: A structured format used with LaTeX to store bibliographic information and generate references. 

A reference may require the author, title, publication year, journal or conference name, volume, issue, page range, and DOI, depending on the source and citation style. 

Implementation decision: Store the available bibliographic fields in SQLite and generate formatted citations from those fields when possible. If required information is missing, the application should avoid inventing it and should indicate that the citation may be incomplete. 

Verification needed: Before submission, add one accurate, source-checked reference example for each style using the relevant official style guidance. 

## **5. Identifiers and Metadata APIs** 

A Digital Object Identifier (DOI) is a persistent identifier used to identify a digital object, such as a research paper. A DOI can help the application look up publication metadata when the PDF contains a DOI. 

Crossref provides a REST API for retrieving bibliographic metadata about works registered with Crossref. A work can be looked up using its DOI through this endpoint pattern: 

"https://api.crossref.org/works/{doi}" 

The DOI must be URL-encoded when necessary. A successful response contains a JSON object with a "message" field holding metadata such as the title, author information, publication dates, and publication venue when available. 

Possible implementation: Extract a DOI from the PDF text, query Crossref, and use the returned metadata to supplement the information extracted from the document. The app should handle network failures, missing records, and incomplete responses. 

Limitations: Not every paper has a DOI registered with Crossref, and not every metadata field is guaranteed to be present. Metadata returned by an API should be checked against the PDF where possible. 

Verification needed: Confirm the endpoint, usage guidance, and response-field details against the official Crossref documentation. Do not include fabricated API responses or treat sample placeholder authors as real publication metadata. 

## **6. PDF Extraction Methods** 

Several Python libraries can help extract text and metadata from research-paper PDFs. 

- PyMuPDF: Provides PDF text extraction and access to document information. It is a candidate for extracting text from uploaded papers. 

- pypdf: Can extract text and access PDF metadata, although complex layouts may affect the reading order. 

- pdfplumber: Offers tools for extracting text and working with page layouts and tables. 

- OCR: Optical Character Recognition can help extract text from scanned pages, but its accuracy depends on the scan quality and document layout. 

- GROBID: A specialized tool for extracting structured information from scholarly documents, but it adds setup and integration complexity. 

Proposed choice: Use PyMuPDF for the initial implementation because the project needs a practical way to extract text from uploaded PDFs. Check whether the extracted text is empty or unusually short so that the app can flag files that may need OCR or manual review. 

Limitations: Text extraction does not guarantee accurate identification of the title, authors, abstract, or references. Two-column layouts, tables, mathematical notation, and scanned pages can still cause problems. 

Verification needed: Confirm installation requirements and extraction capabilities using the official documentation for the chosen library. Any OCR feature should be tested separately before being described as implemented. 

## **7. Automatic Topic Tagging** 

Automatic topic tagging assigns descriptive labels to research papers so users can organize, search, and filter their library. 

Possible approaches include: 

- Keyword-based tagging: Identify important words or phrases in the title and abstract, then use them as tags. This is simple but may select common or irrelevant words. 

- TF-IDF: Give more importance to words that are frequent in a document but less common across the collection. This can help identify useful keywords. 

- Topic modelling: Techniques such as Latent Dirichlet Allocation (LDA) can identify groups of words that appear together across a collection of documents. The resulting topics may require interpretation. 

- Embedding-based methods: These can identify semantic similarities between documents, but may require additional libraries or computational resources. 

Proposed choice: Start with lightweight keyword extraction from the title and abstract. Normalize the text, remove common stop words, and select a small number of useful keywords as suggested tags. Allow users to edit the tags because automatic suggestions may not always represent a paper accurately. 

Limitations: Short abstracts, technical vocabulary, and papers from different subject areas can reduce tagging quality. Suggested tags should therefore be treated as recommendations rather than guaranteed classifications. 

Verification needed: Check the official scikit-learn documentation before choosing a specific TF-IDF implementation, and test the approach on several papers before judging its usefulness. 

## **8. Knowledge Graph Model** 

A knowledge graph represents entities and the relationships between them. For this project, the main entities are research papers, authors, and topics. 

The application can represent these entities using three main database tables: 

- Papers: Stores each paper's title, abstract, DOI, publication date, and other available metadata. 

- Authors: Stores author names so that authors can be associated with multiple papers. 

- Topics: Stores topic labels that can be linked to multiple papers. 

Relationship tables can connect papers to authors and papers to topics. For example, a paper may have several authors and several topic tags, while an author may contribute to multiple papers. 

A simple relational design in SQLite can represent these many-to-many relationships. The frontend can then display the connections as a graph, with papers, authors, and topics shown as nodes and their relationships shown as edges. 

Proposed choice: Use SQLite to store the entities and relationships. Retrieve the connected records through SQL queries and display them using a JavaScript graph-visualization library. 

Limitations: Duplicate author names can make it difficult to determine whether two records refer to the same person. Missing metadata can also leave some connections incomplete. The app should avoid creating relationships when the available evidence is insufficient. 

Verification needed: Check the official SQLite documentation for foreign-key relationships and the chosen graph library's documentation for its supported node and edge formats. 

## **9. Edge Cases and Failure Modes** 

The application should handle unexpected input and incomplete information without crashing or losing existing records. 

Important cases include: 

- Duplicate uploads: The same PDF may be uploaded more than once. The app should detect possible duplicates using a file hash or another suitable comparison method. 

- Missing metadata: A PDF may not contain a title, author, DOI, or publication date that can be extracted reliably. These fields should be allowed to remain empty until corrected. 

- Scanned PDFs: A document may contain page images rather than extractable text. The app should identify this situation and explain that OCR may be needed. 

- Corrupted or unsupported files: The app should validate uploaded files and report processing errors clearly. 

- Network failures: An external metadata lookup may time out or fail. The application should still retain any successfully extracted information. 

- Incorrect extraction: Text extraction may produce an incorrect title, author, or abstract. Users should be able to review and edit the metadata. 

- Incomplete topic tags: Automatic tagging may produce irrelevant or too few tags. Users should be able to modify them. 

- Database relationships: Foreign-key constraints should help prevent relationships from pointing to nonexistent records. 

Proposed choice: Use input validation, exception handling, duplicate checks, editable metadata, and clear error messages. Keep successfully extracted data where possible, even if an optional lookup or tagging step fails. 

Testing requirement: Test normal PDFs, duplicate uploads, a PDF with missing metadata, and a scanned or text-poor PDF. Record which cases work correctly and which remain limitations. 

## **10. Sample-Paper Findings** 

This section will document observations from examining sample research-paper PDFs. The purpose is to identify which metadata fields can be extracted reliably and which documents require additional handling. 

For each paper tested, record: 

- The paper title and source. 

- Whether the PDF contains selectable text or scanned page images. 

- Whether the title, authors, abstract, DOI, and publication date can be identified. 

- Any extraction problems, such as incorrect reading order or missing information. 

- What the observations suggest about the application's design. 

Status: Sample-paper testing has not yet been documented. Findings will be added after the PDFs have actually been examined. Any conclusions will be based on the observed results rather than assumptions. 

Design relevance: These tests can help determine how the application should handle incomplete metadata, scanned documents, and extraction errors. 

## **11. Discarded Information and Reasons** 

During the research phase, some information needs further checking before it can be used in the project. 

- Unverified API examples: Sample API responses that have not been confirmed against the official service should not be presented as genuine responses. 

- Unverified technical claims: Claims about installation, rate limits, authentication, or library capabilities should not be treated as confirmed until checked against official documentation. - Overly complex approaches: Techniques that introduce unnecessary setup or dependencies may be excluded if a simpler approach satisfies the project requirements. 

- Unsupported extraction assumptions: The application should not assume that every PDF contains complete metadata or extractable text. 

Current decision: The Gemini research document included an example that paired the DOI "10.1038/nature12373" with the author name “Jane Doe.” I have not verified that this combination is genuine, so I will not use it as a verified real API response. 

This is a provisional record. Additional items will be added only when I have actually checked them and decided not to use them. The reasons for excluding information should reflect its reliability, relevance, or compatibility with the assignment's restrictions. 

## **12. Sources** 

The following sources are relevant to the research and proposed implementation. They should be consulted when verifying technical claims and citation examples. 

1. UMass Chan Medical School Library — Parts of a Research Paper https://libraryguides.umassmed.edu/scientific-writing/parts-of-paper 

2. Tulane University Libraries — Anatomy of an Academic Paper https://libguides.tulane.edu/academicgenre/anatomy 

3. PyMuPDF — Frequently Asked Questions https://pymupdf.readthedocs.io/en/latest/faq/index.html 

4. PyMuPDF — Installation and OCR Information https://pymupdf.readthedocs.io/en/latest/installation.html 

5. Crossref — REST API Documentation 

https://www.crossref.org/documentation/retrieve-metadata/rest-api/ 

6. Crossref — Tips for Using the REST API 

https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-the-crossref-re st-api/ 

7. Purdue University Online Writing Lab — APA Formatting and Style Guide https://owl.purdue.edu/owl/research_and_citation/apa_style/apa_formatting_and_style_guide/ 

8. Purdue University Online Writing Lab — MLA Formatting and Style Guide 

https://owl.purdue.edu/owl/research_and_citation/mla_style/mla_formatting_and_style_guide/ml a_formatting_and_style_guide.html 

9. SQLite — Foreign Key Support https://www.sqlite.org/foreignkeys.html 

10. vis-network — Documentation 

https://visjs.github.io/vis-network/docs/ 

11. scikit-learn — Feature Extraction https://scikit-learn.org/stable/modules/feature_extraction.html 

12. arXiv — API User Manual 

https://info.arxiv.org/help/api/user-manual.html 

Source-use note: These links are a research list, not proof that every claim in this document has already been verified. For the final submission, consult the sources relevant to each claim, record any additional sources actually used, and make sure the citation examples and technical details match their references. 

