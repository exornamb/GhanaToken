"""
src/tokenizer_benchmark.py
Loads the baseline multilingual tokenizers and measures tokenization
efficiency on Twi and Ewe sentences.
"""
from transformers import AutoTokenizer

BASELINE_TOKENIZERS = {
    "mBERT": "bert-base-multilingual-cased",
    "XLM-R": "xlm-roberta-base",
    "AfroXLMR": "Davlan/afro-xlmr-large-29L",
}

# ABENA is Twi-only (trained on Akuapem Twi, never saw Ewe), so it is kept
# separate from the main baseline dictionary and only ever evaluated on
# the Twi test set, never on Ewe.
TWI_ONLY_TOKENIZERS = {
    "ABENA": "Ghana-NLP/abena-base-akuapem-twi-cased",
}


def load_tokenizers() -> dict:
    """Loads all three general baseline tokenizers into a dictionary."""
    tokenizers = {}
    for short_name, hf_name in BASELINE_TOKENIZERS.items():
        print(f"Loading {short_name} ({hf_name}) ...")
        tokenizers[short_name] = AutoTokenizer.from_pretrained(hf_name)
    return tokenizers


def load_twi_only_tokenizers() -> dict:
    """Loads bonus tokenizers that only support Twi, such as ABENA."""
    tokenizers = {}
    for short_name, hf_name in TWI_ONLY_TOKENIZERS.items():
        print(f"Loading {short_name} ({hf_name}) ...")
        tokenizers[short_name] = AutoTokenizer.from_pretrained(hf_name)
    return tokenizers
