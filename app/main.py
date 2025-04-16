from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from sentence_transformers import SentenceTransformer, util
import faiss
import json
import torch

app = FastAPI()

# Load embedding model
embed_model = SentenceTransformer("models/all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("disaster_index.faiss")

# Load metadata
with open("disaster_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load TinyLlama model (4-bit quantized)
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)
model.eval()

# Define request/response models
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

# Generate chatbot response
def generate_response(prompt, max_new_tokens=250):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
            pad_token_id=tokenizer.eos_token_id
        )
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    return response_text.split("Answer:")[-1].strip() if "Answer:" in response_text else response_text

# Chat endpoint
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
        prompt = (
            f"You are a disaster management assistant. Use the context below to help the user.\n\n"
            f"Context:\n{selected_context}\n\n"
            f"Question: {user_query}\n"
            f"Answer:"
        )
    else:
        prompt = (
            f"You are a helpful assistant. Respond conversationally.\n\n"
            f"User: {user_query}\n"
            f"Assistant:"
        )

    answer = generate_response(prompt)
    return ChatResponse(answer=answer)
