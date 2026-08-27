# GhanaToken: Tokenizer Optimization for Ghanaian Languages (Twi & Ewe)

A comparative evaluation of subword tokenization efficiency across modern multilingual tokenizers (mBERT, XLM-R, AfroXLMR), regional models (ABENA), and **GhanaTok**—a dedicated, bilingual byte-level BPE and SentencePiece Unigram tokenizer designed for **Twi (Akan)** and **Ewe (Gbe)**.

**Course**: DCIT 316, Individual Research Project  
**Author**: Jennifer Banibensu  
**Final Report**: [reports/final_report.md](reports/final_report.md)  
**Data Card**: [reports/data_card.md](reports/data_card.md)  

---

## 1. Key Results Summary

On sealed held-out test sets (608 Twi sentences, 347 Ewe sentences), **GhanaTok** eliminates the severe fragmentation observed in standard multilingual models:

| Language | Tokenizer | Mean Fertility (Tokens/Word) | Density (Tokens/Char) | Fragmentation Rate (% Words Split) | Reduction vs Best General Baseline |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Ewe** | AfroXLMR / XLM-R | 2.608 | 0.505 | 70.99% | — |
| **Ewe** | mBERT | 2.291 | 0.445 | 63.87% | Baseline (0.0%) |
| **Ewe** | **GhanaTok (BPE)** | **1.750** | **0.341** | **51.25%** | **-23.6%** |
| **Ewe** | *GhanaTok-Unigram (Bonus)* | *1.349* | *0.263* | *22.83%* | *-41.1%* |
| **Twi** | AfroXLMR / XLM-R | 2.444 | 0.482 | 70.26% | — |
| **Twi** | ABENA (Twi only) | 2.419 | 0.477 | 72.12% | — |
| **Twi** | mBERT | 2.389 | 0.471 | 70.47% | Baseline (0.0%) |
| **Twi** | **GhanaTok (BPE)** | **1.656** | **0.327** | **48.82%** | **-30.7%** (*-31.5% vs ABENA*) |
| **Twi** | *GhanaTok-Unigram (Bonus)* | *1.251* | *0.248* | *17.58%* | *-47.6%* |

### Key Findings:
1. **Elimination of the African Language Tokenization Tax**: An 8,000-vocabulary bilingual tokenizer reduces token fertility by **30.7% on Twi** and **23.6% on Ewe** relative to mBERT (and >32% vs XLM-R/AfroXLMR).
2. **Robust Dialect-Aware Pre-Tokenization**: Protecting extended Latin characters (`ɛ`, `ɔ`, `ɖ`, `ŋ`, `ʋ`, `ƒ`) and injecting seed morphemes (`Akwaaba`, `Medaase`, `Woezɔ`, `mbe-`, `-foɔ`, `-wo`) prevented single-character and byte scattering.
3. **ABENA Asymmetry Note**: ABENA was evaluated strictly on Twi (monolingual design for Akuapem Twi) and achieved 2.419 tokens/word on the held-out test set; GhanaTok outperformed it by 31.5%.
4. **Secondary / Bonus Extensions**:
   - **GhanaTok-Unigram**: Explored SentencePiece Unigram probabilistic pruning, achieving 1.251 tokens/word on Twi and winning 597 of 939 sentence head-to-head comparisons against BPE.
   - **Downstream Sentiment Probe**: Evaluated on the AfriSenti Twi dataset (3,869 train+val, 949 test); all tokenizers achieved statistically indistinguishable Macro F1 scores (95% bootstrap CIs overlapping between 0.50 and 0.60), but GhanaTok used **over 50% fewer unique feature dimensions** (1,899 vs 3,896–4,483).

---

## 2. Project Layout

```text
GhanaToken/
├── data/
│   ├── raw/                       # Raw GhanaNLP parallel corpora
│   │   ├── twi/raw_sentences.csv
│   │   └── ewe/raw_sentences.csv
│   └── processed/                 # Cleaned train/val/test splits & joint training corpus
│       ├── twi/                   # train.txt (4,857), val.txt (607), test.txt (608)
│       ├── ewe/                   # train.txt (2,764), val.txt (345), test.txt (347)
│       └── ghanatok_train_corpus.txt
├── models/
│   ├── ghanatok/                  # GhanaTok Byte-Level BPE (8k vocab)
│   │   └── ghanatok_tokenizer.json
│   └── ghanatok_unigram/          # GhanaTok SentencePiece Unigram (8k vocab)
│       ├── ghanatok_unigram.model
│       └── ghanatok_unigram.vocab
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_preprocessing_cleaning.ipynb
│   ├── 03_tokenizer_benchmark.ipynb
│   ├── 04_ghanatok_training.ipynb
│   ├── 05_evaluation_error_analysis.ipynb
│   └── 06_sentiment_probe.ipynb
├── reports/
│   ├── figures/                   # Visualization charts (.png)
│   ├── tables/                    # Master evaluation and probe CSVs (.csv)
│   ├── data_card.md               # Dataset provenance & limitations documentation
│   └── final_report.md            # Comprehensive final research report
├── scripts/
│   ├── check_project_structure.py # Submission structure verification script
│   ├── run_sentiment_probe.py     # Downstream sentiment probe runner
│   └── find_ghananlp_datasets.py
├── src/
│   ├── preprocessing.py           # Text cleaning, NFC normalisation, deduplication
│   ├── tokenizer_benchmark.py     # Per-word fertility and fragmentation analysis
│   └── train_ghanatok.py          # BPE & Unigram training recipes with seed morphemes
├── requirements.txt
└── README.md
```

---

## 3. How to Reproduce

### 1. Set Up Python Environment
```bash
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate

# On Windows PowerShell:
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Project Integrity
```bash
python scripts/check_project_structure.py
```

### 4. Run Notebooks or Scripts
Execute the notebooks in sequence:
- `notebooks/01_data_audit.ipynb` — Initial corpus inspection.
- `notebooks/02_preprocessing_cleaning.ipynb` — NFC normalisation, regex cleaning, train/val/test splitting.
- `notebooks/03_tokenizer_benchmark.ipynb` — Baseline calibration on mBERT, XLM-R, AfroXLMR, ABENA.
- `notebooks/04_ghanatok_training.ipynb` — Training GhanaTok (BPE and Unigram).
- `notebooks/05_evaluation_error_analysis.ipynb` — Sealed held-out evaluation, statistical tests, qualitative case studies.
- `notebooks/06_sentiment_probe.ipynb` — Downstream AfriSenti Twi classification probe.

Or run the standalone probe script:
```bash
python scripts/run_sentiment_probe.py
```
