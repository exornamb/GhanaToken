"""
scripts/run_sentiment_probe.py
Step 11: Downstream Sentiment Probe (Optional Extension)
Evaluates whether lower token fertility from GhanaTok translates into downstream
performance differences on a lightweight Twi sentiment classification task (AfriSenti).
Uses a simple bag-of-tokens Logistic Regression to ensure fairness across tokenizers.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from datasets import concatenate_datasets, load_dataset
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from transformers import PreTrainedTokenizerFast

import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
from src.tokenizer_benchmark import load_tokenizers, load_twi_only_tokenizers
from src.train_ghanatok import SentencePieceWrapper


def tokenizer_to_analyzer(tokenizer):
    """Wraps any tokenizer so CountVectorizer can use it as a text splitter."""
    return lambda text: tokenizer.tokenize(text)


def run_sentiment_probe(n_bootstraps: int = 1000, random_state: int = 42) -> pd.DataFrame:
    print("Loading AfriSenti Twi dataset (official splits)...")
    ds = load_dataset("masakhane/afrisenti", "twi")
    
    # Official benchmark split: Train + Validation for training, Test for evaluation
    train_val = concatenate_datasets([ds["train"], ds["validation"]])
    test_ds = ds["test"]
    
    text_col = "tweet" if "tweet" in train_val.column_names else "text"
    X_train_text = train_val[text_col]
    y_train = train_val["label"]
    X_test_text = test_ds[text_col]
    y_test = test_ds["label"]

    print(f"Dataset: {len(X_train_text)} train+val tweets, {len(X_test_text)} held-out test tweets")
    print(f"Train label distribution: {pd.Series(y_train).value_counts().to_dict()}")
    print(f"Test label distribution:  {pd.Series(y_test).value_counts().to_dict()}")

    # Load baseline tokenizers
    baseline_tokenizers = load_tokenizers()
    twi_only_tokenizers = load_twi_only_tokenizers()

    # Load GhanaTok BPE & Unigram
    ghanatok = PreTrainedTokenizerFast(
        tokenizer_file=str(PROJECT_ROOT / "models" / "ghanatok" / "ghanatok_tokenizer.json"),
        unk_token="<unk>", pad_token="<pad>", bos_token="<s>", eos_token="</s>",
    )
    ghanatok_unigram = SentencePieceWrapper(
        str(PROJECT_ROOT / "models" / "ghanatok_unigram" / "ghanatok_unigram.model")
    )

    all_probe_tokenizers = {
        **baseline_tokenizers,
        "ABENA": twi_only_tokenizers["ABENA"],
        "GhanaTok": ghanatok,
        "GhanaTok-Unigram": ghanatok_unigram,
    }

    classes = sorted(list(set(y_test)))
    probe_results = []
    preds_dict = {}

    print("\nRunning bag-of-tokens Logistic Regression probe across all tokenizers...")
    for name, tok in all_probe_tokenizers.items():
        print(f"Evaluating {name}...")
        vectorizer = CountVectorizer(analyzer=tokenizer_to_analyzer(tok))
        X_train = vectorizer.fit_transform(X_train_text)
        X_test = vectorizer.transform(X_test_text)
        
        clf = LogisticRegression(max_iter=1000, random_state=random_state)
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)
        preds_dict[name] = preds
        
        acc = accuracy_score(y_test, preds)
        macro_f1 = f1_score(y_test, preds, average="macro")
        per_class_f1 = f1_score(y_test, preds, average=None, labels=classes)
        vocab_used = X_train.shape[1]

        probe_results.append({
            "tokenizer": name,
            "vocab_size_used": vocab_used,
            "accuracy": round(acc, 4),
            "macro_f1": round(macro_f1, 4),
            "f1_negative": round(per_class_f1[classes.index("negative")], 4),
            "f1_neutral": round(per_class_f1[classes.index("neutral")], 4),
            "f1_positive": round(per_class_f1[classes.index("positive")], 4),
        })

    probe_df = pd.DataFrame(probe_results)

    # 1000-iteration Bootstrap 95% Confidence Intervals for Macro F1
    print(f"\nComputing {n_bootstraps}-iteration bootstrap 95% confidence intervals on Macro F1...")
    np.random.seed(random_state)
    y_test_arr = np.array(y_test)
    n_test = len(y_test_arr)
    ci_list = []

    for name in probe_df["tokenizer"]:
        preds = preds_dict[name]
        boot_f1s = []
        for _ in range(n_bootstraps):
            idx = np.random.choice(n_test, size=n_test, replace=True)
            boot_f1s.append(f1_score(y_test_arr[idx], preds[idx], average="macro"))
        ci_lower = np.percentile(boot_f1s, 2.5)
        ci_upper = np.percentile(boot_f1s, 97.5)
        ci_list.append(f"[{ci_lower:.4f}, {ci_upper:.4f}]")

    probe_df["macro_f1_95ci"] = ci_list
    
    # Save output
    output_path = PROJECT_ROOT / "reports" / "tables" / "sentiment_probe.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    probe_df.to_csv(output_path, index=False)
    print(f"\nSaved probe results to {output_path}")
    print(probe_df.to_string(index=False))

    return probe_df


if __name__ == "__main__":
    run_sentiment_probe()
