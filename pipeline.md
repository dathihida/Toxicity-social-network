```mermaid
graph LR
    classDef input fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef process fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef decision fill:#fff9c4,stroke:#f9a825,stroke-width:2px;
    classDef llm fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px;
    classDef output fill:#ffe0b2,stroke:#ef6c00,stroke-width:2px;

    Start[New Comment] --> Input[Input]:::input

    subgraph Data["Data"]
        Cmt[Comment]
        Ctx[Context]
    end

    Input --> Cmt
    Input --> Ctx

    Cmt --> Prep[Preprocessing]:::process
    Ctx --> Prep

    Prep --> LSTM[LSTM]:::process
    LSTM --> D1{Confident?}:::decision

    D1 -->|Yes| Out
    D1 -->|No| BERT[PhoBERT]:::process

    BERT --> D2{Confident?}:::decision
    D2 -->|Yes| Out
    D2 -->|No| LLM[LLM]:::llm

    LLM --> Out

    Out[Label + Prob]:::output --> Ext[Extension]
