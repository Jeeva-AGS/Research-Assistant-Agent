# Personal Research Assistant Agent

An end-to-end **Agentic AI system** that accepts a research query, retrieves relevant academic papers, semantically analyzes them, and produces a **structured research report** using Large Language Models.

The system is designed with **production-grade modularity**, streaming outputs, and a clean separation of concerns.

---

## ✨ Features

- Intelligent query planning
- Academic paper retrieval (arXiv)
- Chunking + semantic embeddings
- Vector-based retrieval
- LLM-powered synthesis
- Token-by-token streaming output
- Interactive Streamlit UI with live progress updates

---

## 🧠 System Architecture

```text
User Query
   ↓
Planner
   ↓
Retriever (arXiv)
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Store
   ↓
Semantic Retrieval
   ↓
LLM Summarizer (Streaming)
   ↓
UI Output


# 📁 Project Structure

src/
├── agent.py                # Orchestrates the full research pipeline
├── planner.py              # Converts user query into search strategy
├── retriever.py            # Fetches papers from arXiv
├── summarizer.py           # LLM-based research synthesis (streaming)
│
├── models/
│   └── embeddings/
│       └── embedding_model.py
│
├── utils/
│   ├── chunking.py         # Text chunking logic
│   ├── vector_store.py     # In-memory vector storage
│   └── logging.py          # Centralized logging
│
└── web/
    └── app.py              # Streamlit UI



## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd personal-research-assistant


### 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Set environment variables
GROQ_API_KEY=your_groq_api_key_here

### 4. Running the Application
streamlit run src/web/app.py
