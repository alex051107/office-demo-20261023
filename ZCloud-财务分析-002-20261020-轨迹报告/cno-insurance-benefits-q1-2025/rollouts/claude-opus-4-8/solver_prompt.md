You are a financial analyst supporting CNO Financial Group management. CNO Financial Group management needs a workbook comparing insurance policy benefits for the first quarter of 2025 with the fourth quarter of 2024.

The materials are drawn from public filings and have been prepared for this exercise; some figures and passages may differ from the published versions.

The input folder holds four workbooks, one per company filing: `CNO_2024-09-30_10Q.xlsx`, `CNO_2024-12-31_10K.xlsx`, `CNO_2025-03-31_10Q.xlsx` and `CNO_2025-06-30_10Q.xlsx`. In each, worksheet `Text` holds the filing text one paragraph per row (with `[Tnnn]` marking where a table stands) and worksheets `T001`, `T002` and so on hold the tables.

Report the change as the first-quarter amount minus the fourth-quarter amount, in USD millions to one decimal place.
Report the percentage change relative to the fourth-quarter amount, to two decimal places.

The following are left to you: Additional supporting worksheets and workbook layout; Static values or formulas for the requested Results values.

## Deliverables

Save the workbook as `/app/output/answer.xlsx` with the three sheets below.

**Results.** Row 1 holds the headers `label`, `value`, `unit`, `source_note` in A1:D1. Rows 2 and 3 hold one value each, with the stated unit and a source_note identifying the filing and location used, using these labels exactly and in this order:

| row | label | unit |
|---|---|---|
| 2 | Change in insurance policy benefits, first quarter of 2025 versus fourth quarter of 2024 | USD millions |
| 3 | Percentage change in insurance policy benefits, first quarter of 2025 versus fourth quarter of 2024 | percent |

**Analysis.** One row per quarter, two rows in all, under these headers in row 1:

`period | measure | amount | unit | source_document | source_page`

- `period`: `Fourth quarter of 2024` or `First quarter of 2025`.
- `measure`: `Insurance policy benefits`.
- `amount`: insurance policy benefits for that quarter.
- `unit`: `USD millions`.
- `source_document`: the supplied file used; `source_page`: the worksheet or table used.

**Summary.** One row each for `Fourth quarter of 2024` and `First quarter of 2025`, under these headers in row 1:

`quarter | insurance_policy_benefits`

A pivot table, a formula-based summary or an equivalent static summary is acceptable.


Input materials are in /app/input. Save your output files to /app/output, following the instruction exactly. Use local tools to inspect the supplied files. Do not use external web search.