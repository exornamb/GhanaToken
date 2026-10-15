# Reproducibility Checklist: GhanaToken

Following the machine learning reproducibility guidelines established by Pineau et al. (2021) and the NeurIPS Reproducibility Program.

---

## 1. Scope of Claims & Verification Status

| Item | Requirement | Status | Documented In |
| :--- | :--- | :---: | :--- |
| **1.1** | Clearly stated research questions (RQ1-3) and bounded empirical claims. | Yes | [README.md](README.md), [reports/final_report.md](reports/final_report.md) |
| **1.2** | Disclosure that token compression does not guarantee downstream accuracy gains. | Yes | [FAILURE_LOG.md](FAILURE_LOG.md), [reports/final_report.md](reports/final_report.md) |
| **1.3** | Distinguishes between primary findings (RQ1-3) and exploratory extensions (sentiment probe). | Yes | [README.md](README.md), [notebooks/06_sentiment_probe.ipynb](notebooks/06_sentiment_probe.ipynb) |

---

## 2. Models & Algorithmic Recipes

| Item | Requirement | Status | Verification Detail |
| :--- | :--- | :---: | :--- |
| **2.1** | Explicit description of tokenizer architectures, tokenization algorithms, and hyperparameters. | Yes | Detailed in [MODEL_CARD.md](MODEL_CARD.md) and `src/train_ghanatok.py`. |
| **2.2** | Pre-tokenizer regex pattern and normalization rules explicitly provided. | Yes | `GHANA_PRETOKENIZER_PATTERN` and NFC normalization defined in `src/train_ghanatok.py`. |
| **2.3** | Seed morphemes and special token lists explicitly enumerated in code. | Yes | `SEED_MORPHEMES` listed in `src/train_ghanatok.py` (lines 18–25). |
| **2.4** | Trained model artifacts preserved and directly loadable. | Yes | Byte-Level BPE (`models/ghanatok/`) and Unigram (`models/ghanatok_unigram/`). |

---

## 3. Data & Preprocessing Integrity

| Item | Requirement | Status | Verification Detail |
| :--- | :--- | :---: | :--- |
| **3.1** | Exact source of raw corpora identified and cited with license information. | Yes | GhanaNLP Parallel Corpora (CC BY-NC-SA 4.0) and AfriSenti (CC BY 4.0) in [DATA_CARD.md](DATA_CARD.md). |
| **3.2** | Preprocessing transformations (Unicode NFC, deduplication, length filtering) specified. | Yes | Fully implemented in `src/preprocessing.py`. |
| **3.3** | Deterministic train/validation/test split logic with fixed random seed. | Yes | `split_and_save(..., seed=42)` in `src/preprocessing.py`. |
| **3.4** | Exact split sizes verified against physical files. | Yes | Twi: 4,857 train, 607 val, 608 test; Ewe: 2,764 train, 345 val, 347 test. |
| **3.5** | Held-out test sets strictly sealed until final evaluation run. | Yes | Maintained without leakage throughout calibration and training. |

---

## 4. Computational Setup & Environment

- **Operating System:** Windows 11 (build tested on Windows, reproducible on Linux/macOS)
- **Python Version:** 3.10+ / 3.14 compatible
- **Hardware Requirements:** Consumer laptop CPU (e.g. Intel Core i5/i7 or AMD Ryzen), $\ge 8$ GB RAM. No GPU required.
- **Compute Time:**
  - Tokenizer Training (BPE + Unigram): $\sim 1.5$ minutes total
  - Held-out Benchmark: $\sim 2.0$ minutes total
  - Latency Benchmark (5 runs with warmup): $\sim 45$ seconds
  - Downstream Sentiment Probe: $\sim 35$ seconds
- **Dependencies:** Exact versions locked in `requirements.txt`:
  - `tokenizers>=0.19.0`
  - `transformers>=4.44.0`
  - `sentencepiece>=0.2.0`
  - `datasets>=2.20.0`
  - `scikit-learn>=1.5.0`
  - `scipy>=1.13.0`
  - `statsmodels>=0.14.0`
  - `pandas>=2.2.0`, `numpy>=1.26.0`, `matplotlib>=3.9.0`, `seaborn>=0.13.0`

---

## 5. Statistical Rigor & Testing

| Item | Requirement | Status | Verification Detail |
| :--- | :--- | :---: | :--- |
| **5.1** | Paired sentence-by-sentence alignment across all evaluated tokenizers. | Yes | Implemented in `get_paired_fertility()` (`src/significance.py`). |
| **5.2** | Non-parametric hypothesis testing suitable for skewed fertility distributions. | Yes | Two-sided Wilcoxon signed-rank test (`paired_wilcoxon_test`). |
| **5.3** | Multiplicity adjustment for all simultaneous statistical comparisons. | Yes | Holm-Bonferroni step-down correction (`apply_holm_bonferroni`). |
| **5.4** | Non-parametric bootstrap confidence intervals (1,000 iterations, 95% CI). | Yes | `paired_bootstrap_ci()` and `unpaired_bootstrap_ci()`. |
| **5.5** | Reporting exact sample sizes ($N$) and degrees of freedom / sentence counts. | Yes | $N=608$ (Twi), $N=347$ (Ewe) reported in every results table. |

---

## 6. Artifact Verification & Checksum Table

All evaluation metrics, figures, and model checkpoints are saved in the repository:

| Artifact Type | Path | Verification Check |
| :--- | :--- | :--- |
| **Trained BPE Tokenizer** | `models/ghanatok/ghanatok_tokenizer.json` | 8,000 vocab, byte-level BPE, 1.656 Twi / 1.750 Ewe fertility |
| **Trained Unigram Tokenizer** | `models/ghanatok_unigram/ghanatok_unigram.model` | 8,000 vocab, SentencePiece unigram, 1.251 Twi / 1.349 Ewe fertility |
| **Baseline Benchmark CSV** | `reports/tables/baseline_summary.csv` | Calibration data on 3,000 train/val sentences |
| **Final Test Evaluation CSV** | `reports/tables/final_heldout_results.csv` | 5,383 rows across 9 evaluated model-language pairings |
| **Final Test Summary CSV** | `reports/tables/final_summary.csv` | Aggregated held-out test metrics |
| **Significance Results CSV** | `reports/tables/rq2_significance_results.csv` | Wilcoxon stats, Holm-corrected $p$-values, bootstrap CIs |
| **Cross-Lingual Comparison** | `reports/tables/rq3_significance_results.csv` | Mann-Whitney U test between Twi and Ewe reductions |
| **Latency Benchmark CSV** | `reports/tables/latency_benchmark.csv` | Mean sec/run, sentences/sec, chars/sec over 5 runs |
| **Cost Multiplier CSV** | `reports/tables/cost_multiplier.csv` | Normalized pricing multipliers vs. GhanaTok |
| **Context Budget CSV** | `reports/tables/context_budget.csv` | Usable words in 4k, 32k, and 128k context windows |
| **Vocab Sweep CSV** | `reports/tables/vocab_size_sweep_summary.csv` | 4k, 8k, 16k, 32k scaling curves |
| **Sentiment Probe CSV** | `reports/tables/sentiment_probe.csv` | Accuracy, Macro F1, active feature dimensions |
| **Baseline Fertility Figure** | `reports/figures/baseline_fertility_by_tokenizer.png` | Publication-ready bar chart |
| **Final Held-Out Figure** | `reports/figures/final_heldout_fertility_comparison.png` | Publication-ready comparison bar chart |
| **Vocab Sweep Figure** | `reports/figures/vocab_size_sweep_fertility.png` | 4-point vocabulary scaling curve |
| **Cost & Context Figure** | `reports/figures/cost_and_context_budget.png` | Dual-panel economic and context capacity plot |

---

## 7. Step-by-Step Reproduction Command Sequence

To completely reproduce the project from a fresh shell:

```bash
# 1. Clone repository and navigate to root
git clone https://github.com/exornamb/GhanaToken.git
cd GhanaToken

# 2. Initialize virtual environment and activate
python -m venv .venv
# On Windows:
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify environment and repository structure
pytest -v tests/test_project_structure.py

# 5. Re-run training (optional; models already provided)
python -c "
from src.train_ghanatok import build_training_corpus, train_ghanatok, train_ghanatok_unigram
build_training_corpus()
train_ghanatok()
train_ghanatok_unigram()
"

# 6. Run automated test suite
pytest -v tests/
```
