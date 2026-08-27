# Data Card: GhanaToken

**Source:** GhanaNLP Parallel Corpora (2026), Twi and Ewe portions only.

**Size after cleaning:**
- **Twi (`twi`):** 6,072 cleaned sentences (Train: 4,857, Val: 607, Test: 608; initial raw: 6,090 sentences).
- **Ewe (`ewe`):** 3,456 cleaned sentences (Train: 2,764, Val: 345, Test: 347; initial raw: 3,488 sentences).

**Sample used for benchmark:** 3,000 sentences per language, drawn from the combined train and validation splits (test set strictly reserved for later evaluation).

**Preprocessing applied:** Unicode NFC normalisation, whitespace cleanup, duplicate removal, minimum 2 words per sentence filter.

**Known limitations:**
- Domain skew towards conversational dialogues, religious texts (Bible translations), and civic administration notices.
- Twi data contains mixed orthographic conventions across Akuapem and Asante dialects (e.g., variation in vowel harmony markings and dialectal spelling).
- Ewe data exhibits unique orthographic characters (e.g., `ɖ`, `ŋ`, `ɔ`, `ɛ`, `ʋ`, `ƒ`, and tone accents like `è`, `é`, `ẽ`) which suffer significant character-level fragmentation in standard multilingual tokenizers.

**Tokenizer coverage note:** ABENA (`Ghana-NLP/abena-base-akuapem-twi-cased`) is included as an additional comparison point but was trained only on Twi (Akuapem dialect). It is evaluated on the Twi dataset only and does not appear anywhere in the Ewe results, since it was never trained on Ewe.

**Akuapem check:** 76 of 608 Twi held-out sentences (12.5%) matched a small set of Akuapem spelling markers. ABENA's mean fertility on this flagged subset was 2.377, versus 2.425 on the rest. This is a lightweight, keyword-based check, not a validated dialect classification, and is reported as a directional signal only.

**Licence:** CC BY-NC-SA 4.0 (GhanaNLP), used here for non-commercial academic research only.
