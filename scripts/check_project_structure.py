"""
scripts/check_project_structure.py
Confirms every expected file and folder from the project plan exists,
so nothing is missing at submission time.
"""
from pathlib import Path

REQUIRED_PATHS = [
    "data/raw/twi/raw_sentences.csv",
    "data/raw/ewe/raw_sentences.csv",
    "data/processed/twi/train.txt",
    "data/processed/twi/val.txt",
    "data/processed/twi/test.txt",
    "data/processed/ewe/train.txt",
    "data/processed/ewe/val.txt",
    "data/processed/ewe/test.txt",
    "models/ghanatok/ghanatok_tokenizer.json",
    "reports/tables/baseline_summary.csv",
    "reports/tables/final_summary.csv",
    "reports/tables/master_comparison.csv",
    "reports/figures/baseline_fertility_by_tokenizer.png",
    "reports/figures/final_heldout_fertility_comparison.png",
    "reports/data_card.md",
    "reports/final_report.md",
    "README.md",
    "requirements.txt",
]

missing = [p for p in REQUIRED_PATHS if not Path(p).exists()]
if missing:
    print("MISSING FILES:")
    for m in missing:
        print("-", m)
else:
    print("All required files present.")
