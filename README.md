
# DataPipe - Daily Sales Data Pipeline

## Project Overview
DataPipe is a Python-based ETL pipeline that collects daily sales data from multiple stores, cleans and validates the records, and generates an Excel report.

## Features
- Extracts data from CSV files and REST APIs.
- Combines sales data from four stores.
- Validates and cleans sales records.
- Identifies duplicate and invalid records.
- Calculates sales amounts automatically.
- Generates Excel reports using OpenPyXL.
- Maintains execution history across multiple runs.

## Technologies Used
- Python
- Requests
- OpenPyXL
- CSV
- REST API

## Project Structure
datapipe/
- data/
  - pune.csv
  - nagpur.csv
- main.py
- sources.py
- extract.py
- transform.py
- load.py
- report.py
- requirements.txt
- .gitignore
- README.md

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python main.py
```

## Output
The pipeline generates `datapipe_output.xlsx` containing:

1. Sales
2. Rejected
3. Summary
4. Run_History

## Data Sources
- Pune – CSV
- Nagpur – CSV
- Mumbai – REST API
- Nashik – REST API

## Author
Gayatri Narendra Sawant
