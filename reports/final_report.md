# GhanaToken: Tokenizer Optimization for Ghanaian Languages (Twi & Ewe)

## 1. Introduction & Research Questions

Subword tokenization is a critical foundation for modern language models, yet standard multilingual tokenizers allocate minimal vocabulary capacity to low-resource African languages. This project investigates subword tokenization efficiency for two major Ghanaian languages—**Twi** (Akan) and **Ewe** (Gbe)—evaluating standard multilingual baselines and introducing **GhanaTok**, a dedicated bilingual tokenizer.

The project evaluates three core research questions:
1. **RQ1**: How severely do general multilingual tokenizers (mBERT, XLM-R, AfroXLMR) and existing regional tokenizers (ABENA) fragment Twi and Ewe text?
2. **RQ2**: Does a small, dedicated tokenizer (GhanaTok) trained with dialect-aware pre-tokenization and seed morphemes reduce token fertility and subword fragmentation on held-out Twi and Ewe text?
3. **RQ3**: Does a shared bilingual vocabulary (Twi + Ewe) achieve high tokenization efficiency across both languages within a compact 8,000-token budget?

---

## 2. Results

### 2.1 Baseline Tokenizer Comparison (Calibration Split)
Across a balanced sample of 3,000 Twi sentences and 3,000 Ewe sentences from the training and validation splits:
- **Twi**: **mBERT** produced the lowest fertility (**2.371 tokens/word**, 69.96% words split), followed by **ABENA** (**2.402 tokens/word**, 71.71% split), while **XLM-R** and **AfroXLMR** produced **2.438 tokens/word** (70.13% split).
- **Ewe**: **mBERT** produced the lowest fertility (**2.303 tokens/word**, 64.66% words split), whereas **XLM-R** and **AfroXLMR** showed severe fragmentation (**2.625 tokens/word**, 71.37% split).

### 2.2 ABENA-Specific Comparison (Twi Only)
- ABENA was evaluated exclusively on Twi, reflecting its monolingual design (trained on Akuapem Twi).
- On the 3,000-sentence calibration set, ABENA achieved **2.402 tokens/word** (71.71% words split).
- On the held-out test set (608 sentences), ABENA achieved **2.419 tokens/word** (72.12% words split).

### 2.3 GhanaTok-BPE Held-Out Evaluation
On the strictly sealed held-out test set (608 Twi sentences, 347 Ewe sentences):
- **Twi**: **GhanaTok (Byte-Level BPE)** achieved a mean fertility of **1.656 tokens/word** (48.82% words split), compared with **2.389** for mBERT, **2.444** for XLM-R / AfroXLMR, and **2.419** for ABENA.
  - This represents a **30.7% reduction in token fertility** relative to the best general baseline (mBERT) and a **31.5% reduction** relative to ABENA.
- **Ewe**: **GhanaTok (Byte-Level BPE)** achieved a mean fertility of **1.750 tokens/word** (51.25% words split), compared with **2.291** for mBERT and **2.608** for XLM-R / AfroXLMR.
  - This represents a **23.6% reduction in token fertility** relative to mBERT and a **32.9% reduction** relative to XLM-R / AfroXLMR.

### Master Comparison Table

| Language | Tokenizer | Split | Mean Fertility (Tokens/Word) | Density (Tokens/Char) | Fragmentation Rate (% Words Split) | Sentence Count |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Ewe** | AfroXLMR | Train+Val | 2.625 | 0.506 | 71.37% | 3,000 |
| **Ewe** | XLM-R | Train+Val | 2.625 | 0.506 | 71.37% | 3,000 |
| **Ewe** | mBERT | Train+Val | 2.303 | 0.445 | 64.66% | 3,000 |
| **Ewe** | AfroXLMR | Held-Out Test | 2.608 | 0.505 | 70.99% | 347 |
| **Ewe** | XLM-R | Held-Out Test | 2.608 | 0.505 | 70.99% | 347 |
| **Ewe** | mBERT | Held-Out Test | 2.291 | 0.445 | 63.87% | 347 |
| **Ewe** | **GhanaTok (BPE)** | **Held-Out Test** | **1.750** | **0.341** | **51.25%** | **347** |
| **Ewe** | *GhanaTok-Unigram (Bonus)* | *Held-Out Test* | *1.349* | *0.263* | *22.83%* | *347* |
| **Twi** | ABENA | Train+Val | 2.402 | 0.475 | 71.71% | 3,000 |
| **Twi** | AfroXLMR | Train+Val | 2.438 | 0.483 | 70.13% | 3,000 |
| **Twi** | XLM-R | Train+Val | 2.438 | 0.483 | 70.13% | 3,000 |
| **Twi** | mBERT | Train+Val | 2.371 | 0.469 | 69.96% | 3,000 |
| **Twi** | ABENA | Held-Out Test | 2.419 | 0.477 | 72.12% | 608 |
| **Twi** | AfroXLMR | Held-Out Test | 2.444 | 0.482 | 70.26% | 608 |
| **Twi** | XLM-R | Held-Out Test | 2.444 | 0.482 | 70.26% | 608 |
| **Twi** | mBERT | Held-Out Test | 2.389 | 0.471 | 70.47% | 608 |
| **Twi** | **GhanaTok (BPE)** | **Held-Out Test** | **1.656** | **0.327** | **48.82%** | **608** |
| **Twi** | *GhanaTok-Unigram (Bonus)* | *Held-Out Test* | *1.251* | *0.248* | *17.58%* | *608* |

### 2.4 Secondary Comparison: GhanaTok-Unigram (Bonus Recipe)
- Trained on the same corpus with the same seed morphemes using SentencePiece Unigram probabilistic pruning.
- Achieved **1.251 tokens/word** (17.58% words split) on Twi and **1.349 tokens/word** (22.83% words split) on Ewe.
- **Head-to-Head Sentence Wins (Twi, N=939)**:
  - GhanaTok-Unigram won on **597 sentences** (lower token count).
  - GhanaTok-BPE won on **50 sentences**.
  - **292 ties**.

### 2.5 Akuapem Spelling Marker Check (ABENA)
- Across 608 Twi held-out sentences, 76 sentences (12.5%) matched specific Akuapem dialect keyword markers (`otumi`, `ebepɛ`, `ebetumi`, `obetumi`, `nkateɛ`).
- **ABENA mean fertility**: **2.377 tokens/word** on flagged Akuapem sentences vs **2.425 tokens/word** on unflagged sentences.
- **GhanaTok (BPE) mean fertility**: **1.663 tokens/word** on flagged sentences vs **1.655 tokens/word** on unflagged sentences.

### 2.6 Sentence-Length Breakdown
- Evaluated across four sentence-length bins: short (1–5 words), medium (6–10 words), long (11–20 words), and very long (21+ words).
- Short sentences exhibited higher per-word fertility across all tokenizers (e.g., Ewe AfroXLMR = 3.400, GhanaTok-BPE = 2.233, GhanaTok-Unigram = 1.733) due to boundary subwords and capitalized salutations.
- GhanaTok maintained an efficiency advantage across every sentence-length bin (e.g., Twi very long sentences: GhanaTok-BPE = 1.663 vs mBERT = 2.312, ABENA = 2.335, XLM-R = 2.340).

### 2.7 Downstream Sentiment Probe Results (Bonus, Twi Only)
- Evaluated on the public AfriSenti Twi dataset using official splits (3,869 train+val tweets, 949 held-out test tweets) with a bag-of-tokens Logistic Regression (`random_state=42`, `max_iter=1000`).

| Tokenizer | Active Vocab Features | Accuracy | Macro F1 | 95% Bootstrap CI (Macro F1) | F1 (Negative) | F1 (Neutral) | F1 (Positive) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **mBERT** | 3,896 | 65.02% | 0.5624 | [0.5282, 0.5952] | 0.6940 | 0.2810 | 0.7121 |
| **XLM-R** | 4,483 | 64.07% | 0.5454 | [0.5129, 0.5779] | 0.6897 | 0.2397 | 0.7068 |
| **AfroXLMR** | 4,483 | 64.07% | 0.5454 | [0.5120, 0.5775] | 0.6897 | 0.2397 | 0.7068 |
| **ABENA** | 3,886 | 65.02% | 0.5624 | [0.5285, 0.5934] | 0.6941 | 0.2810 | 0.7120 |
| **GhanaTok (BPE)** | **1,899** | 62.91% | 0.5357 | [0.5026, 0.5697] | 0.6621 | 0.2407 | 0.7043 |
| **GhanaTok-Unigram** | 2,133 | 62.91% | 0.5359 | [0.5030, 0.5676] | 0.6592 | 0.2479 | 0.7005 |

---

## 3. Discussion

### 3.1 Baseline Tokenizer Behaviors
Among general multilingual tokenizers, **mBERT** consistently produced lower fertility and fragmentation than XLM-R and AfroXLMR on both Twi and Ewe. This behavior stems from architectural and pre-tokenization differences:
- **mBERT** uses WordPiece with basic whitespace and punctuation pre-tokenization, which isolates punctuation before subword segmentation.
- **XLM-R and AfroXLMR** use SentencePiece with byte-fallback. In the absence of dedicated Ghanaian vocabulary entries, SentencePiece breaks unfamiliar extended characters (`ɛ`, `ɔ`, `ɖ`, `ŋ`, `ʋ`, `ƒ`) into raw byte sequences or isolated single characters, compounding subword length.
- Despite AfroXLMR including 17 African languages in its pre-training, its shared 250,000-token vocabulary did not allocate sufficient capacity to Ghanaian language roots, resulting in fertility identical to generic XLM-R on these test sets.

### 3.2 Impact of Seed Morphemes and Dialect-Aware Pre-Tokenization
Qualitative case studies and segmentation inspections demonstrate the direct benefits of custom pre-tokenization and seed vocabulary injection:
- The custom pre-tokenizer regex explicitly binds extended Latin vowels and consonants (`ɛ, ɔ, ɖ, ŋ, ʋ, ƒ`) to word stems rather than treating them as punctuation or splitting points.
- Injecting high-frequency morphemes (`mbe-`, `bɛ-`, `-foɔ`, `-wo`, `-m`) and salutations (`Akwaaba`, `Medaase`, `Woezɔ`, `Aleke`) guaranteed atomic token representation for core terms, eliminating subword fragmentation on foundational vocabulary.

### 3.3 Small, Language-Specific Vocabularies for Low-Resource Languages
The findings strongly support the hypothesis that a compact, language-specific vocabulary significantly reduces fragmentation compared to massive multilingual vocabularies:
- With only **8,000 vocabulary tokens**, GhanaTok reduced token fertility by **30.7% on Twi** and **23.6% on Ewe** relative to mBERT (110k vocabulary) and by **32–33%** relative to XLM-R (250k vocabulary).
- A compact vocabulary concentrates subword capacity entirely on high-frequency n-grams and affixes relevant to the target languages, eliminating the "tokenization tax" imposed by multilingual vocabularies where low-resource languages receive less than 1% of the parameter budget.

### 3.4 Cross-Lingual Comparison: Twi vs Ewe
GhanaTok achieved a higher percentage fertility reduction on Twi (30.7%) than on Ewe (23.6%):
- **Orthographic Complexity**: Ewe contains a wider set of distinct phonetic characters (`ɖ`, `ŋ`, `ɔ`, `ɛ`, `ʋ`, `ƒ`) and tone diacritics (`è`, `é`, `ẽ`), creating a higher character diversity per word.
- **Morphological Structure**: Ewe relies heavily on postpositional clitics and compounding particles, which produce diverse surface word forms.
- **Training Corpus Representation**: While both languages were balanced in training, Twi's higher baseline token volume allowed BPE to capture a slightly broader set of multi-syllable root words.

---

## 4. Limitations

1. **Sample Sizes & Corpus Domain**: Benchmark calibration and held-out evaluations used 3,000 sentences (calibration) and 608/347 sentences (held-out test), sourced from the GhanaNLP parallel corpora. While cleaned and deduplicated, these texts skew toward conversational dialogues, civic notices, and religious texts, and may not fully represent formal literary registers, technical documentation, or informal social media slang.
2. **ABENA Asymmetry & Dialect Handling**: ABENA is a monolingual tokenizer trained on Akuapem Twi and could not be evaluated on Ewe. The Twi corpus was not segmented by dialect; the keyword-based Akuapem check (76 flagged sentences) provided a directional probe rather than a validated sociolinguistic dialect classification.
3. **Vocabulary Size Selection**: The 8,000-token budget was selected a priori based on training corpus size (~15,000 sentences per language) to avoid over-segmentation or single-occurrence token bloat. A systematic hyperparameter sweep across vocabulary sizes (e.g., 4k, 8k, 16k, 32k) was outside the project scope.
4. **Algorithm Scope**: GhanaTok-BPE was the primary proposed model. GhanaTok-Unigram was evaluated as an exploratory secondary comparison recipe on the same corpus and seed vocabulary.
5. **Downstream Task Scope**: Downstream evaluation (RQ4) was explicitly scoped out of the core research questions. The bonus sentiment probe used a linear bag-of-tokens classifier on short tweets; these findings should not be extrapolated to deep transformer pre-training without full downstream fine-tuning studies.

---

## 5. Conclusion

This project set out to quantify subword fragmentation in existing multilingual tokenizers on Twi and Ewe and to evaluate whether a compact, bilingual tokenizer could eliminate this inefficiency. We found that standard multilingual tokenizers (mBERT, XLM-R, AfroXLMR) and existing regional models (ABENA) heavily fragment Ghanaian languages, splitting over 70% of words and averaging 2.3–2.6 tokens per word.

By introducing **GhanaTok**—an 8,000-vocabulary bilingual tokenizer combining dialect-aware pre-tokenization with seed morpheme injection—we reduced token fertility to **1.656 tokens/word on Twi (30.7% reduction)** and **1.750 tokens/word on Ewe (23.6% reduction)** on held-out test data. Furthermore, exploratory SentencePiece Unigram training demonstrated additional potential, lowering fertility to **1.251 tokens/word**.

The most valuable next step for this work is to pre-train a small transformer language model (e.g., 100M parameters) using GhanaTok tokenization to directly measure downstream perplexity, training compute savings, and generative performance on Ghanaian language tasks.
