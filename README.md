# 🌪️ AI Disaster Chatbot

A lightweight AI-powered chatbot that helps users during natural disasters by providing guidance, safety protocols, and actionable steps. Built with **FastAPI**, **TinyLlama**, and **FAISS**, this chatbot uses a **Retrieval-Augmented Generation (RAG)** approach to combine real-world disaster knowledge with open-ended reasoning.

---

## 🚀 Features

- 🔍 Semantic search using **FAISS**
- 🤖 Fast, quantized **TinyLlama-1.1B-Chat** model for chatbot responses
- 🧠 Hybrid RAG system (context-aware when relevant, fallback to general chat when not)
- ⚡ Lightweight, fast, and deployable on free-tier services like **Render**
- 🔌 Easily integratable into **Wix**, websites, and mobile apps via REST API

---

## 🗂️ Folder Structure

ai-disaster-chatbot/ ├── app/ │ ├── main.py # FastAPI backend │ ├── disaster_index.faiss # Vector index for semantic search │ ├── disaster_metadata.json # Indexed metadata chunks │ └── models/ │ └── all-MiniLM-L6-v2/ # Embedding model (optional, auto-downloadable) ├── requirements.txt # All Python dependencies ├── .gitignore # Ignore cache and temp files └── README.md # You're reading it!

yaml
Copy
Edit

---

## 🛠️ Setup Instructions

### 🔁 Clone the Repo

```bash
git clone https://github.com/adityakumar0308/ai-disaster-chatbot.git
cd ai-disaster-chatbot
📦 Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Ensure you're using Python 3.10+ for compatibility.

🚀 Run the Server
bash
Copy
Edit
uvicorn app.main:app --host 0.0.0.0 --port 8000
API will be available at: http://localhost:8000/docs

🤖 How It Works
User sends a message like “What should I do in a flood?”

The query is embedded using all-MiniLM-L6-v2

FAISS searches for top relevant chunks from your custom disaster dataset

If relevance is high, the context + query is passed to TinyLlama

If not, the model responds generically using just the query

Final answer is returned in a chatbot-friendly format

🧠 Technologies Used
FastAPI

TinyLlama (quantized for speed)

FAISS for semantic retrieval

Sentence-Transformers for embeddings

🌐 Deployment Guide (Render)
Push this repo to GitHub

Go to Render.com

Create a new Web Service

Set:

Build Command: pip install -r requirements.txt

Start Command: uvicorn app.main:app --host 0.0.0.0 --port 10000

Python version: 3.10+

Add your Hugging Face token as an environment variable if needed

💬 Wix Integration
Add this to your Wix frontend JavaScript:

js
Copy
Edit
fetch("https://your-api-url.onrender.com/query", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ query: "What do I do during a wildfire?" })
})
.then(res => res.json())
.then(data => {
  // Display chatbot response
  console.log(data.answer);
});
🧾 API Reference
POST /query

json
Copy
Edit
Request:
{
  "query": "How can I stay safe during a cyclone?"
}

Response:
{
  "answer": "Make sure your phone is charged, stay indoors, and listen to local authorities for updates."
}
📜 License
MIT License. Use, adapt, and build on it freely!

🙌 Acknowledgements
Hugging Face

Sentence Transformers

FAISS by Facebook AI Research

TinyLlama Team

Made with ❤️ to help people in disaster situations.
