# Personal Research Assistant Agent

An end-to-end **Agentic AI research system** that takes a user query, retrieves relevant academic papers from arXiv, semantically analyzes them, and generates a **well-structured research report** using Large Language Models (LLMs).

This project demonstrates a complete research automation pipeline - from intelligent query planning to final synthesized report generation — accessible through an interactive Streamlit interface.

---

## Overview

The Personal Research Assistant Agent automates the research workflow:

1. Understands and refines a research query  
2. Retrieves relevant academic papers from arXiv  
3. Processes and chunks retrieved documents  
4. Generates semantic embeddings  
5. Performs vector-based retrieval  
6. Synthesizes findings using an LLM  
7. Streams a structured research report in real-time 

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
Structured Research Report (UI)
```

## Project Structure

```
src/
├── agent.py
├── planner.py 
├── retriever.py 
├── summarizer.py
├── .gitignore
├── README.md
├── Dockerfile
├── .dockerignore
│
├── models/
│   └── llms.py
│   └── embeddings.py
│
├── utils/
│   ├── chunking.py
│   ├── vector_store.py
│   └── logging.py
│
└── web/
    └── app.py

```

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd personal-research-assistant
```

### 2. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Set environment variables
```
GROQ_API_KEY=your_groq_api_key_here
ARXIV_API_URL=http://export.arxiv.org/api/query
```

### 5. Running the Application
```
streamlit run src/web/app.py
```
