# **1. Technology and Version Table** 

|**Technology**|**Recommended**<br>**Version**|**Official Source**|**Reason for choice**|
|---|---|---|---|
|Python|Python 3.13.x<br>(provisional; verify<br>the exact patch<br>version before<br>implementation)|https://www.python.or<br>g/|Runs the backend<br>and supports the<br>PDF extraction,<br>metadata processing,<br>and database<br>libraries needed for<br>the project.|
|Flask|3.1.3|https://flask.palletspro<br>jects.com/en/stable/|A lightweight Python<br>web framework for<br>handling requests,<br>routes, PDF uploads,<br>and communication<br>between the frontend<br>and backend.|
|PyMuPDF|2.0|https://pymupdf.readt<br>hedocs.io/en/latest/|Extracts text and<br>metadata from<br>uploaded PDF<br>research papers.<br>Supports PDF<br>processing and<br>OCR-related<br>workflows.|
|SQLite|version bundled with<br>Python's sqlite3<br>module|https://www.sqlite.org<br>/|Stores paper records,<br>authors, topics,<br>relationships, and<br>activity logs in a<br>lightweight database.<br>SQLite is free to use.|
|Vis-network|10.1.2|https://github.com/visj<br>s/vis-network|Displays interactive<br>connections between<br>research papers,<br>authors, and topics|
|Bootstrap Icons|1.13.2|https://icons.getboots<br>trap.com/|Provides icons for<br>buttons and interface<br>elements and can be<br>loaded through a<br>CDN without a<br>frontend build|



||||system**.**|
|---|---|---|---|
|HTML, CSS and<br>vanilla JavaScript|Standard Browser<br>Technologies|https://developer.moz<br>illa.org/en-US**/**|Builds the user<br>interface while<br>following the<br>assignment's<br>restriction against<br>frontend frameworks<br>and build tools.|



**Before continuing: Other tables are made using x|y|z to separate fields and records.** 

# **2. System Architecture** 

- The application will use a simple three-part architecture. The frontend will be built with HTML, CSS, and vanilla JavaScript. It will allow users to 

- upload PDF research papers, search and filter the library, edit metadata, and explore connections in a knowledge graph. The backend will use 

- Python with Flask to handle uploads, extract metadata, manage requests, and communicate with the database. SQLite will store paper details, 

- authors, topics, relationships, and activity logs. PyMuPDF will be used to extract text and metadata from PDFs, while vis-network will display the 

- knowledge graph in the browser. The frontend will communicate with the backend through HTTP endpoints that exchange JSON data where appropriate. 

# **3. Proposed Folder Structure** 

research-paper-library/ ├── app.py ├── database.py ├── pdf_processor.py ├── metadata.py 

├── requirements.txt ├── README.md ├── research_library.db ├── uploads/ 

├── templates/ │   ├── index.html │   ├── paper_detail.html │   └── graph.html └── static/ ├── css/ │   └── style.css └── js/ ├── app.js └── graph.js 

Purpose of the main files and folders: 

- "app.py": Runs the Flask application and defines the HTTP routes. - "database.py": Creates and manages the SQLite database and its queries. 

- "pdf_processor.py": Extracts text and metadata from uploaded PDFs. 

- "metadata.py": Cleans, validates, and organizes extracted metadata. 

- "requirements.txt": Lists the Python packages required to run the app. 

- "README.md": Explains installation, setup, and usage. 

- "uploads/": Stores uploaded PDF files. 

- "templates/": Contains the HTML pages rendered by Flask. 

- "static/css/": Contains the application's styles. 

- "static/js/": Contains the frontend JavaScript and graph visualization code. - "research_library.db": The SQLite database file, created when the application initializes. 

# **4. Database Schema** 

The application will use SQLite to store research papers and their relationships. The database will contain the following tables. 

# _4.1 Papers_ 

Field| Type| Purpose id| INTEGER PRIMARY KEY| Unique paper identifier title| TEXT| Paper title abstract| TEXT| Paper abstract doi| TEXT| Digital Object Identifier, if available publication_year| INTEGER| Year of publication journal| TEXT| Journal or publication name pdf_path| TEXT| Location of the uploaded PDF created_at| TEXT| Date and time the record was created 

# _4.2 Authors_ 

Field| Type| Purpose id| INTEGER PRIMARY KEY| Unique author identifier name| TEXT| Author's name 

# _4.3 Paper_Authors_ 

Field| Type| Purpose paper_id| INTEGER| References Papers.id author_id| INTEGER| References Authors.id 

This junction table allows one paper to have multiple authors and one author to appear on multiple papers. 

# _4.4 Topics_ 

Field| Type| Purpose id| INTEGER PRIMARY KEY| Unique topic identifier name| TEXT UNIQUE| Topic name 

# _4.5 Paper_Topics_ 

Field| Type| Purpose paper_id| INTEGER| References Papers.id topic_id| INTEGER| References Topics.id 

This junction table allows papers to have multiple topic tags. 

# _4.6 Activity_Log_ 

Field| Type| Purpose id|INTEGER PRIMARY KEY| Unique activity identifier action| TEXT| Description of the activity paper_id| INTEGER| Related paper, if applicable created_at| TEXT| Date and time of the activity 

_Database Design Notes_ 

- Primary keys uniquely identify records. 

- Foreign keys connect related records between tables. 

- DOI values should be checked for duplicates when present. 

- Junction tables represent many-to-many relationships. 

- The application should enable SQLite foreign-key enforcement and use parameterized queries. 

- The schema may be extended during implementation to support additional metadata and error-handling requirements. 

# **5. API Contract** 

The frontend will communicate with the Flask backend using HTTP requests. The backend will return JSON responses for data-related operations and appropriate HTTP status codes when errors occur. 

Method| Endpoint| Purpose| Expected response 

GET| "/api/papers"| Retrieve the paper library| List of papers in JSON POST| "/api/papers/upload"| Upload a PDF and process its metadata| Upload result and paper details 

GET| "/api/papers/<id>"| Retrieve one paper's details| Paper metadata in JSON 

PUT| "/api/papers/<id>"| Update a paper's metadata| Updated paper record DELETE| "/api/papers/<id>"| Delete a paper record| Confirmation of deletion 

GET| "/api/topics"| Retrieve available topic tags| List of topics in JSON GET| "/api/graph"| Retrieve papers, authors, topics, and their relationships| Graph nodes and edges in JSON 

GET| "/api/activity"| Retrieve recent library activity| List of activity records in JSON 

Request and Response Rules 

- The upload endpoint will accept a PDF file using a multipart form request. 

- Other data-changing requests will validate the supplied fields before modifying the database. 

- Successful responses will use suitable HTTP status codes, such as "200 OK" or "201 Created". 

- Invalid input will return an appropriate error response, such as "400 Bad Requests". 

- A missing paper will return "404 Not Found". 

- Unexpected server errors will be handled without exposing sensitive internal details. 

- Search and filtering will be supported through query parameters on the paper-list endpoint, for example "/api/papers?q=machine+learning&topic=AI". 

- Uploaded files will be checked to ensure they are valid PDFs and within the application's configured size limit. 

These endpoints are a proposed contract. Their implementation and exact response formats will be tested during development. 

# **6. Frontend Views and CDN Libraries** 

The frontend will use HTML, CSS, and vanilla JavaScript. No frontend frameworks, Node.js, npm, or build tools will be used. 

# _6.1 Main Views_ 

View| Main features 

Library Dashboard| Displays saved papers, upload controls, search, and filters 

Paper Details| Shows paper metadata, authors, abstract, DOI, and topic tags 

Edit Metadata| Allows users to correct extracted information Knowledge Graph| Displays connections between papers, authors, and topics 

Activity Log| Shows recent uploads, edits, and deletions 

# _6.2 External Browser Libraries_ 

Library| Purpose| Loading method 

vis-network| Interactive knowledge graph visualization| JavaScript CDN Bootstrap Icons| Icons for buttons and interface elements| CSS CDN 

The application will use official CDN instructions and verified versioned URLs when implementation begins. The frontend will remain usable without these optional visual enhancements wherever practical. 

# _6.3 Frontend Behaviour_ 

- JavaScript will send requests to the Flask API using the Fetch API. 

- Search and filtering controls will update the displayed paper list. 

- Forms will provide validation feedback before submission. 

- The graph view will render nodes for papers, authors, and topics, with edges representing their relationships. 

- Loading states, empty results, and error messages will be displayed clearly. 

# **7. Numbered Coding Prompts for Qwen 2.5 Coder 7B Instruct** 

The prompts below are planned instructions for the coding phase. They will be submitted to Qwen during implementation, and the actual prompts, outputs, and changes will be recorded in the build log. 

_Prompt 1 — Project Setup and Database_ 

Create the initial structure for a Research Paper Library and Knowledge Graph application. Use Python, Flask, SQLite, HTML, CSS, and vanilla JavaScript only. Do not use Node.js, npm, React, Vue, Angular, TypeScript, or frontend build tools. 

Create the Flask application entry point, database initialization code, requirements file, and basic HTML template. Implement the database tables for papers, authors, paper-author relationships, topics, paper-topic relationships, and activity logs. Use parameterized SQL queries and enable foreign-key enforcement. Explain how to run the application locally. 

_Prompt 2 — PDF Upload and Metadata Extraction_ 

Implement a PDF upload feature using Flask and PyMuPDF. Validate uploaded files, enforce a configurable size limit, handle invalid or 

unreadable PDFs, and extract available text and metadata. Save uploaded files safely and store extracted metadata in SQLite. Avoid inventing missing metadata. Return clear error messages and record successful uploads in the activity log. 

_Prompt 3 — Metadata Editing and Paper Library_ 

Implement the paper library interface, including paper listing, keyword search, topic filtering, and a paper details page. Allow users to edit extracted metadata and save changes to SQLite. Validate input, handle missing records, and provide useful success and error messages. 

_Prompt 4 — Topic Tagging and Knowledge Graph_ 

Implement basic automatic topic tagging using meaningful keywords from available paper titles and abstracts. Allow users to review and edit tags. Create a graph API that returns paper, author, and topic nodes with their relationships. Use vis-network through a browser CDN to display the interactive graph. Handle empty graphs and incomplete relationships. 

_Prompt 5 — Activity Log and Error Handling_ 

Implement an activity log for uploads, metadata changes, and deletions. Improve handling of duplicate papers, missing metadata, invalid PDFs, database errors, and unavailable external services. Do not allow an external metadata lookup failure to prevent a paper from being saved when sufficient local information is available. 

_Prompt 6 — Testing, Documentation, and Final Review_ 

Review the complete application against the assignment's required features. Test uploads, metadata extraction, database persistence, search, filters, editing, topic tags, graph relationships, and error cases. Fix problems without introducing prohibited technologies. Create a README 

explaining installation, configuration, startup, usage, and limitations. List any unimplemented or partially working features honestly. 

These prompts are starting drafts. They will be refined based on the actual outputs from Qwen and recorded verbatim in the implementation log when used. 

# **8. Acceptance Tests** 

The application will be tested against the following criteria. Each test will be marked as passed or failed after the relevant feature has been implemented and tested. 

Test ID| Feature| Test procedure| Expected result 

AT01| Application startup| Start the Flask application| The application starts without errors 

AT02| PDF upload| Upload a valid research-paper PDF| The PDF is accepted and a paper record is created 

AT03| Invalid upload| Upload a non-PDF file| The application rejects it with a clear error message 

AT04| Metadata extraction| Upload a PDF containing a title and author information| Available metadata is extracted without inventing missing values 

AT05| Database persistence| Restart the application after saving a paper| The saved paper remains available 

AT06| Search| Search for a word in a paper's title| Matching papers are displayed 

AT07| Topic filtering| Filter papers by a topic tag| Only matching papers are displayed 

AT08| Metadata editing| Edit a paper's title and save| The updated title persists in the database 

AT09| Duplicate handling| Upload a paper with a DOI already in the library| The duplicate is detected or clearly flagged 

AT10| Knowledge graph| Open the graph view with saved papers and relationships| Relevant nodes and edges are displayed 

AT11| Empty graph| Open the graph view with no saved papers| A useful empty-state message is displayed 

AT12| Activity log| Upload or edit a paper| The corresponding activity is recorded 

AT13| Missing metadata| Upload a PDF with incomplete metadata| The app handles missing fields without crashing 

AT14| Database relationships| Create a paper with authors and topics| Relationships are stored and retrieved correctly 

AT15| Error handling| Attempt to open a nonexistent paper record| A clear not-found response is returned 

The tests will be executed against the actual application during implementation. No test will be marked as passed until it has been performed and its result recorded. 

# **9. Build Log and Manual Edit Log** 

# _9.1 Build Log_ 

This log will record the actual coding process, including prompts submitted to Qwen 2.5 Coder 7B Instruct, the outputs received, errors encountered, and fixes made. 

Step| Build activity| Outcome / status 

1| Selected Python 3.13.17, Flask 3.1.3, SQLite, PyMuPDF 2.0, HTML, CSS and JavaScript.| Completed 

   - 2| Created the project structure, including the application, database module, services, templates, static files and tests.| Completed 

   - 3| Set up the Python virtual environment and installed the required dependencies.| Completed 

   - 4| Implemented the Flask application and SQLite database for storing research-paper information.| Completed 

- 5| Implemented PDF uploading and text extraction using PyMuPDF.| Tested successfully with an uploaded PDF 

- 6| Implemented paper search functionality.| Manually tested successfully 

- 7| Implemented paper editing and saving.| Manually tested successfully 8| Implemented topic tagging and checked that tags persisted after refreshing the page.| Manually tested successfully 

   - 9| Implemented the knowledge graph to display paper and topic relationships.| Manually checked successfully 

10| Added an activity log to display recent application actions.| Manually 

            - checked successfully 

   - 11| Created a README with setup instructions, dependencies, features, limitations and usage information| Completed 

      - 12| Created a PDF extraction test script and recorded its result in 

         - "TEST_RESULTS.md".| Test passed 

   - 13| Added a floral lavender theme and styled the PDF upload success page.| Visually checked successfully 

- 14| Cleared the saved papers, topics, authors, tags and activity history from the submission copy.| Completed; dashboard reopened with an empty library 

# _9.2 Manual Edit Log_ 

Any changes made manually to AI-generated code will be documented here. This includes bug fixes, corrections to generated code, compatibility adjustments, and changes required to satisfy the assignment's restrictions. 

Step| File edited| Manual change made| Reason 

- 1| "static/css/style.css"| Added floral emoji decorations around the page 

- and subtle floral details on cards and headings| To personalise the interface with a soft, cute visual theme. 

- 2| "static/css/style.css"| Added responsive styling for smaller screens.| To keep the decorations subtle on mobile devices 

3| "app.py"| Changed the successful PDF-upload response to render "upload_success.html" with the paper ID.| To replace plain text with a dedicated success page. 

4| "templates/upload_success.html"| Created a success page with a confirmation icon, paper ID and a link back to the library.| To improve user feedback after a successful upload. 

- 5| "static/css/style.css"| Added styling for the upload success page, 

- including a lavender-pink gradient, rounded corners and a styled navigation link.| To match the success page to the rest of the interface. 

- 6| "tests/test_pdf_extract.py"| Adjusted the script to locate the project folder before importing the PDF extraction service and select a non-empty PDF from the uploads folder.| To make the test script easier to run from the project directory. 

- 7| "TEST_RESULTS.md"| Documented the PDF extraction test method, expected result, observed result and pass status.| To record testing evidence. 

- 8| "README.md"| Documented installation, startup, features, limitations, 

- dependencies and project structure.| To help users run and understand the application. 

9| "requirements.txt"| Specified the Flask and PyMuPDF dependency versions.| To support reproducible setup. 

# _9.3 Record-Keeping Rules_ 

- Record the actual prompts submitted to Qwen verbatim. 

- Summarize the output honestly rather than claiming that untested features work. 

- Record significant errors and how they were resolved. 

- Distinguish AI-generated code from manual changes. 

- Mark tests as passed only after running them. 

- Keep a record of any features that remain incomplete. 

# **10. Known Limitations and Risks** 

The proposed application has several technical limitations and risks that must be considered during implementation. 

1. PDF extraction accuracy: Text extraction may produce incorrect reading order, particularly in multi-column papers, tables, equations, and documents with unusual layouts. 

2. Scanned PDFs: A scanned PDF may contain page images rather than extractable text. OCR may be needed, and OCR results may contain errors. 

3. Incomplete metadata: Some PDFs may not contain a DOI, abstract, publication year, or reliable author information. Missing information must remain unknown rather than being invented. 

4. Automatic topic tagging: Keyword-based tagging may produce irrelevant or overly broad topics. Users should be able to review and correct automatically generated tags. 

5. Duplicate detection: DOI matching can identify many duplicate records, but papers without DOIs may require additional checks using titles and author information. 

6. External service availability: DOI metadata services may be unavailable or return incomplete results. The application should handle lookup failures gracefully. 

7. File security: Uploaded files must be validated, filenames handled safely, and upload sizes limited. The application should not execute uploaded content. 

8. Database integrity: Relationships between papers, authors, and topics must remain consistent when records are edited or deleted. 

9. Knowledge graph readability: Large libraries may create crowded graphs. Search, filtering, and graph display options may be needed to improve usability. 

10. Version compatibility: Python packages and browser libraries must be checked for compatible versions before installation and use. 

These risks will be addressed through validation, error handling, user-editable metadata, database constraints, and acceptance testing. Any remaining limitations will be documented in the final README. 

# **11. Final Deliverable Checklist** 

The following checklist will be completed before submission. 

- [✓  ] Verify the recommended technology versions and compatibility. - [✓  ] Confirm that the project uses Python, Flask, SQLite, HTML, CSS, and vanilla JavaScript. 

- [✓  ] Confirm that no prohibited frontend frameworks or build tools are used. 

- [✓  ] Implement PDF upload and text extraction. 

- [ ✓ ] Implement metadata storage and editing. 

- [ ✓ ] Implement search and topic filtering. 

- [✓ ] Implement author and topic relationships. 

- [✓  ] Implement the knowledge graph. 

- [✓  ] Implement the activity log. 

- [ ✓ ] Test invalid files, missing metadata, duplicates, and other edge cases. 

- [✓  ] Run all acceptance tests and record the actual results. 

- [✓  ] Write a README with installation and usage instructions. 

- [✓  ] Verify that the application can be launched from a clean setup. 

- [✓  ] Record actual AI coding prompts, outputs, and manual edits. 

- [ ✓ ] Package the completed application into the required ZIP file. 

- [✓  ] Convert the final documentation to the required Markdown format. 

- [✓  ] Replace "[HeUserID]" with the assigned ID in the final filenames. 

- [✓  ] Check that all required deliverables are included before submission. 

Items will only be checked off after they have actually been completed and verified. 

# **12. References and Verification Notes** 

The following official documentation and release pages will be used to verify implementation decisions. Version numbers and compatibility details must be checked again before the application is installed and tested. 

1. Python Downloads: https://www.python.org/downloads/ 

2. Flask Documentation: https://flask.palletsprojects.com/en/stable/ 

3. PyMuPDF Documentation: https://pymupdf.readthedocs.io/en/latest/ 

4. SQLite Official Website: https://sqlite.org/ 

5. SQLite Python Interface: https://docs.python.org/3/library/sqlite3.html 

6. vis-network Releases: https://github.com/visjs/vis-network/releases 

7. vis-network Documentation: 

https://visjs.github.io/vis-network/docs/network/ 

8. Bootstrap Icons Usage: https://icons.getbootstrap.com/usage/ 

9. MDN Web Documentation: 

https://developer.mozilla.org/en-US/docs/Web 10. Crossref REST API Documentation: https://www.crossref.org/documentation/retrieve-metadata/rest-api/ 11. Flask File Upload Patterns: https://flask.palletsprojects.com/en/stable/patterns/fileuploads/ 

_Verification Notes_ 

- Official documentation and release pages take priority over unverified recommendations. 

- The selected package versions must be compatible with the chosen Python installation. 

- CDN URLs must be checked against the relevant library's official documentation before use. 

- Licensing terms must be reviewed for libraries included in the project. 

- Any implementation decisions that differ from the original plan will be documented with their reasons. 

- Research findings, AI-generated suggestions, and personally tested results must be clearly distinguished. 

# **Entry 1 — Initial Flask Setup** 

- Tool: Qwen 2.5 Coder 7B Instruct 

- Output: Generated a basic Flask application, "requirements.txt", an HTML home page, CSS styling, and setup instructions. 

- Status: Generated; not yet run or tested. 

- Issue to review: The generated requirements file pins Flask 3.0.0. Check compatibility and select the project version before installation. 

- Next action: Create the files and run the initial application. 

# **Entry 2 — Initial Flask Setup Test** 

- Tool: Qwen 2.5 Coder 7B Instruct, with manual setup and testing. 

- Environment: Windows 10, Python 3.13.17 (64-bit), Flask 3.1.3. 

- Result: Created the initial Flask application, installed dependencies in a virtual environment, and successfully opened the homepage at "http://127.0.0.1:5000". 

- Status: Initial homepage test passed. 

- Limitations: PDF uploads, SQLite storage, search, topic tags, and the knowledge graph have not yet been implemented. 

# **Entry 3 — PDF Upload Test** 

- Implementation: Added a PDF upload form to "templates/index.html" and an upload route to "app.py". 

- Validation: The route checks the file extension, uses a unique filename, and limits uploads to 20 MB. 

- Test performed: Uploaded a PDF through the browser. 

- Observed result: The website displayed “PDF uploaded successfully!” and the upload succeeded. 

- Status: Basic PDF upload test passed. 

- Limitations: The PDF's metadata and text are not yet extracted or saved in the database. File content is not yet validated as a genuine PDF. 

