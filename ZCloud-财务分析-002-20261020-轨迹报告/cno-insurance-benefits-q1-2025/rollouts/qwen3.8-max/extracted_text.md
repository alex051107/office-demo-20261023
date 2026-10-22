
## Results

A1=label | B1=value | C1=unit | D1=source_note
A2=Change in insurance policy benefits, first quarter of 2025 versus fourth quarter of 2024 | B2==ROUND(Analysis!C3-Analysis!C2,1) | C2=USD millions | D2=Q1 2025 $580.1M per CNO_2025-03-31_10Q.xlsx, worksheet T010 (Consolidated Statement of Operations, p. 5); less Q4 2024 $545.5M, derived as full-year 2024 $2,471.9M per CNO_2024-12-31_10K.xlsx, worksheet T050 (Consolidated Statement of Operations, p. 97) less nine months ended 9/30/2024 $1,926.4M per CNO_2024-09-30_10Q.xlsx, worksheet T010 (Consolidated Statement of Operations, p. 5)
A3=Percentage change in insurance policy benefits, first quarter of 2025 versus fourth quarter of 2024 | B3==ROUND((Analysis!C3-Analysis!C2)/Analysis!C2*100,2) | C3=percent | D3=Change of $34.6M divided by the fourth-quarter 2024 base of $545.5M, expressed as a percentage to two decimal places. Base and current-quarter sources: CNO_2025-03-31_10Q.xlsx worksheet T010 (Consolidated Statement of Operations, p. 5); CNO_2024-12-31_10K.xlsx worksheet T050 (p. 97) less CNO_2024-09-30_10Q.xlsx worksheet T010 (p. 5)

## Analysis

A1=period | B1=measure | C1=amount | D1=unit | E1=source_document | F1=source_page
A2=Fourth quarter of 2024 | B2=Insurance policy benefits | C2==Source_Data!B4 | D2=USD millions | E2=CNO_2024-12-31_10K.xlsx; CNO_2024-09-30_10Q.xlsx | F2=T050 (FY 2024, p. 97) less T010 (nine months 2024, p. 5)
A3=First quarter of 2025 | B3=Insurance policy benefits | C3==Source_Data!B5 | D3=USD millions | E3=CNO_2025-03-31_10Q.xlsx | F3=T010 (Consolidated Statement of Operations, p. 5)

## Summary

A1=quarter | B1=insurance_policy_benefits
A2=Fourth quarter of 2024 | B2==Analysis!C2
A3=First quarter of 2025 | B3==Analysis!C3

## Source_Data

A1=item | B1=amount | C1=unit | D1=source_document | E1=source_page | F1=note
A2=Insurance policy benefits, year ended December 31, 2024 | B2=2471.9 | C2=USD millions | D2=CNO_2024-12-31_10K.xlsx | E2=T050 (Consolidated Statement of Operations, p. 97) | F2=Full-year 2024 as reported in the Form 10-K
A3=Insurance policy benefits, nine months ended September 30, 2024 | B3=1926.4 | C3=USD millions | D3=CNO_2024-09-30_10Q.xlsx | E3=T010 (Consolidated Statement of Operations, p. 5) | F3=First three quarters of 2024 as reported in the Form 10-Q
A4=Insurance policy benefits, fourth quarter of 2024 (derived) | B4==ROUND(B2-B3,1) | C4=USD millions | D4=CNO_2024-12-31_10K.xlsx; CNO_2024-09-30_10Q.xlsx | E4=T050 less T010 | F4=Full year 2024 less nine months ended September 30, 2024; a fourth-quarter amount is not separately disclosed
A5=Insurance policy benefits, three months ended March 31, 2025 | B5=580.1 | C5=USD millions | D5=CNO_2025-03-31_10Q.xlsx | E5=T010 (Consolidated Statement of Operations, p. 5) | F5=First quarter of 2025 as reported in the Form 10-Q

## Notes

A1=topic | B1=detail
A2=Question | B2=Compare insurance policy benefits for the first quarter of 2025 with the fourth quarter of 2024, reporting the change (Q1 2025 less Q4 2024) in USD millions to one decimal place and the percentage change relative to Q4 2024 to two decimal places.
A3=First quarter of 2025 | B3=$580.1 million - 'Insurance policy benefits' line item, three months ended March 31, 2025, in CNO_2025-03-31_10Q.xlsx worksheet T010 (Consolidated Statement of Operations, filing page 5).
A4=Fourth quarter of 2024 | B4=$545.5 million, derived. CNO does not present a separate fourth-quarter statement of operations, so Q4 2024 = full year 2024 $2,471.9 million (CNO_2024-12-31_10K.xlsx worksheet T050, filing page 97) less nine months ended September 30, 2024 $1,926.4 million (CNO_2024-09-30_10Q.xlsx worksheet T010, filing page 5).
A5=Derivation check | B5=The same full-year-less-nine-months method reproduces every line the 10-K quarterly financial data note does disclose for Q4 2024 (CNO_2024-12-31_10K.xlsx worksheet T137, filing page 184): revenues $4,449.5 - $3,352.3 = $1,097.2; income before income taxes $518.3 - $307.8 = $210.5; net income $404.0 - $237.9 = $166.1. The note does not disclose insurance policy benefits, hence the derivation.
A6=Result | B6=Change = $580.1M - $545.5M = $34.6M. Percentage change = $34.6M / $545.5M = 6.34%.
A7=Basis of presentation | B7=Both quarters are taken as reported in the filings that report those periods (Q1 2025 Form 10-Q; FY 2024 Form 10-K less the Q3 2024 Form 10-Q nine-month amount). CNO_2025-06-30_10Q.xlsx covers a period after both comparison quarters and was not used for the reported amounts.
A8=Limitation - later revisions | B8=Neither compared quarter is presented on a restated basis in the supplied files, so both are used as reported. For context, CNO_2025-06-30_10Q.xlsx worksheet T016 (filing page 12) discloses immaterial error corrections, to be reflected in future filings, of +$15.6 million to insurance policy benefits for the nine months ended September 30, 2024 (market risk benefit accretion reclassification) and -$21.6 million for the year ended December 31, 2024 (embedded derivative overstatement). Restating only the nine-month input would give Q4 2024 of $529.9 million (change +$50.2 million, +9.47%); applying both corrections would give $508.3 million (change +$71.8 million, +14.13%). No revised Q1 2025 statement-of-operations amount is quantified in the supplied files, so restating one side only would break comparability between the two quarters.
A9=Rounding | B9=Source figures are USD millions to one decimal place. The change is rounded to one decimal place and the percentage change to two decimal places; percentages are computed on the unrounded derivation (545.5).
