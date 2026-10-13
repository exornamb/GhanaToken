# GhanaToken: Tokenizer Optimization for Ghanaian Languages (Twi & Ewe)

A comparative evaluation of subword tokenization efficiency across modern multilingual tokenizers (mBERT, XLM-R, AfroXLMR), regional models (ABENA), and **GhanaTok**—a dedicated, bilingual byte-level BPE and SentencePiece Unigram tokenizer designed for **Twi (Akan)** and **Ewe (Gbe)**.

**Course**: DCIT 316, Individual Research Project  
**Author**: Jennifer Banibensu  
**Final Report**: [reports/final_report.md](reports/final_report.md)  
**Data Card**: [reports/data_card.md](reports/data_card.md)  

---

## 1. Key Results Summary

On sealed held-out test sets (608 Twi sentences, 347 Ewe sentences), **GhanaTok** eliminates the severe fragmentation observed in standard multilingual models:

| Language | Tokenizer | Mean Fertility (Tokens/Word) | Density (Tokens/Char) | Fragmentation Rate (% Words Split) | Reduction vs Best General Baseline | 95% Bootstrap CI | Statistical Significance |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ewe** | AfroXLMR / XLM-R | 2.608 | 0.505 | 70.99% | — | — | — |
| **Ewe** | mBERT | 2.291 | 0.445 | 63.87% | Baseline (0.0%) | — | — |
| **Ewe** | **GhanaTok (BPE)** | **1.750** | **0.341** | **51.25%** | **-23.6%** | **[22.08%, 24.95%]** | **$p < 0.001$ (Holm-corrected)** |
| **Ewe** | *GhanaTok-Unigram (Bonus)* | *1.349* | *0.263* | *22.83%* | *-41.1%* | *[39.67%, 42.39%]* | *$p < 0.001$ (Holm-corrected)* |
| **Twi** | AfroXLMR / XLM-R | 2.444 | 0.482 | 70.26% | — | — | — |
| **Twi** | ABENA (Twi only) | 2.419 | 0.477 | 72.12% | — | — | — |
| **Twi** | mBERT | 2.389 | 0.471 | 70.47% | Baseline (0.0%) | — | — |
| **Twi** | **GhanaTok (BPE)** | **1.656** | **0.327** | **48.82%** | **-30.7%** (*-31.5% vs ABENA*) | **[29.85%, 31.44%]** | **$p < 0.001$ (Holm-corrected)** |
| **Twi** | *GhanaTok-Unigram (Bonus)* | *1.251* | *0.248* | *17.58%* | *-47.6%* | *[46.81%, 48.43%]* | *$p < 0.001$ (Holm-corrected)* |

### Key Findings:
1. **Statistically Defensible Compression**: An 8,000-vocabulary bilingual tokenizer reduces token fertility by **30.7% on Twi** ($p < 0.001$, Holm-corrected) and **23.6% on Ewe** ($p < 0.001$, Holm-corrected) relative to mBERT (and >32% vs XLM-R/AfroXLMR).
2. **Robust Dialect-Aware Pre-Tokenization**: Protecting extended Latin characters (`ɛ`, `ɔ`, `ɖ`, `ŋ`, `ʋ`, `ƒ`) and injecting seed morphemes (`Akwaaba`, `Medaase`, `Woezɔ`, `mbe-`, `-foɔ`, `-wo`) prevented single-character and byte scattering.
3. **ABENA Asymmetry Note**: ABENA was evaluated strictly on Twi (monolingual design for Akuapem Twi) and achieved 2.419 tokens/word on the held-out test set; GhanaTok outperformed it by 31.5% ($p < 0.001$).
4. **Vocabulary Scaling & Diminishing Returns**: Swept 4k, 8k, 16k, and 32k budgets; confirmed that 8,000 tokens captures >95% of theoretical compression with corpus saturation at ~11k unique subwords.
5. **Operational & Cost Implications**:
   - **API Cost Multipliers**: Multilingual models (mBERT, XLM-R) impose a **+44% to +49% cost penalty** relative to GhanaTok-BPE, and up to **+95% (+1.95x)** relative to GhanaTok-Unigram.
   - **Context Window Capacity**: In a 4,000-token window, GhanaTok-BPE accommodates **+47.5% more Twi words** (+778 words) and **+49.0% more Ewe words** (+752 words) compared to XLM-R.
   - **Tokenization Speed**: GhanaTok encodes up to 3,345 sentences/sec (BPE) and 26,363 sentences/sec (Unigram binary wrapper).
6. **Secondary / Bonus Extensions**:
   - **GhanaTok-Unigram**: Explored SentencePiece Unigram probabilistic pruning, achieving 1.251 tokens/word on Twi and winning 597 of 939 sentence head-to-head comparisons against BPE ($p < 0.001$).
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
│   ├── ghanatok_unigram/          # GhanaTok SentencePiece Unigram (8k vocab)
│   │   ├── ghanatok_unigram.model
│   │   └── ghanatok_unigram.vocab
│   └── ghanatok_{bpe,unigram}_{4000,8000,16000,32000}/ # Vocab sweep models
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_preprocessing_cleaning.ipynb
│   ├── 03_tokenizer_benchmark.ipynb
│   ├── 04_ghanatok_training.ipynb
│   ├── 05_evaluation_error_analysis.ipynb
│   ├── 06_sentiment_probe.ipynb
│   ├── 07_vocab_size_sweep.ipynb
│   ├── 08_statistical_significance.ipynb
│   └── 09_latency_and_cost.ipynb
├── reports/
│   ├── figures/                   # Visualization charts (.png)
│   │   ├── baseline_fertility_by_tokenizer.png
│   │   ├── final_heldout_fertility_comparison.png
│   │   ├── vocab_size_sweep_fertility.png
│   │   └── cost_and_context_budget.png
│   ├── tables/                    # Evaluation, significance, latency, & cost CSVs (.csv)
│   ├── data_card.md               # Dataset provenance & limitations documentation
│   └── final_report.md            # Comprehensive final research report
├── src/
│   ├── preprocessing.py           # Text cleaning, NFC normalisation, deduplication
│   ├── tokenizer_benchmark.py     # Per-word fertility and fragmentation analysis
│   ├── train_ghanatok.py          # BPE & Unigram training recipes with seed morphemes
│   ├── significance.py            # Paired Wilcoxon, bootstrap CIs, and Holm-Bonferroni
│   └── latency_benchmark.py       # Multi-run latency & throughput measurement
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

### 3. Run Notebooks
Each stage of the research pipeline is structured as a self-contained, reproducible notebook in `notebooks/`:

* **`01_data_audit.ipynb`**: Initial raw data audit, character distributions, and language checks.
* **`02_preprocessing_cleaning.ipynb`**: Unicode NFC normalization, deduplication, and train/val/test splitting.
* **`03_tokenizer_benchmark.ipynb`**: Calibration benchmarking of multilingual baselines on train/val splits.
* **`04_ghanatok_training.ipynb`**: Training GhanaTok (Byte-Level BPE) and GhanaTok-Unigram (SentencePiece).
* **`05_evaluation_error_analysis.ipynb`**: Held-out test evaluation, qualitative case studies, and dialect checks.
* **`06_sentiment_probe.ipynb`**: AfriSenti downstream classification probe and active feature analysis.
* **`07_vocab_size_sweep.ipynb`**: 4k, 8k, 16k, and 32k vocabulary size scaling sweep and diminishing returns analysis.
* **`08_statistical_significance.ipynb`**: Paired Wilcoxon signed-rank tests, bootstrap CIs, and Holm-Bonferroni correction.
* **`09_latency_and_cost.ipynb`**: Tokenization latency, API processing cost multipliers, and context window budgets.

To launch Jupyter and execute the notebooks:
```bash
jupyter notebook notebooks/
```

