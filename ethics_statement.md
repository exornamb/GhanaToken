# Ethics Statement: Tokenization Efficiency in Ghanaian Low-Resource Languages

Author: Jennifer Banibensu
Project: DCIT 316 individual project (Twi and Ewe tokenization, GhanaTok)

## 1. Purpose and intended beneficiaries

This project measures how well common tokenizers handle Twi and Ewe and trains a small tokenizer, GhanaTok, for both. The aim is lower cost and better use of context for Ghanaian language text. The project does not train or release a language model.

## 2. Data sources and licences

| Data | Source | Licence | Use here |
|---|---|---|---|
| Twi and Ewe sentences | GhanaNLP Parallel Corpora | CC BY-NC-SA 4.0 (as recorded in the data card) | Training, validation, sealed test sets, academic research only |
| Twi tweets for sentiment | AfriSenti | CC BY 4.0 | Small sentiment probe, academic research only |

Both datasets are public and were made for research. No new text was collected or scraped.


## 3. Privacy and people

The sentences are translated text. The AfriSenti tweets are public posts from a released research dataset. No attempt was made to identify any writer, records were not linked to other sources, and no data was stored beyond the released text.

## 4. Fair representation

- Twi has several dialects, and the Twi text mixes Akuapem and Asante spelling. ABENA was trained on Akuapem only. The dialect check uses a short keyword list, serving as a rough signal rather than a classifier.
- Much of the text is dialogue, Bible text and civic notices. Results may not hold for news, books, social media or spoken-style writing.
- The analysis addresses Twi and Ewe solely as represented in the data. No claims are made regarding how all Ghanaians speak or write.

## 5. Possible harms and risk mitigation

| Risk | Mitigation |
|---|---|
| Over-claiming. A lower token count is read as a better language model. | The paper notes that fertility is not quality, and explicitly reports no clear accuracy gain from the sentiment probe. |
| Unfair comparison. GhanaTok was trained on the same corpus as the test text. | Disclosed directly in the Discussion and Limitations sections. |
| Cost claims taken as real bills. | Figures represent estimates derived from token counts; commercial services use proprietary tokenizers. |
| Small data and no speaker review. | Both factors are listed as limitations. Token counts were measured without evaluating the linguistic validity of subword splits with Twi or Ewe speakers. |
| Licence misuse. | Licences are stated in the data card and in Section 2. |

## 6. Honest reporting

- The test sets stayed sealed until the final run.
- Every number in the paper comes from the CSV files in reports/tables, and the paper tables are generated from those files.
- Tests are paired and corrected for multiple comparisons; overlapping intervals (sentiment probe) are reported directly instead of declaring a winner.
- The vocabulary size sweep was run on the test sets after 8,000 tokens was chosen, as documented in the paper.

## 7. Compute and environment

Training one GhanaTok tokenizer takes minutes on a laptop. No large model was trained, so the energy use is small.

## 8. AI tools

AI use is described in ai_use_disclosure.md.

## 9. What remains open

- Review of the splits by Twi and Ewe speakers.
- Testing on other kinds of text.
- Checking whether a language model trained with GhanaTok improves real tasks.
