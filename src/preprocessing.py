"""
src/preprocessing.py
Functions for loading, cleaning, and splitting the Twi and Ewe corpora.
"""
import re
import unicodedata
from pathlib import Path
import pandas as pd
from datasets import load_dataset

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def download_raw(dataset_name: str, language: str, text_column: str = "label") -> pd.DataFrame:
    """Downloads a Ghana-NLP dataset and saves the raw sentences untouched."""
    ds = load_dataset(dataset_name, split="train")
    df = ds.to_pandas()
    out_path = RAW_DIR / language / "raw_sentences.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Saved {len(df)} raw rows for {language} to {out_path}")
    return df


def clean_text(text: str) -> str:
    """Normalises unicode, trims whitespace, and collapses repeated spaces."""
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFC", text)
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def clean_dataframe(df: pd.DataFrame, text_column: str) -> pd.DataFrame:
    """Cleans, deduplicates, and drops empty or too-short sentences."""
    df = df.copy()
    if text_column not in df.columns and "label" in df.columns:
        df = df.rename(columns={"label": text_column})
    df[text_column] = df[text_column].apply(clean_text)
    df = df[df[text_column].str.len() > 0]
    df = df.drop_duplicates(subset=[text_column])
    df = df[df[text_column].str.split().str.len() >= 2]
    return df.reset_index(drop=True)


def split_and_save(df: pd.DataFrame, text_column: str, language: str,
                   train_frac=0.8, val_frac=0.1, seed=42) -> None:
    """Splits cleaned sentences into train/val/test and saves each as .txt,
    one sentence per line, ready for tokenizer training and evaluation."""
    if text_column not in df.columns and "label" in df.columns:
        df = df.rename(columns={"label": text_column})
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    n = len(df)
    n_train = int(n * train_frac)
    n_val = int(n * val_frac)
    splits = {
        "train": df.iloc[:n_train],
        "val": df.iloc[n_train:n_train + n_val],
        "test": df.iloc[n_train + n_val:],
    }
    out_dir = PROCESSED_DIR / language
    out_dir.mkdir(parents=True, exist_ok=True)
    for split_name, split_df in splits.items():
        out_path = out_dir / f"{split_name}.txt"
        split_df[text_column].to_csv(out_path, index=False, header=False, encoding="utf-8")
        print(f"{language} {split_name}: {len(split_df)} sentences saved to {out_path}")
