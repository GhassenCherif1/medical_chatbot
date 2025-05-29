# 🩺 Medical Chatbot (FastAPI + Docker)

A medical chatbot specialized in respiratory diseases, built with FastAPI and containerized using Docker.

---

## 🚀 Features

- FastAPI backend for high-performance medical Q&A
- ChromaDB for embedding storage


---

## 📦 Requirements

- [Docker](https://www.docker.com/get-started)
- [Ollama](https://ollama.com/)
- [Git](https://git-scm.com/)

---

## 🧠 Using Ollama for LLM and Embedding Models

This project uses [Ollama](https://ollama.com) to run large language and embedding models locally.

### 1. Install Ollama

Download and install Ollama from:  
👉 https://ollama.com/download

### 2. Pull Required Models

After installing Ollama, pull the models used in this project:

```bash
ollama pull llama3.2:1b-instruct-q6_K
ollama pull bge-m3
```

---
## 🐳 Deploying with Docker

Follow these steps to deploy the project using Docker:

### 1. Clone the Repository

```bash
git clone https://github.com/GhassenCherif1/medical_chatbot.git
cd medical_chatbot
```
### 2. Build the Docker Image

```bash
docker build -t medical_chatbot .
```

### 3. Run the Docker Container

```bash
docker run -p 8000:8000 medical_chatbot
```

The app will be available at:
👉 http://localhost:8000

API docs (Swagger UI):
👉 http://localhost:8000/docs

