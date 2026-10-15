"""
src/evaluation.py
Comprehensive evaluation, metric aggregation, error analysis, and dialect breakdown
utilities for GhanaTok and baseline tokenizers across Twi and Ewe.
"""

from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import unicodedata
import pandas as pd
import numpy as np
from tqdm import tqdm

from src.tokenizer_benchmark import analyze_sentence, run_benchmark

# Known orthographic markers and extended Latin characters in Ghanaian languages
EXTENDED_LATIN_CHARS = {
    "twi": ["ɛ", "ɔ", "Ɛ", "Ɔ"],
    "ewe": ["ɖ", "ŋ", "ɔ", "ɛ", "ʋ", "ƒ", "Ɖ", "Ŋ", "Ɔ", "Ɛ", "Ʋ", "Ƒ"],
}

# Akuapem Twi dialect markers (frequent morphemes/spellings distinct from Asante)
AKUAPEM_MARKERS = [
    "sɛnea", "sɛdeɛ", "enti", "ampa", "nhoma", "nhomasua", "petee", "guare", "kɔkɔɔ"
]


def evaluate_heldout(
    tokenizers: Dict[str, Any],
    twi_sentences: List[str],
    ewe_sentences: List[str],
    twi_only_tokenizers: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """
    Evaluates all tokenizers on sealed held-out test sets for Twi and Ewe.
    Language-specific tokenizers (e.g., ABENA) are strictly applied only to their target language.
    """
    dfs = []
    
    # 1. Twi evaluation across general baselines and custom models
    print(f"Evaluating {len(tokenizers)} tokenizers on {len(twi_sentences)} held-out Twi sentences...")
    twi_df = run_benchmark(tokenizers, twi_sentences, language="twi", sample_size=len(twi_sentences))
    dfs.append(twi_df)
    
    # 2. Regional Twi-only baseline (ABENA)
    if twi_only_tokenizers:
        print(f"Evaluating {len(twi_only_tokenizers)} regional baseline(s) on Twi...")
        twi_reg_df = run_benchmark(twi_only_tokenizers, twi_sentences, language="twi", sample_size=len(twi_sentences))
        dfs.append(twi_reg_df)
        
    # 3. Ewe evaluation across general baselines and custom models
    print(f"Evaluating {len(tokenizers)} tokenizers on {len(ewe_sentences)} held-out Ewe sentences...")
    ewe_df = run_benchmark(tokenizers, ewe_sentences, language="ewe", sample_size=len(ewe_sentences))
    dfs.append(ewe_df)
    
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df


def compute_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates per-sentence evaluation metrics into a publication-ready summary table.
    """
    summary = df.groupby(["language", "tokenizer"]).agg(
        mean_fertility=("tokens_per_word", "mean"),
        std_fertility=("tokens_per_word", "std"),
        mean_tokens_per_char=("tokens_per_char", "mean"),
        mean_pct_words_split=("pct_words_split", "mean"),
        n_sentences=("n_words", "count"),
        total_words=("n_words", "sum"),
        total_tokens=("n_tokens", "sum"),
    ).round(4).reset_index()
    return summary


def analyze_extended_latin_fragmentation(
    tokenizers: Dict[str, Any],
    sentences: List[str],
    language: str,
) -> pd.DataFrame:
    """
    Measures how subword tokenizers treat words containing extended Latin characters
    (e.g., ɛ, ɔ, ɖ, ŋ, ʋ, ƒ). Calculates the proportion of such words that suffer
    sub-token or byte-level fragmentation.
    """
    target_chars = set(EXTENDED_LATIN_CHARS.get(language, []))
    if not target_chars:
        return pd.DataFrame()
        
    # Collect all words containing target characters
    words_with_extended = []
    for s in sentences:
        for w in s.strip().split():
            if any(ch in target_chars for ch in w):
                words_with_extended.append(w)
                
    unique_words = sorted(list(set(words_with_extended)))
    rows = []
    
    for name, tok in tokenizers.items():
        split_count = 0
        total_tokens = 0
        byte_isolated_count = 0
        
        for w in unique_words:
            tokens = tok.tokenize(w) if hasattr(tok, "tokenize") else [str(t) for t in tok.encode(w)]
            total_tokens += len(tokens)
            if len(tokens) > 1:
                split_count += 1
            # Check for byte fallback (hex patterns like <0x..> or isolated multi-byte chunks)
            if any("<0x" in t or "" in t for t in tokens):
                byte_isolated_count += 1
                
        rows.append({
            "tokenizer": name,
            "language": language,
            "unique_words_tested": len(unique_words),
            "mean_fertility_on_extended": round(total_tokens / len(unique_words), 3) if unique_words else 0.0,
            "pct_words_fragmented": round(split_count / len(unique_words) * 100, 2) if unique_words else 0.0,
            "byte_fallback_words": byte_isolated_count,
        })
        
    return pd.DataFrame(rows)


def analyze_akuapem_dialect_signal(
    twi_results_df: pd.DataFrame,
    twi_sentences: List[str],
) -> pd.DataFrame:
    """
    Directional heuristic check assessing performance on sentences matching Akuapem spelling markers.
    Returns comparative fertility on flagged Akuapem subset vs. remaining Asante/general sentences.
    """
    # Map each sentence to whether it contains Akuapem keywords
    is_akuapem = []
    for s in twi_sentences:
        lower_words = set(s.lower().split())
        match = any(m in lower_words or m in s.lower() for m in AKUAPEM_MARKERS)
        is_akuapem.append(match)
        
    # Construct sentence mapping dataframe
    sentence_map = pd.DataFrame({
        "sentence_idx": list(range(len(twi_sentences))),
        "is_akuapem": is_akuapem,
    })
    
    df = twi_results_df[twi_results_df["language"] == "twi"].copy()
    if "sentence_idx" not in df.columns:
        df["sentence_idx"] = df.groupby(["language", "tokenizer"]).cumcount()
        
    merged = df.merge(sentence_map, on="sentence_idx", how="left")
    
    rows = []
    for tok_name, group in merged.groupby("tokenizer"):
        akuapem_fert = group[group["is_akuapem"] == True]["tokens_per_word"].mean()
        other_fert = group[group["is_akuapem"] == False]["tokens_per_word"].mean()
        rows.append({
            "tokenizer": tok_name,
            "akuapem_fertility": round(akuapem_fert, 3) if not np.isnan(akuapem_fert) else 0.0,
            "other_fertility": round(other_fert, 3) if not np.isnan(other_fert) else 0.0,
            "diff_akuapem_vs_other": round(akuapem_fert - other_fert, 3) if not np.isnan(akuapem_fert) else 0.0,
            "n_akuapem_matched": int(group["is_akuapem"].sum()),
            "n_total_twi": len(group),
        })
        
    return pd.DataFrame(rows)
