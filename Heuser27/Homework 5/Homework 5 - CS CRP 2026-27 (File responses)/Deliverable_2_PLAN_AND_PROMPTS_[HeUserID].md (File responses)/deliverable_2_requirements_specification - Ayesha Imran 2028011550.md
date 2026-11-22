# Deliverable 2: System Requirements & User Stories

**Project Title:** Research Paper Library & Knowledge Graph System  
**User ID:** [HeUserID]  

---

## 1. Functional Requirements

### 1.1 Document Ingestion & Management
* **FR-1.1:** System shall accept PDF file uploads up to 50MB.
* **FR-1.2:** System shall extract standard metadata ($title$, $authors$, $publication\ date$, $abstract$) automatically.
* **FR-1.3:** System shall parse section headers, tables, and references from the main text body.

### 1.2 Knowledge Graph & Extraction
* **FR-2.1:** System shall perform Named Entity Recognition (NER) to classify entities into categories: *Paper*, *Author*, *Method*, *Dataset*, and *Concept*.
* **FR-2.2:** System shall construct directed edges representing semantic interactions between nodes.
* **FR-2.3:** System shall update graph entities incrementally upon ingesting new publications.

### 1.3 Search & Visualization
* **FR-3.1:** System shall support vector-based semantic search across document contents and graph entities.
* **FR-3.2:** System shall render an interactive visual graph representation allowing node dragging, filtering, and zooming.
* **FR-3.3:** Clicking a node shall display associated papers, summaries, and relation details in a context side panel.

---

## 2. Non-Functional Requirements

* **NFR-1 (Performance):** Graph node queries and rendering must complete within 1.5 seconds for graphs with up to 10,000 nodes.
* **NFR-2 (Scalability):** Data storage architecture must support scaling up to $10^5$ research paper records without degrading search performance.
* **NFR-3 (Usability):** UI layout must adhere to modern accessibility standards (WCAG 2.1 AA compliant).
* **NFR-4 (Reliability):** Document parsing pipelines must maintain a success rate $\ge 98\%$ on standard double-column academic PDFs.

---

## 3. User Stories

| ID | As a... | I want to... | So that I can... |
| :--- | :--- | :--- | :--- |
| **US-01** | Researcher | Upload PDFs of literature in bulk | Quickly populate my project library. |
| **US-02** | Student | View graph nodes connecting methods to datasets | Identify which benchmarks are standard for specific techniques. |
| **US-03** | Academic | Search by concept rather than exact keyword | Uncover interdisciplinary papers related to my thesis topic. |
| **US-04** | Reviewer | Trace citation lineages visually | See how foundational papers influenced recent implementations. |