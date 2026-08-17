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


def analyze_sentence(tokenizer, sentence: str) -> dict:
    """
    Measures tokenization efficiency for one sentence, word by word.
    This word-by-word approach matches how token fertility is measured
    in the tokenizer fairness literature (for example Petrov et al. 2023
    and Ahia et al. 2023): each whitespace-separated word is encoded on
    its own, so the fertility score reflects how the vocabulary handles
    that specific word, not accidental merges across word boundaries.
    """
    words = sentence.strip().split()
    n_words = len(words)
    n_chars = len(sentence)
    total_subword_tokens = 0
    words_split_into_multiple = 0
    for word in words:
        token_ids = tokenizer.encode(word, add_special_tokens=False)
        n_subtokens = len(token_ids)
        total_subword_tokens += n_subtokens
        if n_subtokens > 1:
            words_split_into_multiple += 1
    return {
        "n_words": n_words,
        "n_chars": n_chars,
        "n_tokens": total_subword_tokens,
        "tokens_per_word": total_subword_tokens / n_words if n_words else 0.0,
        "tokens_per_char": total_subword_tokens / n_chars if n_chars else 0.0,
        "pct_words_split": (words_split_into_multiple / n_words * 100) if n_words else 0.0,
    }
