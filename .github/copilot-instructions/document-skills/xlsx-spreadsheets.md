# Excel Spreadsheets (XLSX)

## Overview

Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. Use when working with Excel files (.xlsx, .xlsm, .csv, .tsv) - creating new spreadsheets, reading/analyzing data, modifying while preserving formulas, or performing calculations.

## When to Use

- Creating new Excel spreadsheets with formulas and formatting
- Reading or analyzing data from existing spreadsheets
- Modifying spreadsheets while preserving formulas and formatting
- Data analysis and visualization in spreadsheets
- Recalculating formulas and updating values
- Converting between formats (CSV, TSV, XLSX)
- Building financial models or data reports

## Core Requirements

### Zero Formula Errors
**Critical:** Every Excel file MUST be delivered with ZERO formula errors:
- No #REF! (invalid reference)
- No #DIV/0! (division by zero)
- No #VALUE! (wrong type)
- No #N/A (not available)
- No #NAME? (unrecognized name)

### Preserve Existing Templates
When updating existing files:
- Study and EXACTLY match existing format, style, and conventions
- Never impose standardized formatting on files with established patterns
- Existing template conventions ALWAYS override these guidelines

### Color Coding Standards (Financial Models)

Unless otherwise stated by user or existing template:

**Industry-Standard Color Conventions:**
- **Blue text (RGB: 0,0,255)** - Hardcoded inputs, numbers users will change for scenarios
- **Black text (RGB: 0,0,0)** - ALL formulas and calculations
- **Green text (RGB: 0,128,0)** - Links pulling from other worksheets within same workbook
- **Red text (RGB: 255,0,0)** - External links to other files
- **Yellow background (RGB: 255,255,0)** - Key assumptions needing attention or cells requiring updates

## Workflows

### Workflow 1: Create New Excel File

**Using openpyxl (Python):**
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

# Create workbook
wb = Workbook()
ws = wb.active
ws.title = "Sales Data"

# Add headers
headers = ["Month", "Revenue", "Expenses", "Profit"]
ws.append(headers)

# Format headers
for cell in ws[1]:
    cell.font = Font(bold=True)
    cell.fill = PatternFill(start_color="CCCCCC", fill_type="solid")

# Add data
ws.append(["January", 10000, 7000, "=B2-C2"])
ws.append(["February", 12000, 8000, "=B3-C3"])

# Save
wb.save("sales_report.xlsx")
```

**Using pandas (Python):**
```python
import pandas as pd

# Create DataFrame
data = {
    'Month': ['January', 'February', 'March'],
    'Revenue': [10000, 12000, 15000],
    'Expenses': [7000, 8000, 9000]
}
df = pd.DataFrame(data)
df['Profit'] = df['Revenue'] - df['Expenses']

# Save to Excel
df.to_excel('sales_report.xlsx', index=False)
```

### Workflow 2: Read and Analyze Data

```python
import pandas as pd

# Read Excel file
df = pd.read_excel('data.xlsx', sheet_name='Sales')

# Basic analysis
print(df.head())
print(df.describe())
print(f"Total Revenue: {df['Revenue'].sum()}")
print(f"Average Profit: {df['Profit'].mean()}")

# Filter data
high_revenue = df[df['Revenue'] > 10000]
print(high_revenue)

# Group by
monthly_summary = df.groupby('Month').agg({
    'Revenue': 'sum',
    'Expenses': 'sum',
    'Profit': 'sum'
})
print(monthly_summary)
```

### Workflow 3: Update Existing Spreadsheet

```python
from openpyxl import load_workbook
from openpyxl.styles import Font

# Load existing workbook
wb = load_workbook('existing_file.xlsx')
ws = wb.active

# Update specific cell
ws['A1'] = 'Updated Title'
ws['A1'].font = Font(bold=True, size=14)

# Update range
for row in range(2, 10):
    ws[f'C{row}'] = f'=A{row}*B{row}'  # Add formula

# Add new row
ws.append(['New Item', 100, '=A10*B10'])

# Save (preserves formulas and formatting)
wb.save('existing_file.xlsx')
```

### Workflow 4: Apply Formatting and Styles

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()
ws = wb.active

# Write value
ws['A1'] = "Important Header"

# Apply multiple styles
ws['A1'].font = Font(
    name='Arial',
    size=14,
    bold=True,
    color='FFFFFF'
)
ws['A1'].fill = PatternFill(
    start_color='0066CC',
    fill_type='solid'
)
ws['A1'].alignment = Alignment(
    horizontal='center',
    vertical='center'
)

# Add borders
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
ws['A1'].border = thin_border

wb.save('formatted.xlsx')
```

### Workflow 5: Work with Formulas

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Add data
ws['A1'] = "Item"
ws['B1'] = "Price"
ws['C1'] = "Quantity"
ws['D1'] = "Total"

# Add items
ws['A2'] = "Widget"
ws['B2'] = 10.50
ws['C2'] = 5

# Add formulas
ws['D2'] = "=B2*C2"  # Price * Quantity

# More complex formulas
ws['A10'] = "Grand Total"
ws['D10'] = "=SUM(D2:D9)"

# Conditional formula
ws['E2'] = "=IF(D2>50, 'High', 'Low')"

# VLOOKUP example
# ws['F2'] = "=VLOOKUP(A2, Sheet2!A:B, 2, FALSE)"

wb.save('formulas.xlsx')
```

### Workflow 6: Financial Model Pattern

```python
from openpyxl import Workbook
from openpyxl.styles import Font

wb = Workbook()
ws = wb.active
ws.title = "Financial Model"

# Blue text for inputs (hardcoded values)
blue_font = Font(color='0000FF')
black_font = Font(color='000000')
green_font = Font(color='008000')

# Assumptions section
ws['A1'] = "Assumptions"
ws['A1'].font = Font(bold=True)

ws['A2'] = "Initial Investment"
ws['B2'] = 100000
ws['B2'].font = blue_font  # Input value

ws['A3'] = "Annual Growth Rate"
ws['B3'] = 0.15
ws['B3'].font = blue_font  # Input value

# Calculations section
ws['A5'] = "Calculations"
ws['A5'].font = Font(bold=True)

ws['A6'] = "Year 1 Revenue"
ws['B6'] = "=B2*(1+B3)"  # Formula
ws['B6'].font = black_font  # Formula = black

ws['A7'] = "Year 2 Revenue"
ws['B7'] = "=B6*(1+B3)"
ws['B7'].font = black_font

wb.save('financial_model.xlsx')
```

### Workflow 7: Convert Between Formats

```python
import pandas as pd

# CSV to XLSX
df = pd.read_csv('data.csv')
df.to_excel('data.xlsx', index=False)

# XLSX to CSV
df = pd.read_excel('data.xlsx')
df.to_csv('data.csv', index=False)

# Multiple sheets to separate CSVs
xlsx_file = pd.ExcelFile('workbook.xlsx')
for sheet_name in xlsx_file.sheet_names:
    df = pd.read_excel(xlsx_file, sheet_name=sheet_name)
    df.to_csv(f'{sheet_name}.csv', index=False)
```

## Examples

### Example 1: Sales Report with Charts

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference

wb = Workbook()
ws = wb.active

# Add data
data = [
    ['Month', 'Sales'],
    ['Jan', 100],
    ['Feb', 120],
    ['Mar', 140],
]

for row in data:
    ws.append(row)

# Create chart
chart = BarChart()
chart.title = "Monthly Sales"
chart.x_axis.title = "Month"
chart.y_axis.title = "Sales"

# Set data ranges
data_ref = Reference(ws, min_col=2, min_row=1, max_row=4)
categories = Reference(ws, min_col=1, min_row=2, max_row=4)
chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(categories)

# Add chart to sheet
ws.add_chart(chart, "D2")

wb.save('sales_chart.xlsx')
```

### Example 2: Data Validation

```python
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation

wb = Workbook()
ws = wb.active

# Create dropdown list
dv = DataValidation(
    type="list",
    formula1='"Red,Green,Blue"',
    allow_blank=True
)
ws.add_data_validation(dv)
dv.add(ws['A2:A100'])

# Number validation
num_dv = DataValidation(
    type="whole",
    operator="between",
    formula1=1,
    formula2=100,
    errorTitle="Invalid number",
    error="Please enter a number between 1 and 100"
)
ws.add_data_validation(num_dv)
num_dv.add(ws['B2:B100'])

wb.save('validation.xlsx')
```

## Resources

### Workspace References

**Core Documentation:**
- `document-skills/xlsx/SKILL.md` - Complete Excel skill documentation

**Scripts:**
- `document-skills/xlsx/scripts/` - Utility scripts (if available)

### Python Libraries

**Primary Libraries:**
- `openpyxl` - Read/write Excel files, formulas, formatting
- `pandas` - Data analysis, reading/writing Excel
- `xlwings` - Control Excel application (Windows/Mac)

**Installation:**
```bash
pip install openpyxl pandas xlsxwriter
```

## Guidelines

### Best Practices

1. **Validate Formulas** - Always check for formula errors before saving
2. **Preserve Formatting** - When updating, maintain existing styles
3. **Use Appropriate Libraries**:
   - `openpyxl` - Full Excel feature support
   - `pandas` - Data analysis and manipulation
   - `xlwings` - Excel automation (requires Excel installed)

4. **Performance**:
   - Use `read_only=True` for large files
   - Use `write_only=True` for writing large datasets
   - Process in chunks for very large files

### Common Patterns

**Safe Update Pattern:**
```python
from openpyxl import load_workbook

try:
    wb = load_workbook('file.xlsx')
    ws = wb.active
    
    # Make changes
    ws['A1'] = 'Updated'
    
    # Save
    wb.save('file.xlsx')
except Exception as e:
    print(f"Error: {e}")
finally:
    wb.close()
```

**Formula Validation:**
```python
def validate_formulas(worksheet):
    """Check for formula errors"""
    errors = []
    for row in worksheet.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str):
                if cell.value.startswith('#'):
                    errors.append(f"{cell.coordinate}: {cell.value}")
    return errors
```

## Troubleshooting

### Problem: Formulas not calculating
**Solution:** Formulas calculate in Excel, not Python. Use xlwings or Excel to recalculate.

### Problem: Formatting lost when using pandas
**Solution:** Use openpyxl for formatting, pandas for data manipulation.

### Problem: Large files too slow
**Solution:** Use read_only/write_only modes, or process in chunks.

### Problem: Can't open file created by openpyxl
**Solution:** Check file extension is .xlsx, not .xls (old format).

## Next Steps

After mastering basics:

1. **Advanced Formulas** - VLOOKUP, INDEX/MATCH, array formulas
2. **Charts and Visualization** - Create various chart types
3. **Pivot Tables** - Use openpyxl or xlwings
4. **Macros** - Integrate VBA with Python
5. **Automation** - Build complete reporting pipelines

## Additional Context

This instruction set covers common Excel operations. For complete skill documentation including advanced patterns and edge cases, see `document-skills/xlsx/SKILL.md`.

Use @workspace to query the original skill for specific scenarios.
