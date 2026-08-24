# GhanaToken: Custom Tokenizer Optimization for Ghanaian Languages (Twi & Ewe)

## Baseline Tokenizer Comparison

Across **3,000 Twi sentences** and **3,000 Ewe sentences** drawn from the cleaned training and validation splits, **mBERT** produced the lowest average fertility on both languages (**2.371 tokens per word** on Twi and **2.303 tokens per word** on Ewe), while **XLM-R** and **AfroXLMR** produced the highest average fertility (**2.438 tokens per word** on Twi and **2.625 tokens per word** on Ewe). 

This empirical pattern aligns with prior African-language tokenizer research (such as Petrov et al., 2023; Ahia et al., 2023), where general-purpose massively multilingual tokenizers systematically over-fragment low-resource African languages due to limited vocabulary allocation and inadequate representation of open vowels and specialized orthographic characters (`ɛ`, `ɔ`, `ɖ`, `ŋ`, `ʋ`, `ƒ`).

The Ghana-specific **ABENA** baseline (trained exclusively on Akuapem Twi) achieved an average fertility of **2.402 tokens per word** on Twi with a subword fragmentation rate of **71.71%**. ABENA is evaluated strictly on Twi (3,000 sentences) and does not appear in the Ewe evaluation as it was never trained on Ewe.

### Baseline Summary Results

| Language | Tokenizer | Mean Fertility (Tokens / Word) | Subword Fragmentation Rate (% Words Split) | Density (Tokens / Char) | Sampled Sentences |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Ewe** | AfroXLMR | 2.625 | 71.37% | 0.506 | 3,000 |
| **Ewe** | XLM-R | 2.625 | 71.37% | 0.506 | 3,000 |
| **Ewe** | mBERT | 2.303 | 64.66% | 0.445 | 3,000 |
| **Twi** | ABENA | 2.402 | 71.71% | 0.475 | 3,000 |
| **Twi** | AfroXLMR | 2.438 | 70.13% | 0.483 | 3,000 |
| **Twi** | XLM-R | 2.438 | 70.13% | 0.483 | 3,000 |
| **Twi** | mBERT | 2.371 | 69.96% | 0.469 | 3,000 |

*Note: Ewe results contain 3 models and Twi contains 4 models because ABENA is a Twi-only model.*
