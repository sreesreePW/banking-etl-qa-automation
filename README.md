# Banking ETL QA Automation Framework

A demonstration Python-based ETL / Data Quality automation framework using pytest, PySpark, SQL, Databricks, and GitHub Actions.

This project uses only synthetic banking data and contains no employer or client proprietary information.

## Purpose

This framework demonstrates how to validate an end-to-end banking ETL pipeline across:

Source
→ Staging
→ Data Quality
→ Reference Validation
→ Transformation
→ Target Reconciliation
→ CI/CD Quality Gate

## Technology Stack

- Python
- pytest
- PySpark
- SQL
- Databricks SQL Connector
- Git
- GitHub Actions
- pytest-html

## Framework Structure

```text
banking-etl-qa-automation/
├── config/
│   └── config.py
├── utils/
│   ├── db_utils.py
│   ├── source_utils.py
│   ├── validation_utils.py
│   └── reconciliation_utils.py
├── tests/
│   ├── test_source_validation.py
│   ├── test_source_to_staging.py
│   ├── test_staging_data_quality.py
│   ├── test_reference_validation.py
│   ├── test_transformation_validation.py
│   └── test_target_reconciliation.py
├── data/
├── reports/
├── .github/
│   └── workflows/
│       └── etl-qa.yml
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
