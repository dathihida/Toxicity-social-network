import torch
import torch.nn as nn
from transformers import AutoModel


class Attention(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.attn = nn.Linear(hidden_dim, 1)

    def forward(self, x, mask):
        scores = self.attn(x).squeeze(-1)
        scores = scores.masked_fill(mask == 0, -1e9)
        weights = torch.softmax(scores, dim=1)
        return torch.sum(x * weights.unsqueeze(-1), dim=1)


class PhoBERT_LSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = AutoModel.from_pretrained("vinai/phobert-base")

        self.lstm = nn.LSTM(
            input_size=768,
            hidden_size=256,
            batch_first=True,
            bidirectional=True
        )

        self.attention = Attention(512)
        self.fc = nn.Linear(512, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, input_ids, attention_mask):
        with torch.no_grad():
            outputs = self.bert(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

        x = outputs.last_hidden_state
        x, _ = self.lstm(x)
        x = self.attention(x, attention_mask)
        return self.sigmoid(self.fc(x)).squeeze(-1)
