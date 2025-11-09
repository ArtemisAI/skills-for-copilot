# Data Analysis Output Formats

## Standard Analysis Report

```markdown
# Data Analysis: [Dataset Name]

## Dataset Overview
- **Rows**: [count]
- **Columns**: [count]  
- **Date Range**: [if applicable]
- **Quality**: [assessment]

## Key Findings

### Finding 1: [Title]
[Pattern/insight with supporting numbers]

### Finding 2: [Title]
[Pattern/insight with supporting numbers]

## Summary Statistics

| Metric | Value |
|--------|-------|
| [Metric] | [Value] |

## Recommendations
1. [Actionable recommendation]
2. [Actionable recommendation]

## Data Quality Notes
[Issues, limitations, caveats]
```

## Comparative Analysis

```markdown
# Comparative Analysis: [Topic]

## Comparison Summary

| Category | Metric A | Metric B | Metric C |
|----------|----------|----------|----------|
| Group 1  | [value]  | [value]  | [value]  |
| Group 2  | [value]  | [value]  | [value]  |

## Key Differences
- [Notable difference with percentage or magnitude]
- [Notable difference with percentage or magnitude]

## Implications
[What these differences mean for decision-making]
```

## Trend Analysis

```markdown
# Trend Analysis: [Metric Over Time]

## Overall Trend
[Description: increasing, decreasing, cyclical, stable]

## Period-over-Period Changes

| Period | Value | Change | % Change |
|--------|-------|--------|----------|
| [Date] | [val] | [+/-]  | [%]      |

## Notable Events
- **[Date]**: [Anomaly or significant change with explanation]

## Forecast Considerations
[Factors that may impact future trends]
```

## Analysis Techniques Reference

**Summary statistics**: count, mean, median, min, max, percentiles (p50, p95, p99)

**Pattern detection**: sorting, grouping, time-series trends, outlier detection (>2 SD from mean)

**Comparisons**: period-over-period (MoM, QoQ, YoY), category analysis, correlations

**Quality checks**: missing values, duplicates, range validation, format consistency

