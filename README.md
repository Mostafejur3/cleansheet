# CleanSheet — Smart CSV Data Cleaner

CleanSheet is a lightweight data-quality app that helps people inspect and clean messy CSV files without writing code.

**Problem:** CSV files often contain missing values, duplicate records and inconsistent whitespace. Fixing these issues manually is repetitive and error-prone.

**Solution:** Upload a CSV, inspect a transparent quality report, choose cleaning strategies, preview the result and download a cleaned file.

## Features

- CSV upload with UTF-8 and Latin-1 fallback
- Dataset overview: rows, columns, missing cells and duplicate rows
- Per-column quality report
- Transparent heuristic data-quality score
- Missing-value handling for numeric and non-numeric columns
- Optional whitespace trimming and duplicate removal
- Before/after preview and cleaning summary
- Download cleaned CSV in UTF-8 with BOM for spreadsheet compatibility
- Sample dataset and unit tests

## Tech stack

- Python
- Pandas
- Streamlit
- Plotly
- Pytest

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/cleansheet.git
cd cleansheet
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Launch the app

```bash
streamlit run app.py
```

Open the local URL printed in the terminal (usually http://localhost:8501).

## Run tests

```bash
pytest -q
```

## Deploy on Streamlit Community Cloud

1. Push this project to a public GitHub repository.
2. Open https://share.streamlit.io/.
3. Sign in with GitHub and choose **Create app**.
4. Select your repository, branch `main`, and main file `app.py`.
5. Deploy.

## Data handling

CleanSheet processes the uploaded CSV in the active app session. The app does not include a database, user account system or permanent file storage. Do not upload confidential or personally identifiable data to a public demo.

## How the quality score works

The score is a simple heuristic, not an industry certification:

`score = 100 - (missing_cell_percentage × 0.7) - (duplicate_row_percentage × 0.3)`

The result is rounded and constrained to 0–100. Review the underlying counts as well as the score.

## Cleaning behaviour

- Numeric missing values: median, mean, zero, or drop rows.
- Non-numeric missing values: most frequent value, `Unknown`, or drop rows.
- Whitespace trimming: optional.
- Exact duplicate removal: optional.

The original uploaded data is never overwritten. Always review the cleaned preview before using the output in important analysis.

## Project structure

```text
cleansheet/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   ├── __init__.py
│   └── data_quality.py
├── tests/
│   └── test_data_quality.py
└── sample_data/
    └── messy_sales.csv
```

## Limitations

- CSV only (Excel `.xlsx` support is not included).
- Duplicate detection checks exact full-row matches.
- Automatic cleaning cannot determine business-specific correctness.
- The quality score is a lightweight heuristic.

## License

MIT — see [LICENSE](LICENSE).

## Production deployment with Docker

Build and run the container:

```bash
docker build -t cleansheet:latest .
docker run --rm -p 8501:8501 cleansheet:latest
```

Then open `http://localhost:8501`. For a public deployment, place the app behind
HTTPS at a trusted reverse proxy or use a managed container platform. Configure
resource limits and upload limits to match your environment. The app processes
files in memory; it does not persist uploads.

## Verification

Run the test suite with:

```bash
python -m pytest -q
```
