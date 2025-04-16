Here's an improved version of your `README.md` with a more human-friendly tone, better structure, and the additional information included:

---

# 🌪️ AI Disaster Chatbot

A lightweight, AI-powered chatbot designed to assist users during natural disasters by providing crucial guidance, safety protocols, and actionable steps. Powered by **FastAPI**, **TinyLlama**, and **FAISS**, this chatbot combines real-world disaster knowledge with open-ended reasoning using a **Retrieval-Augmented Generation (RAG)** approach.

---

## 🚀 Key Features

- **🔍 Semantic Search**: Uses **FAISS** for fast, contextually aware search of disaster-related content.
- **🤖 Fast AI Responses**: Powered by the quantized **TinyLlama-1.1B-Chat** model for quick, relevant answers.
- **🧠 Hybrid RAG System**: Context-aware when needed; falls back to general chat when necessary.
- **⚡ Lightweight & Fast**: Optimized for quick deployment on free-tier services like **Render**.
- **🔌 Easy Integration**: Can be seamlessly embedded into **Wix**, websites, and mobile apps via a REST API.

---

## 🗂️ Project Structure

Here's the breakdown of the project folder structure:

```
ai-disaster-chatbot/
├── app/
│   ├── main.py               # FastAPI backend
│   ├── disaster_index.faiss  # Vector index for semantic search
│   ├── disaster_metadata.json # Metadata for indexed chunks
│   └── models/
│       └── all-MiniLM-L6-v2/ # Embedding model (auto-downloadable)
├── requirements.txt          # Python dependencies
├── .gitignore                # Ignore cache and temp files
└── README.md                 # You're reading it!
```

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/adityakumar0308/ai-disaster-chatbot.git
cd ai-disaster-chatbot
```

### 2️⃣ Install Dependencies

Make sure you have Python 3.10+ installed, then install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Server

To start the FastAPI server, run:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Your API will now be live at [http://localhost:8000/docs](http://localhost:8000/docs), where you can interact with the chatbot and explore its API documentation.

#### 🚀 Run FastAPI with Uvicorn on a different port

If you'd prefer to run the server on port `10000`, use the following command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

---

## 🤖 How It Works

Here’s the step-by-step breakdown of how the chatbot functions:

1. **User Input**: The user asks a question like "What should I do in a flood?"
2. **Embedding**: The query is embedded using the **all-MiniLM-L6-v2** model.
3. **FAISS Search**: FAISS performs a semantic search to find the most relevant disaster-related information.
4. **Contextual Response**: If the retrieved content is relevant, it's passed to **TinyLlama** for a context-aware response.
5. **Fallback Response**: If the relevance is low, **TinyLlama** provides a generic answer.
6. **Final Answer**: The chatbot responds with a human-friendly, helpful answer.

---

## 🧠 Technologies Used

- **FastAPI** for building the backend and API endpoints
- **TinyLlama** (quantized for speed) for generating chatbot responses
- **FAISS** by Facebook AI Research for efficient semantic search
- **Sentence-Transformers** for generating embeddings from user queries

---

## 🌐 Deployment Guide (Render)

Deploy the chatbot on **Render** for easy, scalable hosting. Here’s how to do it:

1. Push your repo to GitHub.
2. Go to [Render.com](https://render.com) and create a new Web Service.
3. Set the following options:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
   - **Python Version**: 3.10+
4. Add your Hugging Face token as an environment variable if necessary.

---

## 💬 Wix Integration

You can integrate this chatbot into your **Wix** site with just a few lines of JavaScript. Here’s an example:

```javascript
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
```

---

## 🧾 API Reference

### POST /query

#### Request Example:

```json
{
  "query": "How can I stay safe during a cyclone?"
}
```

#### Response Example:

```json
{
  "answer": "Make sure your phone is charged, stay indoors, and listen to local authorities for updates."
}
```

---

## 🙌 Acknowledgements

A big thank you to the following libraries and teams that made this possible:

- **Hugging Face** for their powerful models.
- **Sentence Transformers** for embeddings.
- **FAISS** by Facebook AI Research for semantic search.
- **TinyLlama Team** for the lightweight model.
- And finally, a special thanks to all contributors who help improve disaster response!

---

This project was created with ❤️ to assist people in disaster situations, providing them with accurate, quick guidance when they need it most.

