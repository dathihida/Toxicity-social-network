from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer
import time

from model.phobert_lstm_attention import PhoBERT_LSTM
from utils.preprocessing import preprocess_text
from utils.llm_fallback import llm_predict

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

#  APP 
app = FastAPI(title="Vietnamese Toxic Comment API (2025)")

DEVICE = torch.device("cpu")

#  TOKENIZER
tokenizer = AutoTokenizer.from_pretrained(
    "vinai/phobert-base",
    use_fast=False
)

#  MODEL
model = PhoBERT_LSTM()
model.load_state_dict(
    torch.load("weights/toxicity_model.pt", map_location=DEVICE)
)
model.eval()

#  REQUEST 
class CommentRequest(BaseModel):
    comment: str
    title: str
    topic: str

#  CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Private-Network"],
)

@app.options("/{path:path}")
async def preflight_handler(path: str):
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response

@app.middleware("http")
async def add_pna_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

LAST_LLM_CALL = 0
LLM_COOLDOWN = 45 

def can_call_llm():
    global LAST_LLM_CALL
    now = time.time()
    if now - LAST_LLM_CALL >= LLM_COOLDOWN:
        LAST_LLM_CALL = now
        return True
    return False

@app.post("/predict")
def predict(req: CommentRequest):
    text = preprocess_text(req.comment, req.title, req.topic)

    encoded = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=128
    )

    with torch.no_grad():
        output = model(
            encoded["input_ids"],
            encoded["attention_mask"]
        )

    prob = round(float(output.item() * 100), 2)
    if prob >= 65:
        toxic = True
        source = "phobert"

    elif prob <= 35:
        toxic = False
        source = "phobert"

    else:
        if can_call_llm():
            toxic = llm_predict(req.comment, req.title, req.topic)
            source = "llm"
        else:
            toxic = True
            source = "failsafe"

    return {
        "toxic": toxic,
        "confidence": prob,
        "source": source
    }
