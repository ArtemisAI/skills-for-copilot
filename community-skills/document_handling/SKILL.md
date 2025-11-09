---
name: document-handling
description: Process, extract, transform, and analyze documents in various formats (Excel, CSV, JSON). Use when loading documents, converting formats, extracting/filtering data, merging/splitting files, or generating reports with visualizations.
license: Apache 2.0
---

# Document Handling Skill

Process, extract, transform, and analyze documents in various formats (Excel, CSV, JSON).

## Skill Modules

### `document_loader.py`
Loads documents with automatic format detection.

**Usage**:
```python
from skills.document_handling.scripts.document_loader import load_document

result = load_document(
    file_path="Data/recruitment.xlsx",
    sheet_name="Sheet1"  # optional
)
```

### `format_converter.py`
Converts between Excel, CSV, JSON formats.

**Usage**:
```python
from skills.document_handling.scripts.format_converter import convert_format

result = convert_format(
    input_path="Data/file.xlsx",
    output_format="csv"
)
```

### `data_extractor.py`
Extracts specific data based on criteria.

**Usage**:
```python
from skills.document_handling.scripts.data_extractor import extract_data

result = extract_data(
    df=dataframe,
    filters={"poste": "Developer", "age": ">25"}
)
```

### `report_generator.py`
Creates reports with charts and visualizations.

**Usage**:
```python
from skills.document_handling.scripts.report_generator import generate_report

result = generate_report(
    df=dataframe,
    output_path="reports/summary.xlsx",
    include_charts=True
)
```

## When to Use

- "load Excel file"
- "convert to CSV"
- "extract rows where..."
- "merge multiple files"
- "create report with charts"

## Dependencies

```python
pandas>=2.0.0
openpyxl>=3.1.0
xlsxwriter>=3.1.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

## Test Data

Use files in `Data/` directory:
- `Test_Excel_Recrutement_v3.0*.xlsx`
- `Aitor-Patino.xlsx`

## Output Format

```json
{
  "status": "success",
  "data": {
    "records": [...],
    "output_file": "path/to/output"
  },
  "metadata": {
    "rows_processed": 100,
    "processing_time_ms": 250
  }
}
```

## Implementation Status

**Phase**: POC - Implementation skeleton ready  
**Next**: Implement actual document processing in Phase 3 MVP

