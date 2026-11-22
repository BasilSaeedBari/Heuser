# Deliverable 3: User Prompts & Reflection Log
**User ID:** 2028010416  
**System:** Research Paper Library & Knowledge Graph Application  

---

## Verbatim User Prompts Executed

### Prompt 1 (Context Engineering Pack Generation)
> "Generate Deliverable 1: Context Engineering Pack for my Research Paper Library & Knowledge Graph system. Include all 12 sections detailed in Section 6.1.5, including PDF extraction challenges, citation styles, API schemas, tool evaluation matrix, graph schemas, edge cases, real paper excerpts, and sifting log. Append my user ID 2028010416."

### Prompt 2 (System Execution Plan)
> "Create Deliverable 2 containing Sections A through D with complete system architecture diagrams, tech stack choices, code prompt chains with acceptance tests, and build execution logs for project ID 2028010416."

### Prompt 3 (Full End-To-End Interactive Web App Implementation)
> "Create a complete, single-file interactive Web Application for the Research Paper Library and Knowledge Graph system. Include an upload tab for PDF text parsing, manual metadata search via arXiv/DOI, structured paper library management with filtering, and a force-directed Knowledge Graph visualization powered by Vis.js."

---

## Tools & Libraries Utilized

* **Vis.js Network Engine**: Rendered interactive force-directed graph diagrams directly in the frontend browser context without external server dependencies.
* **Tailwind CSS CDN**: Rendered responsive web UI components, modal dialogs, tag chips, and layout grids.
* **Lucide Icons**: Standardized icons for action buttons, navigation tabs, and system status indicators.
* **Regex Engine**: Handled DOI and arXiv identifier pattern matching.

---

## Reflection & System Analysis

1. **Key Insight on Knowledge Graphs**: Constructing direct author-to-author `CO_AUTHORED_WITH` edges during paper ingestion drastically reduces graph traversal complexity, enabling instant visual exploration of author networks without compute-heavy graph join transformations.
2. **Spatial Parsing Trade-offs**: While pure OCR engines process raster images effectively, spatial coordinate extraction via bounding box grouping provides a multi-fold speed advantage for native vector PDFs.
3. **User Interface Integration**: Providing immediate visual feedback through interactive node highlighting and real-time paper library filtering significantly enhances research workflow efficiency.