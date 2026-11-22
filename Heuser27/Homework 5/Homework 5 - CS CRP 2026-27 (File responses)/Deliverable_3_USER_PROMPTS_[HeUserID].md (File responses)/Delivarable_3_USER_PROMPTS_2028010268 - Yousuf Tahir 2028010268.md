## PROMPT TO CLAUDE TO DESGIN THE PROMPT FOR QWEN

6.3.1 What you give Claude 1. Your cleaned context pack (from Phase 1). 2. Your stack table with exact versions (from Phase 2). 3. The functional requirements F1–F12 and the full constraints from Section 5. 4. A description of the executor: “The code will be written by Qwen 2.5 Coder 7B, a small model with a limited effective context. Each prompt must therefore be self-contained, produce one file or one small group of functions, and state all interfaces explicitly.” 6.3.2 What the plan must contain 1. Overview & design decisions (including the graph-storage choice from Section 4.3). 2. Technology table (from Phase 2). 3. Architecture: a complete file/folder tree, the responsibility of each file, and the data flow from upload to graph (a simple diagram or numbered list). 4. Database schema: full CREATE TABLE statements with primary/foreign keys, uniqueness rules, and indexes; including the activity-log table. 5. API contract: every endpoint with method, path, request format, response JSON (with an example) and error responses. 6. Frontend specification: pages/views, the DOM structure at a high level, the exact CDN. The code will be written by Qwen 2.5 Coder 7B, a small model with a limited effective context. Each prompt must therefore be self-contained, produce one file or one small group of functions, and state all interfaces explicitly.F11:Delete a paper (and keep the graph and database consistent) F12:Handle bad input gracefully: non-PDF files, scanned PDFs without text, duplicate uploads. Show clear error messages instead of crashing. Section5:• The project must be web-based. • Backend language: Python. Database: SQLite. You may use any number of Python libraries (installed with pip and listed in requirements.txt). • Nobuild process for the frontend or the backend. • Strictly forbidden: Node.js, Bun, Deno, and any JavaScript backend; npm (and yarn, pnpm); any package.json or node_modules in your project. 5.2 Strict Frontend Constraints (No-Build Architecture) 1. Environment: browser-native client-side code only: HTML5, CSS3 and vanilla ES6+ JavaScript. 2. No Node.js: do not generate a package.json; do not use npm or node_modules; do not use build tools (no Vite, Webpack, Babel or TypeScript). 3. Noframeworks: no React, Vue, Angular or JSX. Manipulate the DOM directly with standard Web APIs (document.querySelector, fetch, etc.). 4. External libraries via CDN only: if you need third-party libraries (for ex ample vis-network or cytoscape for graphs, pdf.js for PDFs), load them strictly through



# PROMPTS TO PERPLEXITY

1: Python web frame work PDF text/layout ex traction Metadata extraction / APIs Tagging / keyword extraction SQLite access Graph visualization (CDN) Which lightweight framework (e.g. Flask, FastAPI, or another) fits a small app that also serves static files and accepts file uploads? Current stable version? Any upload or CORS gotchas? Which actively maintained library (e.g. PyMuPDF, pdfplumber, pypdf) best handles two-column papers? Is any option deprecated or unmaintained (e.g. PyPDF2)? Which HTTP client library? Current endpoint and response format for Crossref / Semantic Scholar / OpenAlex / arXiv? Rate limits? Which Python library (if any) for local keyword extraction? Is it maintained? Does it need big model downloads? Use the standard-library sqlite3 or an ORM? What is the recommended way to avoid SQL injection? Current stable version of vis-network, cytoscape.js or similar; the exact jsDelivr URL; the required data format; does it need an extra CSS file? Record for each choice: library name, exact version, purpose, why chosen over alternatives, and the source URL. Prefer official documentation or package-index pages over blog posts.

2: Make a technology table out of all this information that i can easily feed to Claude for my next step



# PROMPTS TO GEMINI

1: Okay first of all a gist of what we are doing today. I want to make a research papers of my own. You are in direct competition with deepseek right now. i will ask you for information and also inform you what my topic is. Deepseek will correct and criticize each mistake you make(if you make one, for example citation or wrong sources). Got it?

2: Q1. Anatomy of a research paper. Which sections exist, in what order, and what do they contain

(title block, authors and affiliations, abstract, keywords, introduction, methods, results,

discussion, conclusion, acknowledgements, references)? How do conference papers, journal

papers and arXiv preprints differ?

Q2. The PDF problem. How does a PDF actually store text? Why do two-column layouts,

headers/footers, footnotes, equations, ligatures and hyphenation break naive text extraction?

What is the difference between a text PDF and a scanned PDF?

Q3. Citation and reference styles. What do IEEE (numbered), APA, MLA, Chicago and BibTeX

style references look like? How are in-text citations different from the bibliography? Give a

real example of each.

Q4. Identifiers and metadata services. What are a DOI and an arXiv ID, what do they look like

(patterns), and where do they appear in a PDF? Which free scholarly APIs can turn them

into clean metadata? What fields do they return, and what are the rate limits and terms. Q5. Extraction techniques. Which Python libraries extract text and layout from PDFs (and what

are their trade-offs)? Which approaches find the title, authors, abstract and reference section

(heuristics such as font size and position, regular expressions, section-heading detection,

metadata lookup, or an LLM)?

Q6. Tagging and topic assignment. Which techniques can assign keywords/topics automatically

using only free and local tools (for example keyword extraction such as RAKE/YAKE/TF

IDF, using the paper’s own keywords, matching against a small controlled vocabulary, or

topic information returned by a scholarly API)? What are the strengths and limits of each?

Q7. Knowledge graphs. What is a graph in the data-structure sense (nodes, edges, directed vs.

undirected)? How do you represent one in relational tables? Which browser libraries draw

interactive graphs from a CDN, and what JSON format do they expect?

Q8. Edge cases. What goes wrong in real papers: missing abstract, multi-line titles, many

authors, non-English text, no DOI, scanned pages, references split across columns, duplicate

uploads

3: I will now provide you with DeepSeek's corrections and it's point of view on how you could have made it better

4:Q1✅No hard errorsQ2✅No hard errorsQ3⚠️APA 7th conference proceedings example format not standardizedQ4❌Crossref rate limit outdated; arXiv DOI key omissionQ5⚠️PyMuPDF AGPL license not mentionedQ6✅No hard errorsQ7✅D3 format minor omissionQ8✅Minor supplementation

Suggestion: For your research paper, the content of Q1, Q2, Q6, Q7, and Q8 can be used directly (with minor supplementation of the points I mentioned). Q3's APA example must be replaced with the standardized format I provided. Q4's rate limit data must be updated according to Crossref's official announcement, and the arXiv DOI information must be added. Q5 must add a note about PyMuPDF's license.

5: Aim for a context pack small enough to paste into a model with a modest window together with

other instructions: roughly 1500 to 3500 words, dense and well structured. In Deliverable_1_

CONTEXT_[HeUserID].md, include a short “What I discarded and why” section; this shows

your sifting judgement

6: Right now You've made it according to your own format. let me send you some sample research papers. extract

the title, authors, abstract and references, and to describe the exact patterns it sees (where the

DOI appears, how the reference section starts, how references are numbered). Put the observed

patterns and a few short, real excerpts into your context pack. Real samples beat imagination;

this is the single best way to stop the coding model from hallucinating about the input. Evidence

of this step (the prompt, the sample list, and the findings) is required to receive the bonus

7: These files were only for your knowledge so you adjust the deliverable file accordingly. Could you make the deliverable file now?



# PROMPTS TO DEEPSEEK

1: Okay first of all a gist of what we are doing today. I want to make a research papers of my own. You are in direct competition with Gemini right now. i will ask Gemini for information and also inform you what my topic is. Deepseek will correct and criticize each mistake Gemini makes(if it make one, for example citation or wrong sources). Got it?

2: These are the questions i asked gemini. let me provide you with it's response. your job is to sift through it. Find mistakes/better replacements

