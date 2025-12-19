
![ssf9648217k](https://github.com/user-attachments/assets/2a2b28ed-d0dc-4d9a-bfe8-2be5b852b931)


# 📚 Research Paper Intelligence System

An AI-powered research assistant that helps researchers **ingest, organize, search, and explore academic papers** using **semantic search, vector databases (FAISS), and a Streamlit UI**.

This project implements **Part I (Paper Ingestion & Structuring)** and **Part II (Semantic Search & Indexing)** of a full Research Intelligence Platform.

---

## 🚀 Project Motivation

Researchers face major challenges today:
- Thousands of papers published every month
- Difficulty in finding relevant work quickly
- Long PDFs that are hard to scan
- Keyword search that fails to capture meaning

This system solves these problems by:
- Structuring research papers into academic sections
- Indexing papers semantically using embeddings
- Enabling meaning-based search instead of keyword search
- Providing a clean researcher-facing UI

---

## 🎯 Key Features (Current Scope)

### ✅ Part I – Paper Ingestion & Structuring
- Upload research paper PDFs
- Extract text from PDFs
- Detect academic sections (Abstract, Methodology, Experiments, etc.)
- Store papers in a structured internal representation

### ✅ Part II – Semantic Search & Indexing
- Section-aware chunking of papers
- Embedding generation using Sentence Transformers
- FAISS-based vector indexing
- Semantic search across papers and sections
- Paper-level and chunk-level result presentation

### ✅ Streamlit UI
- Upload and manage papers
- Index papers on demand
- Semantic search interface
- Full paper view on request

---

## 🧱 Project Architecture (High Level)

<img width="358" height="505" alt="image" src="https://github.com/user-attachments/assets/71c826b7-e68b-488c-aa0d-a095856806cf" />


ResearchLLM/
│
├── app.py # Streamlit UI & main orchestrator
├── requirements.txt # Project dependencies
│
├── backend/
│ ├── models.py # Data schemas (ResearchPaper, PaperSection)
│ ├── pdf_parser.py # PDF parsing & section extraction
│ ├── chunking.py # Section-based chunking logic
│ └── vector_store.py # FAISS indexing & semantic search
│
├── data/
│ └── papers/ # Uploaded PDF files
│
└── .venv/ # Python virtual environment (local)



---

## 🧠 Module-by-Module Explanation

### 1️⃣ `app.py` – UI & Orchestration Layer
- Built using **Streamlit**
- Handles:
  - PDF upload
  - Paper ingestion
  - Indexing trigger
  - Semantic search
  - Full paper view
- Controls when backend modules are executed

---

### 2️⃣ `models.py` – Data Schema Layer
Defines structured representations using **Pydantic**:

- `ResearchPaper`
- `PaperSection`

Ensures:
- Clean, validated data
- Consistent structure across the system
- Easy extensibility for future features (citations, summaries)

---

### 3️⃣ `pdf_parser.py` – PDF Understanding Layer
- Extracts raw text from PDF pages
- Detects academic section headers using regex
- Handles different formats:
  - Roman numerals (I., IV.)
  - Numbered sections (1., 2.)
  - Inline headers (Abstract—, Index Terms—)
- Outputs structured `PaperSection` objects

---

### 4️⃣ `chunking.py` – Knowledge Segmentation
- Splits each section into small semantic chunks
- Uses token-aware chunking
- Preserves metadata:
  - paper_id
  - section name
  - year
  - keywords

Chunking improves:
- Retrieval accuracy
- Embedding quality
- RAG performance (future)

---

### 5️⃣ `vector_store.py` – Semantic Memory
- Uses **Sentence Transformers** for embeddings
- Stores vectors in **FAISS**
- Provides:
  - `index_papers()` → build vector index
  - `semantic_search()` → retrieve relevant chunks

FAISS works at **chunk-level**, not document-level.

---

## 🔄 How the System Works (Step-by-Step)

### 📌 Step 1: Upload Paper
- User uploads a PDF via Streamlit
- PDF is parsed into text and sections
- A `ResearchPaper` object is created and stored in session state

### 📌 Step 2: Index Papers
- User clicks “Index All Papers”
- Sections are chunked
- Chunks are embedded
- FAISS index is created in memory

### 📌 Step 3: Semantic Search
- User enters a natural language query
- Query is embedded
- FAISS retrieves semantically similar chunks
- Results are grouped by paper and displayed

### 📌 Step 4: Show Full Paper
- If user types **“show the paper”**
- System bypasses FAISS
- Displays the full structured paper section-by-section

---

## ⚙️ Setup Instructions (Local)

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd ResearchLLM



🔮 Planned Extensions

Part III: Paper Summarization & RAG Q&A

Part IV: Citation graph & MCP tools

Part V: Research trend analysis

Persistent vector store

Multi-paper comparison
