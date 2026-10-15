# Model Card: GhanaTok (Byte-Level BPE & SentencePiece Unigram)

## 1. Model Details

- **Model Name:** GhanaTok
- **Variants:**
  - `GhanaTok` (Byte-Level BPE, 8,000 subwords) — Primary architecture
  - `GhanaTok-Unigram` (SentencePiece Unigram, 8,000 subwords) — Exploratory probabilistic variant
  - Vocabulary scaling sweep checkpoints: 4,000, 8,000, 16,000, and 32,000 tokens for both architectures
- **Developer:** Jennifer Banibensu (DCIT 316 Individual Research Project)
- **Model Type:** Subword Tokenizer
- **Target Languages:** Twi / Akan (`twi`, Niger-Congo, Kwa branch) and Ewe / Gbe (`ewe`, Niger-Congo, Gbe branch)
- **Frameworks:** Hugging Face `tokenizers` (0.19.0+), Google `sentencepiece` (0.2.0+), Hugging Face `transformers` (4.44.0+)
- **License:** CC BY-NC-SA 4.0 (derived from GhanaNLP Parallel Corpora training text)
- **Repository:** `exornamb/GhanaToken`
- **Model Artifacts Location:**
  - Primary BPE: `models/ghanatok/ghanatok_tokenizer.json`
  - Primary Unigram: `models/ghanatok_unigram/ghanatok_unigram.model`, `models/ghanatok_unigram/ghanatok_unigram.vocab`
  - Sweep Models: `models/ghanatok_{bpe,unigram}_{4000,8000,16000,32000}/`

---

## 2. Intended Use & Scope

### 2.1 Intended Use Cases
- Subword tokenization and pre-tokenization for language model pre-training, fine-tuning, and embedding generation in Twi (Akuapem and Asante dialects) and Ewe.
- High-efficiency text preprocessing for classification, machine translation, and speech transcription pipelines.
- Research benchmark for measuring cross-lingual token fertility, context window efficiency, and API cost parity in low-resource African languages.

### 2.2 Out-of-Scope & Misuse
- **Direct Language Generation:** GhanaTok is a tokenizer, not an autoregressive language model or text generator. It produces integer token IDs, not predictions.
- **Unadapted Third-Party Languages:** Applying GhanaTok to languages outside the Akan and Gbe families (e.g., Hausa, Swahili, English) will yield fallback byte segmentation and is not supported.
- **Dialect Erasure:** GhanaTok does not enforce standardized spelling; dialectal orthographic variants (e.g., Akuapem vs. Asante spellings) are both accommodated without bias.

---

## 3. Linguistic Architecture & Tokenizer Design

Standard multilingual tokenizers (e.g., mBERT, XLM-R, AfroXLMR) inflict an exorbitant "token tax" on Ghanaian languages due to character-level splitting and byte fallback. GhanaTok overcomes this via two architectural innovations:

### 3.1 Dialect-Aware Pre-Tokenization Pattern
Standard whitespace or ASCII-regex pre-tokenizers split on non-ASCII characters or detach apostrophes unpredictably. GhanaTok incorporates a specialized regex:
```regex
's|'[tmdllve]|\s?[\p{L}\p{M}ɛɔɖŋʋƒƐƆƉŊƲƑ]+|[^\s\p{L}\p{M}]+
```
- **Extended Latin Alphabet Protection:** Explicitly includes open vowels (`ɛ`, `ɔ`, `Ɛ`, `Ɔ`) used in Akan orthography, and voiced retroflex/implosive consonants and bilabial fricatives (`ɖ`, `ŋ`, `ʋ`, `ƒ`, `Ɖ`, `Ŋ`, `Ʋ`, `Ƒ`) used in Ewe orthography.
- **Byte-Level Encoding:** Backed by byte-level fallback (`ByteLevel(add_prefix_space=False, use_regex=False)`) to guarantee zero out-of-vocabulary (`<unk>`) exceptions.

### 3.2 Seed Morpheme Injection
Frequent grammatical affixes, particles, and cultural greetings were seeded into the initial vocabulary to prevent frequency-based exclusion:
- **Twi Affixes:** `"mbe-"`, `"n-"`, `"bɛ-"`, `"-foɔ"`, `"-nom"`, `"-yeɛ"`
- **Ewe Particles & Affixes:** `"-wo"`, `"-m"`, `"mega-"`, `"ɖe-"`
- **High-Frequency Roots & Greetings:** `"Akwaaba"`, `"akwaaba"`, `"Medaase"`, `"medaase"`, `"Woezɔ"`, `"woezɔ"`, `"Aleke"`, `"aleke"`, `"Akpe"`, `"akpe"`

---

## 4. Training Data & Preprocessing

- **Corpus Source:** GhanaNLP Parallel Corpora (Adu Gyamfi et al., 2026), Twi and Ewe subsets.
- **Training Splits:** Strictly drawn from combined training splits:
  - Twi: 4,857 sentences (`data/processed/twi/train.txt`)
  - Ewe: 2,764 sentences (`data/processed/ewe/train.txt`)
  - Total Training Corpus: 7,621 sentences, 721 KB (`data/processed/ghanatok_train_corpus.txt`)
- **Held-Out Test Sets:** 608 Twi sentences and 347 Ewe sentences were sealed and completely withheld from training and vocabulary induction.
- **Preprocessing:** Unicode NFC normalisation, whitespace collapsing, duplicate removal, minimum 2-word filter.

---

## 5. Quantitative Evaluation & Benchmark Results

### 5.1 Held-Out Test Evaluation (Sealed Test Sets)

| Language | Tokenizer | Mean Fertility (Tokens/Word) | Density (Tokens/Char) | Fragmentation Rate (% Split) | Reduction vs mBERT | 95% Bootstrap CI | Wilcoxon $p$-value (Holm-corrected) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ewe** | AfroXLMR / XLM-R | 2.608 | 0.505 | 70.99% | — | — | — |
| **Ewe** | mBERT | 2.291 | 0.445 | 63.87% | Baseline (0.0%) | — | — |
| **Ewe** | **GhanaTok (BPE)** | **1.750** | **0.341** | **51.25%** | **-23.60%** | **[22.08%, 24.95%]** | **$p = 2.48 \times 10^{-52}$** |
| **Ewe** | *GhanaTok-Unigram* | *1.349* | *0.263* | *22.83%* | *-41.11%* | *[39.67%, 42.39%]* | *$p = 9.84 \times 10^{-57}$* |
| **Twi** | AfroXLMR / XLM-R | 2.444 | 0.482 | 70.26% | — | — | — |
| **Twi** | ABENA (Twi only) | 2.419 | 0.477 | 72.12% | — | — | — |
| **Twi** | mBERT | 2.389 | 0.471 | 70.47% | Baseline (0.0%) | — | — |
| **Twi** | **GhanaTok (BPE)** | **1.656** | **0.327** | **48.82%** | **-30.67%** (*-31.54% vs ABENA*) | **[29.85%, 31.44%]** | **$p = 7.45 \times 10^{-99}$** |
| **Twi** | *GhanaTok-Unigram* | *1.251* | *0.248* | *17.58%* | *-47.63%* | *[46.81%, 48.43%]* | *$p = 2.25 \times 10^{-100}$* |

### 5.2 Latency & Throughput (Intel Core CPU, 5 runs with warmup)

| Tokenizer | Language | Mean Sec / Run | Throughput (Sentences/sec) | Throughput (Chars/sec) |
| :--- | :---: | :---: | :---: | :---: |
| mBERT | Twi | 0.3131 s | 1,942 sent/s | 147,329 char/s |
| XLM-R | Twi | 0.3055 s | 1,990 sent/s | 150,984 char/s |
| ABENA | Twi | 0.1972 s | 3,083 sent/s | 233,864 char/s |
| **GhanaTok (BPE)** | Twi | 0.2916 s | 2,085 sent/s | 158,201 char/s |
| **GhanaTok-Unigram** | Twi | **0.0231 s** | **26,363 sent/s** | **2,000,026 char/s** |
| mBERT | Ewe | 0.1270 s | 2,732 sent/s | 294,384 char/s |
| XLM-R | Ewe | 0.1319 s | 2,632 sent/s | 283,606 char/s |
| **GhanaTok (BPE)** | Ewe | 0.1037 s | 3,345 sent/s | 360,468 char/s |
| **GhanaTok-Unigram** | Ewe | **0.0239 s** | **14,536 sent/s** | **1,566,548 char/s** |

### 5.3 Downstream Sentiment Probe (AfriSenti Twi)
Using a bag-of-tokens Logistic Regression classifier on 3,481 training tweets and 20% stratified holdout:
- **GhanaTok (BPE):** Accuracy: **0.5968**, Macro F1: **0.5110**, Features: **1,773**
- **mBERT:** Accuracy: 0.5911, Macro F1: 0.4921, Features: 3,386
- **XLM-R / AfroXLMR:** Accuracy: 0.5997, Macro F1: 0.4889, Features: 3,907
- **ABENA:** Accuracy: 0.5940, Macro F1: 0.4945, Features: 3,381
- **Finding:** GhanaTok achieves equivalent downstream predictive capability using **over 47% fewer unique features**, demonstrating representational compactness without performance degradation.

---

## 6. Caveats & Limitations

1. **Subword Quality vs. Downstream Accuracy:** A lower fertility score does not automatically guarantee higher accuracy in complex generative LLMs; downstream gains must be validated on large-scale model pre-training.
2. **Domain Representation:** Training text originates primarily from public religious translations, civic administration notices, and conversational dialogues; performance on modern slang, colloquial social media text, or technical legal jargon may require domain expansion.
3. **Dialect Balance:** While seed morphemes represent both Akuapem and Asante variants, Fante (another major Akan dialect) was not directly included in the seed list.
4. **Native Speaker Verification:** Computational subword boundary segmentations have not undergone qualitative validation by native Ghanaian linguists.

---

## 7. Ethical Considerations

- **No Personal Identifiable Information:** The training and evaluation sets contain no private personal communications.
- **Fair Linguistic Access:** By decreasing fertility by up to 47.6%, GhanaTok directly mitigates economic discrimination against Ghanaian language users of token-metered APIs.
