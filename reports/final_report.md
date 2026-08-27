# GhanaToken: Custom Tokenizer Optimization for Ghanaian Languages (Twi & Ewe)

## 1. Baseline Tokenizer Comparison (Calibration on Train/Val Splits)

Across **3,000 Twi sentences** and **3,000 Ewe sentences** drawn from the cleaned training and validation splits:
- On **Twi**, **mBERT** produced the lowest average fertility (**2.371 tokens per word**), while **XLM-R** and **AfroXLMR** produced higher average fertility (**2.438 tokens per word**). The Ghana-specific **ABENA** baseline achieved **2.402 tokens per word** (71.71% fragmentation rate).
- On **Ewe**, **mBERT** achieved **2.303 tokens per word**, whereas **XLM-R** and **AfroXLMR** showed severe fragmentation of **2.625 tokens per word** (71.37% words split).
- **ABENA** is evaluated strictly on Twi (3,000 sentences), reflecting its monolingual design; it does not appear in the Ewe evaluation.

---

## 2. GhanaTok vs Baseline Tokenizers (Held-Out Test Set)

On a completely held-out test set of **608 Twi sentences** and **347 Ewe sentences** (which was strictly sealed and never seen during tokenizer training or vocabulary construction):

- **GhanaTok (Byte-Level BPE)** (an 8,000-vocabulary byte-level BPE tokenizer trained on combined Twi and Ewe data with a dialect-aware pre-tokenizer and seed morphemes) achieved a mean fertility of **1.656 tokens per word** on Twi and **1.750 tokens per word** on Ewe, compared with **2.389** (Twi) and **2.291** (Ewe) for the strongest general multilingual baseline, **mBERT**.
- This represents a **30.7% reduction in token fertility on Twi** and a **23.6% reduction in token fertility on Ewe** relative to the strongest general baseline (and over a **32% reduction** relative to XLM-R / AfroXLMR).
- On Twi only, GhanaTok was additionally compared against **ABENA**, an existing Twi-specific tokenizer built by the GhanaNLP team. GhanaTok achieved a mean fertility of **1.656** against ABENA's **2.419**, representing a **31.5% reduction in token fertility**. ABENA was not evaluated on Ewe, since it was trained only on Twi.
- **GhanaTok-Unigram (Bonus Recipe)**: Evaluated using SentencePiece Unigram probabilistic pruning with the same seed morphemes, achieving **1.251 tokens per word** on Twi (17.58% words split) and **1.349 tokens per word** on Ewe (22.83% words split).

### Held-Out Evaluation Summary Table

| Language | Tokenizer | Mean Fertility (Tokens / Word) | Density (Tokens / Char) | Fragmentation Rate (% Words Split) | Evaluated Test Sentences |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Ewe** | AfroXLMR | 2.608 | 0.505 | 70.99% | 347 |
| **Ewe** | XLM-R | 2.608 | 0.505 | 70.99% | 347 |
| **Ewe** | mBERT | 2.291 | 0.445 | 63.87% | 347 |
| **Ewe** | **GhanaTok (BPE)** | **1.750** | **0.341** | **51.25%** | **347** |
| **Ewe** | *GhanaTok-Unigram (Bonus)* | *1.349* | *0.263* | *22.83%* | *347* |
| **Twi** | ABENA | 2.419 | 0.477 | 72.12% | 608 |
| **Twi** | AfroXLMR | 2.444 | 0.482 | 70.26% | 608 |
| **Twi** | XLM-R | 2.444 | 0.482 | 70.26% | 608 |
| **Twi** | mBERT | 2.389 | 0.471 | 70.47% | 608 |
| **Twi** | **GhanaTok (BPE)** | **1.656** | **0.327** | **48.82%** | **608** |
| **Twi** | *GhanaTok-Unigram (Bonus)* | *1.251* | *0.248* | *17.58%* | *608* |

*Note: ABENA is evaluated exclusively on Twi because it was built specifically for Akuapem Twi.*

---

## 3. Qualitative Error Analysis & Word-Level Case Studies

Inspecting word-level tokenization behaviors reveals why GhanaTok outperforms general multilingual baselines and existing regional tokenizers:

### Case Study 1: Twi Subword Preservation (GhanaTok vs XLM-R)
- **`Esiane`** (*because / since*):
  - **GhanaTok**: `['Esiane']` (1 token — preserved as single whole word)
  - **XLM-R**: `['▁Esi', 'ane']` (2 tokens — split into arbitrary subword pieces)
- **`Mprempren`** (*now / currently*):
  - **GhanaTok**: `['Mprempren']` (1 token — whole word)
  - **XLM-R**: `['▁M', 'prem', 'pren']` (3 tokens — excessive fragmentation)
- **`Ahwɛyie`** (*carefulness / vigilance*):
  - **GhanaTok**: `['A', 'hwɛ', 'yie']` (3 tokens — clean morphological segments)
  - **XLM-R**: `['▁Ah', 'w', 'ɛ', 'y', 'ie']` (5 tokens — character-level breakdown on open vowel `ɛ`)

### Case Study 2: Head-to-Head on Twi (GhanaTok vs ABENA)
- **`Ghana`**:
  - **GhanaTok**: `['Ghana']` (1 token — single atomic token)
  - **ABENA**: `['gh', '##ana']` (2 tokens — split despite being a core geographic entity)
- **`Esiane`**:
  - **GhanaTok**: `['Esiane']` (1 token)
  - **ABENA**: `['esi', '##ane']` (2 tokens)

### Case Study 3: Ewe Special Orthography (GhanaTok vs XLM-R)
- **`Aƒetɔ`** (*Lord / Master*):
  - **GhanaTok**: `['Aƒetɔ']` (1 token — whole word preserved despite rare Latin-extended `ƒ` and `ɔ`)
  - **XLM-R**: `['▁A', 'ƒ', 'et', 'ɔ']` (4 tokens — single characters isolated)
- **`Dɔwɔnyawo`** (*work-related matters / deeds*):
  - **GhanaTok**: `['Dɔ', 'wɔnyawo']` (2 tokens — sensible root + compound affix)
  - **XLM-R**: `['▁D', 'ɔ', 'w', 'ɔ', 'nya', 'wo']` (6 tokens — severe character scattering)

---

## 4. Key Takeaways & Significance
1. **Elimination of the African Language Tokenization Tax**: Custom bilingual vocabulary allocation reduces subword fragmentation by 30–32%, directly translating to reduced compute cost and longer effective context lengths for downstream LLM training.
2. **Robustness of Custom Pre-Tokenization**: Protecting extended Latin characters (`ɛ`, `ɔ`, `ɖ`, `ŋ`, `ʋ`, `ƒ`) prevented the character isolation pathology observed across general multilingual baselines.
3. **Bilingual Utility**: Training a shared 8,000-token vocabulary across both Twi and Ewe achieved strong cross-lingual efficiency without requiring separate monolingual tokenizers.
