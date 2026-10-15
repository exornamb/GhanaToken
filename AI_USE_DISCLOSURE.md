# AI Use Disclosure: Tokenization Optimization for Ghanaian Languages

- **Author:** Jennifer Banibensu
- **Project:** DCIT 316 Individual Research Project (Twi and Ewe Tokenization, GhanaTok)
- **Institution:** Department of Computer Science, University of Ghana

In accordance with academic integrity guidelines, conference transparency policies (e.g., ACL / AfricaNLP AI policy), and course evaluation criteria, this document provides full disclosure of generative AI assistance utilized during this research project, how all outputs were verified, and how intellectual ownership was maintained.

---

## 1. AI Tools Utilized

- **Primary Assistant:** Anthropic Claude & Google Antigravity IDE assistant
- **Role:** Interactive pair-programming assistant, technical editor, and reference lookup verification tool.

---

## 2. Granular Breakdown of AI Assistance

| Research Phase | Specific AI Assistance | Human Responsibility & Control | Verification Mechanism |
| :--- | :--- | :--- | :--- |
| **Research Formulation & RQ Definition** | Brainstorming operational phrasing for research questions; formatting literature review headings. | Formulated original research questions (RQ1-3) based on semester project proposal and Ghanaian language needs. | Proposal approved by course instructor; strictly aligned with course scope. |
| **Code Implementation & Refactoring** | Assisted in drafting initial boilerplate for Hugging Face `tokenizers` and `sentencepiece` Python bindings; suggesting vectorized Pandas/NumPy idioms. | Designed the pre-tokenization regex, seed morpheme list, data splitting logic, and benchmark loop architecture. | Line-by-line manual code review; automated unit tests (`tests/test_project_structure.py`) passing 100%. |
| **Writing & Formatting** | Assisted in drafting plain-language report summaries, structuring LaTeX/Markdown tables, and proofreading draft sections for grammatical flow. | Authored all research interpretations, arguments, error analyses, and defended design trade-offs. | Every numeric claim, percentage, and $p$-value was manually cross-checked against generated CSV tables in `reports/tables/`. |
| **Literature Search & Citations** | Assisting in querying bibtex citation keys and verifying conference publication years (ACL Anthology, NeurIPS, EMNLP, COLING). | Selected all referenced papers based on relevance to subword tokenization and African NLP. | All citations independently verified online via DOI, arXiv, and ACL Anthology URLs. |

---

## 3. What Generative AI Did NOT Do

1. **Did Not Fabricate or Impute Data:** Every metric, mean fertility score, standard deviation, bootstrap interval, and throughput number originated directly from the execution of the Python codebase and was written deterministically to CSV files.
2. **Did Not Make High-Level Architectural Decisions:** The decisions to use an 8,000-vocabulary budget, to inject seed morphemes, to isolate ABENA to Twi, and to combine Twi and Ewe into a bilingual model were independent human research decisions made by the author.

---

## 4. Verification Protocol & Quality Assurance

1. **Deterministic Code Execution:**
   - All code snippets were tested through interactive notebooks and automated pytest test suites.
   - Assertions were placed on data shapes, missing value counts (`isna().sum() == 0`), and token ID decodability.
2. **Fact-Checking Against Ground-Truth CSV Tables:**
   - Every single numeric claim in `README.md`, `final_report.md`, and `reports/` was reconciled against `reports/tables/*.csv`.

---

## 5. Academic Ownership & Defense Statement

Jennifer Banibensu is the sole author of this research project and codebase. Every architectural choice, mathematical formulation, code implementation, empirical result, and stated limitation contained within this repository has been independently developed, verified, and is defended by the author during examination and academic defense.
