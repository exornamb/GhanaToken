"""
Quick sanity check: are mBERT and ABENA producing identical predictions?
"""
from datasets import load_dataset, concatenate_datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from transformers import AutoTokenizer
import numpy as np
import sys
sys.path.append(".")

ds = load_dataset("masakhane/afrisenti", "twi")
train_val = concatenate_datasets([ds["train"], ds["validation"]])
test_ds = ds["test"]
text_col = "tweet"
X_train_text = train_val[text_col]
y_train = train_val["label"]
X_test_text = test_ds[text_col]
y_test = list(test_ds["label"])

mbert = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
abena = AutoTokenizer.from_pretrained("Ghana-NLP/abena-base-akuapem-twi-cased")

def make_analyzer(tok):
    return lambda text: tok.tokenize(text)

preds = {}
for name, tok in [("mBERT", mbert), ("ABENA", abena)]:
    vec = CountVectorizer(analyzer=make_analyzer(tok))
    X_tr = vec.fit_transform(X_train_text)
    X_te = vec.transform(X_test_text)
    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(X_tr, y_train)
    preds[name] = list(clf.predict(X_te))
    acc = accuracy_score(y_test, preds[name])
    mf1 = f1_score(y_test, preds[name], average="macro")
    vocab = X_tr.shape[1]
    print(f"{name}: vocab={vocab}, acc={acc:.4f}, macro_f1={mf1:.4f}")

# Agreement check
agree_count = sum(a == b for a, b in zip(preds["mBERT"], preds["ABENA"]))
total = len(y_test)
print(f"\nPrediction agreement: {agree_count}/{total} ({agree_count/total:.4f})")
disagree = [(i, preds["mBERT"][i], preds["ABENA"][i], y_test[i]) for i in range(total) if preds["mBERT"][i] != preds["ABENA"][i]]
print(f"Disagreements: {len(disagree)}")
if disagree:
    print("First 5 disagreements (index, mBERT_pred, ABENA_pred, true_label):")
    for i, mb, ab, true in disagree[:5]:
        print(f"  [{i}] mBERT={mb}, ABENA={ab}, true={true}, tweet={X_test_text[i][:60]}")
