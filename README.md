# GhanaToken

Tokenization efficiency in Ghanaian low-resource languages: a comparative evaluation of modern multilingual tokenizers for Twi and Ewe, and a small custom Ghanaian-language tokenizer trained to reduce fragmentation.

**Course**: DCIT 316, Individual Research Project  
**Author / Solo Team**: Jennifer Banibensu  

---

## Project Layout

See `docs/DCIT316_SemesterProject_22013023_JenniferBanibensu.pdf` for the full proposal and [`reports/final_report.md`](reports/final_report.md) for results as they are produced.

```text
GhanaToken/
├── data/
│   ├── raw/             # Raw dataset files
│   └── processed/       # Preprocessed and cleaned datasets
├── models/
│   └── ghanatok/        # Trained custom tokenizer artifacts
├── reports/
│   ├── data_card.md     # Dataset documentation & provenance
│   └── final_report.md  # Comprehensive research results & evaluation
├── scripts/
│   └── check_project_structure.py
├── src/
│   ├── preprocessing.py
│   ├── tokenizer_benchmark.py
│   ├── train_ghanatok.py
│   └── evaluation.py
├── tests/
│   └── test_project_structure.py
├── requirements.txt     # Python package dependencies
└── README.md
```

---

## How to Reproduce

### 1. Set up the Virtual Environment

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Notebooks
Run the notebooks in sequential order: `01`, `02`, `03`, `04`, `05`.
