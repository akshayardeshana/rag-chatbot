# RAG-Based Complaint Chatbot

This project is a Retrieval-Augmented Generation (RAG) based chatbot that allows users to:
- Interact with an intelligent assistant using natural language
- Register complaints via a conversational flow
- Check complaint status using complaint_id
- Retrieve relevant answers from a knowledge base

---

## Features

- Conversational chatbot built with **Streamlit**
- RAG integration using **LangChain** and **Groq (LLaMA3)** for smart responses
- Vectorized knowledge base using **Chroma**
- Complaint API built with **FastAPI**
- Stores and retrieves complaints from an **SQLite** database
- Interactive step-by-step data collection (name, phone, issue)
- Simple REST API for complaint creation and retrieval

---

## 🗂Project Structure

```bash
.
├── app.py                # Streamlit chatbot interface
├── api.py                # FastAPI complaint registration & status API
├── rag_engine.py         # RAG logic using Groq + Chroma
├── db.py                 # Complaint database handler (SQLite)
├── sample_kb.txt         # Knowledge base for retrieval
├── requirements.txt      # All dependencies
