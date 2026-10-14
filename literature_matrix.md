# Literature Matrix: Tokenization Efficiency in Ghanaian Low-Resource Languages

Project: DCIT 316 individual project (Twi and Ewe tokenization, GhanaTok)
Author: Jennifer Banibensu



## A. Why tokenizer efficiency matters (the problem)

| Source | What it found or did | How this project uses it | Where in the paper | Check |
|---|---|---|---|---|
| Petrov et al. (2023), NeurIPS. Language Model Tokenizers Introduce Unfairness Between Languages | The same text needs very different numbers of tokens in different languages. | Starting evidence for RQ1, evaluated on Twi and Ewe. | Introduction, Related Work | Project notes |
| Ahia et al. (2023), EMNLP. Do All Languages Cost the Same? | Commercial models charge per token, so languages with more tokens cost more. | Basis for cost and context estimates. | Introduction, Related Work, Section 5.6 | Project notes |
| Lundin et al. (2026), AfricaNLP. The Token Tax: Systematic Bias in Multilingual Tokenization | Across 16 African languages, higher fertility goes with lower accuracy, and doubling tokens roughly quadruples training cost. | Justification for evaluating fertility; the sentiment probe does not evaluate downstream accuracy claims. | Introduction, Related Work | Online (ACL Anthology, AfricaNLP 2026) |
| Somide (2026), arXiv 2606.24460. The African Language Tax | 20 African languages and 11 tokenizers. Every language costs more than English (median 1.88 times on GPT-5's tokenizer, up to 8.9 times the inference cost). Concludes that tokenizers designed for African languages are needed. | Supports the cost framing and the motivation to build a dedicated tokenizer. Cost figures represent estimates from fertility rather than measured bills. | Related Work, Section 5.6 | Online (arXiv). Preprint, not peer reviewed. |

## B. Tokenizer design

| Source | What it found or did | How this project uses it | Where in the paper |
|---|---|---|---|
| Kautsar and Koto (2025), arXiv 2510.06128. Parallel Tokenizers | Builds tokenizers per language and aligns them to improve cross-language fertility balance and transfer. | A related approach; GhanaTok employs a single shared compact vocabulary instead. | Related Work |
| Rust et al. (2021), ACL-IJCNLP. How Good is Your Tokenizer? | Tokenizer quality affects how well a multilingual model works for one language. | Supports the selection of fertility as an evaluation metric. | Related Work |
| Sennrich et al. (2016), ACL. Subword units (BPE) | Byte pair encoding for subwords. | GhanaTok (BPE). | Related Work, Section 4 |
| Kudo (2018), ACL. Subword Regularization (Unigram) | Unigram language model tokenizer. | GhanaTok-Unigram. | Related Work, Section 4 |
| Kudo and Richardson (2018), EMNLP demos. SentencePiece | Tool used to train and run Unigram and XLM-R style tokenizers. | Training GhanaTok-Unigram. | Related Work, Section 4 |

## C. Models and tokenizers compared

| Source | What it is | How this project uses it | Where in the paper |
|---|---|---|---|
| Devlin et al. (2019), NAACL. BERT, with multilingual BERT (mBERT) | WordPiece multilingual model. | Baseline tokenizer. Lowest fertility among general tokenizers. | Section 3 |
| Conneau et al. (2020), ACL. XLM-R | SentencePiece vocabulary of 250,000 tokens. | Baseline tokenizer. | Section 3 |
| Alabi et al. (2022), COLING. AfroXLMR (multilingual adaptive fine-tuning) | XLM-R adapted to African languages. | Baseline tokenizer. Gave identical token counts to XLM-R on every test sentence. | Section 3 |
| Azunre et al. (2021), arXiv 2103.15963. Contextual Text Embeddings for Twi (ABENA) | BERT-style model for Twi (Akuapem). | Twi-only baseline. Never tested on Ewe. | Introduction, Section 3 |

## D. Ghanaian and African data and resources

| Source | What it is | How this project uses it | Where in the paper |
|---|---|---|---|
| Adu Gyamfi et al. (2026), arXiv 2603.13793. GhanaNLP Parallel Corpora | English-aligned text for Twi, Fante, Ewe, Ga and Kusaal (CC BY-NC-SA 4.0 per the data card). | Primary Twi and Ewe training, validation, and test text. | Section 3, Ethics |
| Muhammad et al. (2023), EMNLP. AfriSenti | Twitter sentiment data for African languages, including Twi (CC BY 4.0). | Small sentiment probe. | Section 5.7 |
| Issaka et al. (2024), arXiv 2405.06818. The Ghanaian NLP Landscape: A First Look | Survey of NLP work on Ghanaian languages. | Shows the gap this project addresses. | Introduction, Related Work | 
| Issaka et al. (2026), ACL 2026. The African Languages Lab | Large collaborative data effort for African languages that includes Twi. | Context for data work on African languages. | Related Work | 



## Relationship of findings to the literature

1. Earlier work demonstrates a fertility gap for African languages, confirmed here on Twi and Ewe: 64% to 72% of words split and 2.3 to 2.6 tokens per word.
2. Somide (2026) concludes that the gap will not close without tokenizers designed for African languages. GhanaTok results align with this finding, within the scope of fertility metrics, cost estimates, and a sentiment probe.
3. Lundin et al. (2026) link fertility to accuracy. The sentiment probe demonstrates no clear accuracy difference; consequently, no claim is made that lower fertility improves accuracy.
