from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer, util
import faiss
import json
import torch
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS for all origins (replace with your domain for security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model and index
embed_model = SentenceTransformer("models/all-MiniLM-L6-v2")
index = faiss.read_index("disaster_index.faiss")
with open("disaster_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load FLAN-T5 model
model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cpu")
model.eval()

# Request/response models
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

# Generate chatbot response
def generate_response(prompt, max_new_tokens=200):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.95
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

# API endpoint
@app.post("/query", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    user_query = req.query
    query_embedding = embed_model.encode([user_query])
    D, I = index.search(query_embedding, k=2)
    top_chunks = [metadata[i]["content"] for i in I[0]]
    top_embeddings = embed_model.encode(top_chunks)
    similarities = [float(util.cos_sim(query_embedding[0], emb)) for emb in top_embeddings]
    best_score = max(similarities)

    SIM_THRESHOLD = 0.5
    if best_score >= SIM_THRESHOLD:
        selected_context = "\n".join(top_chunks)
        prompt = f"Answer the question using the context.\n\nContext:\n{selected_context}\n\nQuestion: {user_query}\nAnswer:"
    else:
        prompt = f"Answer the question as best as you can.\n\nQuestion: {user_query}\nAnswer:"

    answer = generate_response(prompt)
    return ChatResponse(answer=answer)
