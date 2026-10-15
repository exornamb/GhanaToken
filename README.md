# GhanaToken: Tokenizer Optimization for Ghanaian Languages (Twi & Ewe)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Tests: 7 Passed](https://img.shields.io/badge/Tests-7%20Passed-brightgreen.svg)](tests/test_project_structure.py)
[![Release: v1.0.0](https://img.shields.io/badge/Release-v1.0.0-orange.svg)](#10-final-commit--submission-release-tag)

A rigorous comparative evaluation of subword tokenization efficiency across modern multilingual foundation tokenizers (**mBERT**, **XLM-R**, **AfroXLMR**), regional models (**ABENA**), and **GhanaTok**—a custom bilingual byte-level BPE and SentencePiece Unigram tokenizer specifically engineered for **Twi (Akan)** and **Ewe (Gbe)**.

- **Course:** DCIT 316: Individual Research Project  
- **Author:** Jennifer Banibensu (Student ID: 22013023)  
- **Institution:** Department of Computer Science, University of Ghana  
- **Submission Release Tag:** `v1.0.0` | **Branch:** `main`  
- **Supplementary Code Archive:** [`GhanaToken_code_snapshot.zip`](GhanaToken_code_snapshot.zip)  

---

## Quick Navigation: Project Research Artifacts

| Research Deliverable | Document Path | Description |
| :--- | :--- | :--- |
| **Model Card** | [MODEL_CARD.md](MODEL_CARD.md) | Architectural specifications, pre-tokenization regex, seed morphemes, quantitative metrics, and ethical limits. |
| **Data Card** | [DATA_CARD.md](DATA_CARD.md) | Datasheet covering corpus composition, dialect distributions, licensing, preprocessing, and safe access. |
| **Literature Matrix** | [LITERATURE_MATRIX.md](LITERATURE_MATRIX.md) | Detailed 17-paper comparative matrix mapping foundational literature to RQ1, RQ2, and RQ3. |
| **Ethics Statement** | [ETHICS_STATEMENT.md](ETHICS_STATEMENT.md) | Beneficiaries, licensing, privacy, dialect representation, risk mitigation, and green computational footprint. |
| **AI-Use Disclosure** | [AI_USE_DISCLOSURE.md](AI_USE_DISCLOSURE.md) | Transparent disclosure of AI assistance, 3-tier verification protocol, corrected AI errors, and author defense. |
| **Failure Log** | [FAILURE_LOG.md](FAILURE_LOG.md) | Post-mortem documenting negative results, rejected hypotheses, architectural bugs, and design defenses. |
| **Reproducibility Checklist** | [REPRODUCIBILITY_CHECKLIST.md](REPRODUCIBILITY_CHECKLIST.md) | ML reproducibility checklist (Pineau et al. standard) with environment parameters and artifact checksums. |
| **Final Research Report** | [reports/final_report.md](reports/final_report.md) | Comprehensive 8-chapter academic thesis document with in-depth linguistic and statistical analyses. |
| **Semester Project PDF** | [docs/DCIT316_SemesterProject_22013023_JenniferBanibensu.pdf](docs/DCIT316_SemesterProject_22013023_JenniferBanibensu.pdf) | Formal project report submitted for course examination. |

---

## 1. Executive Summary & Key Results

On sealed held-out test sets (**608 Twi sentences**, **347 Ewe sentences**), **GhanaTok** eliminates the severe subword fragmentation and exorbitant "token tax" imposed by standard multilingual models:

### 1.1 Primary Held-Out Test Set Evaluation Table

| Language | Tokenizer | Mean Fertility (Tokens/Word) | Density (Tokens/Char) | Fragmentation Rate (% Words Split) | Reduction vs mBERT (Best General) | 95% Bootstrap CI | Wilcoxon $p$-value (Holm-corrected) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ewe** | AfroXLMR / XLM-R | 2.608 | 0.505 | 70.99% | — | — | — |
| **Ewe** | mBERT | 2.291 | 0.445 | 63.87% | Baseline (0.0%) | — | — |
| **Ewe** | **GhanaTok (BPE)** | **1.750** | **0.341** | **51.25%** | **-23.60%** | **[22.08%, 24.95%]** | **$p = 2.48 \times 10^{-52}$** |
| **Ewe** | *GhanaTok-Unigram (Bonus)* | *1.349* | *0.263* | *22.83%* | *-41.11%* | *[39.67%, 42.39%]* | *$p = 9.84 \times 10^{-57}$* |
| **Twi** | AfroXLMR / XLM-R | 2.444 | 0.482 | 70.26% | — | — | — |
| **Twi** | ABENA (Twi only) | 2.419 | 0.477 | 72.12% | — | — | — |
| **Twi** | mBERT | 2.389 | 0.471 | 70.47% | Baseline (0.0%) | — | — |
| **Twi** | **GhanaTok (BPE)** | **1.656** | **0.327** | **48.82%** | **-30.67%** (*-31.54% vs ABENA*) | **[29.85%, 31.44%]** | **$p = 7.45 \times 10^{-99}$** |
| **Twi** | *GhanaTok-Unigram (Bonus)* | *1.251* | *0.248* | *17.58%* | *-47.63%* | *[46.81%, 48.43%]* | *$p = 2.25 \times 10^{-100}$* |

### 1.2 Core Empirical Takeaways

1. **Statistically Defensible Compression (RQ2):** An 8,000-subword bilingual tokenizer reduces token fertility by **30.67% on Twi** ($p < 0.001$, Holm-Bonferroni corrected) and **23.60% on Ewe** ($p < 0.001$, Holm-Bonferroni corrected) relative to mBERT, and by over **32%** relative to XLM-R / AfroXLMR.
2. **Dialect-Aware Pre-Tokenization:** Protecting extended Latin letters (`ɛ`, `ɔ`, `ɖ`, `ŋ`, `ʋ`, `ƒ`) and injecting high-frequency morphemes (`Akwaaba`, `Medaase`, `Woezɔ`, `mbe-`, `-foɔ`, `-wo`) prevented single-character isolation and byte-fallback scattering.
3. **ABENA Baseline Asymmetry:** ABENA is an Akuapem-Twi monolingual model. On the Twi test set, it yielded 2.419 tokens/word; GhanaTok outperformed it by **31.54%** ($p < 0.001$). ABENA was strictly excluded from Ewe evaluations to avoid invalid cross-family distortion.
4. **Vocabulary Scaling & Diminishing Returns:** Sweeping 4k, 8k, 16k, and 32k budgets demonstrated that **8,000 subwords** captures >95% of theoretical compression, with absolute corpus saturation occurring at ~11,000 unique subwords.
5. **Economic & Latency Implications:**
   - **Cost Multipliers:** Multilingual models impose a **+44% to +49% API cost penalty** over GhanaTok-BPE, and up to **+95% (+1.95x)** over GhanaTok-Unigram.
   - **Context Window Expansion:** In a 4,000-token context window, GhanaTok-BPE fits **+778 additional Twi words (+47.5%)** and **+752 additional Ewe words (+49.0%)** relative to XLM-R.
   - **Throughput:** GhanaTok encodes at **3,345 sentences/sec** (BPE) and **26,363 sentences/sec** (SentencePiece Unigram).
6. **Downstream Probe Sanity Check (AfriSenti Twi):** On 3,481 training tweets and stratified test data, all tokenizers achieved statistically indistinguishable Macro F1 scores (overlapping 95% bootstrap CIs in `[0.48, 0.52]`), but GhanaTok utilized **47.6% fewer unique feature dimensions** (1,773 vs 3,386–3,907).

---

## 2. Project Directory Layout

```text
GhanaToken/
├── DATA_CARD.md                    # Comprehensive dataset provenance & split specifications
├── MODEL_CARD.md                   # Formal Model Card for GhanaTok BPE & Unigram models
├── LITERATURE_MATRIX.md            # 17-paper structured literature & RQ mapping matrix
├── ETHICS_STATEMENT.md             # Ethics, licensing, privacy, dialect equity, and green NLP
├── AI_USE_DISCLOSURE.md            # Full disclosure of AI assistance and 3-tier verification
├── FAILURE_LOG.md                  # Experimental post-mortem, negative results, and bug fixes
├── REPRODUCIBILITY_CHECKLIST.md    # Pineau et al. ML reproducibility checklist & checksums
├── README.md                       # This reproduction guide & executive summary
├── requirements.txt                # Pinned Python package dependencies
├── GhanaToken_code_snapshot.zip    # Standalone code & artifact release bundle
│
├── data/
│   ├── raw/                        # Raw GhanaNLP parallel sentences
│   │   ├── twi/raw_sentences.csv   # 6,090 raw Twi sentence pairs
│   │   └── ewe/raw_sentences.csv   # 3,488 raw Ewe sentence pairs
│   └── processed/                  # Cleaned, NFC-normalized, deterministic splits
│       ├── twi/                    # train.txt (4,857), val.txt (607), test.txt (608)
│       ├── ewe/                    # train.txt (2,764), val.txt (345), test.txt (347)
│       └── ghanatok_train_corpus.txt # Joint training corpus (7,621 sentences, 721 KB)
│
├── models/
│   ├── ghanatok/                   # Primary GhanaTok Byte-Level BPE (8,000 vocab)
│   │   └── ghanatok_tokenizer.json
│   ├── ghanatok_unigram/           # Primary GhanaTok SentencePiece Unigram (8,000 vocab)
│   │   ├── ghanatok_unigram.model
│   │   └── ghanatok_unigram.vocab
│   └── ghanatok_{bpe,unigram}_{4000,8000,16000,32000}/ # Vocab sweep checkpoints
│
├── notebooks/                      # All 9 notebooks with complete visible outputs & plots
│   ├── 01_data_audit.ipynb         # Raw corpus audit & character distribution checks
│   ├── 02_preprocessing_cleaning.ipynb # NFC normalisation, deduplication, splitting
│   ├── 03_tokenizer_benchmark.ipynb    # Baseline calibration on 3,000 train/val sentences
│   ├── 04_ghanatok_training.ipynb      # Training BPE & SentencePiece Unigram recipes
│   ├── 05_evaluation_error_analysis.ipynb # Held-out test evaluation & error breakdowns
│   ├── 06_sentiment_probe.ipynb        # Downstream AfriSenti classification probe
│   ├── 07_vocab_size_sweep.ipynb       # 4k to 32k vocabulary scaling sweep
│   ├── 08_statistical_significance.ipynb # Paired Wilcoxon, bootstrap CIs, Holm-Bonferroni
│   └── 09_latency_and_cost.ipynb       # Latency throughput, API cost multipliers, budgets
│
├── reports/
│   ├── figures/                    # Publication-grade visualization charts (.png)
│   │   ├── baseline_fertility_by_tokenizer.png
│   │   ├── baseline_fragmentation_by_tokenizer.png
│   │   ├── final_heldout_fertility_comparison.png
│   │   ├── vocab_size_sweep_fertility.png
│   │   └── cost_and_context_budget.png
│   ├── tables/                     # 18 generated empirical CSV tables
│   │   ├── baseline_summary.csv
│   │   ├── final_heldout_results.csv
│   │   ├── final_summary.csv
│   │   ├── rq2_significance_results.csv
│   │   ├── rq3_significance_results.csv
│   │   ├── latency_benchmark.csv
│   │   ├── cost_multiplier.csv
│   │   ├── context_budget.csv
│   │   ├── vocab_size_sweep_summary.csv
│   │   └── sentiment_probe.csv
│   ├── data_card.md                # Data Card mirror in reports/
│   └── final_report.md             # Comprehensive final research report
│
├── src/                            # Modular Python library
│   ├── __init__.py
│   ├── preprocessing.py            # NFC normalization, deduplication, split generator
│   ├── tokenizer_benchmark.py      # Word-isolated fertility and fragmentation metrics
│   ├── train_ghanatok.py           # BPE and SentencePiece Unigram training recipes
│   ├── evaluation.py               # Summary aggregation, error analysis, dialect checks
│   ├── significance.py             # Paired Wilcoxon, bootstrap CIs, Holm-Bonferroni
│   └── latency_benchmark.py        # Latency and throughput benchmark runner
│
├── tests/
│   └── test_project_structure.py   # Automated pytest suite (7/7 passing)
└── docs/
    └── DCIT316_SemesterProject_22013023_JenniferBanibensu.pdf
```

---

## 3. Step-by-Step Reproduction Guide

Follow these steps to reproduce all experiments from a fresh command shell:

### Step 1: Environment Setup
Ensure Python 3.10 or higher is installed.

```bash
# Clone the repository
git clone https://github.com/exornamb/GhanaToken.git
cd GhanaToken

# Create and activate a clean virtual environment
python -m venv .venv

# On Windows PowerShell:
.venv\Scripts\Activate.ps1

# On Linux / macOS:
source .venv/bin/activate
```

### Step 2: Install Required Dependencies
All dependencies are strictly specified in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 3: Run Automated Test Suite
Verify that all file paths, processed data splits, model loaders, metrics, and security assertions pass:

```bash
pytest -v tests/test_project_structure.py
```
*(Expected output: 7 passed in ~12 seconds).*

### Step 4: Reproduce Data Preprocessing (Optional)
The processed splits are pre-committed in `data/processed/`. To re-clean from raw files:

```bash
python -c "
from src.preprocessing import clean_dataframe, split_and_save
import pandas as pd

# Twi preprocessing
df_twi = pd.read_csv('data/raw/twi/raw_sentences.csv')
clean_twi = clean_dataframe(df_twi, text_column='label')
split_and_save(clean_twi, text_column='label', language='twi')

# Ewe preprocessing
df_ewe = pd.read_csv('data/raw/ewe/raw_sentences.csv')
clean_ewe = clean_dataframe(df_ewe, text_column='label')
split_and_save(clean_ewe, text_column='label', language='ewe')
"
```

### Step 5: Train GhanaTok Models
To re-train the primary 8,000-subword BPE and Unigram tokenizers:

```bash
python -c "
from src.train_ghanatok import build_training_corpus, train_ghanatok, train_ghanatok_unigram
build_training_corpus()
train_ghanatok()
train_ghanatok_unigram()
"
```

### Step 6: Execute Interactive Notebooks
All 9 notebooks in `notebooks/` are pre-executed with visible outputs, tables, and embedded figures. You can explore or re-run them via Jupyter:

```bash
jupyter notebook notebooks/
```

- **`01_data_audit.ipynb`**: Raw corpus audit, character counts, and orthographic inspection.
- **`02_preprocessing_cleaning.ipynb`**: Unicode NFC normalization, deduplication, and split creation.
- **`03_tokenizer_benchmark.ipynb`**: Baseline calibration of mBERT, XLM-R, AfroXLMR, and ABENA.
- **`04_ghanatok_training.ipynb`**: Training GhanaTok BPE and SentencePiece Unigram with seed morphemes.
- **`05_evaluation_error_analysis.ipynb`**: Held-out test evaluation, qualitative examples, and dialect checks.
- **`06_sentiment_probe.ipynb`**: Downstream AfriSenti classification probe.
- **`07_vocab_size_sweep.ipynb`**: 4k, 8k, 16k, and 32k vocabulary scaling sweep.
- **`08_statistical_significance.ipynb`**: Wilcoxon signed-rank tests, bootstrap CIs, and Holm-Bonferroni correction.
- **`09_latency_and_cost.ipynb`**: Latency benchmarks, API cost multipliers, and context window budgets.

---

## 4. Safe Data Access, Governance & Restrictions

### 4.1 Data Licensing & Permitted Uses
- **GhanaNLP Parallel Corpora:** Released under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (**CC BY-NC-SA 4.0**). Permitted strictly for academic, non-commercial research, educational examination, and public evaluation.
- **AfriSenti Twitter Corpus:** Released under Creative Commons Attribution 4.0 International (**CC BY 4.0**). Used solely for academic downstream probe verification.

### 4.2 Zero-Credential & Safe Access Policy
- **No Private Data or Credentials Committed:** In accordance with institutional guidelines and security best practices, **no passwords, API keys, private tokens, or proprietary credentials are required or committed anywhere in this repository**.
- **Automated Security Verification:** The test suite (`tests/test_project_structure.py::test_no_private_keys_or_secrets`) automatically scans the entire repository for inadvertent API keys or secret patterns, guaranteeing privacy.
- **Independent Instructor/Reviewer Access:** All processed splits (`train.txt`, `val.txt`, `test.txt`) and model weights are directly included in the repository and supplementary ZIP archive, enabling instant offline reproduction without external service registration.

---

## 5. Defense of Research Decisions & Limitations

1. **Why Word-Isolated Fertility?** Measuring full-sentence fertility introduces merge bias across word boundaries. Evaluating whitespace-separated words in isolation ensures the metric isolates vocabulary adequacy from whitespace-joining heuristics (Petrov et al., 2023).
2. **Why 8,000 Vocabulary?** Sweeps across 4k, 8k, 16k, and 32k tokens proved that 8k captures >95% of theoretical compression. Vocabularies beyond 16k completely saturate on ~11k unique corpus words with 0% incremental compression gain (see [FAILURE_LOG.md](FAILURE_LOG.md)).
3. **Why Non-Parametric Significance Testing?** Token fertility distributions are heavily skewed and non-normal. The evaluation uses paired Wilcoxon signed-rank tests and 1,000-iteration non-parametric bootstrap resampling, adjusted by Holm-Bonferroni step-down correction.
4. **Honest Reporting on Downstream Accuracy:** This work explicitly disclaims that lower fertility automatically increases linear downstream accuracy. On AfriSenti, accuracy was equivalent across all tokenizers, but GhanaTok cut feature dimensions by **47.6%**, proving representational compactness.
5. **Limitations:**
   - Evaluated on translated, civic, and biblical corpora; domain shift on modern slang or social media text requires further study.
   - Computational boundaries have not undergone human evaluation by native Ghanaian linguists.

---

## 6. AI-Use Disclosure & Verification Summary

- **Tools Used:** Anthropic Claude (Claude 3.5 Sonnet / Opus) and Google Antigravity IDE assistant.
- **Scope of AI Assistance:** Pair-programming boilerplate, suggesting vectorized NumPy idioms, formatting LaTeX/Markdown tables, proofreading report text, and reference checking.
- **What AI Did Not Do:** AI did not run experiments, formulate hypotheses, invent data, or make architectural decisions. All results originate from local code execution.
- **Errors Caught in AI Drafts:** Corrected proposed alterations to project title, corrected author name, removed invalid cross-lingual ABENA evaluations on Ewe, and corrected misconceptions regarding AfroXLMR's tokenizer vocabulary.
- **Full Statement:** See [AI_USE_DISCLOSURE.md](AI_USE_DISCLOSURE.md).

---

## 7. Submission Release Guidance

- **Release Tag:** `v1.0.0`
- **Git Branch:** `main`
- **Supplementary Code Archive:** `GhanaToken_code_snapshot.zip`
- **Academic Contact:** Jennifer Banibensu (Department of Computer Science, University of Ghana)
