# Failure Log: GhanaToken Research & Engineering Post-Mortem

This document records the experimental failures, invalid hypotheses, architectural dead-ends, and engineering bugs encountered during the development and evaluation of **GhanaTok**. In accordance with scientific integrity and reproducibility standards, all negative findings and their corrective actions are transparently detailed below.

---

## 1. Experimental Failures & Invalid Hypotheses

### 1.1 Hypothesis: Lower Subword Fertility Automatically Boosts Downstream Classification Accuracy
- **Original Hypothesis:** Based on claims in the multilingual tokenization literature (e.g., Lundin et al., 2026), the initial hypothesis posited that reducing subword fertility by 23% to 47% would yield a statistically significant improvement in classification accuracy on downstream sentiment analysis.
- **Experimental Setup:** Implemented a downstream bag-of-tokens Logistic Regression probe on the official AfriSenti Twi dataset (3,481 train, 388 validation, 949 test tweets). Evaluated all baseline tokenizers alongside GhanaTok (BPE) and GhanaTok-Unigram.
- **Empirical Result:**
  - mBERT Macro F1: `0.4921`
  - XLM-R / AfroXLMR Macro F1: `0.4889`
  - ABENA Macro F1: `0.4945`
  - GhanaTok (BPE) Macro F1: `0.5110`
  - GhanaTok-Unigram Macro F1: `0.4866`
  - **95% Bootstrap Confidence Intervals:** All confidence intervals overlapped in the range `[0.48, 0.52]`.
- **Root Cause & Learning:** Subword fertility is a measure of vocabulary coverage and representation density, not semantic discriminative power. For linear classification, bag-of-tokens features from fragmented words still provide sufficient bag-of-ngrams signals. However, GhanaTok achieved equivalent predictive accuracy using **47% fewer unique features** (1,773 vs 3,386–3,907), proving representational compactness rather than raw accuracy supremacy.
- **Resolution:** Updated research claims to explicitly disclaim downstream accuracy superiority. Framed the benefit around compute budget, context window capacity, and API cost parity.

---

### 1.2 Hypothesis: Scaling Vocabulary Size to 32,000 Tokens Would Continually Improve Compression
- **Original Hypothesis:** Scaling the subword vocabulary from 8k to 16k and 32k would yield steady gains in token compression.
- **Experimental Setup:** Trained BPE and SentencePiece Unigram tokenizers across four target vocabulary budgets: 4,000, 8,000, 16,000, and 32,000 tokens (`07_vocab_size_sweep.ipynb`).
- **Empirical Result:**
  - Twi BPE: 4k (`1.777`) $\rightarrow$ 8k (`1.656`, -6.81%) $\rightarrow$ 16k (`1.585`, -4.29%) $\rightarrow$ 32k (`1.585`, **0.00%**)
  - Ewe BPE: 4k (`1.846`) $\rightarrow$ 8k (`1.750`, -5.20%) $\rightarrow$ 16k (`1.712`, -2.17%) $\rightarrow$ 32k (`1.712`, **0.00%**)
  - Unigram sweeps plateaued completely between 16k and 32k.
- **Root Cause & Learning:** The combined training corpus (7,621 sentences) contains ~11,000 unique word types. Beyond 16,000 tokens, the corpus vocabulary was completely exhausted; every possible subword and whole word had already been allocated a vocabulary slot. Setting `hard_vocab_limit=False` in SentencePiece prevented training crashes, but revealed absolute corpus saturation.
- **Resolution:** Formally defended 8,000 tokens as the optimal operational sweet spot. 8k captures >95% of theoretical compression while maintaining a compact embedding matrix suitable for resource-constrained fine-tuning.

---

### 1.3 Hypothesis: ABENA Could Serve as a Unified Ghanaian Regional Baseline
- **Original Hypothesis:** ABENA (`Ghana-NLP/abena-base-akuapem-twi-cased`), being a Ghanaian language model, could be evaluated as a regional baseline across both Twi and Ewe.
- **Experimental Setup:** Attempted to encode Ewe text using ABENA's tokenizer in early calibration scripts.
- **Empirical Result:** ABENA produced extreme fragmentation (>80% words split) and completely failed on Ewe phonemic consonants (`ɖ`, `ŋ`, `ʋ`, `ƒ`), segmenting them into unknown tokens or raw single characters.
- **Root Cause & Learning:** ABENA was designed and trained monolingually on Akuapem Twi. Twi is in the Kwa language branch, whereas Ewe is in the Gbe branch with distinct phonology and orthography. Expecting cross-lingual transfer across non-cognate branches without training data was flawed.
- **Resolution:** Architected a strict separation: ABENA was placed in `TWI_ONLY_TOKENIZERS` and evaluated solely on Twi. It was explicitly documented as absent from Ewe tables to prevent unfair or misleading cross-lingual metrics.

---

## 2. Engineering Bugs & Architectural Dead-Ends

### 2.1 Bug: Extended Latin Character Fragmentation in Default ByteLevel BPE
- **Symptom:** In early prototypes, words containing `ɛ`, `ɔ`, `ɖ`, `ŋ`, `ʋ`, `ƒ` were split into 3–4 sub-tokens even when the word was present in the training set.
- **Root Cause:** Standard Hugging Face `tokenizers.pre_tokenizers.ByteLevel` uses a default GPT-2 regex that splits unicode character classes based on ASCII assumptions, separating non-ASCII letters from adjacent ASCII letters.
- **Fix:** Implemented a two-stage pre-tokenizer sequence:
  1. A custom regex split: `Regex(r"'s|'[tmdllve]|\s?[\p{L}\p{M}ɛɔɖŋʋƒƐƆƉŊƲƑ]+|[^\s\p{L}\p{M}]+")`
  2. ByteLevel pre-tokenizer with `use_regex=False`: `ByteLevel(add_prefix_space=False, use_regex=False)`
- **Verification:** Whole words like `Akwaaba`, `Woezɔ`, `Medaase` and affixes like `-foɔ`, `-wo` are preserved intact.

---

### 2.2 Bug: Unicode NFD Decomposed Diacritic Splitting
- **Symptom:** Certain accented characters in Ewe (e.g., `è` vs `e` + `\u0300`) resulted in 2 subword tokens (the base letter followed by the isolated combining accent token).
- **Root Cause:** Data collected from web and Bible corpora mixed precomposed Unicode (NFC) with decomposed Unicode (NFD).
- **Fix:** In `src/preprocessing.py`, enforced `unicodedata.normalize("NFC", text)` on all input strings before deduplication, splitting, or tokenization.

---

### 2.3 Bug: Full-Sentence Merge Bias vs. Word-Isolated Fertility Metric
- **Symptom:** Measuring fertility using `len(tokenizer.encode(sentence)) / len(sentence.split())` produced contradictory results depending on whether tokenizers prepended spaces (e.g. `_` in SentencePiece vs `##` in WordPiece).
- **Root Cause:** Full-sentence encoding allows cross-word merges (e.g., merging trailing punctuation or adjacent spaces), confounding vocabulary quality with boundary merge heuristics.
- **Fix:** Refactored `analyze_sentence()` in `src/tokenizer_benchmark.py` to evaluate each whitespace-separated word in isolation without special tokens, exactly aligning with the standardized protocol of Petrov et al. (2023) and Ahia et al. (2023).

---

## 3. Summary of Design Defenses

| Design Decision | Alternative Rejected | Justification |
| :--- | :--- | :--- |
| **8,000 Token Vocabulary** | 32,000 tokens | Empirical sweep proved corpus saturation at ~11k unique subwords; 8k preserves memory and training speed with <5% compression loss. |
| **Bilingual Twi+Ewe Model** | Monolingual separate tokenizers | A shared bilingual model allows joint representation, cross-lingual transfer, and halved deployment maintenance for Ghanaian NLP. |
| **Byte-Level BPE Fallback** | Pure WordPiece (BERT style) | Byte fallback guarantees 0% out-of-vocabulary (`<unk>`) rate on unseen text and slang. |
| **Paired Wilcoxon & Bootstrap** | Standard Student's $t$-test | Token fertility distributions are non-normal and heavily right-skewed; non-parametric tests prevent invalid significance claims. |
| **Sealed Held-Out Test Set** | Cross-validation or test re-use | Test splits were isolated on Day 2 and never inspected during training or vocabulary tuning, eliminating data leakage. |
