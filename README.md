# ✦ CleanSheet — Smart CSV Data Cleaner

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-2EA44F?style=for-the-badge)

### Turn messy CSV files into clean, reliable, analysis-ready datasets.

CleanSheet is a lightweight, user-friendly data-cleaning application designed to simplify the process of inspecting, understanding, and cleaning messy CSV datasets — without writing a single line of code.

**Upload. Analyze. Clean. Validate. Export.**

[Features](#-features) · [Installation](#-getting-started) · [Usage](#-how-to-use-cleansheet) · [Architecture](#-project-structure) · [License](#-license)

</div>

---

## 📌 Overview

Working with real-world datasets often means dealing with missing values, duplicate records, inconsistent formatting, and other data-quality problems.

Cleaning these datasets manually can be time-consuming, repetitive, and error-prone.

**CleanSheet solves this problem through a simple, interactive workflow.**

Users can upload a CSV file, automatically inspect its quality, identify problems, apply appropriate cleaning strategies, compare the results, and export a cleaned dataset.

No advanced programming knowledge is required.

### The CleanSheet Workflow

```text
       📂 Upload CSV
             |
             ▼
      🔍 Inspect Dataset
             |
             ▼
      📊 Analyze Data Quality
             |
             ▼
       🧹 Clean Your Data
             |
             ▼
      ✅ Validate Results
             |
             ▼
       📥 Export Clean CSV
```

---

## ✨ Features

### 1. 📂 Easy CSV Upload
- Upload CSV files directly through the interface.
- Supports UTF-8 and Latin-1 encoding with fallback handling.
- Quickly load and inspect datasets.
- Includes sample data for demonstration.

### 2. 📊 Instant Dataset Overview

Get an immediate overview of your uploaded dataset.

- Total number of rows.
- Total number of columns.
- Missing cell count.
- Duplicate row count.
- Overall data-quality score.

### 3. 🔍 Column-Level Quality Analysis

Understand the quality of individual columns.

- Identify missing values.
- Inspect data completeness.
- Review column-level statistics.
- Detect potential data-quality issues.

### 4. 🧠 Smart Missing Value Handling

Choose appropriate strategies depending on the column type.

**For numerical columns:**
- Median
- Mean
- Zero
- Drop rows containing missing values

**For text and categorical columns:**
- Most frequent value
- Replace with `Unknown`
- Drop rows containing missing values

### 5. 🧹 Advanced Cleaning Operations

Clean your dataset using simple interactive controls.

- Remove leading and trailing whitespace.
- Remove exact duplicate rows.
- Handle missing values.
- Apply cleaning operations without modifying the original uploaded dataset.

### 6. 📈 Before & After Comparison

Evaluate the impact of your cleaning operations.

- Compare original and cleaned datasets.
- Review changes in missing values.
- Compare duplicate records.
- Monitor data-quality improvements.

### 7. 📥 Export Cleaned Dataset

Download your cleaned dataset as a CSV file.

- UTF-8 encoding with BOM for spreadsheet compatibility.
- Convenient export functionality.
- Ready for further analysis in Excel, Python, Power BI, and other tools.

### 8. 🧪 Built-in Sample Dataset

New users can explore CleanSheet without preparing their own data.

Use the included sample dataset to understand the application's cleaning workflow.

---

## 🛠 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Pandas | Data manipulation and cleaning |
| Plotly | Data visualization |
| Pytest | Unit testing |

---

# 🚀 Getting Started

Follow the instructions below to download, install, and run CleanSheet on your computer.

No complicated configuration is required.

## Prerequisites

Before starting, make sure you have the following installed:

| Requirement | Recommended version |
|---|---|
| Python | 3.9 or newer |
| Git | Latest stable version |
| Web Browser | Chrome, Firefox, Edge, or Safari |
| Code Editor | VS Code (optional) |

### Step 1 — Install Python

Download Python from the official website:

https://www.python.org/downloads/

During Windows installation, make sure to select:

**Add Python to PATH**

Verify your installation:

```bash
python --version
```

On Windows, you can also use:

```powershell
py --version
```

### Step 2 — Install Git

Download Git from:

https://git-scm.com/downloads

Verify the installation:

```bash
git --version
```

### Step 3 — Clone the Repository

Open your terminal, Command Prompt, PowerShell, or VS Code terminal.

Run:

```bash
git clone https://github.com/Mostafejur3/cleansheet.git
```

Move into the project directory:

```bash
cd cleansheet
```

You now have a local copy of the CleanSheet project.

### Step 4 — Create a Virtual Environment

A virtual environment keeps project dependencies separate from your system-wide Python packages.

**Windows (PowerShell / CMD)**

```powershell
py -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

If PowerShell blocks script execution, you can use Command Prompt instead:

```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux**

Create the environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

After successful activation, your terminal should display something similar to:

```text
(.venv)
```

### Step 5 — Upgrade pip

Upgrade the Python package installer:

```bash
python -m pip install --upgrade pip
```

### Step 6 — Install Project Dependencies

Install all required packages from the project's requirements file:

```bash
python -m pip install -r requirements.txt
```

Wait until the installation finishes successfully.

### Step 7 — Run CleanSheet

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

Your terminal will display a local application address.

### Step 8 — Open CleanSheet in Your Browser

Open your browser and visit:

**http://localhost:8501**

Congratulations! 🎉

CleanSheet is now running locally on your computer.

---

## ⚡ Quick Start — Copy & Run

Already have Python and Git installed?

You can use the following commands to get started quickly.

**Windows PowerShell:**

```powershell
git clone https://github.com/Mostafejur3/cleansheet.git

cd cleansheet

py -m venv .venv

.venv\Scripts\activate

python -m pip install --upgrade pip

python -m pip install -r requirements.txt

python -m streamlit run app.py
```

**macOS / Linux:**

```bash
git clone https://github.com/Mostafejur3/cleansheet.git

cd cleansheet

python3 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

python -m pip install -r requirements.txt

python -m streamlit run app.py
```

---

## 💻 How to Use CleanSheet

Once the application is running, follow this workflow:

**1. Upload Your Dataset**

Select a CSV file from your computer or use the available sample dataset.

**2. Inspect Your Data**

Review the dataset overview, column information, missing values, and duplicate records.

**3. Analyze Data Quality**

Check the quality report and identify which columns need attention.

**4. Configure Cleaning Options**

Choose the appropriate missing-value strategy and enable additional cleaning operations.

**5. Apply Cleaning**

Execute the selected operations and generate your cleaned dataset.

**6. Validate the Results**

Compare the original and cleaned datasets to understand what changed.

**7. Download Your Dataset**

Export the cleaned CSV file and use it for your next analysis project.

---

## 🧪 Running Tests

CleanSheet includes automated unit tests for its data-quality logic.

Make sure your virtual environment is activated and dependencies are installed.

Run:

```bash
python -m pytest -q
```

To run the tests with more detailed output:

```bash
python -m pytest -v
```

---

## 📂 Project Structure

The project is organized into separate application, processing, and testing components.

```text
cleansheet/
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── LICENSE
│
├── .gitignore
│
├── src/
│   ├── __init__.py
│   └── data_quality.py
│
├── tests/
│   └── test_data_quality.py
│
└── sample_data/
    └── messy_sales.csv
```

### Main Files

| File | Description |
|---|---|
| `app.py` | Main Streamlit application and user interface |
| `requirements.txt` | Required Python packages |
| `src/data_quality.py` | Core data-quality and cleaning logic |
| `tests/` | Automated unit tests |
| `sample_data/` | Example dataset for testing |
| `README.md` | Project documentation |
| `LICENSE` | MIT license information |
| `.gitignore` | Files excluded from Git tracking |

---

## 🧠 Understanding the Data Quality Score

CleanSheet uses a simple heuristic to provide an overview of dataset quality.

The score is calculated using:

```text
Score = 100
        - (Missing Cell Percentage × 0.7)
        - (Duplicate Row Percentage × 0.3)
```

The resulting score is rounded and constrained between 0 and 100.

The score is intended as a quick indicator rather than an industry-standard data-quality certification.

Always consider the underlying missing-value and duplicate counts when evaluating a dataset.

---

## 🔐 Data Handling & Privacy

CleanSheet is designed to process uploaded datasets within the active application session.

- **In-memory processing:** Uploaded datasets are processed during the active session.
- **No database:** The application does not require a database or user account system.
- **No permanent upload storage:** The application does not provide permanent file storage.
- **Original data protection:** Cleaning operations work on a separate working dataset rather than intentionally overwriting the original uploaded data.
- **User-controlled export:** Download the cleaned dataset when you are satisfied with the results.

**Important:** Avoid uploading confidential, sensitive, or personally identifiable information to publicly accessible demo instances.

---

## ⚠️ Current Limitations

CleanSheet focuses on practical CSV data-cleaning operations.

Current limitations include:

- CSV files only; Excel `.xlsx` support is not currently included.
- Duplicate detection identifies exact full-row matches.
- Automatic cleaning cannot determine business-specific data correctness.
- The data-quality score is a lightweight heuristic.
- Cleaning strategies may require human review before important business or research use.

---


### ✦ CleanSheet

**Make messy data meaningful.**

Built with ❤️ using Python, Pandas, and Streamlit.

[GitHub Repository](https://github.com/Mostafejur3/cleansheet)

⭐ If you find CleanSheet useful, consider giving the repository a star!

</div>
