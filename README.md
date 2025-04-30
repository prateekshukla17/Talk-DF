# Talk-DF

A full-stack AI-powered web application that allows users to upload PDF documents and ask questions based on their content using RAG (Retrieval-Augmented Generation) with LangChain and LLM integration.

## Features

- Upload PDF documents from the frontend

- Ask natural language questions based on PDF content

- Uses LangChain with vector embeddings and RAG to generate accurate answers

- Real-time Q&A chat interface

- Clean UI with feedback states (uploading, processing, typing...)

- Robust FastAPI backend handling PDF processing, vector storage, and question handling

## Tech Stack

### Frontend

- React.js
- TailwindCSS
- React Router

### Backend

- FastAPI

- LangChain

- PyMuPDF (for PDF text extraction)

- ChromaDB / FAISS (for vector embeddings)

- OpenAI / LLM API (via LangChain)

- SQLite (for storing metadata)

## File Structure

```bash
/frontend
  ├── src/
  │   ├── Chat.jsx
  │   ├── Dashboard.jsx
  │   └── App.jsx

Backend/
├── services/
│   ├── uploads/
│   ├── vectorstore/
│   ├── pdf_text_handler.py
│   ├── server.py
│   └── test.py

```

## Installation & Setup

### Backend Setup

```bash
cd backend
python -m venv venv
source \Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## API Endpoint

`POST /process`

- Accepts: PDF File

- Action: Extracts text, creates vector embeddings, initializes conversation chain

`POST /ask`

- Accepts: { question: "your question" }

- Action: Uses LangChain to answer question based on the uploaded document

## System Achitecture

![Architecture](Arch.png)

- User uploads a PDF

- Backend extracts text using PyMuPDF

- Vector embeddings are created using LangChain

- Vectors are stored in memory (Chroma / FAISS)

- User sends a question → LangChain retrieves relevant chunks using similarity search

- LLM (like OpenAI) generates the final response

- Response is displayed in the chat UI

## Limitations

- While the application demonstrates a fully functional end-to-end RAG pipeline, there are a few known limitations:

- Local Model Performance: Running embedding models and LLMs locally can be resource-intensive and slow, especially on machines without dedicated GPUs.

- Response Time: The time taken to generate responses can be significant due to local vector search and model inference delays.

- OpenAI Integration (Optional): Using OpenAI’s hosted models (via API) significantly improves response time and output quality, but may require a valid API key and incurs usage costs.

## Author

Prateek Shukla
🔗 [Linked In](www.linkedin.com/in/prateekshukla17)
