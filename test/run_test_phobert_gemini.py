import torch
import pandas as pd
from transformers import AutoTokenizer
from phobert_lstm_attention import PhoBERT_LSTM
from run_gemini import llm_predict

MODEL_PATH = "toxicity_model.pt"
TEST_FILE = "test_train.xlsx"

TEXT_COLUMN = "Comment"
TITLE_COLUMN = "Title"
TOPIC_COLUMN = "Topic"

LOW_TH = 0.35
HIGH_TH = 0.65

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

model = PhoBERT_LSTM()
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.to(DEVICE)
model.eval()

df = pd.read_excel(TEST_FILE)

final_labels = []
final_conf = []
used_llm = []
probs = []

with torch.no_grad():
    for _, row in df.iterrows():
        comment = str(row[TEXT_COLUMN])
        title = str(row.get(TITLE_COLUMN, ""))
        topic = str(row.get(TOPIC_COLUMN, ""))

        inputs = tokenizer(
            comment,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=128
        )

        input_ids = inputs["input_ids"].to(DEVICE)
        attention_mask = inputs["attention_mask"].to(DEVICE)

        prob = model(input_ids, attention_mask).item()

        if prob < LOW_TH:
            final_labels.append(0)
            final_conf.append(round((1 - prob) * 100, 2))
            used_llm.append(0)
            probs.append(prob)

        elif prob > HIGH_TH:
            final_labels.append(1)
            final_conf.append(round(prob * 100, 2))
            used_llm.append(0)
            probs.append(prob)

        else:
            is_toxic = llm_predict(
                comment=comment,
                title=title,
                topic=topic
            )

            final_labels.append(1 if is_toxic else 0)
            final_conf.append(50.0)
            used_llm.append(1)
            probs.append(prob)

df["final_label"] = final_labels
df["confidence_%"] = final_conf
df["used_LLM"] = used_llm
df["prob"] = probs
df.to_excel("result_phobert_gemini.xlsx", index=False)

print("Done! Saved to result_phobert_gemini.xlsx")
