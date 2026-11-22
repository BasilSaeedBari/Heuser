# Deliverable 3: System Architecture & Technical Design

**Project Title:** Research Paper Library & Knowledge Graph System  
**User ID:** [HeUserID]  

---

## 1. System Architecture Overview

The system follows a modular microservice-oriented design structured into four key layers:

1. **Ingestion & Processing Layer:** Handles file uploads, text parsing (using `PyMuPDF` / `Grobid`), and OCR fallback.
2. **NLP & Extraction Layer:** Leverages LLM/NER pipelines to transform unstructured paper text into structured triples $(Entity_1, Relation, Entity_2)$.
3. **Data Persistence Layer:**
   * **Graph DB (Neo4j):** Stores graph topology (nodes and edge relationships).
   * **Vector DB (Milvus / Qdrant):** Stores document chunk embeddings for vector search.
   * **Relational DB (PostgreSQL):** Stores user profiles, metadata, and app config.
4. **Presentation & Application Layer:** Web application frontend providing dynamic canvas rendering and document viewer panes.

---

## 2. Data Flow Architecture

```
[ PDF Upload ] 
      │
      ▼
[ Grobid / Text Parser ] ────► [ Vector Store (Embeddings) ]
      │
      ▼
[ NLP Entity & Relation Extractor ]
      │
      ▼
[ Graph Engine (Neo4j) ] ────► [ UI API Layer (GraphQL/REST) ] ────► [ Interactive Canvas ]
```

---

## 3. Database Schema Blueprint

### Graph Database Node Schema (Cypher Example)
```cypher
// Paper Node
(:Paper {
  id: "paper_id_uuid",
  title: "String",
  year: Integer,
  doi: "String",
  abstract: "String"
})

// Method Node
(:Method {
  id: "method_id_uuid",
  name: "String",
  category: "String"
})

// Relationship Example
(p:Paper)-[:USES_METHOD {confidence: 0.94}]->(m:Method)
```

---

## 4. API Endpoints Specification

* `POST /api/v1/papers/upload` - Upload PDF for parsing and graph ingestion.
* `GET /api/v1/graph/nodes` - Query graph node clusters based on spatial coordinates or search filters.
* `GET /api/v1/graph/relationships` - Retrieve directional edges connected to specified Node ID.
* `POST /api/v1/search/semantic` - Query vector database for semantically relevant passages and return related graph nodes.