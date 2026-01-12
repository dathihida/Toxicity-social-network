import torch
import pandas as pd
from transformers import AutoTokenizer
from phobert_lstm_attention import PhoBERT_LSTM


MODEL_PATH = "toxicity_model.pt"
TEST_FILE = "test_train.xlsx"
TEXT_COLUMN = "Comment" 
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

model = PhoBERT_LSTM()
state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
model.load_state_dict(state_dict)
model.to(DEVICE)
model.eval()

df = pd.read_excel(TEST_FILE)

scores = []
labels = []
pct_toxic = []
pct_non_toxic = []

with torch.no_grad():
    for text in df[TEXT_COLUMN]:
        inputs = tokenizer(
            str(text),
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=128
        )

        input_ids = inputs["input_ids"].to(DEVICE)
        attention_mask = inputs["attention_mask"].to(DEVICE)

        prob = model(input_ids, attention_mask).item()

        score = prob * 100
        label = 1 if prob >= 0.5 else 0

        scores.append(score)
        labels.append(label)
        pct_toxic.append(score)
        pct_non_toxic.append(100 - score)

# luu kết quả
df["toxicity_score"] = scores
df["predicted_label"] = labels
df["toxic_%"] = pct_toxic
df["non_toxic_%"] = pct_non_toxic

df.to_excel("result_test.xlsx", index=False)

print("Done! Result saved to result_test.xlsx")
