

# 📄 PDF Chatbot using LangChain, RAG, Gemini & FAISS

A **PDF Question Answering Chatbot** built using **Streamlit, LangChain, Google Gemini API, and FAISS**.  
This project allows users to **upload a PDF, process its contents, and ask questions based on the uploaded document**.

The chatbot uses a **basic RAG (Retrieval-Augmented Generation) pipeline**:
- extract text from the PDF
- split it into chunks
- generate embeddings
- store them in a FAISS vector database
- retrieve the most relevant chunks for a user question
- send the retrieved context to Gemini to generate the final answer

---

# 🚀 Project Overview

Large Language Models are powerful, but they do not automatically know the content of a private PDF uploaded by the user.  
To solve this, this project uses a **RAG-based approach** so that the chatbot answers using the **content of the uploaded PDF**, not only the model’s general knowledge.

This project demonstrates how **LangChain + RAG + Vector Search + Gemini** can be combined to build a practical **document-aware Generative AI application**.

---

# ✨ Features

- 📤 Upload a PDF file
- 📚 Extract text from the uploaded PDF
- ✂️ Split the PDF text into chunks using LangChain
- 🧠 Generate embeddings using **Google Gemini Embeddings**
- 🗂️ Store embeddings in **FAISS vector database**
- 🔎 Retrieve relevant PDF chunks for a user question
- 💬 Generate answers using **Gemini**
- 🖥️ Simple and interactive **Streamlit UI**
- 🔐 Uses **`.gitignore`** to avoid uploading sensitive and unnecessary files

---

# 🧠 Core Concepts Used

## 1) LangChain
LangChain is used in this project for:
- **text splitting**
- **prompt templating**
- **vector store integration**
- **Gemini model / embedding integration**

## 2) RAG (Retrieval-Augmented Generation)
This project is a **basic RAG-based PDF chatbot**.

Instead of directly asking the LLM to answer only from its pre-trained knowledge, the system:
1. retrieves relevant content from the uploaded PDF
2. adds that content to the prompt
3. asks Gemini to generate the answer based on the retrieved context

---

# 🏗️ Tech Stack

- **Python**
- **Streamlit** – web interface
- **LangChain** – LLM application framework
- **Google Gemini API** – embeddings + answer generation
- **FAISS** – vector database for semantic retrieval
- **PyPDF** – PDF text extraction
- **python-dotenv** – environment variable management

---

# 🔄 Project Workflow

```text
User uploads PDF
      ↓
Extract text from PDF
      ↓
Split text into chunks
      ↓
Generate embeddings using Gemini Embeddings
      ↓
Store embeddings in FAISS
      ↓
User asks a question
      ↓
Retrieve relevant chunks from FAISS
      ↓
Add retrieved chunks to prompt
      ↓
Send prompt to Gemini
      ↓
Generate final answer
````

---

# 📂 Project Structure

```bash
PDF_ChatBot/
│── app.py              # Main Streamlit application
│── requirements.txt    # Project dependencies
│── .gitignore          # Excludes sensitive/unnecessary files
│── README.md           # Project documentation
```

---

# 🔐 Security Note

This project uses a **`.gitignore`** file to prevent uploading sensitive or unnecessary files to GitHub.

## Files excluded:

* **`venv/`** → virtual environment folder
* **`.env`** → contains the **Gemini API key**
* **`__pycache__/`** and Python cache files

### Why?

* The **virtual environment** is large and system-specific, so it should not be pushed to GitHub.
* The **API key** is confidential and must not be exposed publicly.
* Cache files are unnecessary for the repository.

## Example `.gitignore`

```gitignore
venv/
.env
__pycache__/
*.pyc
```

---


# 📌 Requirements

The project uses the following packages:

```txt
streamlit
langchain
langchain-community
langchain-google-genai
langchain-text-splitters
faiss-cpu
pypdf
python-dotenv
```

---

# 💡 How It Works in This Project

## Step 1: PDF Processing

* User uploads a PDF
* Text is extracted using **PyPDF**
* The text is split into chunks using **LangChain’s RecursiveCharacterTextSplitter**

## Step 2: Embedding + Storage

* Each chunk is converted into embeddings using **Gemini Embeddings**
* The embeddings are stored in **FAISS**

## Step 3: Question Answering

* User asks a question
* The app retrieves the most relevant chunks from FAISS
* Those chunks are passed as **context** to Gemini
* Gemini generates the final answer

---

# 📚 Example Use Cases

* Student PDF Q&A assistant
* Notes summarizer
* Research paper question answering
* Document understanding chatbot
* Study material assistant

---

# 🌟 Why this project is useful

This project shows how **Generative AI can be combined with retrieval systems** to build useful applications on top of **private documents**.

It is a practical example of:

* **LangChain-based application development**
* **RAG architecture**
* **vector databases**
* **LLM-powered document understanding**

---

# 🚧 Future Enhancements

* Support for **multiple PDF uploads**
* Chat history / conversational memory
* Better UI with sidebar and PDF preview
* Save FAISS index locally
* Add document summarization
* Add keyword extraction / topic extraction
* Support larger PDFs with optimized retrieval

---
