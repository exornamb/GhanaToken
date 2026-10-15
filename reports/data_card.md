# Data Card: GhanaToken Corpora & Benchmark Data

Following the Datasheets for Datasets standard (Gebru et al., 2021) and Hugging Face Data Card conventions.

---

## 1. Dataset Summary & Motivation

- **Dataset Name:** GhanaToken Parallel Corpora & Downstream Evaluation Splits
- **Languages:**
  - **Twi (Akan)** (`twi`): Major Kwa language of Ghana, spoken by over 9 million native and L2 speakers. Includes orthographic variations from Akuapem and Asante dialects.
  - **Ewe (Gbe)** (`ewe`): Major Gbe language spoken in southeastern Ghana and southern Togo by over 7 million people, utilizing extended Latin characters (`ɖ`, `ŋ`, `ɔ`, `ɛ`, `ʋ`, `ƒ`) and tone diacritics.
- **Primary Purpose:** Benchmarking subword tokenization fragmentation, token fertility, context-window saturation, and API cost multipliers across state-of-the-art multilingual and custom domain-specific tokenizers.
- **Curator & Maintainer:** Jennifer Banibensu (DCIT 316 Semester Research Project).

---

## 2. Dataset Composition & Split Statistics

All data splits are saved as plain `.txt` files (one sentence per line, UTF-8 encoded) in `data/processed/`:

### 2.1 Sentence Splits

| Dataset Partition | File Path | Sentence Count | Total Whitespace Words | Total Characters |
| :--- | :--- | :---: | :---: | :---: |
| **Twi Training** | `data/processed/twi/train.txt` | 4,857 | ~78,400 | ~410,000 |
| **Twi Validation** | `data/processed/twi/val.txt` | 607 | ~9,800 | ~51,200 |
| **Twi Sealed Test** | `data/processed/twi/test.txt` | 608 | 9,842 | 46,125 |
| **Twi Total** | — | **6,072** | **~98,042** | **~507,325** |
| **Ewe Training** | `data/processed/ewe/train.txt` | 2,764 | ~45,200 | ~248,000 |
| **Ewe Validation** | `data/processed/ewe/val.txt` | 345 | ~5,600 | ~30,900 |
| **Ewe Sealed Test** | `data/processed/ewe/test.txt` | 347 | 5,618 | 37,395 |
| **Ewe Total** | — | **3,456** | **~56,418** | **~316,295** |
| **Combined Train Corpus** | `data/processed/ghanatok_train_corpus.txt` | **7,621** | **~123,600** | **~658,000** |

### 2.2 Downstream Evaluation Split (AfriSenti Twi)
- **Source:** AfriSenti Twitter Sentiment Corpus (Muhammad et al., 2023, `masakhane/afrisenti`)
- **Composition:** 4,818 total tweets
  - Official Train: 3,481 tweets
  - Official Validation: 388 tweets
  - Official Test: 949 tweets
- **Class Labels:** 3-class sentiment (`positive`: 2,277, `negative`: 1,815, `neutral`: 726).
- **Role in Research:** Secondary sanity check to verify whether compression preserves classification representations.

---

## 3. Data Collection, Preprocessing & Cleaning Pipeline

### 3.1 Raw Data Sources
- **GhanaNLP Parallel Corpora (2026):** Publicly accessible parallel sentences between English and Ghanaian languages (Adu Gyamfi et al., 2026).
- Raw sentences were downloaded into `data/raw/twi/raw_sentences.csv` (initial count: 6,090 rows) and `data/raw/ewe/raw_sentences.csv` (initial count: 3,488 rows).

### 3.2 Preprocessing Transformation Steps (`src/preprocessing.py`)
1. **Unicode NFC Normalisation:** Decomposed characters (e.g., base vowel + combining diacritic accents such as `e` + `\u0300`) are normalized into single precomposed code points (`è`), preventing artificial multi-byte splitting.
2. **Whitespace Sanitization:** Trimming leading/trailing whitespace and collapsing multiple spaces/newlines.
3. **Deduplication:** Duplicate sentence strings within each language partition are removed.
4. **Length Filtering:** Sentences shorter than 2 whitespace-separated words or with zero characters are discarded.
5. **Deterministic Stratified Splitting:** 80% train, 10% validation, 10% test split created with a fixed random seed (`seed=42`).

---

## 4. Linguistic Characteristics & Dialect Nuances

### 4.1 Akan / Twi Dialects
- **Orthographic Mixing:** The Twi sentences exhibit spelling variations between Akuapem Twi and Asante Twi (e.g., differences in vowel harmony suffixes, `-yeɛ` vs. `-yɛ`, `sɛnea` vs. `sɛdeɛ`).
- **Akuapem Marker Analysis:** A keyword audit identified 76 of 608 test sentences (12.5%) containing distinct Akuapem markers. Baseline ABENA (trained specifically on Akuapem) exhibited 2.377 tokens/word on this subset vs 2.425 on the remainder, verifying that regional baseline performance is sensitive to dialect variations.

### 4.2 Ewe Orthography & Character Frequencies
- Ewe features unique IPA-derived orthographic symbols:
  - `ɖ` (voiced retroflex stop)
  - `ŋ` (velar nasal)
  - `ɔ` (open-o)
  - `ɛ` (open-e)
  - `ʋ` (voiced labiodental approximant)
  - `ƒ` (voiceless bilabial fricative)
- In standard multilingual tokenizers (mBERT, XLM-R), these characters are missing from whole-word subword units, forcing fallback to individual byte sequences (e.g., `<0x..>` or individual ASCII byte pairs).

---

## 5. Licensing, Safe Data Access & Restrictions

### 5.1 Licenses
- **GhanaNLP Parallel Corpora:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (**CC BY-NC-SA 4.0**).
- **AfriSenti Dataset:** Creative Commons Attribution 4.0 International (**CC BY 4.0**).

### 5.2 Safe Data Access Protocol
- **Public Availability:** All data used in this project is public and was developed explicitly for academic NLP research.
- **Academic Research Scope:** In compliance with CC BY-NC-SA 4.0, all data, preprocessed splits, and trained tokenizers in this repository are restricted to non-commercial academic research and educational evaluation.
- **Reproducibility Guarantee:** Preprocessed splits are directly tracked in `data/processed/`, enabling complete, deterministic replication without requiring external download accounts or proprietary credentials.
- **Zero-Credential Security:** No private API keys, tokens, or credentials are required to run any script or notebook in this repository.

### 5.3 Privacy & Human Rights Considerations
- The sentences represent public translations of civic notices, biblical texts, and parallel dialogues.
- No personal identifiable information (PII), private correspondence, or confidential records are present in any dataset.
