# preprocessing/build_dataset.py

import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from clean_text import preprocess_text, load_stopwords

RAW_PATH = "../data/raw/comment_toxic_test_train.xlsx"
STOPWORD_PATH = "../data/raw/vietnamese-stopwords-dash.txt"
OUT_DIR = "../data/processed/"

tqdm.pandas()


def main():
    print("Loading data...")
    df = pd.read_excel(RAW_PATH)

    required_cols = ["Comment", "Toxicity", "Title", "Topic"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"❌ Missing column: {col}")

    stopwords = load_stopwords(STOPWORD_PATH)

    print("Preprocessing text...")
    df["comment_clean"] = df["Comment"].progress_apply(
        lambda x: preprocess_text(str(x), stopwords)
    )
    df["title_clean"] = df["Title"].progress_apply(
        lambda x: preprocess_text(str(x), stopwords)
    )
    df["topic_clean"] = df["Topic"].progress_apply(
        lambda x: preprocess_text(str(x), stopwords)
    )

    print("Build contextual input...")
    df["text"] = (
        "[TITLE] "
        + df["title_clean"]
        + " [TOPIC] "
        + df["topic_clean"]
        + " [COMMENT] "
        + df["comment_clean"]
    )

    df_final = df[["text", "Toxicity"]].rename(
        columns={"Toxicity": "label"}
    )

    print("Split dataset...")
    train_df, test_df = train_test_split(
        df_final, test_size=0.15, random_state=42, stratify=df_final["label"]
    )

    train_df, val_df = train_test_split(
        train_df, test_size=0.15, random_state=42, stratify=train_df["label"]
    )

    print("Saving files...")
    train_df.to_csv(OUT_DIR + "train.csv", index=False)
    val_df.to_csv(OUT_DIR + "val.csv", index=False)
    test_df.to_csv(OUT_DIR + "test.csv", index=False)

    print("DONE")
    print("Train:", train_df.shape)
    print("Val  :", val_df.shape)
    print("Test :", test_df.shape)


if __name__ == "__main__":
    main()
