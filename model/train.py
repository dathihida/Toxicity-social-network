
import torch
import pandas as pd
from torch.utils.data import DataLoader
from transformers import AutoTokenizer
from sklearn.metrics import accuracy_score, f1_score
from tqdm import tqdm

from dataset import ToxicDataset
from phobert_lstm_attention import PhoBERT_LSTM

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 16
EPOCHS = 5
LR = 1e-3

def load_data(path):
    df = pd.read_csv(path)
    return df["text"].tolist(), df["label"].tolist()

def train_epoch(model, loader, optimizer, loss_fn):
    model.train()
    losses = []

    for batch in tqdm(loader):
        optimizer.zero_grad()
        out = model(
            batch["input_ids"].to(DEVICE),
            batch["attention_mask"].to(DEVICE)
        )
        loss = loss_fn(out, batch["label"].to(DEVICE))
        loss.backward()
        optimizer.step()
        losses.append(loss.item())

    return sum(losses) / len(losses)

def eval_model(model, loader):
    model.eval()
    preds, labels = [], []

    with torch.no_grad():
        for batch in loader:
            out = model(
                batch["input_ids"].to(DEVICE),
                batch["attention_mask"].to(DEVICE)
            )
            preds.extend(out.cpu().numpy())
            labels.extend(batch["label"].numpy())

    preds_bin = [1 if p >= 0.5 else 0 for p in preds]
    return (
        accuracy_score(labels, preds_bin),
        f1_score(labels, preds_bin)
    )

def main():
    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

    X_train, y_train = load_data("train.csv")
    X_val, y_val = load_data("val.csv")

    train_ds = ToxicDataset(X_train, y_train, tokenizer)
    val_ds = ToxicDataset(X_val, y_val, tokenizer)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE)

    model = PhoBERT_LSTM().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = torch.nn.BCELoss()

    best_f1 = 0

    for epoch in range(EPOCHS):
        print(f"\nEpoch {epoch+1}/{EPOCHS}")
        loss = train_epoch(model, train_loader, optimizer, loss_fn)
        acc, f1 = eval_model(model, val_loader)

        print(f"Loss: {loss:.4f} | Acc: {acc:.4f} | F1: {f1:.4f}")

        if f1 > best_f1:
            best_f1 = f1
            torch.save(model.state_dict(), "toxicity_model.pt")
            print("✅ Saved best model")

if __name__ == "__main__":
    main()
