---
name: data-interrogation
description: Analyze CSV and tabular data to extract executive-level insights, identify patterns and anomalies, and create actionable recommendations. Claude should use this skill when analyzing spreadsheets, CSV files, or tabular data requiring summary statistics and business insights.
---

## When to use this skill

Use this skill to analyze CSV files, spreadsheets, sales data, customer metrics, operational data, survey results, or any tabular data requiring pattern analysis and executive-level insights.

## How to use this skill

1. **Inspect data** - Structure, completeness, quality check
2. **Analyze patterns** - Summary statistics, trends, outliers
3. **Generate insights** - Prioritize business-relevant findings
4. **Create output** - Use executive-ready format from `references/formats.md`

## Key principles

1. **Executive lens** - Focus on decision-useful insights, not just statistics
2. **Flag issues** - Call out data quality problems clearly
3. **Show methodology** - Explain calculations for reproducibility
4. **Context matters** - Ask for clarification if data context unclear
5. **Appropriate depth** - Match detail level to data complexity

## Output format

See [references/formats.md](references/formats.md) for:
- Standard analysis report
- Comparative analysis
- Trend analysis

## For large datasets

When analyzing >10,000 rows, focus on summary statistics and patterns rather than row-by-row review.

## Keywords

data analysis, CSV analysis, spreadsheet analysis, data interrogation, business intelligence, metrics analysis, statistical summary, trend analysis
