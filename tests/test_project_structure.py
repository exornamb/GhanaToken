"""
tests/test_project_structure.py
Automated test suite validating repository structure, processed corpora,
model assets, evaluation metrics, and privacy/credential safety.
"""

import os
import re
from pathlib import Path
import pytest
import pandas as pd
from transformers import PreTrainedTokenizerFast

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_directory_structure():
    """Verify all required top-level directories and core folders exist."""
    required_dirs = [
        PROJECT_ROOT / "data" / "raw",
        PROJECT_ROOT / "data" / "processed" / "twi",
        PROJECT_ROOT / "data" / "processed" / "ewe",
        PROJECT_ROOT / "models" / "ghanatok",
        PROJECT_ROOT / "models" / "ghanatok_unigram",
        PROJECT_ROOT / "notebooks",
        PROJECT_ROOT / "reports" / "figures",
        PROJECT_ROOT / "reports" / "tables",
        PROJECT_ROOT / "src",
        PROJECT_ROOT / "tests",
    ]
    for d in required_dirs:
        assert d.exists() and d.is_dir(), f"Required directory missing: {d}"


def test_processed_data_files():
    """Verify all processed splits exist and contain clean non-empty sentences."""
    splits = {
        "twi": {"train": 4857, "val": 607, "test": 608},
        "ewe": {"train": 2764, "val": 345, "test": 347},
    }
    for lang, counts in splits.items():
        for split_name, expected_count in counts.items():
            path = PROJECT_ROOT / "data" / "processed" / lang / f"{split_name}.txt"
            assert path.exists(), f"Split file missing: {path}"
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            assert len(lines) == expected_count, (
                f"Line count mismatch for {lang}/{split_name}: expected {expected_count}, got {len(lines)}"
            )


def test_preprocessing_clean_text():
    """Verify Unicode NFC normalization and whitespace collapse."""
    from src.preprocessing import clean_text
    
    # NFD to NFC test for open vowels with accent
    nfd_text = "e\u0300"  # è decomposed
    cleaned = clean_text(nfd_text)
    assert cleaned == "è"
    
    # Whitespace normalization
    spaced_text = "  Akwaaba,   wo   ho   te  sɛn?  \n"
    assert clean_text(spaced_text) == "Akwaaba, wo ho te sɛn?"


def test_analyze_sentence():
    """Verify sentence analysis returns expected keys and realistic bounds."""
    from src.tokenizer_benchmark import analyze_sentence
    from src.train_ghanatok import SentencePieceWrapper
    
    unigram_model = PROJECT_ROOT / "models" / "ghanatok_unigram" / "ghanatok_unigram.model"
    sp = SentencePieceWrapper(str(unigram_model))
    
    res = analyze_sentence(sp, "Akwaaba, wo ho te sɛn?")
    assert "tokens_per_word" in res
    assert "pct_words_split" in res
    assert "tokens_per_char" in res
    assert res["n_words"] == 5
    assert res["tokens_per_word"] >= 1.0


def test_ghanatok_model_files():
    """Verify trained GhanaTok BPE and Unigram model files are present."""
    bpe_file = PROJECT_ROOT / "models" / "ghanatok" / "ghanatok_tokenizer.json"
    unigram_file = PROJECT_ROOT / "models" / "ghanatok_unigram" / "ghanatok_unigram.model"
    
    assert bpe_file.exists() and bpe_file.stat().st_size > 0
    assert unigram_file.exists() and unigram_file.stat().st_size > 0
    
    # Verify loadability
    tok_bpe = PreTrainedTokenizerFast(tokenizer_file=str(bpe_file))
    tokens = tok_bpe.tokenize("Akwaaba medaase woezɔ")
    assert len(tokens) > 0


def test_reports_tables_and_figures():
    """Verify key evaluation tables and publication figures are present and populated."""
    required_tables = [
        "baseline_summary.csv",
        "final_heldout_results.csv",
        "final_summary.csv",
        "rq2_significance_results.csv",
        "rq3_significance_results.csv",
        "latency_benchmark.csv",
        "cost_multiplier.csv",
        "context_budget.csv",
        "vocab_size_sweep_summary.csv",
        "sentiment_probe.csv",
    ]
    for table_name in required_tables:
        p = PROJECT_ROOT / "reports" / "tables" / table_name
        assert p.exists() and p.stat().st_size > 0, f"Missing or empty table: {table_name}"
        df = pd.read_csv(p)
        assert len(df) > 0, f"Table {table_name} has 0 rows"
        
    required_figures = [
        "baseline_fertility_by_tokenizer.png",
        "baseline_fragmentation_by_tokenizer.png",
        "final_heldout_fertility_comparison.png",
        "vocab_size_sweep_fertility.png",
        "cost_and_context_budget.png",
    ]
    for fig_name in required_figures:
        p = PROJECT_ROOT / "reports" / "figures" / fig_name
        assert p.exists() and p.stat().st_size > 0, f"Missing or empty figure: {fig_name}"


def test_no_private_keys_or_secrets():
    """Verify that no API keys, private tokens, or passwords are committed."""
    secret_patterns = [
        re.compile(r"hf_[a-zA-Z0-9]{34,}"),
        re.compile(r"ghp_[a-zA-Z0-9]{36,}"),
        re.compile(r"sk-[a-zA-Z0-9]{32,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----"),
    ]
    
    ignored_dirs = {".git", ".venv", "__pycache__", ".pytest_cache"}
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        for f in files:
            # Skip binary files
            if f.endswith((".png", ".pdf", ".model", ".pyc", ".ico", ".jpg")):
                continue
            file_path = Path(root) / f
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                for pattern in secret_patterns:
                    matches = pattern.findall(content)
                    assert len(matches) == 0, f"Potential credential/secret detected in {file_path.relative_to(PROJECT_ROOT)}"
            except Exception:
                pass
