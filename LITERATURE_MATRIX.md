# Literature Matrix: Tokenization Efficiency in Ghanaian Low-Resource Languages

- **Project:** DCIT 316 Individual Research Project — Tokenizer Optimization for Ghanaian Languages (Twi & Ewe)
- **Author:** Jennifer Banibensu
- **Target Languages:** Twi / Akan (`twi`) and Ewe / Gbe (`ewe`)
- **Key Artifacts:** [MODEL_CARD.md](MODEL_CARD.md) | [DATA_CARD.md](DATA_CARD.md) | [FAILURE_LOG.md](FAILURE_LOG.md) | [reports/final_report.md](reports/final_report.md)

---

## 1. Structured Literature Synthesis Table

| Citation | Category | Core Contribution / Finding | How GhanaToken Employs It | Empirical Mapping in GhanaToken | Status / Peer-Review |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Petrov et al. (2023)**<br>*NeurIPS* | Fairness & Token Tax | Language model tokenizers introduce systematic unfairness; low-resource languages require 2x–5x more tokens for the same semantic content. | Theoretical motivation for **RQ1** (quantifying the token tax on Twi and Ewe). Adopted word-isolated tokenization metric to avoid boundary merge artifacts. | Section 1, Section 3, `src/tokenizer_benchmark.py` | Peer-reviewed (NeurIPS 2023) |
| **Ahia et al. (2023)**<br>*EMNLP* | Economic Disparity | Commercial LLM APIs charge uniformly per token, imposing higher operational costs on non-English users. | Grounding for API cost multiplier formulas and context window budget calculations. | Section 5.6, `src/latency_benchmark.py`, `09_latency_and_cost.ipynb` | Peer-reviewed (EMNLP 2023) |
| **Lundin et al. (2026)**<br>*AfricaNLP @ ACL* | African Token Bias | Evaluated 16 African languages; showed that high fertility correlates with downstream degradation and quadrupled pre-training cost. | Justification for fertility as a core efficiency metric. Led to testing whether fertility reduction boosts downstream probe accuracy. | Section 2, Section 5.7, `06_sentiment_probe.ipynb` | Peer-reviewed (AfricaNLP 2026) |
| **Somide (2026)**<br>*arXiv:2606.24460* | African Language Tax | Across 20 African languages and 11 tokenizers, African text costs up to 8.9x more in inference; argues general tokenizers cannot fix this without African-specific designs. | Justifies creating a dedicated, compact regional tokenizer (GhanaTok) rather than relying on multilingual adaptation. | Section 1, Section 2, Section 5.6 | Preprint (arXiv) |
| **Sennrich et al. (2016)**<br>*ACL* | Subword Modeling | Introduced Byte Pair Encoding (BPE) for open-vocabulary neural machine translation. | Foundation for **GhanaTok (BPE)** architecture, enhanced with custom regex and seed morphemes. | Section 4, `src/train_ghanatok.py` | Peer-reviewed (ACL 2016) |
| **Kudo (2018)**<br>*ACL* | Subword Regularization | Introduced the Unigram language model subword segmentation algorithm with probabilistic candidate pruning. | Foundation for **GhanaTok-Unigram**, evaluated as an exploratory alternative to greedy BPE merges. | Section 4, Section 5.4, `src/train_ghanatok.py` | Peer-reviewed (ACL 2018) |
| **Kudo & Richardson (2018)**<br>*EMNLP Demos* | Tooling & Implementation | SentencePiece library: language-independent subword tokenizer treating whitespace as a basic symbol (`_`). | Utilized directly to train and wrap GhanaTok-Unigram with `SentencePieceWrapper`. | Section 4, `src/train_ghanatok.py` | Peer-reviewed (EMNLP 2018) |
| **Kautsar & Koto (2025)**<br>*arXiv:2510.06128* | Tokenizer Architectures | Explores training parallel independent tokenizers per language family to balance cross-lingual fertility. | Comparative architectural baseline; contrasted with GhanaTok's compact bilingual joint vocabulary design. | Section 2, Section 6 | Preprint (arXiv) |
| **Rust et al. (2021)**<br>*ACL-IJCNLP* | Evaluation Methodology | Comprehensive study demonstrating that tokenizer quality directly limits multilingual language model transfer and efficiency. | Validates using token fertility, characters-per-token density, and fragmentation rate as primary metrics. | Section 2, Section 3, `src/tokenizer_benchmark.py` | Peer-reviewed (ACL-IJCNLP 2021) |
| **Devlin et al. (2019)**<br>*NAACL* | Multilingual Baselines | Multilingual BERT (mBERT) trained with WordPiece over 104 languages using a 110,000 subword vocabulary. | Primary multilingual baseline (achieved lowest fertility among general baselines: 2.389 Twi, 2.291 Ewe). | Section 3, Section 5 | Peer-reviewed (NAACL 2019) |
| **Conneau et al. (2020)**<br>*ACL* | Multilingual Baselines | XLM-RoBERTa (XLM-R) using SentencePiece with 250,000 vocabulary trained across 100 languages. | Multilingual baseline; exhibited severe fragmentation on Ghanaian text (2.444 Twi, 2.608 Ewe). | Section 3, Section 5 | Peer-reviewed (ACL 2020) |
| **Alabi et al. (2022)**<br>*COLING* | African Multilingual Baselines | AfroXLMR: adaptive fine-tuning of XLM-R on African languages. | Baseline evaluated to test if African domain fine-tuning changed tokenizer vocabulary (verified vocabulary is identical to XLM-R). | Section 3, Section 5 | Peer-reviewed (COLING 2022) |
| **Azunre et al. (2021)**<br>*arXiv:2103.15963* | Regional Baselines | ABENA: first contextual embedding model for Twi (Akuapem dialect) trained on Ghanaian text. | Regional monolingual baseline for Twi. Evaluated strictly on Twi; out-performed by GhanaTok by 31.54%. | Section 1, Section 3, Section 5.3 | Preprint (arXiv) |
| **Adu Gyamfi et al. (2026)**<br>*arXiv:2603.13793* | Corpora & Datasets | GhanaNLP Parallel Corpora: sentence-aligned parallel corpora for Ghanaian languages (Twi, Ewe, Fante, Ga, Kusaal). | Core training, validation, and held-out test corpora for GhanaTok. | Section 3, [DATA_CARD.md](DATA_CARD.md), `src/preprocessing.py` | Preprint (arXiv) |
| **Muhammad et al. (2023)**<br>*EMNLP* | Downstream Benchmarks | AfriSenti: benchmark sentiment dataset covering 14 African languages on Twitter, including Twi. | Downstream task data for secondary classification probe (`06_sentiment_probe.ipynb`). | Section 5.7, `reports/tables/sentiment_probe.csv` | Peer-reviewed (EMNLP 2023) |
| **Issaka et al. (2024)**<br>*arXiv:2405.06818* | Survey & Landscape | The Ghanaian NLP Landscape: comprehensive survey of computational linguistics resources for Ghanaian languages. | Documents the scarcity of dedicated tokenization infrastructure for Ghanaian languages. | Section 1, Section 2 | Preprint (arXiv) |
| **Issaka et al. (2026)**<br>*ACL 2026* | Collaborative Infrastructure | The African Languages Lab: collaborative initiative to curate and expand open datasets for African NLP. | Provides contextual foundation for open Ghanaian language resource stewardship. | Section 2 | Peer-reviewed (ACL 2026) |

---

## 2. Research Questions to Literature Mapping

### RQ1: Extent of the African Language Token Tax on Ghanaian Languages
- **Literature Context:** Petrov et al. (2023) and Somide (2026) established the existence of unequal tokenization overhead for non-Latin and African scripts.
- **GhanaToken Contribution:** Quantifies the exact tax on Twi and Ewe across general baselines (mBERT, XLM-R, AfroXLMR) and regional baselines (ABENA). On held-out text, multilingual models split **63.8% to 72.1% of words**, producing **2.29 to 2.61 tokens per word** (compared to ~1.00 for English).
- **Novel Finding:** AfroXLMR, despite its African language focus, shares XLM-R's exact SentencePiece vocabulary and provides zero subword compression relief.

### RQ2: Impact of Custom Dialect-Aware Tokenization (GhanaTok)
- **Literature Context:** Sennrich et al. (2016) and Kudo (2018) demonstrated subword efficiency in high-resource settings; Kautsar & Koto (2025) argued for targeted tokenizers.
- **GhanaToken Contribution:** Proves that an 8,000-subword bilingual tokenizer reduces token fertility by **30.67% on Twi** ($p < 0.001$, Holm-corrected) and **23.60% on Ewe** ($p < 0.001$, Holm-corrected) relative to mBERT, and >32% relative to XLM-R. GhanaTok-Unigram achieves even greater compression (up to 47.63% reduction on Twi).

### RQ3: Cross-Language Disparity Between Twi and Ewe
- **Literature Context:** Dialectal variation and extended Latin orthographies remain underexplored in subword tokenizer benchmarks (Issaka et al., 2024).
- **GhanaToken Contribution:** Identifies that Ewe's unique orthography (`ɖ`, `ŋ`, `ɔ`, `ɛ`, `ʋ`, `ƒ`) suffers higher baseline fragmentation than Twi due to single-character isolation. Protecting these characters in `GHANA_PRETOKENIZER_PATTERN` produced statistically significant cross-lingual compression gains (Mann-Whitney U $p = 7.75 \times 10^{-19}$).

---

## 3. Methodological Divergences & Empirical Lessons

1. **Downstream Accuracy vs. Fertility Claims (Lundin et al. 2026 Divergence):**
   - *Literature Claim:* Lundin et al. (2026) linked higher fertility directly to lower downstream classification accuracy.
   - *GhanaToken Empirical Finding:* On the AfriSenti Twi probe, GhanaTok and multilingual baselines produced overlapping Macro F1 scores (0.486 to 0.511 with 95% bootstrap CIs overlapping). While compression does not instantly enhance linear classification accuracy, it cuts representation dimension by 47.6%, yielding substantial memory and computational efficiency.
2. **Vocabulary Scaling Saturation (BPE Sweep Finding):**
   - *Standard Assumption:* Larger vocabularies (e.g. 32k or 50k) universally improve compression.
   - *GhanaToken Finding:* In corpora of ~10k unique word types, vocabulary sizes beyond 16,000 saturate with 0.00% incremental compression gain. 8,000 tokens captures >95% of theoretical compression while preserving compact embedding matrices.
