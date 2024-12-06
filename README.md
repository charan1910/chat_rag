# CHAT_RAG: Retrieval-Augmented Generation Pipeline

RAGify is a Flask-based Retrieval-Augmented Generation (RAG) pipeline for processing and querying large documents. It combines the power of document chunking, embedding-based retrieval, and generative AI to deliver contextual answers.

---

## Features

- Upload and process PDF documents.
- Extract text and split it into meaningful chunks using a sliding window approach.
- Generate embeddings for efficient similarity search.
- Use FAISS for fast and scalable vector indexing.
- Query relevant document chunks and generate responses using a custom LLM chain.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/charan1910/chat_rag.git
   cd chatrag
