# Data Quality Monitoring Tool

A reusable Python-based Data Quality Monitoring tool designed to automatically scan datasets and generate comprehensive, color-coded data quality reports. Built for Data Engineers to validate data drops before they hit production systems.

## Features & Checks Performed
- **Null/Missing Value Detection**: Exact counts and percentages per column.
- **Duplicate Row Detection**: Catches full-row duplicates across the dataset.
- **Data Type Validation**: Identifies pandas data types correctly.
- **Outlier Detection**: Utilizes the Interquartile Range (IQR) method for numeric columns to flag extreme values.
- **Column-level Statistics**: Generates Min, Max, Mean, and Standard Deviation metrics for numerical data.
- **Cardinality Checks**: Tracks unique values and percentages across all columns.
- **Pattern & Format Validation**: Implements Regex checks automatically triggered by column name heuristics (e.g., `email`, `date`, `phone`).

## Architecture & Reusability
The project is split cleanly into reusable modules:
- **`dq_checker.py`**: The Click CLI entrypoint orchestrating the workflow.
- **`dq_core/`**:
  - `checks.py`: Contains pure, decoupled pandas functions for analytical calculations. Return dictionaries of metrics.
  - `reporters.py`: Consumers of the metrics. Converts the dictionaries into JSON and renders Jinja2 HTML.
  - `utils.py`: Helpers for file reading and preliminary type inference.
- **`templates/report_template.html`**: A clean, vanilla CSS customized UI template with color-coded warnings designed to mimic a production dashboard.
- **`scripts/generate_sample.py`**: A helper script to emulate a messy Kaggle financial dataset, letting you test out the tool instantly.

## Installation / Setup

1. Make sure you have Python 3.8+ installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Instructions

Run the scanner directly via the command line on any CSV file:

```bash
python dq_checker.py --file path/to/dataset.csv --output my_report.html
```

### Try the Demo
To see the tool in action over a mock financial dataset laden with intentional errors (nulls, duplicates, invalid emails, string injected into amount columns, etc):

1. Generate the sample data:
   ```bash
   python scripts/generate_sample.py
   ```
   *This drops `sample_financial_data.csv` in your folder.*

2. Run the Data Quality tool over the data:
   ```bash
   python dq_checker.py --file sample_financial_data.csv --output sample_report.html
   ```

3. Open `sample_report.html` in your favorite web browser to view the generated UI. You will also see `sample_report.json` generated alongside it, serving pipeline orchestration needs.

## Visual Formatting
The HTML report outputs color-coded badges based on warning thresholds:
- **Green**: Data bounds are stable / perfectly fine (e.g., 0% duplicates).
- **Yellow**: Medium-level warnings requiring investigation.
- **Red**: Critical conditions (e.g., >5% missing data, >5% outliers). 
