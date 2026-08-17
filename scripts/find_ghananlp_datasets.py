"""
scripts/find_ghananlp_datasets.py
Finds the exact dataset names published by the Ghana-NLP organisation
on Hugging Face, so we never hardcode a guessed name.
"""
from huggingface_hub import HfApi

api = HfApi()
datasets = api.list_datasets(author="Ghana-NLP")

print("Datasets published by Ghana-NLP on Hugging Face:")
for d in datasets:
    print("-", d.id)
