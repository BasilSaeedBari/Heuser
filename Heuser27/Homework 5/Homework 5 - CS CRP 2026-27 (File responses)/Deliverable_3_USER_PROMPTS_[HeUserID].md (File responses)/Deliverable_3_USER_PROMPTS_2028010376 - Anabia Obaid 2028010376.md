# **USER PROMPTS LOG** 

## **Entry 01 — Initial planning** 

- Tool: ChatGPT 

- Phase: Initial task clarification 

- Prompt (verbatim): “Explain my homework comprehensively to me as you would to a beginner” - Result: ChatGPT summarized the homework requirements and explained the four deliverables, the technology restrictions, and the recommended workflow. 

- What I kept / discarded and why: I kept the explanation of the requirements and used it to understand the assignment. I still need to complete the assigned research and planning phases using the specified tools. 

## **Entry 02 — Breaking the task into manageable steps** 

- Tool: ChatGPT 

- Phase: Initial task clarification 

- Prompt (verbatim): "Create a work timeline for me to complete the assignment since I have low time" 

- Result: ChatGPT created a time-based checklist for research, planning, coding, testing, and submission. 

- What I kept / discarded and why: I kept the checklist as a rough schedule. I need to adjust it to my available time and follow the assignment's required tool sequence. 

## **Entry 03 — Phase 1 Research** 

- Tool: Gemini (Deep Research) 

- Phase: Phase 1 — Research 

- Prompt (verbatim): “I am researching a school project called “Research Paper Library and Knowledge Graph.” The final app must use Python for the backend, SQLite for the database, and HTML, CSS, and vanilla JavaScript for the frontend. It must accept research-paper PDFs, extract useful metadata, organize papers with topic tags, allow searching and filtering, and show connections between papers, authors, and topics. 

Research the following areas: 

1. The typical sections and metadata of an academic research paper. 

2. Common PDF extraction difficulties, including two-column layouts, scanned PDFs, missing text, and reading order. 

3. APA, MLA, IEEE, and BibTeX citation formats, with accurate examples from verifiable sources. 

4. DOI identification and the Crossref REST API, including a real endpoint, authentication requirements, rate limits or usage guidance, and a small representative JSON response. 

5. The arXiv API and its appropriate uses. 

6. Python PDF extraction libraries and a justified choice for this project. 

7. Practical approaches to automatic topic tagging using Python. 

8. A simple knowledge-graph data model for papers, authors, and topics. 

9. Likely errors, duplicate papers, missing metadata, and other edge cases. Requirements: 

- Prefer official documentation, academic libraries, and primary sources. 

- Include source titles and direct URLs for every important factual claim. 

- Clearly distinguish verified facts from recommendations and assumptions. 

- Do not invent citations, API responses, versions, or technical details. 

- Give concrete findings that would change an implementation decision, rather than generic descriptions. 

- Explain the limitations of each recommended approach. 

- Organize the findings under the nine numbered headings above. 

- End with a short list of the most important design decisions supported by the research.” 

- Result: Gemini produced a 15-page document titled Architecture and Implementation Specification for a Research Paper Library and Knowledge Graph System. It covered academic paper structure, PDF extraction challenges, citation formats, Crossref and arXiv APIs, PDF parsing libraries, automatic topic tagging, a SQLite graph schema, and error handling. ( **https://share.gemini.google/lPO32S7sOj3Y** ) 

- What I kept / discarded and why: 

- Kept provisionally: The discussion of PDF extraction difficulties, candidate metadata fields, lightweight topic tagging, and the proposed SQLite relationships because these are relevant to the application design. 

- Needs verification: API endpoints, rate limits, citation examples, library capabilities, and sample API responses must be checked against reliable primary sources before being used. - Discarded: No findings discarded yet. I will record specific exclusions after checking the research and deciding which findings are useful and reliable. 

## **Entry 04 — Phase 2 Technology and Version Research** 

- Tool: Perplexity 

- Phase: Phase 2 — Technology and Version Verification 

- Prompt (verbatim): I am building a school project called “Research Paper Library and Knowledge Graph.” The required stack is Python for the backend, SQLite for the database, and HTML, CSS, and vanilla JavaScript for the frontend. Node.js, npm, React, Vue, Angular, TypeScript, and frontend build steps are forbidden. 

Please verify the current stable versions and compatibility of the following technologies for a small student project: 

1. Python 

2. Flask 

3. PyMuPDF 

4. SQLite 

5. vis-network, loaded through a CDN 

6. A suitable icon library, loaded through a CDN if needed 

For each technology, provide: 

- The recommended version or version range as of today. 

- An official documentation or release-page URL. 

- The minimum relevant Python version or other compatibility requirements. 

- A short reason it is suitable for this project. 

- Any installation or licensing considerations relevant to a student project. 

- Prefer official documentation and release pages over blogs. Clearly distinguish verified information from recommendations. Do not invent version numbers or compatibility claims. If a detail cannot be verified, say so. 

- Result: Perplexity produced a nine-page technology and compatibility report covering Python, Flask, PyMuPDF, SQLite, vis-network, and Bootstrap Icons. It suggested pinned Python dependencies and browser CDN libraries. 

( **https://www.perplexity.ai/search/0289446b-86bf-4f67-bd47-9a7111ea3072#0** ) 

- What I kept / discarded and why: 

- Kept provisionally: The proposed stack, official documentation links, installation guidance, and licensing notes. 

- Needs verification: Current release versions, compatibility requirements, CDN paths, and licensing details should be checked against official sources before implementation. 

- Correction identified: The report recommends vis-network 10.0.2, but the official releases page lists a newer version. The technology table should use a version verified against the official release page, not copy the recommendation without checking. 

- Discarded: No additional findings discarded yet; record specific exclusions only after evaluating them. 

# **Reflection on AI-Assisted Research** 

**The research and planning stages helped me understand how to approach the Research Paper Library and Knowledge Graph project systematically. I used AI tools to investigate academic paper structure, PDF extraction challenges, citation formats, metadata services, database relationships, and possible implementation technologies. I also learned that AI-generated information should be treated as a starting point rather than automatically accepted as correct.** 

**During the research stage, I kept information that could help guide implementation, such as the need to handle missing PDF metadata, detect duplicate papers, and represent relationships between papers, authors, and topics. I also identified details that required further checking, including software versions, compatibility requirements, CDN URLs, and licensing. This showed me why official documentation is important when making technical decisions.** 

**The planning stage helped turn a broad project idea into smaller parts, including a database schema, API endpoints, frontend views, coding prompts, and acceptance tests. Breaking the work into sections made the project easier to understand and gave me a clearer sequence for implementation.** 

**One limitation of using AI tools is that their answers may contain outdated, incomplete, or unverified claims. For this reason, I need to check important technical details against reliable sources and test the actual application rather than assuming a suggested solution works. I must also keep accurate records of the prompts I use, the outputs I receive, and any changes I make myself.** 

**Overall, AI assistance has helped me organize my research and plan the project, but I remain responsible for verifying the information, understanding the design, testing the application, and honestly documenting the final results** 

## **Entry 05 — Phase 3 Architecture and Implementation Planning** 

- Tool: Claude 

- Phase: Phase 3 — Architecture and Design Planning 

Prompt (verbatim): “I am building a school project called “Research Paper Library and Knowledge Graph.” 

The required stack is Python with Flask for the backend, SQLite for the database, and HTML, CSS, and vanilla JavaScript for the frontend. PDF processing will use PyMuPDF, and the graph will use vis-network through a CDN. 

The app must support: 

1. Uploading research-paper PDFs. 

2. Extracting available text and metadata. 

3. Storing papers and their metadata in SQLite. 

4. Searching and filtering the paper library. 

5. Editing extracted metadata. 

6. Assigning topic tags. 

7. Showing relationships between papers, authors, and topics in an interactive knowledge graph. 

8. Recording activity and handling invalid files, duplicates, missing metadata, and errors. Prohibited technologies include Node.js, npm, React, Vue, Angular, TypeScript, and frontend build tools. 

Create a practical implementation plan for a beginner. Include: 

- A proposed folder structure. 

- A database schema with primary and foreign keys. 

- A Flask API contract with routes, methods, and expected responses. 

- The main frontend views and their responsibilities. 

- An ordered implementation sequence. 

- Acceptance tests for each major feature. 

- Important security, compatibility, and error-handling considerations. 

- Do not write the complete application code yet. Distinguish requirements from recommendations, flag assumptions, and avoid claiming that untested features work.” 

Result summary: Claude produced a structured implementation plan covering assumptions, folder structure, SQLite tables and relationships, Flask API routes, frontend views, implementation order, acceptance tests, security, compatibility, and error handling. It recommended keeping route handlers thin, separating business logic into service modules, storing uploaded files under generated names, and testing PDF extraction before integrating it into the web application. ( **https://claude.ai/share/21f809c6-bcad-4ab1-9108-e9f8756f7340)** 

What I kept / discarded and why 

- Kept provisionally: The modular folder structure, database relationship design, API contract, implementation sequence, and acceptance tests. 

- Needs verification: Package versions, compatibility, PDF extraction behaviour, and whether the proposed implementation fits the assignment's exact requirements. 

- Needs review: Claude assumed a single-user local application without login and suggested that OCR is out of scope. These are assumptions that must be checked against the assignment brief. 

- Not yet demonstrated: The plan has not been implemented or tested, so its acceptance tests remain proposed rather than passed 

## **Qwen 2.5 Coder 7B Instruct — Phase 4 Summary** 

Qwen 2.5 Coder 7B Instruct was used during Phase 4 to begin generating the Research Paper Library application code. The initial prompt requested a basic Flask project setup. Qwen generated a starter "app.py", a "requirements.txt" file specifying Flask 3.0.0, an "index.html" template, a CSS stylesheet, and commands for running the application on Windows, macOS and Linux. 

However, the initial output was only a starting point. It did not yet implement the main project requirements, including PDF uploading, SQLite database integration, research-paper metadata extraction and knowledge graph visualisation. Qwen also stated that it had not executed or tested the generated code. 

The generated starter code was therefore treated as an initial reference rather than a complete solution. The application was subsequently developed and modified to include the required 

functionality, with additional manual changes to the interface, PDF upload success page, testing script and documentation. 

This phase demonstrated that AI-generated code can accelerate initial project setup, but its output must be reviewed, expanded and tested before it can be considered a working application. It also highlighted the importance of checking generated dependency versions against the project's chosen technology stack. 

## **Discarded Output — Qwen 2.5 Coder 7B Instruct** 

The initial Qwen output was not accepted as the final application because it only provided a basic Flask project skeleton. It did not implement essential features such as PDF uploading, SQLite database integration, metadata extraction, paper searching, topic tagging, activity logging or knowledge graph visualisation. 

The generated dependency file also specified Flask 3.0.0, whereas the project used Flask 3.1.3. The output was therefore treated as a starting point rather than a complete solution. The missing functionality and dependency mismatch meant that further development, manual editing and testing were necessary. 

Reason for discarding: Incomplete functionality, mismatch with the selected technology versions, and no evidence that the generated code had been executed or tested. 

