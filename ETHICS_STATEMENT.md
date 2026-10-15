# Ethics Statement: GhanaToken Research Project

- **Author:** Jennifer Banibensu
- **Project:** DCIT 316 Individual Research Project — Tokenizer Optimization for Ghanaian Languages (Twi & Ewe)
- **Institution:** Department of Computer Science, University of Ghana

---

## 1. Purpose and Intended Beneficiaries

Subword tokenization in modern large language models (LLMs) imposes an unacknowledged economic and technical penalty on low-resource and African languages—often referred to as the "token tax" (Petrov et al., 2023; Ahia et al., 2023). Because multilingual models split African words into multiple fragmented characters or raw byte sequences, speakers and developers working in Ghanaian languages face:
1. **Inflated API Costs:** Paying 1.5x to 2x more per sentence compared to English for commercial inference.
2. **Artificial Context Saturation:** Rapidly filling LLM context windows with sub-token fragments, limiting document length and retrieval capacity.
3. **Increased Training and Fine-Tuning Compute:** Requiring longer sequence lengths and more GPU hours to achieve parity.

**Intended Beneficiaries:** This project directly benefits Ghanaian and African language developers, academic researchers, and digital language communities by providing **GhanaTok**—an open, freely accessible, compact bilingual tokenizer engineered specifically to eliminate this fragmentation.

---

## 2. Data Ethics, Provenance & Safe Data Access

| Dataset | Source | Primary License | Permitted Use Here | Safe Access & Restrictions |
| :--- | :--- | :--- | :--- | :--- |
| **GhanaNLP Parallel Corpora** | Ghana-NLP (Adu Gyamfi et al., 2026) | Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (**CC BY-NC-SA 4.0**) | Preprocessing, tokenizer training, validation, and sealed held-out benchmarking. | Strictly academic non-commercial research; no private redistribution; data hosted openly in repo splits. |
| **AfriSenti Twitter Corpus** | Masakhane / Muhammad et al. (2023) | Creative Commons Attribution 4.0 (**CC BY 4.0**) | Downstream linear sentiment probe. | Academic research only; public released dataset; no attempt to de-anonymize or re-identify authors. |

### Safe Data Access & Zero-Credential Policy:
- Both datasets were curated publicly by respected African NLP organizations for open academic evaluation.
- No new text was scraped, web-crawled, or harvested from private groups or non-public platforms.
- The repository follows a **strict zero-credential security posture**: no private API keys, user tokens, or account passwords were used or committed.
- Researchers and course instructors can reproduce all benchmarks directly from the preprocessed text splits without logging in to commercial platforms.

---

## 3. Human Subjects & Privacy Protection

- **Public Text Only:** All sentences are from publicly released parallel translations (civic notices, news translations, biblical passages) or published research datasets.
- **No Personal Identifiable Information (PII):** No individual personal data, contact details, private communications, or confidential records are present in the corpora.
- **No User Profiling or De-anonymization:** In the AfriSenti sentiment probe, tweets were processed strictly as de-contextualized text strings; no attempts were made to identify tweet authors, trace user handles, link social graphs, or retrieve user profiles.

---

## 4. Linguistic Equity & Dialect Representation

- **Dialect Sensitivity (Akuapem vs. Asante):** Twi (Akan) comprises multiple recognized dialects with differing orthographic rules. The training corpus contains mixed Akuapem and Asante spellings. Rather than artificially filtering or imposing a single dialect norm, GhanaTok's pre-tokenizer is designed to accept phonemic characters and vowel harmony variants from both dialects without bias.
- **Ewe Extended Alphabet Defense:** Ewe utilizes Latin characters with distinct phonetic values (`ɖ`, `ŋ`, `ɔ`, `ɛ`, `ʋ`, `ƒ`) and tone diacritics. In multilingual models, these letters are routinely fragmented into byte-level pieces. GhanaTok gives explicit vocabulary representation to these letters, recognizing them as first-class linguistic entities rather than anomalies.
- **Dialect Disclaimer:** The directional keyword check (identifying 76 of 608 Twi sentences with Akuapem markers) is an exploratory heuristic, not a validated sociolinguistic classifier. No claims are made that these corpora capture the full richness of all Ghanaian speech communities or informal spoken dialects.

---

## 5. Potential Harms and Risk Mitigation

| Identified Risk | Severity | Implemented Mitigation Strategy |
| :--- | :---: | :--- |
| **Misinterpreting Compression as General Model Quality** | Medium | The report and Model Card explicitly clarify that subword fertility measures tokenization efficiency, not language understanding or generative quality. |
| **Commercial Exploitation of Protected Data** | Low | The CC BY-NC-SA 4.0 license is prominent across the repo; commercial exploitation of GhanaTok without separate data licensing is prohibited. |
| **Over-claiming Cross-Domain Generalization** | Medium | Explicitly disclosed that training data draws predominantly from translated dialogue, religious texts, and civic notices; domain shift on slang or informal social media is stated as a limitation. |
| **Algorithmic Bias from Corpus Skew** | Low | GhanaTok does not make semantic decisions or text generations; its role is strictly token segmenting. |

---

## 6. Scientific Integrity & Transparent Reporting

- **Sealed Test Set Discipline:** The 608 Twi and 347 Ewe test sentences were isolated on Day 2 and remained strictly sealed until final evaluation; they were never used for vocabulary induction or frequency counts.
- **Reporting Negative & Neutral Findings:** In the sentiment probe, where GhanaTok achieved equivalent Macro F1 rather than superior accuracy, this was reported directly without cherry-picking or declaring an unearned victory.
- **Non-Parametric Statistical Defense:** Because sentence-level fertility distributions violate normality assumptions, paired non-parametric Wilcoxon signed-rank tests and 1,000-sample bootstrap confidence intervals were used, with Holm-Bonferroni correction applied across all primary comparisons.

---

## 7. Computational Footprint & Green NLP

In contrast to energy-intensive large-scale foundation model pre-training, GhanaTok was intentionally architected for extreme computational efficiency:
- **Total Training Time:** Under 2 minutes on a standard consumer laptop CPU (Intel Core i5/i7).
- **Carbon Footprint:** Less than 0.001 kg $\text{CO}_2\text{e}$, utilizing zero GPU hours.
- **Deployment Efficiency:** With an 8,000-token vocabulary, embedding layers consume less than 1/15th the memory of standard multilingual models (XLM-R uses 250,000 subwords), making GhanaTok ideal for deployment on edge devices and low-cost consumer hardware across Africa.
