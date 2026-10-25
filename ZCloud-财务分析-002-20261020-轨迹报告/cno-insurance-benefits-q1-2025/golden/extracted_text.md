# 修订后参考答案单元格提取

2026-10-25从本次参考答案提取；数值保留原存储精度，显示格式单列。非新增文字裁判。

## Results

| 单元格 | 内容 | 显示格式 |
|---|---|---|
| A1 | label | `General` |
| B1 | value | `General` |
| C1 | unit | `General` |
| D1 | source_note | `General` |
| A2 | Change in insurance policy benefits, first quarter of 2025 versus fourth quarter of 2024 | `General` |
| B2 | 61.7 | `0.0` |
| C2 | USD millions | `General` |
| D2 | CNO_2024-12-31_10K.xlsx \| worksheet/table T050!G15: FY 2024 = 2,471.9.<br>CNO_2024-09-30_10Q.xlsx \| worksheet/table T010!S19: 9M 2024 = 1,926.4.<br>CNO_2025-03-31_10Q.xlsx \| worksheet/table T010!G19: Q1 2025 = 580.1.<br>CNO_2025-06-30_10Q.xlsx \| worksheet/table T016!N14: 9M adjustment +15.6; T016!N24: FY adjustment -21.6; worksheet Text!A131: cumulative embedded-derivative overstatement 21.6 at December 31, 2024 and 31.7 at March 31, 2025.<br>Revision basis: the 21.6 and 31.7 embedded-derivative errors are cumulative balances, not separate quarterly expenses. Convert the cumulative error to the quarter's adjustment: Q1 reduction = 31.7 - 21.6 = 10.1.<br>Revised Q4 = (2,471.9 - 21.6) - (1,926.4 + 15.6) = 508.3. Revised Q1 = 580.1 - 10.1 = 570.0.<br>Change = 570.0 - 508.3 = 61.7 USD millions. | `General` |
| A3 | Percentage change in insurance policy benefits, first quarter of 2025 versus fourth quarter of 2024 | `General` |
| B3 | 12.13850088530396 | `0.00` |
| C3 | percent | `General` |
| D3 | CNO_2024-12-31_10K.xlsx \| worksheet/table T050!G15: FY 2024 = 2,471.9.<br>CNO_2024-09-30_10Q.xlsx \| worksheet/table T010!S19: 9M 2024 = 1,926.4.<br>CNO_2025-03-31_10Q.xlsx \| worksheet/table T010!G19: Q1 2025 = 580.1.<br>CNO_2025-06-30_10Q.xlsx \| worksheet/table T016!N14: 9M adjustment +15.6; T016!N24: FY adjustment -21.6; worksheet Text!A131: cumulative embedded-derivative overstatement 21.6 at December 31, 2024 and 31.7 at March 31, 2025.<br>Revision basis: the 21.6 and 31.7 embedded-derivative errors are cumulative balances, not separate quarterly expenses. Convert the cumulative error to the quarter's adjustment: Q1 reduction = 31.7 - 21.6 = 10.1.<br>Revised Q4 = (2,471.9 - 21.6) - (1,926.4 + 15.6) = 508.3. Revised Q1 = 580.1 - 10.1 = 570.0.<br>Percentage change = (570.0 - 508.3) / 508.3 * 100 = 12.1385008853...%; displayed to two decimals: 12.14 percent. | `General` |

## Analysis

| 单元格 | 内容 | 显示格式 |
|---|---|---|
| A1 | period | `General` |
| B1 | measure | `General` |
| C1 | amount | `General` |
| D1 | unit | `General` |
| E1 | source_document | `General` |
| F1 | source_page | `General` |
| A2 | Fourth quarter of 2024 | `General` |
| B2 | Insurance policy benefits | `General` |
| C2 | 508.3 | `0.0` |
| D2 | USD millions | `General` |
| E2 | CNO_2024-12-31_10K.xlsx; CNO_2024-09-30_10Q.xlsx; CNO_2025-06-30_10Q.xlsx | `General` |
| F2 | CNO_2024-12-31_10K.xlsx T050!G15; CNO_2024-09-30_10Q.xlsx T010!S19; CNO_2025-06-30_10Q.xlsx T016!N14 (+15.6), T016!N24 (-21.6), Text!A131. Revised Q4 = (2,471.9 - 21.6) - (1,926.4 + 15.6) = 508.3 USD millions. | `General` |
| A3 | First quarter of 2025 | `General` |
| B3 | Insurance policy benefits | `General` |
| C3 | 570 | `0.0` |
| D3 | USD millions | `General` |
| E3 | CNO_2025-03-31_10Q.xlsx; CNO_2025-06-30_10Q.xlsx | `General` |
| F3 | CNO_2025-03-31_10Q.xlsx T010!G19; CNO_2025-06-30_10Q.xlsx Text!A131 (cumulative errors 31.7 at March 31, 2025 and 21.6 at December 31, 2024), T016!N24 (2024 correction). Quarter-only adjustment = -(31.7 - 21.6) = -10.1. Revised Q1 = 580.1 - 10.1 = 570.0 USD millions. | `General` |

## Summary

| 单元格 | 内容 | 显示格式 |
|---|---|---|
| A1 | quarter | `General` |
| B1 | insurance_policy_benefits | `General` |
| A2 | Fourth quarter of 2024 | `General` |
| B2 | 508.3 | `0.0` |
| A3 | First quarter of 2025 | `General` |
| B3 | 570 | `0.0` |
