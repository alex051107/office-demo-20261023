# 随包输入离线提取

2026-10-22从既有输入字节重新提取，供查证。不是历史裁判请求，也不代表裁判当时读取过全部内容。图片以随包原图及既有记录为准，不生成或假称OCR。

## Distribution_handbook.pdf
SHA256: 401882d13d2d2b4c81b11d3ead1c284f31f69953c4d77b8ad9ca3647ce238c81
来源类型: original

Final decision


 Electricity distribution network
        service providers

   Roll forward model handbook


                                           April 2020




Roll forward model handbook | Electricity distribution network service providers   1
© Commonwealth of Australia 2020

This work is copyright. In addition to any use permitted under the Copyright Act 1968, all
material contained within this work is provided under a Creative Commons Attributions 3.0
Australia licence, with the exception of:

•   the Commonwealth Coat of Arms

•   the ACCC and AER logos

•   any illustration, diagram, photograph or graphic over which the Australian Competition and
    Consumer Commission does not hold copyright, but which may be part of or contained
    within this publication.
The details of the relevant licence conditions are available on the Creative Commons website,
as is the full legal code for the CC BY 3.0 AU licence.

Requests and inquiries concerning reproduction and rights should be addressed to the
Director, Corporate Communications,
Australian Competition and Consumer Commission,
GPO Box 3131,
Canberra ACT 2601
or publishing.unit@accc.gov.au.

Inquiries about this publication should be addressed to:

Australian Energy Regulator
GPO Box 520
Melbourne Vic 3001

Tel: 1300 585 165

Email: ModelReviews@aer.gov.au
AER reference: 65293




Amendment record
Handbook version            Model version            Date                          Pages

1                           1                        June 2008                     21

2                           2                        December 2016                 32

3                           3                        April 2020                    85




Roll forward model handbook | Electricity distribution network service providers                 2
Contents
Shortened forms ............................................................................................. 7

1    Introduction............................................................................................... 8

     1.1 . Role of the model ............................................................................... 8

     1.2 . Confidentiality .................................................................................... 8

     1.3 . Process for revision .......................................................................... 8

2    The model.................................................................................................. 9

     2.1 . Overview of the RFM ......................................................................... 9

     2.2 . DMS input sheet ............................................................................... 11

     2.3 . RFM input sheet ............................................................................... 12

           2.3.1        Opening regulatory asset base and tax asset base ...................... 16

           2.3.2        Actual nominal capital expenditure—as incurred .......................... 18

           2.3.3        Actual nominal asset disposals—as incurred ............................... 19

           2.3.4        Actual nominal capital contributions—as incurred ........................ 19

           2.3.5        Actual real net capital expenditure—as incurred........................... 19

           2.3.6        Lagged inflation option ................................................................. 19

           2.3.7        Inflation and rate of return ............................................................ 19

           2.3.8        Real straight-line RAB depreciation option ................................... 20

           2.3.9    Forecast/actual year-by-year tracking real straight-line RAB
           depreciation ................................................................................................ 20

           2.3.10       Actual tax depreciation option ...................................................... 20

           2.3.11       Year-by-year tracking actual tax depreciation ............................... 21

           2.3.12       Forecast nominal final year asset adjustments ............................. 21

           2.3.13 Ex-post review options: Adjustments for capex in second last year
           (year t–2) of previous regulatory control period ........................................... 21

           2.3.14 Ex-post review inputs: Adjustments for capex in second last year
           (year t–2) of previous regulatory control period ........................................... 22

     2.4 . Adjustment for previous period sheet ........................................... 24


Roll forward model handbook | Electricity distribution network service providers                                              3
          2.4.1    Nominal adjustments for difference between actual and forecast net
          capex in final year (year t–1) ....................................................................... 27

          2.4.2      Ex-post review: Nominal adjustments for excluded capex in second
          last tear (t–2) .............................................................................................. 27

     2.5 . RAB roll forward sheet .................................................................... 28

          2.5.1        Real asset values ......................................................................... 30

          2.5.2        Nominal asset values ................................................................... 31

     2.6 . Total RAB roll forward sheet .......................................................... 31

     2.7 . TAB roll forward sheet .................................................................... 33

          2.7.1        Opening tax asset values ............................................................. 34

          2.7.2        Actual net capex........................................................................... 35

          2.7.3        Actual tax depreciation ................................................................. 35

     2.8 . RAB remaining lives sheet.............................................................. 35

     2.9 . TAB remaining lives sheet .............................................................. 40

     2.10       PTRM input summary sheet ...................................................... 42

     2.11       Inputs working sheet ................................................................. 42

     The depreciation tracking module ........................................................ 44

           Overview of the depreciation tracking module ............................. 44

          A.1.1        RAB depreciation tracking ............................................................ 44

          A.1.2        TAB depreciation tracking ............................................................ 46

     RAB depreciation tracking..................................................................... 47

           RAB input sheet ............................................................................... 47

          B.1.1        General information ...................................................................... 48

          B.1.2        Starting RAB and actual gross capex ........................................... 49

          B.1.3        Actual asset disposals – as incurred ............................................ 50

          B.1.4        Actual capital contributions – as incurred ..................................... 51

          B.1.5        RAB lives ..................................................................................... 51

          B.1.6        Asset adjustments ........................................................................ 52


Roll forward model handbook | Electricity distribution network service providers                                              4
          B.1.7       Asset adjustments – remaining lives ............................................ 52

          B.1.8       Adjustment for difference in t–1 capex ......................................... 52

          B.1.9       Adjustment for excluded t–2 capex............................................... 53

          B.1.10      RFM closing RAB ......................................................................... 53

          B.1.11      RFM closing RAB (adjusted for mid-period reopeners)................. 53

           RAB tracking sheet .......................................................................... 54

          B.2.1       Data derived from RAB input sheet .............................................. 56

          B.2.2       RAB depreciation schedules ........................................................ 58

           RAB tracking summary sheet ......................................................... 58

           Tracking output sheet – RAB .......................................................... 59

           Adding RAB tracking periods to module ....................................... 60

          B.5.1       Updating the RAB input sheet for new regulatory control period... 61

          B.5.2       Updating RAB tracking sheet for new regulatory control period .... 64

           Increasing the number of years (columns) in tracking module ... 65

     TAB depreciation tracking ..................................................................... 68

           TAB input sheet ............................................................................... 68

          C.1.1       General Information ..................................................................... 69

          C.1.2       Starting TAB and actual gross capex ........................................... 70

          C.1.3       Actual immediately expensed capex – as incurred ....................... 71

          C.1.4       Actual asset disposals– as incurred ............................................. 71

          C.1.5       Tax lives ....................................................................................... 72

          C.1.6       RAB standard lives ....................................................................... 72

          C.1.7       Asset adjustments ........................................................................ 72

          C.1.8       Asset adjustments – TAB remaining lives..................................... 73

          C.1.9       Asset adjustments – RAB remaining lives .................................... 73

          C.1.10      Tax depreciation method (SL/DV) ................................................ 73

           TAB tracking sheet .......................................................................... 73

          C.2.1       Data derived from TAB input sheet............................................... 76

Roll forward model handbook | Electricity distribution network service providers                                             5
          C.2.2       TAB depreciation schedules ......................................................... 77

           Tracking output sheet – TAB .......................................................... 79

           Adding TAB tracking periods to module ....................................... 80

          C.4.1       Updating the TAB input sheet for new regulatory control period ... 81

          C.4.2       Updating the TAB tracking sheet for new regulatory control period84

           Increasing the number of years (columns) in tracking module ... 85




Roll forward model handbook | Electricity distribution network service providers                                6
Shortened forms


Shortened form                         Extended form

AER                                    Australian Energy Regulator

capex                                  capital expenditure

CPI                                    consumer price index

DMS                                    data management system

DV                                     diminishing value

DNSP                                   distribution network service provider

NEL                                    National Electricity Law

NER                                    National Electricity Rules

PTRM                                   post-tax revenue model

RAB                                    regulatory asset base

RIN                                    regulatory information notice

RFM                                    roll forward model

SL                                     straight-line

TAB                                    tax asset base

tracking module                        depreciation tracking module

WACC                                   weighted average cost of capital

WARL                                   weighted average remaining life

year t–1                               final year of the previous regulatory control period

year t–2                               second last year of the previous regulatory control period




Roll forward model handbook | Electricity distribution network service providers                    7
1 Introduction
This handbook sets out the Australian Energy Regulator’s (AER) roll forward model (RFM)
for electricity distribution network service providers (DNSPs). The RFM is a set of two
Microsoft Excel workbooks (each a series of Microsoft Excel spreadsheets) developed in
accordance with the requirements of clause 6.5.1 of the National Electricity Rules (NER).
The main workbook—commonly referred to as ‘the RFM’—is where the majority of the
calculations for rolling forward the asset base are performed. The second workbook, which is
an attachment to the main RFM workbook—referred to as ‘the depreciation tracking
module’—is used to calculate depreciation schedules for a DNSP where relevant. 1 We
prepare and publish the RFM in accordance with the distribution consultation procedures set
out in the NER. 2

1.1 Role of the model
DNSPs are required to submit a completed RFM to us as part of their regulatory proposals.

We use the RFM to determine the closing regulatory asset base (RAB) and tax asset base
(TAB) for a regulatory control period. The closing RAB (and TAB) value for a regulatory
control period becomes the opening RAB (and TAB) to be used for the purposes of making a
building block determination for the next regulatory control period. 3 The roll forward of the
opening RAB (and TAB) for the next regulatory control period, on a forecast indicative basis,
is undertaken in our post-tax revenue model (PTRM) in accordance with the requirements of
the NER.

1.2 Confidentiality
Our obligations regarding confidentiality and the disclosure of information provided to us by a
DNSP are governed by the Competition and consumer Act 2010 (Cth), the National
Electricity Law (NEL) and the NER.

1.3 Process for revision
We may amend or replace the RFM from time to time in accordance with clause 6.5.1(c) of
the NER and the distribution consultation procedures. We will publish a revised version of
this handbook to accompany each version of the RFM we amend or replace in the future.

A version number and an effective date of issue will identify each version of this handbook.




1   The depreciation tracking module uses the year-by-year tracking approach, which tracks the asset classes on a yearly
    basis, in addition to grouping assets by type via asset classes.
2   NER, cl. 6.16.
3   Specifically, the RAB is used to calculate the return on and of capital building blocks. The TAB is used to calculate the
    corporate income tax building block.



Roll forward model handbook | Electricity distribution network service providers                                                8
2 The model
2.1 Overview of the RFM
The RFM is used to calculate the total value of assets for a DNSP across a regulatory
control period. Specifically, the RFM is a set of Microsoft Excel spreadsheets (sheets)
combined into one file that perform calculations to derive a closing RAB for the current
regulatory control period from a given set of inputs. 4 The RFM has a depreciation tracking
module as an attachment, which comprises of a separate set of Microsoft Excel sheets in
one file. The RFM allows the user to vary the inputs in order to assess their impact on the
output data and other derived parameters. Figure 1 provides an overview of this process.

In Figure 1, each box represents a sheet within the RFM. Sheets are classified as primarily
about inputs (left column), calculations (centre column) or outputs (right column). The flow of
data is therefore from left to right, and simplified links between the sheets are shown with
blue arrows.

To operate the RFM, the user enters all the required data on the RFM input sheet—for
example, the opening RAB and TAB values, actual capital expenditure (capex) across the
regulatory control period, or the actual consumer price index (CPI) rate. These inputs often
require reconciliation with previous models (RFM or PTRM) approved for the building block
determination applying to the current regulatory control period, depreciation tracking module
for the upcoming reset, or annual information reported by the DNSPs. In this sense, the
majority of inputs to the RFM will be the output from other parts the previous final decision.

The RFM then uses this data to undertake the RAB (and TAB) roll forward, consistent with
the requirements of the NER. Under this approach, the RAB is rolled forward during each
year of the current regulatory control period by adding capex (net of disposals and capital
contributions 5), subtracting depreciation and indexing for actual CPI in the RAB roll forward
sheet. The required true-up for RAB adjustments (such as for using an estimate of capex) in
the final year of the previous regulatory control period is calculated in the Adjustment for
previous period sheet. The Total RAB roll forward sheet then draws the data from the
RAB roll forward and Adjustment for previous period sheets to bring together the closing
RAB for the current regulatory control period.

The roll forward of the TAB is undertaken in a similar, but simpler manner in the TAB roll
forward sheet. Unlike the RAB, the TAB is not used to derive revenues explicitly and so the
final year capex estimate true-up can be accommodated by replacing with actual capex in
the relevant year of incurrence. 6




4   The set of Microsoft Excel sheets which constitute the RFM were created in Microsoft Excel 2016. We recommend this or
    a later version of Microsoft Excel be used in applying these spreadsheets.
5   These include contributions from customers or governments, or gifted assets.
6   Consistent with tax law, the TAB is rolled forward in nominal dollar terms and so there is no indexation required.



Roll forward model handbook | Electricity distribution network service providers                                            9
Figure 1 Overview of the RFM sheets




The RAB remaining lives and TAB remaining lives sheets roll forward the weighted
average remaining life (WARL) of each asset class based on actual depreciation of the
opening asset value and net capex incurred in each regulatory control period. The weighted
average method is one of two approaches in depreciating the opening RAB and TAB, and is
the default position in the RFM for calculating the remaining asset lives for input to the
PTRM. Some DNSPs adopt the alternative year-by-year tracking approach to calculating


Roll forward model handbook | Electricity distribution network service providers        10
depreciation of the PTRM opening RAB and/or opening TAB values, and so they may use
the accompanying depreciation tracking module for this purpose.

Finally, because the outputs of the RFM become inputs to the PTRM, there is a presentation
sheet which provides a summary of output data in the format required for feeding into the
PTRM.

The user should not alter the names of any sheets or defined name ranges within the RFM.
These RFM components are used when automatically importing into our data management
system (DMS). If these elements are changed, errors may occur.

2.2 DMS input sheet
The DMS input sheet captures business specific, non-financial information that is required
for us to import the RFM into its DMS. To allow this automatic import to take place, the user
should not change the layout of this sheet.

Entity details for the relevant business are recorded in rows 14 to 16. These will be stored in
the DMS. These inputs also control the headings displayed at the top of other sheets in the
RFM.

Context details for the RFM are recorded in the lower section. The stage of the regulatory
process is set in cell C22 using a drop down menu. 7 If this is not enough description to
uniquely identify the RFM submission, a description should be placed in cell C23 (for
example, a resubmission of the regulatory proposal RFM with revised data values after an
error was corrected).

Figure 2 provides an example of the DMS input sheet.

Figure 2 DMS input sheet




7   For example, whether the RFM relates to the regulatory proposal, draft decision, revised regulatory proposal or final
    decision.



Roll forward model handbook | Electricity distribution network service providers                                            11
2.3 RFM input sheet
The RFM input sheet provides for key input variables to be entered in the RFM. They are
automatically linked to corresponding cells in other relevant sheets. Values should be
entered into each cell with light blue shading. This sheet comprises of the following sections:
•   opening RAB and opening TAB
•   actual nominal capex—as incurred
•   actual nominal asset disposals—as incurred
•   actual nominal capital contributions—as incurred
•   actual real net capex—as incurred
•   lagged inflation option
•   inflation and rate of return
•   real straight-line RAB depreciation option
•   forecast/actual year-by-year tracking real straight-line RAB depreciation
•   actual tax depreciation option
•   year-by-year tracking actual tax depreciation
•   forecast nominal final year asset adjustments
•   ex-post review options
•   ex-post review inputs.

The input data to be recorded in the RFM must be in a consistent format as the data
collected from the DNSP in accordance with our regulatory information notice (RIN).

The RFM can accommodate input data for up to 11-year period. This includes the final year
of the previous regulatory control period, as well as up to 10 years of the current regulatory
control period. Input cells outside of the relevant regulatory control period should be left
blank.

The RFM is configured as follows:
•   Uses straight-line (SL) depreciation as the default method for calculating depreciation for
    regulatory purposes—If DNSPs intend to propose other depreciation profiles, it is
    recommended that they raise this as part of pre-lodgement discussions. 8 For example,
    this could take place during the framework and approach process for a determination. 9
•   Uses either the SL method or diminishing value (DV) method for tax depreciation—
    Where DV depreciation applies to the regulatory control period, tax depreciation is
    calculated in the depreciation tracking module and entered as an input to the RFM.
    Where DV depreciation does not apply to the regulatory control period, tax depreciation



8   The depreciation profiles would be subject to satisfying the requirements of clauses 6.5.3 and 6.5.5(b) of the NER.
9   Clause 6.8.1 of the NER sets out the requirements of the framework and approach applying to a determination.



Roll forward model handbook | Electricity distribution network service providers                                          12
    can be calculated using the WARL approach within the RFM or using the year-by-year
    approach in the depreciation tracking module and then entered as an input to the RFM.
•   Recognises capex on a full as incurred approach—This method for recognising capex
    calculates the return on capital and return of capital (regulatory depreciation) based on
    as incurred capex; that is, when expenditure is incurred.

Figure 3 and Figure 4 provide an example of the RFM input sheet.




Roll forward model handbook | Electricity distribution network service providers                13
Figure 3 RFM input sheet–first screenshot




Roll forward model handbook | Electricity distribution network service providers   14
Figure 4 RFM input sheet–second screenshot




Roll forward model handbook | Electricity distribution network service providers   15
2.3.1 Opening regulatory asset base and tax asset base
The opening RAB is the value of assets on which a return will be earned. The opening TAB
is used to calculate the depreciation for tax purposes. The RFM input sheet requires values
for the opening RAB (broken into asset classes in rows 7 to 56) at the start of the final year
of the previous regulatory control period. The values for the opening TAB, also broken into
asset classes, are required at the start of the first year of the current regulatory control
period. 10 The RAB and TAB will differ each year to reflect actual capex, asset disposals,
capital contributions (for the RAB), and regulatory depreciation (for the RAB) or tax
depreciation (for the TAB).

The recorded input values are linked to subsequent sheets which calculate an annual
balance of the RAB and TAB for the current regulatory control period. Notes have been
included for various cells with specific comments and explanations about the relevance of
the inputs.

Asset class name

The asset classes/names are recorded in column F. It is important that the number of asset
classes recorded in the RAB section matches the number of asset classes identified in the
capex section. This allows the RFM to model consistent depreciation across the asset
classes.

The RFM is configured to accommodate up to 50 asset classes. The number of asset
classes used in the RFM will vary between businesses. 11 However, for each business, the
number of asset classes used in the RFM must be consistent with that used in our PTRM to
allow the closing RAB values determined in the RFM to be used as inputs to the opening
RAB values in the PTRM.

RAB values by asset class derived from the RFM may be aggregated or disaggregated into
different classes when forming inputs for the PTRM for the subsequent regulatory control
period where this meaningfully improves the accuracy or administrative convenience of
asset calculations.

Opening asset value

The opening asset values for each asset class are recorded in column I. These values
should be as at the start of the final year of the previous regulatory control period and would
be contained in the RFM used for the current building block determination for the DNSP.
They are linked to the RAB roll forward sheet.

Average remaining life

The remaining lives of each asset class are recorded in column J, based on the economic
lives of the assets as at the start of the current regulatory control period. These values


10   The button at the left of row 53 may be pressed to display/hide rows 37 to 52 (asset classes 31 to 46).
11   Asset classes 47 to 49 in the RFM are designed to be used for assets related to ‘In-house software’ and ‘Buildings’ while
     asset class 50 is designed to be used for 'Equity raising costs', consistent with the PTRM.



Roll forward model handbook | Electricity distribution network service providers                                             16
should be consistent with those contained in the PTRM used in the current building block
determination for the DNSP. They are linked to the RAB roll forward and RAB remaining
lives sheets. These inputs would not be required if the option for depreciating the opening
capital base selected in section 2.3.8 is set to year-by-year tracking, in which case ‘n/a’ is to
be recorded into these cells.

Standard life

The standard lives of each asset class are recorded in column K and measure how long the
infrastructure would physically last if it had just been built. These values should be consistent
with those contained in the PTRM used in the current building block determination for the
DNSP. They are linked to the RAB roll forward and RAB remaining lives sheets.

Forecast net capex

The forecast net capex values for each asset class are recorded in column L. They are
based on the estimates made in the final year of the previous regulatory control period.
These values would be contained in the RFM used for the current building block
determination for the DNSP. They are linked to the Adjustment for previous period and
RAB roll forward sheets.

Forecast regulatory depreciation

The forecast regulatory depreciation values for each asset class are recorded in column M.
They are based on the estimates made for the final year of the previous regulatory control
period. These values would be contained in the RFM used for the current building block
determination for the DNSP. They are linked to the RAB roll forward sheet.

Forecast capital contributions

The forecast capital contribution values for each asset class are recorded in column N. They
are based on the estimates made in the final year of the previous regulatory control period.
These values would be contained in the RFM used for the current building block
determination for the DNSP. They are linked to the TAB roll forward sheet.

Difference in final year capex

The difference in final year capex values for each asset class are recorded in column O.
They are based on the capex 'true-up' adjustment made to the closing RAB for the previous
regulatory control period. These values would be contained in the RFM used for the current
building block determination for the DNSP. These values are linked to the RAB roll forward
sheet.

Return on difference in final year capex

The return on difference in final year capex values for each asset class are recorded in
column P. They are based on the accumulated return associated with the final year capex
'true-up' adjustment made to the closing RAB for the previous regulatory control period.
These values would be contained in the RFM used for the current building block
determination for the DNSP. These values are linked to the RAB roll forward sheet.


Roll forward model handbook | Electricity distribution network service providers                17
Other final year adjustments

The other final year adjustment values for each asset class are recorded in column Q. This
data may be required for DNSPs which adjusted their closing RAB by removing or adding
assets (such as a change in service classification) in the final year of the previous regulatory
control period. 12

The amount of other final year adjustments (if any) would be contained in the RFM used for
the current building block determination for the DNSP. These values are linked to the RAB
roll forward sheet.

Tax asset values—opening tax asset value, average tax remaining life, tax
standard life

The RFM includes a mechanism to roll forward tax asset values between regulatory control
periods. The RFM input sheet requires the tax asset values comprising of the opening tax
values, average tax remaining lives and tax standard lives for each asset class. The RFM is
configured to calculate tax asset values using actual as incurred capex, including the value
of contributed assets, asset disposals and tax depreciation.

For each asset class, the opening tax values at the start of the first year of the current
regulatory control period are recorded in column R, the average tax remaining lives are
recorded in column S and the tax standard lives are recorded in column T. These values are
linked to the TAB roll forward sheet to calculate a running balance of the tax asset values
for the current regulatory control period.

Tax remaining lives are not required if the option for depreciating the opening TAB selected
in section 2.3.10 is set to year-by-year tracking, in which case ‘n/a’ is to be recorded into
these cells.

Base regulatory year

The regulatory year for the start of the current regulatory control period is recorded in
cell U7.

Length of the current regulatory control period

The number of years in the current regulatory control period is recorded in cell V7.

2.3.2 Actual nominal capital expenditure—as incurred13
The actual capex values for the current regulatory control period (including the final year for
the previous regulatory control period) are recorded for each year in rows 61 to 110 (by
asset class). Generally, capex falls into three broad categories:

12   Final year adjustments also include any adjustments from an ex-post review of capex.
13   Actual capex, asset disposals and capital contributions are assumed to be undertaken evenly over a year and therefore
     the reported capex values are assumed to be in middle of the year terms. All other input values are assumed to be in end
     of the year terms. At the time of the final decision, these inputs for the final year of the regulatory control period will remain
     as estimates. These final year estimates will be updated with actuals at the next reset. At the time of the draft decision,
     typically these inputs for the last two years of the regulatory control period will remain as estimates.



Roll forward model handbook | Electricity distribution network service providers                                                    18
•    asset augmentation (e.g. works to enlarge a network or to increase the capability of a
     network)
•    asset replacement (e.g. replacing assets that have passed their useful lives)
•    non-network asset (e.g. support the business expenditure).

These inputs are assumed to be in middle of the year terms based on nominal dollar terms.

In the case where an ex-post review determines that a portion of capex is to be excluded
from the RAB, for those years, the actual gross capex inputs in this sheet should reflect the
efficient capex determined in that review.

2.3.3 Actual nominal asset disposals—as incurred
The actual asset disposal values for each year are recorded in rows 115 to 164. These
inputs are assumed to be in middle of the year terms based on nominal dollar terms.

2.3.4 Actual nominal capital contributions—as incurred
The values of actual assets contributed by other parties over the regulatory control period for
each year are recorded in rows 169 to 218. These inputs are assumed to be in middle of the
year terms based on nominal dollar terms.

2.3.5 Actual real net capital expenditure—as incurred
This section on actual real net capex does not require inputs to be recorded. For each asset
class, actual real net capex values are calculated based on the recorded actual nominal
capex values less asset disposal values and contributed assets, and adjusted for actual
inflation. The real net capex values are displayed in rows 223 to 272 and form part of the roll
forward of the RAB in the Adjustment for previous period and RAB roll forward sheets
and the TAB in the TAB roll forward sheet. These values are assumed to be in middle of
the year terms, based on the final year of the previous regulatory control period real dollar
terms.

2.3.6 Lagged inflation option
The RFM provides the user an option at cell E277 (drop down function) to select the RAB roll
forward to be undertaken using partially-lagged or all-lagged actual inflation, so that either
approach can be applied to particular DNSPs where it aligns with their previous historical
treatment. In practice, this will allow the Victorian DNSPs to remain on the all-lagged
approach, while all other DNSPs use the partially-lagged approach. 14

2.3.7 Inflation and rate of return
This section records the actual annual inflation rates (based on CPI) over the current
regulatory control period and in the previous regulatory control period (rows 282 to 283). If


14   For the reasons on why particular DNSPs are to apply certain approaches, see AER, Final decision, Amendment:
     Electricity distribution network service providers, Roll forward model (version 2), 15 December 2016, pp. 11–13.



Roll forward model handbook | Electricity distribution network service providers                                        19
the partially-lagged approach is selected, actual annual inflation (unlagged) rates are to be
recorded at row 282. If the all-lagged approach is selected, actual annual (one-year lagged)
inflation rates are to be recorded at row 282. Row 283 uses the actual annual inflation rates
at row 282 to calculate the actual inflation (one-year lagged) index.

This section also records the forecast inflation and weighted average cost of capital (WACC)
rates used in the building block determinations (annually updated where relevant)
corresponding to the two regulatory control periods (rows 284 to 289). These parameters are
linked to the Adjustment for previous period and RAB roll forward sheets.

2.3.8 Real straight-line RAB depreciation option
The RFM provides the user an option at cell E293 (drop down function) to select the RAB roll
forward to be undertaken using forecast straight-line depreciation, actual year-by-year
tracking depreciation or actual WARL straight-line depreciation. If forecast depreciation or
actual year-by-year tracking depreciation is selected, the RAB roll forward calculations will
use the depreciation inputs at section 2.3.9 which reflect the approved forecasts for the
current regulatory control period. If actual WARL depreciation is selected, the RAB roll
forward calculations will use the RAB lives and actual capex to calculate depreciation.

2.3.9 Forecast/actual year-by-year tracking real straight-line RAB
      depreciation
When the forecast depreciation option is selected, the approved forecast real straight-line
depreciation values for each year are recorded at rows 299 to 348. 15 The approved forecast
depreciation values would be contained in the PTRM used for the current building block
determination for the DNSP. These values are linked to the RAB roll forward sheet.

When the actual year-by-year tracking depreciation option is selected, real straight-line
depreciation values from the depreciation tracking module for each year are recorded at
rows 299 to 348. 16 Where actual WARL straight-line depreciation is selected, there is no
need to record any inputs in this section as the RFM will calculate the values in the RAB roll
forward sheet.

2.3.10 Actual tax depreciation option
The RFM provides the user an option at cell E353 (drop down function) to select the TAB roll
forward to be undertaken using year-by-year tracking approach or WARL approach for
actual tax depreciation purposes.

If actual year-by-year tracking depreciation option is selected, the TAB roll forward
calculations will use the depreciation inputs at section 2.3.11 which are calculated in the
depreciation tracking module. This will be the case where capex in the regulatory control
period is subject to the DV method.


15   This applies regardless of whether the WARL approach or year-by-year tracking approach is used by the DNSP.
16   The actual depreciation values in the depreciation tracking module may need to be converted to the correct dollar terms
     before entering into the RFM.



Roll forward model handbook | Electricity distribution network service providers                                               20
If actual WARL depreciation is selected, the TAB roll forward calculations will use the tax
lives and actual capex inputs entered in the RFM to calculate tax depreciation using the SL
method.

2.3.11 Year-by-year tracking actual tax depreciation
When the actual year-by-year tracking depreciation option is selected, the calculated actual
tax depreciation values from the depreciation tracking module are recorded in rows 358 to
407. These values are linked to the TAB roll forward sheet. If actual WARL depreciation is
selected, there is no need to record any inputs in this section as the RFM will calculate the
values in the TAB roll forward sheet. This option is only valid for those DNSPs where their
capex incurred in the regulatory control period has not yet been subjected to using the DV
depreciation method arising from the 2018 tax review changes.

2.3.12 Forecast nominal final year asset adjustments
Some DNSPs may need to adjust their closing RAB and TAB at the end of the current
regulatory control period for asset movements (such as a change in service classification).
The values for these asset adjustments and associated remaining asset lives are recorded in
rows 412 to 461, and are linked to the Total RAB roll forward and TAB roll forward
sheets. These values are assumed to be in nominal end of the year terms in the final year of
the current regulatory control period.

2.3.13 Ex-post review options: Adjustments for capex in second
      last year (year t–2) of previous regulatory control period
The RFM is configured to allow adjustments to the RAB and TAB in the case where an ex-
post review determines that a portion of year t–2 actual capex is to be excluded from the roll
forward process. It provides the user with 3 input cells (F467 to F469) containing options
(drop down functions). The options selected determine which, if any, ex-post review inputs
(section 2.3.14) are required and the impact the inputs have on the RAB roll forward and
TAB roll forward.

In the case where there is no revision to year t–2 capex from an ex-post review, the user
simply selects ‘no’ in the first drop down option (cell F467) and is not required to enter any
further inputs in cells F468 and F469, or the inputs in rows 475 to 524 (section 2.3.14).

Is year t–2 capex to be revised?

This drop down function (in cell F467) allows the user to select whether or not year t–2
capex has been revised as a result of an ex-post review. If the user selects ‘yes‘, then further
selections are required in rows 468 and 469, and the user is to enter inputs into the ex-post
review inputs section (section 2.3.14).If the user selects ‘no’ at cell F467, then no further
selections are required in rows 468 and 469, and no input are required for the ex-post review
inputs section (section 2.3.14).

Cell F467 is also referenced in the Adjustment for previous period and TAB roll forward
sheets. The selection determines whether any changes are made to the RAB and TAB for
the ex-post review inputs entered in section 2.3.14.


Roll forward model handbook | Electricity distribution network service providers                 21
Depreciation method for RAB roll forward in previous regulatory control period

This drop down function (in cell F468) allows the user to select the depreciation method
used to roll forward the RAB in the previous regulatory control period (actual or forecast
depreciation).

If actual real SL depreciation is selected—and ‘yes’ is selected in cell F467—then the user is
required to enter the standard lives applicable to the previous regulatory control period for
each asset class in the ex-post review inputs section (section 2.3.14). If forecast real SL
depreciation is selected, there is no need to record any inputs in the ex-post review inputs
section.

Depreciation method for TAB roll forward in previous regulatory control period

This drop down function (in cell F469) allows the user to select the depreciation method
used to roll forward the TAB in the previous period (year-by-year tracking depreciation or
WARL depreciation).

If year-by-year tracking is selected—and ‘yes’ is selected in cell F467—then the user is
required to enter the allowed year t–1 tracked tax depreciation and revised year t–1 tax
depreciation in the ex-post review inputs section (section 2.3.14).

If WARL depreciation is selected—and ‘yes’ is selected in cell F467—then the user is
required to enter the tax standard lives applicable to the previous period for each asset class
in the ex-post review inputs section (section 2.3.14).

2.3.14 Ex-post review inputs: Adjustments for capex in second
      last year (year t–2) of previous regulatory control period
This section for ex-post review inputs in rows 475 to 524 is only required to be completed if
an ex-post review has determined that the capex in year t–2 is to be revised. Where ‘no’ is
selected in F467 indicating that there is no revision to year t–2 capex, these ex-post review
inputs in rows 475 to 524 are not required.

Year t–2 excluded capex (as incurred)

If the user selects ‘yes’ at cell F467, then the amount of capex to be excluded is required to
be recorded in column G for each asset class.

The excluded capex values are equal to the efficient capex (determined during the ex-post
review) less the actual capex (as applied in the RFM used for the current building block
determination for the DNSP).These inputs are assumed to be in middle of the year terms
based on nominal dollar terms. They are referenced in calculating the change to year t–1 tax
depreciation in column M and also in the Adjustment for previous period and the TAB roll
forward sheets.

Standard life for previous regulatory control period

If actual real SL depreciation is selected in cell F468—and ‘yes’ is selected in cell F467—
then the standard lives from the previous period are required to be recorded in column H for
each asset class.

Roll forward model handbook | Electricity distribution network service providers             22
These inputs can be sourced from the RFM used for the current building block determination
for the DNSP. They are referenced in the Adjustment for previous period sheet. 17

Tax standard life for previous regulatory control period

If WARL depreciation is selected in cell F469—and ‘yes’ is selected in cell F467—then the
tax standard lives from the previous period are required to be recorded in column J for each
asset class.

These inputs can be sourced from the RFM used for the current building block determination
for the DNSP. They are referenced in the calculation of the change to year t–1 tax
depreciation in column M.

Previously determined year t–1 tracked tax depreciation

If year-by-year tracking depreciation is selected in cell F469—and ‘yes’ is selected in cell
F467—then the previously determined year t–1 tracked tax depreciation values are required
in column K for each asset class.

These inputs can be sourced from the RFM used for the current building block determination
for the DNSP. They are referenced in the calculation of the change to year t–1 tax
depreciation in column M.

Revised year t–1 tracked tax depreciation

If year-by-year tracking depreciation is selected in cell F469—and ‘yes’ is selected in cell
F467—then the revised year t–1 tax depreciation values are required in column L for each
asset class.

These inputs can be sourced from the depreciation tracking module. 18 They are referenced
in the calculation of the change to year t–1 tax depreciation in column M.

Change to year t–1 tax depreciation

The change to year t–1 tax depreciation is calculated for each asset class in column M.
These values reference the input selections in cells F467 and F469 and values in columns
G, J, K and L.

Where ‘no’ is selected in cell F467 there will be no change to year t–1 tax depreciation.

Where ‘yes’ is selected in cell F467, the change to year t–1 tax depreciation will depend on
the selection in F469 for the type of depreciation used to roll forward the TAB in the previous
regulatory control period:
•    if year-by-year tracking was used: the change to year t–1 tax depreciation equals revised
     year t–1 tax depreciation (recorded in column L) less previously determined year t–1 tax
     depreciation (recorded in column K).

17   They are used to calculate the adjustment to actual nominal depreciation in the final year of the previous regulatory control
     period (year t–1) resulting from the adjustment to capex in the second final year (year t–2)
18   The depreciation tracking module must therefore reflect the revision to capex in year t–2 (and other years where relevant)
     to reflect efficient capex.



Roll forward model handbook | Electricity distribution network service providers                                               23
•   if WARL was used: the change to year t–1 tax depreciation equals year t–2 excluded
    capex (recorded in column G) divided by the tax standard life for the previous regulatory
    control period (recorded in column J)

These values are referenced in the TAB roll forward sheet.

2.4 Adjustment for previous period sheet
The Adjustment for previous period sheet calculates the required true-up of RAB
adjustments to be made for the final year of the previous regulatory control period for
forecast and actual net capex values.

This adjustment is consistent with the requirements of clause S6.2.1(e)(3) of the NER, which
specifies that a reconciliation would include adjustments that remove any benefit or penalty
on the returns associated with any difference between the actual and forecast capex values
for the final year of the previous regulatory control period.

This sheet calculates the difference between actual and forecast net capex for the final
regulatory year of the previous regulatory control period (year t–1), as well as the aggregate
compounded return on that difference (rows 13 to 270). This adjustment is made to the
closing RAB at the end of the current regulatory control period in the Total RAB roll forward
sheet. This two-step process is outlined in Box 1.


Box 1 Adjusting for actual capex in the final year of the previous regulatory control period
(year t–1)

1) Calculating the difference between actual and forecast net capex
    Nominal actual net capex (including a half-year nominal vanilla WACC allowance) –
    Nominal forecast net capex (including a half-year nominal vanilla WACC allowance) =
    Nominal difference between actual and forecast net capex.
2) Calculating the nominal return on the difference and compounding it for each year of the
   current regulatory control period
    Nominal difference between actual and forecast net capex × nominal vanilla WACC per annum
    (compounded)

Notes:

•   Nominal forecast net capex = estimated net capex allowed in the final year of the previous
    regulatory control period.
•   Nominal actual net capex = actual net capex incurred during the final year of the previous
    regulatory control period.

•   The nominal return on the difference between actual and forecast net capex is calculated by
    applying the nominal vanilla WACC (adjusted for actual inflation) applicable to the current
    regulatory control period (as determined in the current building block determination).
•   Each of these adjustments is made to the final closing RAB for the current regulatory control
    period in the Total RAB roll forward sheet.


This sheet also calculates the RAB adjustment where an ex-post review determines that an
amount of year t–2 capex will be excluded from the RAB as well as the aggregate
Roll forward model handbook | Electricity distribution network service providers                    24
compounded return on that excluded capex (rows 274 to 531). This adjustment is made to
the closing RAB at the end of the current regulatory control period in the Total RAB roll
forward sheet. This two-step process is outlined in Box 2.

Box 2 Ex-post review: Adjusting for excluded capex in the second last year of the previous
regulatory control period (year t–2)

1) Calculating the difference between efficient and actual net capex
    Nominal year t–2 capex excluded from RAB (including a half-year nominal vanilla WACC
    allowance and indexed one year) +
    Nominal adjustment to year t–1 straight-line depreciation =
    Nominal RAB adjustment for excluded year t–2 capex.
2) Calculating the nominal return on the adjustment and compounding it for each year of the
   current regulatory control period
    Nominal RAB adjustment for excluded year t–2 capex × nominal vanilla WACC per annum
    (compounded)

Notes:
•   Nominal year t–2 capex excluded from RAB (as entered in the RFM input sheet) = efficient gross
    capex minus the actual gross capex in the second last year of the previous regulatory control
    period.

•   The nominal adjustment to year t–1 straight-line depreciation only applies where the RAB was
    rolled forward in the previous regulatory control period using actual depreciation. It is the year t–2
    excluded capex indexed one year (by lagged CPI) divided by the standard asset life from the
    previous regulatory control period. Where the RAB was rolled forward in the previous regulatory
    control period using forecast depreciation, there is no adjustment to year t–1 straight-line
    depreciation.
•   The nominal return on the difference between efficient and actual net capex is calculated by
    applying the nominal vanilla WACC (adjusted for actual inflation) applicable to the current
    regulatory control period (as determined in the current building block determination).
•   Each of these adjustments is made to the final closing RAB for the current regulatory control
    period in the Total RAB roll forward sheet.



Figure 5 provides an example of the Adjustment for previous period sheet.




Roll forward model handbook | Electricity distribution network service providers                        25
Figure 5 Adjustment for previous period sheet




Roll forward model handbook | Electricity distribution network service providers   26
2.4.1 Nominal adjustments for difference between actual and
      forecast net capex in final year (year t–1)
This section calculates the difference between actual and forecast net capex for the final
year of the previous regulatory control period and determines the compounded return on that
difference. The process involved is based on that depicted in Box 1.

The nominal forecast net capex values for each asset class in the final year of the previous
regulatory control period are displayed in rows 13 to 63. The values are sourced from the
RFM input sheet. Row 13 displays the sum of each asset class values for rows 14 to 63.

The nominal actual net capex values (including a half-year WACC allowance) for each asset
class in the final year of the previous regulatory control period are calculated in rows 65 to
115. Given the timing assumption that capex on average takes place halfway through the
year, a half-year nominal vanilla WACC is applied to the actual net capex for each asset
class to ‘gross-up’ the actual values. 19 Row 65 displays the sum of each asset class
calculations for rows 66 to 115.

The differences between the actual and forecast net capex values are calculated in rows 117
to 167. Row 117 displays the sum of each asset class calculations for those rows. These
values are linked to the Total RAB roll forward sheet.

Finally, in rows 169 to 269 a nominal vanilla WACC (row 6) is applied to calculate the
nominal return on the difference, which is compounded to the end of the current regulatory
control period. 20 The total compounded nominal return at the end of the current regulatory
control period is displayed in row 270. These values are linked to the Total RAB roll
forward sheet.

2.4.2 Ex-post review: Nominal adjustments for excluded capex in
      second last tear (t–2)
This section only applies if there is an ex-post review that determines an amount of year t–2
capex will be excluded from the RAB. It calculates the difference between actual and
efficient capex for the second last year of the previous regulatory control period (year t–2)
and determines the compounded return on that difference. The year t–2 adjustment process
involved is based on that depicted in Box 2.

The nominal values of year t–2 capex excluded from the RAB for each asset class in the
second last year of the previous regulatory control period are calculated in rows 274 to 324.
The values in column F are the inputs from the RFM input sheet including a half-year
WACC allowance to bring them to end of year terms. Row 274 displays the sum of each
asset class values for rows 275 to 324.




19   AER, TNSP roll forward model: Final decision, September 2007. See section 4.3.1 which discusses the need for the
     application of a half-year nominal WACC allowance.
20   The nominal vanilla WACC is based on a fixed real time varying WACC—that is, a fixed real vanilla WACC adjusted for
     actual inflation.



Roll forward model handbook | Electricity distribution network service providers                                           27
The nominal adjustment to year t–1 straight-line depreciation values are calculated in rows
326 to 376. If forecast depreciation was used in the previous regulatory control period and
selected on the RFM input sheet (section 2.3.13) then this adjustment is not required and
will be zero. Where actual depreciation was used in the previous regulatory control period,
this value is calculated as the excluded year t–2 capex divided by the standard asset life
from the previous period. Row 326 displays the sum of each asset class calculations for
rows 327 to 376.

The sum of the t–2 excluded capex and t–1 depreciation adjustment are calculated in rows
378 to 428. Row 379 displays the sum of each asset class calculations for rows 379 to 428.
These values are linked to the Total RAB roll forward sheet.

Finally, in rows 430 to 530 a nominal vanilla WACC (row 6) is applied to calculate the
nominal return on the total adjustment, which is compounded to the end of the current
regulatory control period. 21 The total compounded nominal return at the end of the current
regulatory control period is displayed in row 531. These values are linked to the Total RAB
roll forward sheet.

2.5 RAB roll forward sheet
The RAB roll forward sheet calculates the nominal closing RAB (which becomes the
opening RAB for the following year) for each year of the current regulatory control period.
Under clauses 6.5.1(e) and S6.2.1 of the NER, in rolling forward the RAB each year during
the current regulatory control period, we must have regard to actual data such as capex and
inflation outcomes. Accordingly, the opening RAB for the first year of the current regulatory
control period is rolled forward for:
•    actual net capex (as incurred)
•    regulatory depreciation values (adjusted for actual inflation). 22

Depending on which option for depreciation has been selected in the RFM input sheet, the
RAB roll forward calculations will use either forecast straight-line depreciation, actual year-
by-year straight-line depreciation or actual WARL straight-line depreciation. The choice of
forecast or actual depreciation must be consistent with that determined in the current
building block determination for the DNSP. Forecast straight-line depreciation refers to the
amounts approved for the current regulatory control period, reflecting forecast capex used
for the current building block determination. Actual straight-line depreciation uses the
amounts that are calculated based on actual capex incurred during the current regulatory
control period.

The process for rolling forward the RAB from year to year over the current regulatory control
period, under the full as incurred approach for recognising capex, is set out in Box 3. 23




21   The nominal vanilla WACC is based on a fixed real time varying WACC—that is, a fixed real vanilla WACC adjusted for
     actual inflation.
22   Regulatory depreciation is based on the nominal straight-line depreciation less the inflation applied to the opening RAB.
23   For illustrative purposes this is based on a standard five-year regulatory control period.



Roll forward model handbook | Electricity distribution network service providers                                                 28
Box 3 Rolling forward the RAB in the current regulatory control period

Rolling forward actual net capex and depreciation amounts into the RAB
    Opening RAB for year 1 of the current regulatory control period +
    Nominal actual net capex for year 1 –
    Nominal regulatory depreciation for year 1 =
    Closing RAB for year 1 of the current regulatory control period. This becomes:
    Opening RAB for year 2 of the current regulatory control period +
    Nominal actual net capex for year 2 –
    Nominal regulatory depreciation for year 2 =
    Closing RAB for year 2 of the current regulatory control period. This becomes:
    Opening RAB for year 3 of the current regulatory control period
    …=
    Closing RAB for year 5 of the current regulatory control period =
    Interim closing RAB for the current regulatory control period.

Where:

•   Opening RAB for year 1 of the current regulatory control period = closing RAB for the final year of
    the previous regulatory control period.

•   Nominal actual net capex = real actual net capex (including half-year nominal vanilla WACC
    allowance) adjusted for actual inflation.

•   Nominal regulatory depreciation = Nominal straight-line depreciation – actual inflation adjustment
    on the opening RAB.
Notes:

•   The interim closing RAB for the current regulatory period plus the final adjustments for the final
    year of the current regulatory control period (these adjustments are made in the Total RAB roll
    forward sheet—see Box 4 Box 4 for a description) becomes the opening RAB for the next
    regulatory control period.


Figure 6 provides an example of the RAB roll forward sheet.




Roll forward model handbook | Electricity distribution network service providers                         29
Figure 6 RAB roll forward sheet




2.5.1 Real asset values
Real asset values are displayed in rows 11 to 713. This comprises:
•    real actual net capex
•    real straight-line depreciation.

The real actual net capex values (including a half-year nominal vanilla WACC allowance) are
displayed in rows 11 to 61. 24 Row 11 displays the sum of each asset class values for rows
12 to 61.

These capex values for the current regulatory control period (sourced from the RFM input
sheet) are those provided by the DNSP to us for the purpose of rolling forward its RAB to the
end of the current regulatory control period.

The real straight-line depreciation values are set out at rows 63 to 713. Row 63 displays the
sum of each asset class calculations for rows. If the forecast depreciation option or the
actual year-by-year tracking depreciation option was selected in section 2.3.8, then the
depreciation inputs are sourced from the RFM input sheet. If the actual WARL depreciation
option was selected, then the depreciation values are calculated in the RAB roll forward
sheet based on the opening RAB, actual net capex values and asset lives from the RFM
input sheet.

24   The half-year nominal vanilla WACC is based on a fixed real time varying WACC—that is, a fixed real vanilla WACC
     adjusted for actual inflation.



Roll forward model handbook | Electricity distribution network service providers                                        30
2.5.2 Nominal asset values
Nominal asset values are displayed in rows 717 to 1133. The nominal opening RAB values
for each year are displayed in row 717, based on the sum of each asset class calculations
for rows 718 to 767. The nominal opening RAB for the first year of the current regulatory
control period (cell H717) is calculated by taking the opening RAB value for the final year of
the previous regulatory control period (cell G717), adding forecast net capex value for that
year (G769), adding (typically negative) regulatory depreciation value for that year (G821)
and adding other capex/asset adjustment values where relevant (cells G873, G925 and
G977). These values are all sourced from the RFM input sheet.

The nominal opening RAB values for the remaining years of the current regulatory control
period are calculated in accordance with Box 3. The nominal actual net capex values for
each year (row 769) are equal to the real actual net capex values (row 11) indexed by actual
inflation (row 7). The nominal regulatory depreciation values (row 821) are calculated as the
net total of the nominal straight-line depreciation (row 1031) and the actual inflation applied
to the opening RAB (row 1083).

2.6 Total RAB roll forward sheet
The Total RAB roll forward sheet brings together the relevant data from the Adjustment
for previous period and RAB roll forward sheets to calculate the final closing RAB for the
current regulatory control period in nominal terms. 25

In this sheet, row 7 displays the opening RAB values for each year of the current regulatory
control period, based on the sum of each asset class calculations for rows 8 to 57. These
rows are in turn based on the interim closing RAB in row 321. The calculations at rows 8 to
57 reflect the opening RAB values in the RAB roll forward sheet. The nominal actual net
capex (row 59), regulatory depreciation (row 111) values and other as incurred capex/asset
adjustments that may be required—e.g. difference in final year capex (row 163), return on
difference in final year capex (row 215) and other final year adjustments (row 267) are
sourced from the RAB roll forward sheet.

Rows 373 to 631 represent the required adjustments to be made for the final year (t–1) and
second last year (t–2) of the current regulatory control period, and are sourced from the
Adjustment for previous period and RFM input sheets. These adjustments include:
•    the difference between actual and forecast net capex for the final year of the previous
     regulatory control period (and a compounded return on that difference)
•    an adjustment for any excluded year t–2 capex (and a compounded return on that
     adjustment)
•    other asset adjustments for the final year of the current regulatory control period.

The process for calculating the final closing RAB for the current regulatory control period is
set out in Box 4.




25   This sheet has been configured to display the RAB roll forward for a regulatory control period of 2 to 10 years.



Roll forward model handbook | Electricity distribution network service providers                                        31
Box 4 Calculating the final closing RAB for the current regulatory control period

Adjustments to be made for the final year of the current regulatory control period to calculate
final closing RAB
    Interim closing RAB for the current regulatory control period +
    For year t–1, the difference between nominal actual net capex and forecast net capex +
    Compounded nominal return on that difference for net capex +
    For year t–2, an adjustment for any excluded capex (as determined by an ex-post review) +
    Compounded nominal return on that adjustment +
Final year asset adjustments (where applicable) =
    Closing RAB for the current regulatory control period =
    Opening RAB for the first year of the next regulatory control period.

Note:

•   The opening RAB for the first year of the next regulatory control period becomes an input into the
    PTRM for the purposes of determining the return on capital and return of capital (depreciation) for
    the next regulatory control period.


The closing RAB for the current regulatory control period is shown in row 633. This value
becomes the opening RAB for the next regulatory control period and is used as an input into
the PTRM for calculating the allowed return on capital and the return of capital (depreciation)
in the next building block determination. A breakdown of the closing RAB values by asset
classes are displayed in rows 634 to 683.

Figure 7 provides an example of the Total RAB roll forward sheet.

Figure 7 Total RAB roll forward sheet




Roll forward model handbook | Electricity distribution network service providers                     32
2.7 TAB roll forward sheet
The TAB roll forward sheet calculates the nominal opening TAB values for each year of the
current regulatory control period by taking the opening TAB value for the start of the current
regulatory control period and adjusting for forecast net capex, which was included in the final
year of the previous regulatory control period, with actual net capex for that year. 26 Where
an ex-post review determines a revision to year t–2 capex then the opening TAB is adjusted
for the amount of year t–2 excluded capex and the change to year t–1 depreciation.

The opening TAB value is then rolled forward for actual net capex and tax depreciation
values for each year of the current regulatory control period. Since the calculations are
based on actual nominal data the roll forward of the TAB values does not require any
adjustments for inflation. Any required adjustments to be made to the TAB for the final year
of the current regulatory control period are also applied in this sheet.

The process for rolling forward the TAB for year to year over the current regulatory control
period is set out in Box 5. 27


Box 5 Rolling forward the TAB in the current regulatory control period

Rolling forward actual net capex and depreciation amounts into the TAB
     Opening TAB for the first year of the current regulatory control period –
     Nominal forecast net capex for the final year of the previous period (year t–1) +
     Nominal actual net capex for the final year of the period (year t–1) +
     Any excluded year t–2 capex (as a negative value) from an ex-post review +
     The change to year t–1 depreciation from the change to year t–2 capex =
     Adjusted opening TAB for year 1 of the current regulatory control period.
     Adjusted opening TAB for year 1 of the current regulatory control period +
     Nominal actual net capex for year 1 –
     Nominal actual tax depreciation for year 1 =
     Closing TAB for year 1 of the current regulatory control period. This becomes:
     Opening TAB for year 2 of the current regulatory control period +
     Nominal actual net capex for year 2 –
     Nominal actual tax depreciation for year 2 =
     Closing TAB for year 2 of the current regulatory control period. This becomes:
     Opening TAB for year 3 of the current regulatory control period
     …=
     Closing TAB for year 4 of the current regulatory control period. This becomes:
     Opening TAB for year 5 of the current regulatory control period +


26   For TAB purposes net capex is inclusive of capital contributions (net of disposals).
27   For illustrative purposes this is based on a standard five-year regulatory control period.



Roll forward model handbook | Electricity distribution network service providers                  33
    Nominal actual net capex for year 5 –
    Nominal actual tax depreciation for year 5 +
    Final year asset adjustments (where applicable) =
    Closing TAB for year 5 of the current regulatory control period =
    Opening TAB for the first year of the next regulatory control period.

Where:
•   Nominal actual net capex = nominal actual gross capex – nominal actual asset disposals.
Note:

•   The closing TAB for the current regulatory control period becomes the opening TAB for the next
    regulatory control period.


Figure 8 provides an example of the TAB roll forward sheet.

Figure 8 TAB roll forward sheet




2.7.1 Opening tax asset values
The opening tax asset value (cells H7 to H57) at the start of the first year of the current
regulatory control period is adjusted by removing forecast net capex for the final year of the
previous regulatory control period so that actual net capex for that year is included in the
TAB.

Where an ex-post review determines that a portion of year t–2 actual capex is to be
excluded from the RAB, the opening TAB will also be adjusted by the amount of year t–2
capex to be excluded and the change to depreciation in year t–1.

Roll forward model handbook | Electricity distribution network service providers                     34
Rows 8 to 57 roll forward the opening TAB values for each asset class by taking the
previous year’s nominal opening TAB value, then adding nominal actual net capex for the
year and subtracting nominal actual tax depreciation for the year.

Based on the sum of each asset class calculations for those rows, the opening TAB value for
each year of the current regulatory control period is displayed in row 7. These values are
calculated in accordance with Box 5. For a 5 year regulatory control period, the opening TAB
value for the next regulatory control period is shown in cell M7. This value is used as an
input into the PTRM for calculating the tax depreciation in the next building block
determination. A breakdown of the closing TAB values by asset classes are displayed in
cells M8 to M57.

2.7.2 Actual net capex
The actual net capex values for each asset class (rows 60 to 109) and each year of the
current regulatory control period are calculated by taking nominal actual capex from the RFM
input sheet (rows 61 to 110) and subtracting nominal actual disposals from the same sheet
(rows 115 to 164). Note that the resulting capex used for tax purposes includes the value of
capital contributions. Row 59 displays the sum of each asset class calculations for rows 60
to 109.

2.7.3 Actual tax depreciation
The actual tax depreciation values for each asset class and each year of the current
regulatory control period are presented in rows 112 to 761. Depending on which option for
tax depreciation has been selected in the RFM input sheet, the tax depreciation values will
either be calculated based on the nominal opening TAB values, nominal actual net capex
values and tax asset lives, in accordance with the straight-line method, or adopt the actual
year-by-year tracking depreciation values from the tracking module. Row 111 displays the
sum of each asset class calculations for those rows.

2.8 RAB remaining lives sheet
The RAB remaining lives sheet calculates the average RAB remaining lives of each asset
class using a weighted average method. If the actual WARL depreciation option is selected
in section 2.3.8, the weighted average remaining lives at the end of the current regulatory
control period for the RAB are used as inputs to the PTRM for the next regulatory control
period to calculate the depreciation schedules in the building block determination. The sheet
is set up to accommodate asset life tracking over four five-year periods, however the
calculations can be expanded to cover more if required. 28

For the years in the current regulatory control period, the input cells include formula
references to the appropriate cells from the RFM input sheet. 29 For previous regulatory
control periods, the RAB remaining lives sheet will also require inputs obtained from the


28   The ‘Add extra year to calculation’ button included on this sheet runs a macro to extend the RAB and TAB remaining life
     calculations for each asset class for a further year.
29   This method was first included in version 2 of the distribution RFM to accommodate the impact of forecast depreciation
     being used to roll forward the RAB.



Roll forward model handbook | Electricity distribution network service providers                                               35
RFMs for decisions relating to previous periods. 30 The process for updating this data is set
out in 6.


Box 6 Input process required for updating RAB remaining life calculations

As a first step, the first regulatory year in cell C8 is entered. This input will be the same as the year
entered in the same cell in the RAB remaining lives sheet of the previous RFM. Once the year is
entered, the input cells for the current regulatory control period will reference the inputs from the RFM
input sheet. These values include:

•    CPI
•    nominal vanilla WACC (fixed real time varying)
•    value of net addition (capex)

•    standard asset life
•    value of final year asset adjustments
•    remaining life of final year asset adjustments.
The input cells for the earlier regulatory control periods must be replaced with the actual values
approved in the RFMs for those decisions. 31
These values can be copied from the previous decision RFM's RAB remaining lives sheet for each
year of the preceding periods.

The process for calculating the weighted average remaining lives for the RAB is set out in
Box 7. 32 A similar process applies for calculating the weighted average remaining lives for
the TAB.

Box 7 Calculating the RAB weighted average remaining asset lives

Calculating the RAB weighted average remaining asset lives by asset class
     Opening RAB for start year –
     Total real actual depreciation on opening RAB
     = Closing capital value of opening RAB.
     Real actual net capex for year 1 –
     Total real actual depreciation on net capex for year 1
     = Closing capital value of net capex for year 1.
     ... For each year of actual capex…
     Value of final year RAB adjustments –



30   The input cells for the previous regulatory control periods will display an ‘enter input’ prompt.
31   The exception is in the case where an ex-post review determines that a portion of year t–2 actual capex is to be excluded
     from the RAB. In that case the update for the ‘Value of net addition’ for year t–2 should reflect efficient capex.
32   For assets that do not depreciate, there is no remaining life, and the user should input the remaining life as “n/a”. Note that
     although it is possible to enter “n/a” for some years of capex and a numerical value for others, this is conceptually invalid
     and should not be done.



Roll forward model handbook | Electricity distribution network service providers                                                 36
    Total real actual depreciation on RAB adjustments
    = Closing capital value of RAB adjustments
    Sum of closing capital values
    = Total closing capital value for the asset class.


    Opening RAB average remaining life – number of years of depreciation applied to opening RAB
    = Closing average remaining life of opening RAB
    Asset class RAB standard life – number of years of depreciation applied to capex for year 1
    = Closing average RAB remaining life of capex for year 1
    … For each year of actual capex…
    RAB adjustments average remaining life – number of years of depreciation applied to RAB
    adjustments
    = Closing average remaining life of RAB adjustments.


    Closing capital value of opening RAB ÷ Total closing capital value for the asset class × Closing
    average remaining life of opening RAB +
    Closing capital value of net capex for year 1 ÷ Total closing capital value for the asset class ×
    Closing average RAB remaining life of capex for year 1 +
    … For each year of actual capex … +
    Closing capital value of RAB adjustments ÷ Total closing capital value for the asset class ×
    Closing average remaining life of RAB adjustments
    = Weighted average remaining life for the RAB asset class.

Where:

•   Opening RAB for start year = closing RAB for the final year of the regulatory control period
    preceding first use of version 2 of the RFM.
•   Total real actual depreciation on opening RAB = the sum of the real actual depreciation on
    opening RAB calculated for the regulatory control period.

•   Real actual net capex = real actual net capex (including half-year nominal vanilla WACC
    allowance)
•   Total real actual depreciation on net capex = the sum of the real actual depreciation on net capex
    calculated for the regulatory control period

•   The opening RAB average remaining life is that used for the building block determination where
    version 2 of the RFM is first used.
•   The asset class RAB standard life is that used for the current building block determination.
Note: The calculation of the TAB weighted average remaining lives by asset class follows the same
process, with:

•   opening TAB replacing opening RAB
•   total actual depreciation on opening TAB replacing total real actual depreciation on opening RAB

•   actual net capex (excluding half-year nominal vanilla WACC) replacing real actual net capex


Roll forward model handbook | Electricity distribution network service providers                        37
     (including half-year nominal vanilla WACC)

•    final year TAB adjustments replacing final year RAB adjustments
•    total actual depreciation on net capex replacing total real actual depreciation on net capex
•    opening TAB average remaining life replacing opening TAB average remaining life and

•    asset class TAB standard life replacing asset class RAB standard life, and
•    TAB adjustments average remaining life replacing RAB adjustments average remaining life.


In calculating the weighted average remaining lives for each asset class, first the actual
depreciated capital (or asset) value and remaining life of each capital stream is calculated for
each year. 33 For asset class 1 these calculations in real dollar terms are set out in rows
18 to 39 and 42 to 63 respectively. For each year, the remaining life of each capital stream is
then weighted by its associated closing capital value as a proportion of the total closing
capital value of the asset class. The result is the weighted average remaining life for the
asset class as a whole. For asset class 1, this value is shown in row 65. The weighted
average remaining lives for the other asset classes in the RAB are calculated and shown at
rows 119 to 2711.

Figure 9 provides an example of the RAB remaining lives sheet.




33   A capital stream represents the opening asset value, each individual year of capex, and each asset adjustment for each
     asset class.



Roll forward model handbook | Electricity distribution network service providers                                              38
Figure 9 RAB remaining lives sheet




Roll forward model handbook | Electricity distribution network service providers   39
2.9 TAB remaining lives sheet
The TAB remaining lives sheet calculates the average TAB remaining lives of each asset
class using a weighted average method. The process for calculating the remaining asset
lives for the TAB is broadly the same as described in Box 7. However, all calculations are
performed in nominal dollar terms, and actual net capex is gross capex less disposals (but
including capital contributions) and does not include the half-year nominal vanilla WACC
allowance. If the actual WARL depreciation option is selected in section 2.3.10, the weighted
average remaining lives at the end of the current regulatory control period for the TAB are
used as inputs to the PTRM for the next regulatory control period to calculate the tax
depreciation schedules for the purposes of tax analysis in the building block determination.

For the years in the current regulatory control period, the input cells include formula
references to the appropriate cells from the RFM input sheet. For previous regulatory
control periods the same update process as described in Box 7 is required for the TAB
remaining lives sheet. 34 However, only the opening TAB value, tax asset lives, TAB
adjustments and the remaining tax asset lives of TAB adjustments are required inputs for
this sheet. All other TAB inputs are common with the RAB and therefore sourced from the
RAB remaining lives sheet. The weighted average remaining lives for the asset classes in
the TAB are calculated and shown at rows 60 to 2706.

Figure 10 provides an example of the TAB remaining lives sheet.




34   The input cells for the previous regulatory control periods will display an ‘enter input’ prompt.



Roll forward model handbook | Electricity distribution network service providers                         40
Figure 10        TAB remaining lives sheet




Roll forward model handbook | Electricity distribution network service providers   41
2.10 PTRM input summary sheet
The PTRM input summary sheet outlines the opening RAB values (column J) and the
opening TAB values (column N) for the next regulatory control period. These values are set
out by asset classes in rows 7 to 56, based on the closing RAB and TAB values as
calculated in the RFM. The average remaining lives for regulatory and tax purposes, and the
base regulatory year for the start of the next regulatory control period are also displayed in
columns L, O and Q respectively. All values are outputs from the RFM that need to be
entered into the PTRM input sheet of the PTRM for the next regulatory control period. The
information from the PTRM input summary sheet is sourced from the RFM input, Total
RAB roll forward, TAB roll forward, RAB remaining lives and TAB remaining lives
sheets. 35

Figure 11 provides an example of the PTRM input summary sheet.

Figure 11          PTRM input summary sheet




2.11 Inputs working sheet
The Inputs working sheet allows the user to show the worked calculations for some of the
inputs in the RFM input sheet.


35   Where the RAB value is negative, the remaining life will be set to the lower of the standard asset life for the asset class
     and the regulatory period length. Similarly, where the RAB value is positive but the calculated remaining life is zero, the
     remaining life will be set to the lower of the standard life for the asset class and the regulatory control period length.



Roll forward model handbook | Electricity distribution network service providers                                                   42
A common adjustment made by DNSPs is the adjustment to gross capex for movements in
capitalised provisions. Therefore, we have set up the Inputs working sheet to show this
adjustment to gross capex for capitalised provisions. In the case where a DNSP requires
making this adjustment to its gross capex, it can be done so in the Inputs working sheet
and links the adjusted gross capex in this sheet to the input section for gross capex in the
RFM input sheet.

The user can also use the Inputs working sheet to show calculations for other inputs in the
RFM input sheet—for example the worked calculations for the final year adjustments
section inputs. The user can add this below the section for the adjustments for capitalised
provisions.

Alternatively, if the user does not require any adjustments for capitalised provisions and/or
wants to add other workings more prominently it can remove the capitalised provisions
adjustment calculations from this sheet. We have included a ‘Clear Sheet’ button at the top
of the sheet allowing the user to initiate a macro which deletes the calculations provided.
Figure 12 provides an example of the Inputs working sheet.

Figure 12        Inputs working sheet




Roll forward model handbook | Electricity distribution network service providers                43
         The depreciation tracking module
             Overview of the depreciation tracking module
The depreciation tracking module (tracking module) is used to calculate depreciation
schedules of the RAB and TAB for each asset class across the relevant lives of the assets.
Specifically, the tracking module is an attachment to the RFM—comprising a separate set of
Microsoft Excel sheets in one file—that performs calculations to derive: 36
•    forecast RAB and TAB depreciation schedules for the next regulatory control period
•    actual RAB and TAB depreciation schedules for the current regulatory control period.
The tracking module allows the user to vary the inputs to assess their impact on the output
data and other derived parameters. Figure 13 provides an overview of this process.

In this figure, each box with a dark blue header represents a sheet within the tracking
module. Sheets are classified as primarily about inputs (left column), calculations (centre
column) or outputs (right column). The flow of data is therefore from left to right, and
simplified links between the sheets are shown with blue arrows. The figure also shows the
RFM and PTRM in light blue headers and the outputs from the tracking module that serve as
inputs to the RFM and PTRM.

The user should not alter the names of any sheets or defined name ranges within the
tracking module. These components are used in the formulae and macros included in the
module. If these elements are changed, errors may occur.

A.1.1         RAB depreciation tracking
To operate the tracking module for RAB depreciation, enter the inputs in the RAB input
sheet (section B.1)—for example, the starting RAB 37, actual capex, RAB adjustments, RAB
asset lives, or actual CPI rate. These inputs can be sourced from the accompanying RFM for
the current regulatory control period.

The tracking module then uses this data to calculate the depreciation schedules for each
asset class—disaggregated by the starting RAB, each year of capex, RAB adjustments, and
t–1 and t–2 capex true-ups. Under this approach, these asset values are converted into the
base dollar terms of the tracking module to determine the depreciation profiles of each
disaggregated component in the RAB tracking sheet (section B.2). 38

The RAB tracking summary (section B.3) sheet converts the total depreciation for each
asset class from the RAB tracking sheet to PTRM base dollar terms. 39

36   The set of Microsoft Excel sheets which constitute the tracking module were created in Microsoft Excel 2016. We
     recommend this or a later version of Microsoft Excel be used in applying these spreadsheets.
37   This input is only required for the first period that a business begins year-by-year tracking.
38   The base dollar terms of the tracking module are the end of year dollar terms for the year before the first year of tracked
     capex. For example, if a DNSP begins tracking capex from 2015–16, these dollar terms will be 2014–15 dollar terms.
39   The PTRM base dollar terms refers to the input terms of the PTRM for which the tracking module will provide the forecast



Roll forward model handbook | Electricity distribution network service providers                                              44
Figure 13          Overview of the tracking module sheets




Finally, because the RAB depreciation outputs of the tracking module become inputs to the
PTRM, the Tracking output sheet (section B.4) calculates the forecast RAB depreciation for


    RAB depreciation. It is therefore at end of year dollar terms of the current regulatory control period (in relation to RFM), or
    at the start of the next regulatory control period1 (in relation to PTRM).



Roll forward model handbook | Electricity distribution network service providers                                                 45
each asset class in respect of the next regulatory control period. This sheet provides the
data that serve as inputs to the PTRM in the required format. 40

A.1.2         TAB depreciation tracking
To operate the tracking module for TAB depreciation, enter the inputs in the TAB input
sheet (section C.1)—for example, the starting TAB, actual capex, immediate expensing, TAB
adjustments, tax asset lives, or depreciation approach (SL/DV). These inputs can be
sourced from the accompanying RFM. 41

The tracking module then uses this data to calculate the TAB depreciation schedules for
each asset class—broken down further by the starting TAB, each year of capex (adjusted for
immediate expensing), and TAB adjustments. The depreciation schedule of each
disaggregated component is then calculated in the TAB tracking sheet (section C.2). 42
Finally, because the outputs of the tracking module become inputs to the PTRM and RFM,
the Tracking output sheet (section C.3) summarises the calculated TAB depreciation by
asset class in the format required for feeding into the models. For each asset class it
provides:
•    total forecast tax depreciation for the next regulatory control period which serves as an
     input to the PTRM
•    total actual tax depreciation for the current regulatory control period, which serves as an
     input to the RFM.




40   The tracking module can also be used to derive actual RAB depreciation to be used as an input to the RFM.
41   By default, some of the input sections in the TAB input sheet will reference the corresponding sections in the RAB input
     sheet. These inputs comprise business and regulatory control period data, gross capex, disposals, RAB standard lives and
     asset adjustment remaining lives. Where the tracking module is used for both RAB and TAB depreciation, the default
     formulae in the TAB input sheet will reference the correct values in the RAB input sheet and can be retained. Where only
     TAB depreciation tracking is required, the default formulae in the input cells of the TAB input sheet should be overwritten
     with the appropriate values.
42   For each asset class, the total calculated depreciation includes the impact of immediate expensing.



Roll forward model handbook | Electricity distribution network service providers                                             46
         RAB depreciation tracking
            RAB input sheet
The RAB input sheet provides for key input variables for RAB tracking to be entered in the
tracking module. They are automatically linked to corresponding cells in other relevant
sheets. Values should be entered into each cell with light blue shading. This sheet
comprises the following sections:
•    general information
•    starting RAB and actual gross capex
•    actual asset disposals
•    actual capital contributions
•    RAB lives
•    asset adjustments – RAB
•    asset adjustment remaining life – RAB
•    adjustment for year t–1 capex
•    adjustment for year t–2 capex
•    RFM closing RAB
•    RFM closing RAB – adjusted for mid-period reopeners. 43

Unlike the RFM and the PTRM, the tracking module retains inputs and calculations across
multiple regulatory control periods. For the first regulatory control period when tracking
commences, the user enters the required inputs for that period. For each subsequent reset
the user updates the tracking module by adding the inputs relevant to the new regulatory
control period. Notes have been included for various cells with specific comments and
explanations about the relevance of the inputs.

This sheet also contains two buttons that initiate macros that are used to expand the
calculations of the tracking module—inserting additional regulatory control periods for
continuing the tracking calculations, and extending the number of years for calculating
depreciation. Details of these macros are discussed in sections B.5 and B.6.

Figure 14 provides an example of the RAB input sheet.




43   Reopeners includes contingent projects and cost pass throughs.



Roll forward model handbook | Electricity distribution network service providers             47
Figure 14        RAB input sheet




B.1.1       General information
The RAB input sheet captures some general information required to set up the tracking
module, and calculate values consistently. The recorded input values are linked to
subsequent sheets which calculate depreciation in consistent dollar terms and apply the
correct return where relevant. Notes have been included for various cells with specific
comments and explanations about the relevance/source of the inputs.

Business and tracking period inputs

The business name and applicable depreciation tracking for a regulatory control period
(including start and length) are recorded in rows 8 to 11. This allows the tracking module to
begin tracking at the correct point in time—first regulatory year for tracking—and applies
capex true-ups and adjustments in the correct year—based on the length of a regulatory
control period.


Roll forward model handbook | Electricity distribution network service providers            48
The tracking module template is configured to initially accommodate RAB depreciation
tracking for a single period of 5 years in length. 44 This can be expanded using the macro
buttons (discussed below). For subsequent periods of RAB depreciation tracking, the user
initiates the macro to expand the calculations (section B.5), and enters the regulatory control
period inputs—years and length—in the relevant column. 45

Inflation and rate of return

Actual annual inflation rates—based on CPI—over the relevant years of RAB depreciation
tracking are recorded in rows 14 to 15. It also provides the user an option at cell F13 (drop
down function) to select whether the RAB roll forward is undertaken using the partially-
lagged or all-lagged approach to actual inflation. 46 The selected approach has to align with
the approach applied in the accompanying RFM.

This section also records the WACC rates used in the building block determinations
corresponding to the relevant years of RAB depreciation tracking in rows 17 to 20. These
parameters are linked to the RAB tracking and RAB tracking summary sheets.

B.1.2         Starting RAB and actual gross capex
The starting RAB comprises of the values as at the first year of RAB tracking. It is the
regulatory value of the historical assets at the start of RAB depreciation tracking that will be
depreciated as one group. The actual gross capex is adjusted for asset disposals and capital
contributions to calculate the net capex to be depreciated. The RAB input sheet requires
values for the starting RAB (disaggregated by asset classes in rows 25 to 74) at the start of
depreciation tracking. The values for the actual gross capex—also disaggregated by asset
classes—are required for each year of RAB depreciation tracking.

The recorded input values are linked to the RAB tracking sheet which calculates net capex
and tracks the depreciation of the starting RAB and net capex.

Asset class name

The asset classes/names are recorded in column E. It is important that the asset classes
recorded in the tracking module match the asset classes identified in the accompanying
RFM. This allows the tracking module to link with the RFM and output depreciation profiles in
a consistent format for input to the RFM and PTRM, where relevant.

Consistent with the RFM and PTRM, the tracking module is configured to accommodate up
to 50 asset classes. 47 The number of asset classes used in the tracking module will vary

44   Where the first regulatory control period of RAB depreciation tracking is longer than 5 years, the in-built macros (section
     B.5) can also be used to add the required number of additional years to the first period.
45   For example, where a regulatory control period is for 2020–25, details of this period should be entered in the column for
     2020–21. The tracking module has been configured to provide a prompt (row 9) to assist with entering the relevant years
     and length for future regulatory control periods in the correct column.
46   See section 2.3.6.
47   The asset class names are also referenced in the TAB input sheet by default. Asset classes 47 to 50 are listed as those
     for which the straight-line (SL) method of tax depreciation will apply in the regulatory control periods subsequent to the
     2018 tax review. These are for assets related to ‘In-house software’, ‘Buildings’ and ‘Equity raising costs’.



Roll forward model handbook | Electricity distribution network service providers                                               49
between businesses. However, for each business, the number of asset classes used in the
tracking module must be consistent with that used in the RFM and PTRM to allow the
depreciation schedules determined in the tracking module to be used as inputs to the RFM
and PTRM, where relevant.

Starting RAB

The starting RAB values for each asset class are recorded in column G. The starting RAB is
the closing value of the final year for the previous regulatory control period. This is the same
value as the opening RAB at the start of the current regulatory control period where RAB
depreciation tracking commences. These asset values can be sourced from the Total RAB
roll forward sheet of the accompanying RFM or the PTRM input sheet of the relevant
PTRM. These values are linked to the depreciation calculations in the RAB tracking sheet.

Actual gross capex – as incurred

The actual gross capex values for each year of RAB depreciation tracking are recorded in
column H and beyond. Actual gross capex inputs can be sourced from the RFM input sheet
of the accompanying RFM. These inputs (by asset class in rows 25 to 74) are recognised on
an as incurred basis and are assumed to be in middle of the year terms based on nominal
dollar terms. These values are linked to the depreciation calculations in the RAB tracking
sheet.

Consistent with the RFM, at the time the final decision is made these inputs for the final year
of the current regulatory control period will typically remain as estimates. 48 These final year
estimates will be overwritten with actuals at the next reset. 49

B.1.3         Actual asset disposals – as incurred
The actual asset disposals (recorded in rows 79 to 128) are assumed to be in middle of the
year terms based on nominal dollar terms. Actual asset disposals can be sourced from the
RFM input sheet of the accompanying RFM. 50 These values are linked to the depreciation
calculations in the RAB tracking sheet.

Consistent with the RFM, at the time the final decision is made these inputs for the final year
of the current regulatory control period will typically remain as estimates. 51 These final year
estimates will be overwritten with actuals at the next reset.




48   At the draft decision stage, typically the last two years of the current regulatory control period will remain as estimates.
     This is also consistent with the RFM.
49   In the case where an ex-post review determines that some capex should be excluded from the RAB, for those years, the
     actual gross capex inputs in this sheet should reflect the efficient capex included in the RFM.
50   Consistent with the RFM, at the time the final decision is made these inputs for the final year of the regulatory control
     period will typically remain as estimates. These final year estimates will be updated with actuals at the next reset.
51   At the draft decision stage, typically the last two years of the current regulatory control period will remain as estimates.
     This is also consistent with the RFM.



Roll forward model handbook | Electricity distribution network service providers                                                50
B.1.4         Actual capital contributions – as incurred
The values of actual assets contributed by other parties over the regulatory control period for
each year are recorded in rows 133 to 182.These inputs are assumed to be in middle of the
year terms based on nominal dollar terms. Actual capital contributions can be sourced from
the RFM input sheet of the accompanying RFM. 52 These values are linked to the
depreciation calculations in the RAB tracking sheet.

Consistent with the RFM, at the time the final decision is made these inputs for the final year
of the current regulatory control period will typically remain as estimates. 53 These final year
estimates will be overwritten with actuals at the next reset

B.1.5         RAB lives
The RAB standard lives and remaining lives are recorded in rows 187 to 236. These inputs
can be sourced from the RFM input sheet of the accompanying RFM. They are linked to the
depreciation calculations in the RAB tracking sheet.

RAB remaining lives

The RAB remaining lives of each asset class are recorded in column G and reflect the
economic lives of the tracking module’s starting RAB (section B.1.2). These values should
be consistent with those contained in the RFM for the relevant period of depreciation
tracking. These inputs are referenced in the RAB tracking sheet to calculate the
depreciation of the starting RAB values.

RAB standard lives

The RAB standard lives measure how long the infrastructure would physically last if it had
just been built. The RAB standard lives for each asset class are recorded in rows 187 to 236
for each regulatory control period tracked in the relevant column. 54

The standard lives recorded in column F relate to those for the period preceding the first
regulatory control period when tracking commenced. These standard lives are used to
calculate the depreciation of any true-ups for capex prior to the first regulatory control period
for tracking (sections B.1.8 and B.1.9).

The standard lives recorded in column H relate to the standard lives for the first regulatory
control period when tracking commenced. Standard lives for subsequent regulatory control
periods of RAB depreciation tracking are recorded in the relevant column for those periods
(section B.5.1).


52   Consistent with the RFM, at the time the final decision is made these inputs for the final year of the regulatory control
     period will typically remain as estimates. These final year estimates will be updated with actuals at the next reset.
53   At the draft decision stage, typically the last two years of the current regulatory control period will remain as estimates.
     This is also consistent with the RFM.
54   For example, where a regulatory control period is for 2020–25, the RAB standard lives applicable to this period should be
     entered in the column for 2020–21. The tracking module has been configured to provide a heading prompt (row 131) to
     assist with entering the relevant inputs for future regulatory control periods in the correct column.



Roll forward model handbook | Electricity distribution network service providers                                               51
These values should be consistent with those contained in the PTRM used in the relevant
building block determination for the DNSP. They are referenced in the RAB tracking sheet
to calculate the depreciation of each year of net capex, and any adjustments for the true-up
of capex in year t–1 and year t–2 of the previous regulatory control period.

B.1.6         Asset adjustments
The input section for asset adjustments is primarily for recording final year asset adjustments
at the end of the current regulatory control period. This data may be required where the
DNSP has adjusted its closing RAB by removing or adding assets (such as for a change in
service classification) in the final year of the regulatory control period.

The final year asset adjustments are recorded in rows 240 to 289, and these inputs can be
sourced from the RFM input sheet of the accompanying RFM.

The user can also record RAB asset adjustments in one or more years within a regulatory
control period for depreciation tracking rather than at the end of the period. 55 Where inputs
are recorded for within period asset adjustments (i.e. reflecting mid-period reopeners such
as contingent projects or pass throughs that affect the RAB), these values are referenced in
the RAB input sheet for RFM closing RAB – adjusted for mid-period reopeners (section
B.1.11). The asset adjustments are referenced and used for calculating depreciation in the
RAB tracking sheet.

B.1.7         Asset adjustments – remaining lives
The asset adjustment remaining lives reflect the economic lives of the asset adjustments
(section B.1.6). The remaining lives are recorded in rows 294 to 343 in the same columns as
the associated asset adjustments, and these inputs can be sourced from the RFM input
sheet of the accompanying RFM. The asset adjustments remaining lives are referenced in
the RAB tracking sheet.

B.1.8         Adjustment for difference in t–1 capex
The adjustment for the difference in year t–1 capex is recorded in rows 347 to 396. These
refer to the difference between actual and estimated net capex for the year prior to the first
year where RAB tracking applied.

Adjustment for the difference in year t–1 capex can be sourced from the 'Nominal difference
between actual and forecast net capex' section in the Adjustment for previous period
sheet of the accompanying RFM. These inputs are assumed to be in end of year terms
based on nominal dollar terms.

The adjustment for year t–1 capex is referenced and used for calculating depreciation in the
RAB tracking sheet.

55   We consider that these within-period adjustments would be allowed in the case of reopeners such as a contingent project
     determination where RAB adjustments occur within the period. The tracking module has been configured to provide a
     heading prompt (row 291) to assist with entering the relevant inputs for future regulatory control periods in the correct
     column.



Roll forward model handbook | Electricity distribution network service providers                                            52
B.1.9         Adjustment for excluded t–2 capex
The input section is only relevant for recording any excluded year t–2 capex adjustments
following an ex-post review. 56 The adjustments for excluded year t–2 capex are recorded in
rows 401 to 450 in the relevant column for year t–2. 57 The inputs refer to the amount of
actual year t–2 capex excluded from the RAB as a result of an ex-post review adjustment
applied in a regulatory determination.

These inputs can be sourced from the 'Nominal adjustment for year t–2 capex excluded from
RAB' section in the Adjustment for previous period sheet of the accompanying RFM.
They are assumed to be in end of the year terms based on nominal dollar terms.

The adjustments to year t–2 capex are referenced and depreciated in the RAB tracking
sheet.

B.1.10 RFM closing RAB
The RFM closing RAB values are recorded in rows 456 to 505 in the relevant column for the
final year of the current regulatory control period. 58 The inputs refer to the closing RAB
values calculated in the accompanying RFM for the final year of the current regulatory
control period.

These inputs can be sourced from the PTRM input sheet of the RFM and are linked to the
RFM closing RAB adjusted values (section B.1.11). They are used to calculate the RAB
depreciation schedules for each asset class in the Tracking output sheet. 59

The input cells in column F each contain a ‘yes/no’ switch for each asset class to indicate
whether or the asset class is depreciable. These inputs are referenced in the Tracking
output sheet.

B.1.11 RFM closing RAB (adjusted for mid-period reopeners)
This section on RFM closing RAB adjusted values does not require inputs to be recorded.
For each asset class, the adjusted closing RAB is calculated where RAB adjustments
(section B.1.6) are recorded in one or more years within a period rather than at the end of
the period. The RFM closing RAB values (adjusted for mid-period reopeners) are displayed
in rows 511 to 560.


56   An ex-post review can be undertaken to determine if inefficient capex is to be excluded. Here, 'inefficient' past capex refers
     to three specific assessments (labelled the overspending, margin and capitalisation requirements) detailed in NER, cll.
     S6.2.2A and S6A.2.2A. The details of our assessment approach for an ex-post review are set out in the Capital
     expenditure incentive guideline AER, Capital expenditure incentive guideline, November 2013, pp. 13–17.
57   For example, where a regulatory control period is for 2020–25, the adjustment to t–2 capex applicable to this period should
     be entered in the column for 2018–19.
58   For example, where a regulatory control period is for 2020–25, the RFM closing RAB should be entered in the column for
     2024–25.
59   The RFM closing RAB is equivalent to the PTRM opening RAB. Clause 6.5.5(b)(2) of the NER requires that the sum of the
     real value of the depreciation that is attributable to any asset or category of assets must be equivalent to the value at
     which that asset or category of assets was first included in the RAB for the relevant distribution system.



Roll forward model handbook | Electricity distribution network service providers                                                53
If no mid-period asset adjustments are recorded, the values in the RFM closing RAB
adjusted section will be equal to the RFM closing RAB values (section B.1.10).

Where mid-period asset adjustments are recorded, the RFM closing RAB adjusted values
are required to correctly align the forecast RAB depreciation schedule with the asset values
included in the RAB. This is consistent with the requirements of clause 6.5.5(b)(2) of the
NER.

Figure 15 shows the recorded mid-period asset adjustments and Figure 16 shows the
resulting RFM closing RAB adjusted values.

Figure 15 RAB input sheet—RAB adjustments made within the regulatory
control period




Figure 16          RAB input sheet—RFM closing RAB adjusted values




             RAB tracking sheet
The RAB tracking sheet calculates the real straight-line depreciation schedules for each
asset class (in tracking module base dollar terms). 60 For each asset class the depreciation
schedule is disaggregated into separate RAB tracking components for:
•    the starting RAB
•    each year of tracked capex
•    adjustments to t–1 capex, and where relevant t–2 capex


60   The base dollar terms of the tracking module are the end of year dollar terms for the year before the first year of tracked
     capex. For example, if a DNSP begins tracking capex from 2015–16, these dollar terms will be 2014–15 dollar terms.



Roll forward model handbook | Electricity distribution network service providers                                                   54
•   other RAB adjustments.

Figure 17 provides an example of the RAB tracking sheet.

Figure 17        RAB tracking sheet




Roll forward model handbook | Electricity distribution network service providers   55
The RAB tracking sheet comprises 50 sections—one for each asset class. The data for
Asset class 1 is shown in Figure 18 and comprises:
•    data derived from the RAB input sheet in rows 7 to 14 (cells within the bordered section)
•    calculations for year-by-year real straight-line depreciation of RAB tracking components
     in rows 17 to 34. 61

Figure 18          RAB tracking sheet—Asset class 1




B.2.1         Data derived from RAB input sheet
For each asset class, the bordered section contains data derived from the inputs entered in
the RAB input sheet. This section references the starting RAB, and calculates the net
capex, asset adjustment and capex true-up values in end of year terms in real base dollar
terms (dollar terms are listed in cell F4) for the tracking module. 62 It also references and
calculates the relevant standard and remaining lives for each component from the RAB
input sheet.

For Asset class 1, the starting RAB value and associated remaining life are displayed in cells
G7 and G8 respectively. Net capex and associated standard lives are displayed in rows 7
and 8 in columns H and beyond. Adjustments to t–1 and t–2 capex and their remaining lives
are displayed in rows 9 to 12. Asset adjustments and the relevant remaining lives are
displayed in rows 13 and 14. For each asset class presented, the relative order and location
of these values are the same.


61   By default, the RAB tracking sheet accommodates a single regulatory control period of depreciation tracking. This can be
     expanded to include additional periods as required (section B.5.2).
62   The tracking module base dollar terms are listed in cell F4. They are the end of year dollar terms for the year before the
     first year of tracked capex. For example, if a DNSP begins tracking capex from 2015–16, the RAB tracking sheet will
     display the depreciation calculations in real 2014–15 dollar terms. The RAB tracking sheet then continues displaying the
     data in real 2014–15 dollar terms even when subsequent regulatory control periods capex are added to the tracking
     module.



Roll forward model handbook | Electricity distribution network service providers                                            56
Starting RAB and remaining life

The starting RAB asset value is in end of year terms in real base dollar terms for the tracking
module. This should be consistent with the nominal value entered in the RAB input sheet.
The remaining life displayed is the life which applies to the starting RAB.

Net capex and standard lives
The net capex values are calculated based on the recorded actual nominal capex less asset
disposals and capital contributions. The net capex values are converted to display in end of
year terms in real base dollar terms for the tracking module. 63 The standard lives are listed
for each year of capex and are the same for each year within a regulatory control period.

Adjustments for the difference in t–1 capex and remaining life

The adjustments for the difference in year t–1 capex are converted to display in end of year
terms in real base dollar terms for the tracking module. 64 For the initial regulatory control
period when tracking commences, this value comprises the difference between actual and
estimated year t–1 capex and a return on that difference. For subsequent regulatory control
periods of depreciation tracking it comprises only the return on difference. 65

The remaining life displayed is the life which applies to the adjustment when the value enters
the RAB. 66

Adjustments for excluded t–2 capex and remaining life

Where an ex-post review determines that a portion of year t–2 actual capex is to be
excluded from the RAB, these adjustments to t–2 capex are converted to display in end of
year terms in real base dollar terms for the tracking module. For the initial regulatory control
period when tracking commences, this value comprises an adjustment for excluded year t–2
capex—the difference between efficient and actual year t–2 capex—and a return on that
adjustment. For subsequent regulatory control periods of depreciation tracking it comprises
only the return on the adjustment. 67

The remaining life displayed is the life which applies to the adjustment when the value enters
the RAB. 68

63   The net capex in the RAB tracking sheet is converted by applying CPI and a half year WACC to the nominal mid-year
     inputs in the RAB input sheet.
64   The adjustment for the difference in year t–1 capex in the RAB tracking sheet is converted by applying CPI to the nominal
     end-of-year inputs in the RAB input sheet.
65   This is because for the subsequent regulatory control periods of depreciation tracking the difference in t–1 capex is already
     captured by the inputs on the RFM input sheet when updating the previous estimate of gross capex with actual capex
     incurred.
66   It is equal to the standard life for the relevant year of capex less the time taken for the adjustment to enter the RAB. For a
     typical five year regulatory control period this equates to the standard life less 5 years for a t–1 adjustment.
67   This is because for the subsequent regulatory control periods of depreciation tracking the difference in capex is already
     allowed captured by the inputs on the RFM input sheet when updating the previous actual gross capex with actual
     (efficient) capex determined.
68   It is equal to the standard life for the relevant year of capex less the time taken for the adjustment to enter the RAB and
     further less an additional year. For a typical five year regulatory control period this equates to the standard life less 6 years



Roll forward model handbook | Electricity distribution network service providers                                                   57
Asset adjustment and remaining life
Where a DNSP has other asset adjustments (for example, end of period movements due to
a change in service classification) these values are converted to display in end of year terms
in real base dollar terms for the tracking module. The remaining life displayed is the life
which applies to the asset adjustment.

B.2.2         RAB depreciation schedules
For each asset class, the depreciation schedules—disaggregated by RAB components—are
calculated in real base dollar terms for the tracking module. These values are displayed in
the cells below the data derived from the RAB input sheet.

For Asset class 1, the values are displayed in rows 17 to 34 (Figure 18). The depreciation
schedules relate to:
•    the starting RAB (row 17)
•    actual net capex (rows 18 to 22)
•    adjustments to years t–1 and t–2 capex (row 25)
•    other asset adjustments (rows 28 to 32)
•    total asset class depreciation (row 34).
For each asset class presented, the relative order and location of these values are the same.
The depreciation is calculated on a straight-line basis and begins in the year after the asset
enters the RAB.

Details on adding the depreciation rows required for an additional period of RAB tracking are
discussed in section B.5.

The calculated total depreciation amounts in the RAB tracking sheet are referenced in the
RAB tracking summary sheet and the Tracking output sheet.

             RAB tracking summary sheet
The RAB tracking summary sheet converts the total forecast depreciation for the next
regulatory control period (by asset class) from tracking module base dollar terms to PTRM
base dollar terms. 69 The forecast depreciation schedules are contained in columns H to BP
for each asset class.

The RAB tracking summary sheet also calculates an adjustment to ensure the depreciation
schedules are in accordance with the requirements of the NER. 70 For each asset class, the


     for a year t–2 adjustment.
69   The PTRM base dollar terms refers to the start of year 1 for the next regulatory control period real dollar terms for input to
     the PTRM for which the tracking module will provide the forecast RAB depreciation. It is therefore equivalent to end of year
     real dollar terms for the final year of the current regulatory control period.
70   Clause 6.5.5(b)(2) of the NER requires that the sum of the real value of the depreciation that is attributable to any asset or
     category of assets must be equivalent to the value at which that asset or category of assets was first included in the RAB
     for the relevant distribution system.



Roll forward model handbook | Electricity distribution network service providers                                                58
adjustment is displayed in percentage terms in column E and is equal to the RFM closing
RAB (column D) divided by total forecast depreciation (column G). This adjustment is
referenced in the Tracking output sheet.

Figure 19 provides an example of the RAB tracking summary sheet.

Figure 19          RAB tracking summary sheet




             Tracking output sheet – RAB
The Tracking output sheet outlines the RAB (and TAB) depreciation outputs from the
tracking module in the format required to be used as inputs to the PTRM and RFM, where
relevant.

For RAB depreciation tracking, the Tracking output sheet displays the RAB aligned
forecast depreciation values for the next regulatory control period for each asset class in
rows 8 to 57. The values for the RAB aligned forecast depreciation are displayed in PTRM
base dollar terms and reference the values in the RAB tracking summary sheet. 71


71   The PTRM base dollar terms refers to the start of year 1 for the next regulatory control period real dollar terms for input to



Roll forward model handbook | Electricity distribution network service providers                                                 59
For each asset class, the total forecast RAB depreciation for each year displayed in the RAB
tracking summary sheet is multiplied by the adjustment calculated in column E of that
same sheet. This adjustment ensures that for each asset class the sum of the forecast
depreciation equals the RFM closing RAB value consistent with the requirements of the
NER. 72 A check on this adjustment is performed in column F.

Figure 20 provides an example of the Tracking output sheet. Details of the TAB tracking
depreciation outputs are discussed in section C.3.

Figure 20          Tracking output sheet




             Adding RAB tracking periods to module
The tracking module template is set up by default to accommodate a single five year
regulatory control period of RAB depreciation tracking. For subsequent resets, the tracking
module must be expanded to accommodate capex for new regulatory control periods as part
of continuing the depreciation tracking approach. In order to include additional periods of



     the PTRM for which the tracking module will provide the forecast RAB depreciation. It is therefore equivalent to end of year
     real dollar terms for the final year of the current regulatory control period.
72   Clause 6.5.5(b)(2) of the NER requires that the sum of the real value of the depreciation that is attributable to any asset or
     category of assets must be equivalent to the value at which that asset or category of assets was first included in the RAB
     for the relevant distribution system.



Roll forward model handbook | Electricity distribution network service providers                                                60
RAB depreciation tracking, the user must utilise the in-built macros to expand the
calculations in the tracking module. 73

To include additional periods for RAB tracking, the user is required to:
•    update the RAB input sheet with the relevant capex, asset adjustments, inflation etc.
     This includes updating the estimated capex in the final year of the previous regulatory
     control period (t–1) with actual capex74
•    initiate the ‘Insert additional RAB tracking period’ macro—by pressing the button on the
     RAB input sheet. This will add in the required rows into the RAB tracking sheet to
     calculate depreciation for the new period of capex.

This process is then repeated for each new period of RAB depreciation tracking required.

B.5.1         Updating the RAB input sheet for new regulatory control
              period
To update the RAB input sheet for a new regulatory control period of RAB depreciation
tracking, the user must add the required inputs for the ‘Regulatory period’ and ‘Years in
regulatory period’. These are to be entered in the column relating to the first year of the new
period.

A note ‘input for next period’ appears in row 9 above the required input cells for the new
period. This is shown in Figure 21.

Figure 21          RAB input sheet—Update for new regulatory control period




Figure 22 shows how a user must enter the input data in these cells for a new period. In this
case the period is 2020–25, and is 5 years after the initial (2015–20) period for which RAB
depreciation tracking had commenced. Once the inputs are entered, the labels for the
additional years of capex required appear in row 23.




73   Where the first regulatory control period of RAB depreciation tracking is longer than 5 years, the in-built macros can also
     be used to add the required number of additional years to the first period.
74   If an ex-post review determines that some year t–2 capex is to be excluded then the user will update t–2 capex with the
     approved efficient capex



Roll forward model handbook | Electricity distribution network service providers                                               61
Figure 22          RAB input sheet—Regulatory control period added and labels for
capex




The user must then enter all of the required inputs for the years in the new regulatory control
period that has been added. Figure 23 highlights the required new inputs for the example
above, where the 2020–25 regulatory control period is added to the tracking module. The
new inputs required are:
•    CPI and WACC for the 5 years (2020–25)
•    actual gross capex, disposals and capital contributions for 6 years (2019–25) 75
•    standard lives for the 2020–25 regulatory control period
•    any RAB asset adjustments and associated remaining lives for the 2020–25 regulatory
     control period
•    true-up for actual capex incurred in year t–1 (2019–20)
•    any true-up for efficient capex adjustment in year t–2 (2018–19) 76
•    the RFM closing RAB for 2024–25.




75   In the event of an adjustment to t–2 capex as the result of an ex-post review of actual capex, 7 years of inputs (2018–25)
     would be required to be entered, i.e. revising year t–2 (2018–19) with actual efficient capex determined.
76   Shown as zero in this example but would contain values in the case where an ex-post review determined changes were
     required to previously entered year t–2 (2018–19) actual capex.



Roll forward model handbook | Electricity distribution network service providers                                              62
Figure 23        RAB input sheet—Updated with new inputs for added period




Roll forward model handbook | Electricity distribution network service providers   63
B.5.2        Updating RAB tracking sheet for new regulatory control
             period
To update the RAB tracking sheet for an additional regulatory control period of RAB
depreciation tracking, the user must initiate the ‘Insert additional RAB tracking period’ macro
by pressing the button on the RAB input sheet (step 1).

After initiating the macro, the user is prompted to enter the number of years in the additional
period for tracking—typically 5 years (step 2).

Figure 24 and Figure 25 show the steps for adding an extra five year regulatory control
period.

Figure 24         ‘Insert additional RAB tracking period’ macro—step 1




Figure 25         ‘Insert additional RAB tracking period’ macro—step 2




Running the macro may take a few minutes. The progress of the macro is displayed in the
status bar (bottom left corner) as it steps through the process of updating the tracking
module.

When completed, the RAB tracking sheet should include the following calculations (for a
typical five year regulatory control period): 77
•    five additional rows of net capex depreciation
•    an additional row for the depreciation of t–1 and t–2 capex adjustments
•    five additional rows for the depreciation of asset adjustments.




77   The number of rows added for capex and for asset adjustments will be equal to the number of years added.



Roll forward model handbook | Electricity distribution network service providers                                64
Figure 26 shows the updated RAB tracking sheet layout after the macro has been
completed for an extra five year regulatory control period of RAB depreciation tracking.

Figure 26          RAB tracking sheet: macro complete




            Increasing the number of years (columns) in tracking
            module
By default the tracking module includes 65 years of depreciation calculations. This
accommodates 5 years of capex with a maximum standard asset life of 60 years. For the
correct depreciation schedules to be calculated in the tracking module, it is important that the
value of each asset (or adjustment) is fully depreciated by the end of its standard life in the
tracking module. 78

Figure 27 provides an example where some years of capex have not fully depreciated in the
final year of calculation available in the tracking module. In this case additional years of
calculation are required.




78   The RAB alignment adjustment step adjusts the forecast depreciation profile such that the sum of the depreciation is equal
     to the RFM closing RAB. Therefore, if an asset class is not showing its full depreciation in the tracking module (i.e. the
     year columns have not been extended sufficiently), this RAB adjustment (and resulting depreciation schedule) will be
     inaccurate.



Roll forward model handbook | Electricity distribution network service providers                                            65
Figure 27 RAB tracking sheet—asset not fully depreciated in final year of
calculation




To increase the number of years for calculating depreciation in the tracking module, the user
must initiate the ‘Add years to calculation’ macro using the button in the RAB input sheet as
shown in Figure 28 (step 1).

Figure 28          ‘Add years to calculation’ macro—step 1




After initiating the macro, the user is prompted to enter the number of additional years of
calculation required to be added (step 2). As shown in Figure 29, 10 additional years are
being added. The macro increases the number of years (columns) in all input and tracking
labelled sheets within the tracking module by the number input by the user. 79 There is an
identical button on the TAB input sheet that performs the same function (section C.5).
Regardless of whether the user runs the macro from the RAB input sheet or the TAB input
sheet, the outcome will be the same. 80




79   The ‘Add years to calculation’ macro effectively copies the formulas in the far right column of each sheet within the tracking
     module across to the right by a number of columns equal to the number entered by the user when prompted by the macro
     dialogue box (Figure 29). The macro does this quickly but the same outcome can be achieved by copying the formulas
     across manually.
80   Note that this is different to the ‘Insert additional RAB tracking period’ and ‘Insert additional TAB tracking period’ macros
     which only modify the sheets for which they are pressed.



Roll forward model handbook | Electricity distribution network service providers                                                66
Figure 29 ‘Add years to calculation’ macro: step 2




Figure 30 shows the RAB tracking sheet after the macro has been completed. The final
year column displayed is now 2090–91 (previously 2080–81) and the value of the asset
class is now shown to be fully depreciated before this new final year of calculation.

Figure 30        RAB tracking sheet: macro complete




Roll forward model handbook | Electricity distribution network service providers        67
        TAB depreciation tracking
           TAB input sheet
The TAB input sheet provides for key input variables for TAB tracking to be entered in the
tracking module. They are automatically linked to corresponding cells in other relevant
sheets. Values should be entered into each cell with light blue shading. This sheet
comprises the following sections:
•   general information
•   starting TAB and actual gross capex
•   actual immediately expensed capex
•   Actual asset disposals
•   TAB lives
•   RAB standard lives
•   asset adjustments – TAB
•   asset adjustment remaining life – TAB
•   asset adjustment remaining life – RAB
•   tax depreciation method – straight-line (SL)/diminishing value (DV).
As discussed in section B.1, the tracking module retains inputs and calculations across
multiple regulatory control periods. For the first regulatory control period when tracking
commences, the user enters the required inputs for that period. For each subsequent reset
the user updates the tracking module by adding the inputs relevant to the new regulatory
control period for that reset. Notes have been included for various cells with specific
comments and explanations about the relevance of the inputs.

This sheet also contains two buttons that initiate macros that are used to expand the
calculations of the tracking module—inserting additional regulatory control periods for
continuing the tracking calculations, and extending the number of years for calculating
depreciation. Details of these macros are discussed in sections C.4 and C.5.

Figure 31 provides an example of the TAB input sheet.




Roll forward model handbook | Electricity distribution network service providers             68
Figure 31        TAB input sheet




TAB inputs linked to RAB input sheet

By default, some of the inputs sections in the TAB input sheet reference the corresponding
sections in the RAB input sheet. These inputs comprise of:
•   regulatory periods and years
•   gross capex and disposals
•   RAB standard lives and RAB adjustment remaining lives

Where the tracking module is used for both RAB and TAB depreciation, the default formulae
in the TAB input sheet will reference the correct values in the RAB input sheet and can be
retained. Where only TAB depreciation tracking is required the default formulae in the input
cells of the TAB input sheet should be overwritten with the correct values.

C.1.1       General Information
The TAB input sheet captures some general information required to set up the tracking
module, and calculate values consistently. The recorded input values are linked to
subsequent sheets which calculate depreciation in nominal dollar terms. Notes have been
included for various cells with specific comments and explanations about the
relevance/source of the inputs.

Roll forward model handbook | Electricity distribution network service providers          69
Business and tracking period inputs

The business name and applicable depreciation tracking for a regulatory control period
(including start and length) are recorded in rows 8 to 11. 81 This allows the tracking module to
begin tracking at the correct point in time—first regulatory year for tracking—and applies
adjustments in the correct year—based on the length of a regulatory control period.

The tracking module template is configured to initially accommodate TAB depreciation
tracking for a single period of 5 years. 82 This can be expanded using the macro buttons
(discussed below). For subsequent periods of TAB depreciation tracking, the user initiates
the macro to expand the calculations (section C.4), and enters the regulatory control period
inputs—years and length—in the relevant column. 83

Diminishing value multiplier
The DV multiplier is recorded in row 13 for each year in which the DV method applies. The
multiplier is linked to the TAB tracking sheet to calculate the rate to depreciate capex
incurred in that regulatory year that is subject to the DV method of tax depreciation. 84

C.1.2         Starting TAB and actual gross capex
The starting TAB comprises of the values as at the first year of TAB tracking. It is the tax
value of historical assets at the start of TAB depreciation tracking that will be depreciated as
one group. The actual gross capex is adjusted for asset disposals and immediately
expensed capex to calculate the net capex to be depreciated. The TAB input sheet requires
values for the starting TAB (disaggregated by asset classes in rows 18 to 67) at the start of
depreciation tracking. The values for the actual gross capex—also disaggregated by asset
classes—are required for each year of TAB depreciation tracking.

The recorded input values are linked to the TAB tracking sheet which calculates net capex
and tracks the depreciation of the starting TAB and net capex.

Asset class name

The asset classes/names are recorded in column E. It is important that the asset classes
recorded in the tracking module match the asset classes identified in the accompanying
RFM. This allows the tracking module to link with the RFM and output depreciation profiles in
a consistent format for input to the RFM and PTRM, where relevant.

Consistent with the RFM and PTRM, the tracking module is configured to accommodate up
to 50 asset classes. The number of asset classes used in the tracking module will vary

81   By default these inputs reference the RAB input sheet. They can be overwritten where only TAB tracking applies or where
     otherwise appropriate.
82   Where the first regulatory control period of TAB depreciation tracking is longer than 5 years, the in-built macros (section
     C.4) can also be used to add the required number of additional years to the first period.
83   For example, where a regulatory control period is for 2020–25, details of this period should be entered in the column for
     2020–21.
84   The DV multiplier is determined by the Australian Tax Office (ATO). In addition to the depreciation of net capex, the DV
     multiplier input is also required where DV depreciation is applied to the starting TAB.



Roll forward model handbook | Electricity distribution network service providers                                             70
between businesses. However, for each business, the number of asset classes used in the
tracking module must be consistent with that used in the RFM and PTRM to allow the
depreciation schedules determined in the tracking module to be used as inputs to the RFM
and PTRM where relevant. Asset classes 47 to 50 are those for which the SL method of tax
depreciation will apply in the resets subsequent to the 2018 tax review. 85

Starting TAB

The starting TAB values for each asset class are recorded in column G. The starting TAB is
the opening TAB at the start of the current regulatory control period where TAB depreciation
tracking commences adjusted for actual capex in the final year (t–1) of the previous
regulatory control period. 86 These asset values can be sourced from the TAB roll forward
sheet of the accompanying RFM. These values are linked to the calculation of tax
depreciation in the TAB tracking sheet.

Actual gross capex – as incurred

The actual gross capex values for each year of TAB depreciation tracking are recorded in
column H and beyond (by asset class in rows 18 to 67). 87 These values are linked to the
depreciation calculations in the TAB tracking sheet. Further details for these inputs are set
out in section B.1.2.

C.1.3         Actual immediately expensed capex – as incurred
The actual immediately expensed capex values (recorded in rows 72 to 121) are assumed to
be in middle of the year terms based on nominal dollar terms. They are recorded for the
regulatory year in which the immediate expensing has taken place (or is expected to take
place for the final year of the regulatory control period). 88 These values are linked to the
calculation of tax depreciation in the TAB tracking sheet.

C.1.4         Actual asset disposals– as incurred
Actual asset disposals are recorded in rows 126 to 175. 89 These values are linked to the
depreciation calculations in the TAB tracking sheet. Further details for these inputs are set
out in section B.1.3.




85   These are for assets related to ‘In-house software’, ‘Buildings’ and ‘Equity raising costs’.
86   If an ex-post review determines that some year t–2 capex is to be excluded, the starting TAB would also adjust for the
     change in year t–2 capex.
87   By default these inputs reference the RAB input sheet. They can be overwritten where only TAB tracking applies or where
     otherwise appropriate.
88   At the time the final decision is made these inputs for the final year of the regulatory control period will typically remain as
     estimates. These final year estimates will be updated with actuals at the next reset.
89   By default these inputs reference the RAB input sheet. They can be overwritten where only TAB tracking applies or where
     otherwise appropriate.



Roll forward model handbook | Electricity distribution network service providers                                                  71
C.1.5        Tax lives
The TAB remaining lives and tax standard lives are recorded in rows 180 to 229. These
inputs can be sourced from the RFM input sheet of the accompanying RFM. They are linked
to the depreciation calculations in the TAB tracking sheet.

TAB remaining lives

The TAB remaining lives of each asset class are recorded in column G and reflect the
average tax remaining lives of the assets in existence at the start of TAB depreciation
tracking. These values should be consistent with those contained in the accompanying RFM.
These inputs are referenced in the TAB tracking sheet to calculate the depreciation of the
starting TAB values.

Tax standard lives

The tax standard lives for the first regulatory control period of commencing TAB depreciation
tracking are recorded in column H. Tax standard lives for subsequent regulatory control
periods of TAB depreciation tracking are recorded in the relevant column for those periods
(section C.4.1). These inputs are referenced in the TAB tracking sheet to calculate the
depreciation of each year of net capex.

C.1.6        RAB standard lives
The RAB standard lives measure how long the infrastructure would physically last if it had
just been built. Where the DV depreciation method is used to calculate tax depreciation of
capex, it results in a residual value that does not reduce to zero. The RAB standard lives are
referenced in the TAB tracking sheet to determine the year in which the residual asset
value for each year of capex is written-off. 90

The RAB standard lives for the first regulatory control period of when TAB depreciation
tracking commenced are recorded in column H. For subsequent regulatory control periods of
TAB depreciation tracking they are recorded in the relevant column for those periods
(section C.4.1). 91

C.1.7        Asset adjustments
The input section for asset adjustments is primarily for recording final year asset adjustments
at the end of the current regulatory control period. This data may be required where the
DNSP has adjusted its closing TAB by removing or adding assets (such as for a change in
service classification) in the final year of the regulatory control period.

The final year adjustments are recorded in rows 286 to 334, and these inputs are can be
sourced from the RFM input sheet of the accompanying RFM.

90   AER, Final decision amendment - electricity transmission and distribution network service providers post-tax revenue
     models (version 4). April 2019 pp. 13–16.
91   By default these inputs reference the RAB input sheet. They can be overwritten where RAB and TAB are not tracked from
     the same starting year or where otherwise appropriate.



Roll forward model handbook | Electricity distribution network service providers                                       72
The user can also record RAB asset adjustments in one or more years within a regulatory
control period for depreciation tracking. 92

The TAB adjustments are referenced and used for calculating depreciation in the TAB
tracking sheet.

C.1.8         Asset adjustments – TAB remaining lives
The asset adjustment TAB remaining lives are recorded in rows 340 to 389 in the same
columns as the associated asset adjustments (section C.1.7).

These inputs can be sourced from the RFM input sheet of the accompanying RFM. The
asset adjustment TAB remaining lives are referenced in the TAB tracking sheet.

C.1.9         Asset adjustments – RAB remaining lives
Where the DV depreciation method is used to calculate tax depreciation of an asset
adjustment, it results in a residual value that does not reduce to zero. To determine the year
in which the residual value of the asset adjustment is written-off, the associated RAB
remaining lives are recorded in rows 393 to 442. The RAB remaining lives are required to be
recorded in the same year as the TAB asset adjustment and associated TAB remaining
lives. The RAB remaining lives are referenced in the TAB tracking sheet.

C.1.10 Tax depreciation method (SL/DV)
The depreciation method used to calculate tax depreciation—SL or DV—is recorded in rows
446 to 495 for each asset class. The method that applies to the starting TAB is recorded in
column G. 93 The method that applies to net capex in the first regulatory control period of
TAB depreciation tracking is recorded in column H. For subsequent regulatory control
periods of TAB depreciation tracking they are recorded in the relevant column for that period
(section C.4.1). These inputs are referenced and used for calculating depreciation in the
TAB tracking sheet.

Consistent with the RFM, asset classes 47 to 50 are listed as those to which the SL method
of tax depreciation will apply in regulatory control periods that commence after the 2018 tax
review. These are for assets related to ‘In-house software’, ‘Buildings’ and ‘Equity raising
costs’. Asset classes 47 to 50 do not require the tax depreciation method inputs to be
recorded as they will be SL.

            TAB tracking sheet
The TAB tracking sheet calculates the TAB depreciation schedules for each asset class (in
nominal terms). For each asset class the depreciation schedule is disaggregated into
separate TAB tracking components for:


92   We consider that these within-period adjustments would be allowed in the case of reopeners such as a contingent project
     determination where TAB adjustments occur within the period.
93   For the starting TAB, in most cases the switch will be set to ‘SL’.



Roll forward model handbook | Electricity distribution network service providers                                          73
•   the starting TAB
•   each year of tracked capex
•   other TAB adjustments.
Figure 32 provides an example of the TAB tracking sheet.




Roll forward model handbook | Electricity distribution network service providers   74
Figure 32        TAB tracking sheet




The TAB tracking sheet comprises 50 sections—one for each asset class. The data for
Asset class 1 is shown in Figure 33 and comprises:
•   data derived from the TAB input sheet in rows 7 to 15 (cells within the bordered section)


Roll forward model handbook | Electricity distribution network service providers           75
•    calculations for year-by-year depreciation of TAB tracking components in rows 18 to
     32. 94

Figure 33          TAB tracking sheet—Asset class 1




C.2.1         Data derived from TAB input sheet
For each asset class, the bordered section contains data derived from the inputs entered in
the TAB input sheet. This section references the starting TAB, and calculates the net capex
and asset adjustments in nominal dollar terms. It also references and calculates the relevant
standard and remaining lives from the TAB input sheet.

For Asset class 1, the starting TAB value and associated remaining life are displayed in cells
G7 and G8 respectively. Net capex and associated tax standard lives are displayed in rows
7 and 8 in columns H and beyond. RAB standard lives are displayed in row 9. 95 Immediate
expensing of capex is shown in row 10. Asset adjustments and the relevant TAB remaining
lives are displayed in rows 11 and 12, and their RAB remaining lives are in row 13. 96 The DV
multiplier is shown in row 14 and the SL/DV switch is shown in row 15. For each asset class
presented, the relative order and location of these values are the same.
Unlike RAB depreciation, there is no need to separately track adjustments for year t–1 and
year t–2 capex true-ups. 97




94   By default, the TAB tracking sheet accommodates a single regulatory control period of depreciation tracking. This can be
     expanded to include additional periods as required (section C.4.2).
95   In the case where the TAB depreciation approach of DV is applied to each year of net capex, the RAB standard life is used
     to calculate when the residual TAB value is written down to zero.
96   In the case where the TAB depreciation approach of DV is applied to the TAB asset adjustments, the RAB remaining life is
     used to calculate when the residual TAB value is written down to zero.
97   This is because unlike the RAB roll forward, the actual (and efficient) capex for these years enters the TAB as they are
     incurred.



Roll forward model handbook | Electricity distribution network service providers                                           76
Starting TAB and remaining life

The starting TAB asset value is in end of year nominal terms, consistent with the nominal
values entered in the TAB input sheet. The remaining life displayed is the life which applies
to the starting TAB.

Net capex, tax standard lives and RAB standard lives
The net capex values are calculated based on the recorded actual nominal capex less asset
disposals and immediately expensed capex. The net capex values are displayed in nominal
dollar terms. The tax standard lives and the RAB standard lives are listed for each year of
capex, and are the same for each year within a regulatory control period.

Immediate expensing of capex
Where a DNSP has immediately expensed some of its capex, these values are displayed in
nominal dollar terms.

Asset adjustment, TAB remaining life and, RAB remaining life
Where a DNSP has other asset adjustments (for example, end of period movements due to
a change in service classification) these values are displayed in nominal dollar terms. 98

DV multiplier and SL/DV switch
The DV multiplier and SL/DV switch are listed for each year.

C.2.2        TAB depreciation schedules
For each asset class, the depreciation schedules—disaggregated by TAB components—are
calculated in nominal dollar terms. These values are displayed in the cells below the data
derived from the TAB input sheet.

For Asset class 1, the values are displayed in rows 18 to 32 (Figure 33). The depreciation
schedules relate to:
•    the starting TAB (row 18)
•    actual net capex 99 (rows 19 to 23)
•    asset adjustments (rows 26 to 30)
•    total asset class depreciation (row 32). 100

For each asset class presented, the relative order and location of these values are the same.
The depreciation is calculated on either a straight-line or diminishing value basis depending
on which method is selected. Depreciation begins in the year after the asset enters the TAB.


98  In the case where the TAB depreciation approach of DV is applied to the final year TAB adjustment, the RAB remaining life
    is used to calculate when the residual TAB value is written down to zero.
99 The net capex amounts are after adjustments for immediately expensed capex.
100 The total asset class depreciation includes any amounts for immediate expensing.



Roll forward model handbook | Electricity distribution network service providers                                          77
Details on adding the depreciation rows required for an extra period of TAB tracking are in
section C.4.

The calculated total depreciation amounts in the TAB tracking sheet are referenced in the
Tracking output sheet.

For a DNSP using TAB depreciation tracking for the first time and for which the 2018 tax
review changes apply to the RFM, the starting TAB will remain being subject to SL
depreciation and net capex 101 will be subject to DV depreciation. 102

Straight-line method

The formula used to calculate SL tax depreciation for the depreciation of a year of net capex
is presented as: 103

                         Dt = �Nominal net capexi 104 � ÷ tax standard asset life105

where:

Dt is the tax depreciation in year t

D0 = 0

t = 1,2,3, …

i = year 0

Diminishing value method

Where the DV method applies, the depreciation of the starting TAB will typically still be
calculated using the SL depreciation method. The formula used to calculate DV tax
depreciation for the depreciation of a year of net capex is presented as: 106




101 Net capex allocated to asset classes 47–50 will remain subject to SL depreciation after the tax review findings are
    implemented, reflecting assets which are exempt from the DV method of tax depreciation.
102 The 2018 tax review changes would apply to the RFM from the second reset following the tax review. For further details on
    the tax review’s effect on depreciation in the RFM (and tracking module) and the PTRM, see AER, Explanatory statement
    – Electricity transmission and distribution network service providers - proposed amendments to the roll forward models
    (distribution - version 3) (transmission - version 4), Appendix A Implementation of tax review depreciation findings–flow
    chart, December 2019, p. 25.
103 For the depreciation of TAB asset adjustments, the formula is varied such that the value of the adjustment is used instead
    of the nominal net capex and the remaining tax life of the asset adjustment is used instead of the tax standard asset life.
104 Net capex is equal to gross capex (section C.1.2) net of disposals (section C.1.4) and immediately expensed capex
    (section C.1.30).
105 See section C.1.5.
106 For the depreciation of TAB asset adjustments, the formula is varied such that the value of the adjustment is used instead
    of the nominal net capex and the remaining tax life of the asset adjustment is used instead of the tax standard asset life.



Roll forward model handbook | Electricity distribution network service providers                                             78
                                                t−1

      Dt = �Nominal net capexi 107 − � Dn � × DV multiplier108 ÷ tax standard asset life109
                                     n=0

where:

Dt is the tax depreciation in year t

D0 = 0

t = 1,2,3, …

i = year 0

Capex recognised for tax purposes is net of disposals and immediately expensed capex, but
includes the value of capital contributions. Immediately expensed capex for each regulatory
year (section C.1.3) is added to the total tax depreciation of each asset class for that year. 110

The individual tax depreciation profiles for each asset class can be viewed by expanding the
relevant grouped rows. 111 Tax depreciation is calculated separately because asset values
and asset lives for tax purposes generally differ from those for regulatory purposes.

For each asset class the yearly total tax depreciation is calculated by summing the
depreciation of the starting TAB, net capex and asset adjustments. The total tax depreciation
is summarised in the TAB tracking depreciation tables in the Tracking output sheet.

            Tracking output sheet – TAB
The Tracking output sheet outlines the TAB (and RAB) depreciation outputs from the
tracking module in the format required to be used as inputs to the PTRM and RFM, where
relevant.

For TAB depreciation tracking, the Tracking output sheet displays the forecast tax
depreciation values for the next regulatory control period for each asset class in rows 60 to
109 and the actual tax depreciation values for the current regulatory control period for each
asset class in rows 116 to 165. The values for the forecast and actual tax depreciation are
displayed in nominal dollar terms and reference the values in the TAB tracking sheet.

Figure 34 provides an example of the Tracking output sheet. Details of the RAB tracking
outputs are discussed in section B.4.




107 Net capex is equal to gross capex (section C.1.2) net of disposals (section C.1.4) and immediately expensed capex
    (section C.1.3).
108 See section C.1.1.
109 See section C.1.5.
110 For example, using asset class 1, the immediately expensed capex for the first regulatory year of tracking tax depreciation
    is added to cell H32 in the TAB tracking sheet.
111 The grouped rows for all of the asset classes can be expanded at the same time by pressing the ‘2’ in the top margin to
    the left of the sheet.



Roll forward model handbook | Electricity distribution network service providers                                              79
Figure 34          Tracking output sheet




             Adding TAB tracking periods to module
The tracking module template is set up by default to accommodate a single five year
regulatory control period of TAB depreciation tracking. For subsequent resets, the tracking
module must be expanded to accommodate capex for new regulatory control periods as part
of continuing the depreciation tracking approach. In order to include additional periods of
TAB depreciation tracking, the user must utilise the in-built macros to expand the
calculations in the tracking module. 112

To include additional periods for TAB tracking, the user is required to:
•   update the TAB input sheet with the relevant capex, asset adjustments etc. 113 This
    includes updating the estimated capex in the final year of the previous regulatory control
    period (t–1) with actual capex 114

112 Where the first regulatory control period of TAB depreciation tracking is longer than 5 years, the in-built macros can also
    be used to add the required number of additional years to the first period.
113 In the template tracking module, some of the inputs in the TAB input sheet reference similar inputs in the RAB input
    sheet. So in cases where both RAB and TAB depreciation is tracked then some of the inputs in the TAB input sheet will
    update automatically update. This applies to inputs for regulatory period and years in period, gross capex, disposals, RAB
    standard lives and RAB remaining lives for asset adjustments.
114 If an ex-post review determines that some year t–2 capex is to be excluded then the user will update t–2 capex with the
    approved efficient capex.



Roll forward model handbook | Electricity distribution network service providers                                                  80
•   initiate the ‘Insert additional TAB tracking period’ macro—by pressing the button on the
    TAB input sheet. This will add in the required rows into the TAB tracking sheet to
    calculate depreciation for the new period of capex.

This process is then repeated for each new period of TAB depreciation tracking required.

C.4.1       Updating the TAB input sheet for new regulatory control
            period
To update the TAB input sheet for a new regulatory control period of TAB depreciation
tracking, the user must add the required inputs for the ‘Regulatory period’ and ‘Years in
regulatory period’. These are to be entered in the column relating to the first year of the new
period.

A note ‘input for next period’ appears in row 9 above the required input cells for the new
period. This is shown in Figure 35.

Figure 35        TAB input sheet—Update for additional regulatory control period




Figure 36 shows how a user must enter the input data in these cells for a new period. In this
case the period is 2020–25, and is 5 years after the initial (2015–20) period for which TAB
depreciation tracking had commenced. Once the inputs are entered, the labels for the
additional years of capex required appear in row 16.

Figure 36 TAB input sheet—Regulatory control period added and labels for
gross capex




The user must then enter all of the required inputs for the years in the new regulatory control
period that has been added. Figure 37 highlights the required new inputs for the example




Roll forward model handbook | Electricity distribution network service providers               81
above, where the 2020–25 regulatory control period is added to the tracking module. The
new inputs required are: 115
     •    the DV multiplier
     •    actual gross capex and disposals for 6 years (2019–25) 116
     •    actual immediate expensing for 5 years (2020–25) 117
     •    tax standard lives for the 2020–25 regulatory control period
     •    any TAB asset adjustments and associated remaining lives 118 for the 2020–25
          regulatory control period
     •    tax depreciation approach (DV/SL).




115 This example assumes no ex-post review has determined any change to year t–2 capex. If a review did take place for the
    2020–25 regulatory control period shown, it would consider the 5 years of capex from years t–2 (2018–19) through to year
    3 (2022–23). If the review required revisions to actual capex, then the user would enter the approved efficient level of
    capex for the relevant years within the ex-post review period (2018–23). Therefore, if the review determined that year t–2
    (2018–19) actual capex was to be revised, then the previously entered year t–2 (2018–19) actual capex inputs would need
    to be updated to reflect this in the tracking module.
116 In the event of an adjustment to t–2 capex as the result of an ex-post review of actual capex, 7 years of inputs (2018–25)
    would be required to be entered, i.e. revising year t–2 (2018–19) with actual efficient capex determined..
117 For the roll forward of the TAB in the first period subject to the tax review changes, only 5 years will need to be entered
    because the recognition of immediate expensing starts from year t. For subsequent periods of TAB tracking, year t–1
    immediate expensing inputs should be updated for actuals.
118 For both RAB and TAB remaining lives.



Roll forward model handbook | Electricity distribution network service providers                                            82
Figure 37        TAB input sheet—Updated with new inputs for added period




Roll forward model handbook | Electricity distribution network service providers   83
C.4.2        Updating the TAB tracking sheet for new regulatory control
             period
To update the TAB tracking sheet for an additional regulatory control period of TAB
depreciation tracking, the user must initiate the ‘Insert additional TAB tracking period’ macro
by pressing the button on the TAB input sheet (step 1).

After initiating the macro, the user is prompted to enter the number of years in the additional
period for tracking—typically 5 years (step 2).

Figure 38 and Figure 39 show the steps for adding an extra five year regulatory control
period.

Figure 38         ‘Insert additional TAB tracking period’ macro—Step 1




Figure 39         ‘Insert additional TAB tracking period’ macro—Step 2




Running the macro may take a few minutes. The progress of the macro is displayed in the
status bar (bottom left corner) as it steps through the process of updating the tracking
module.

When completed, the TAB tracking sheet should include the following calculations (for a
typical five year regulatory control period): 119
•   five additional rows of net capex depreciation
•   five additional rows for the depreciation of asset adjustments.

Figure 40 shows the updated TAB tracking sheet layout after the macro has been
completed for an extra five year regulatory control period of TAB depreciation tracking.




119 The number of rows added for capex and for asset adjustments will be equal to the number of years added.



Roll forward model handbook | Electricity distribution network service providers                               84
Figure 40          TAB tracking sheet after macro has completed




             Increasing the number of years (columns) in tracking
             module
As detailed in section B.6, to increase the number of years for calculating depreciation in the
tracking module, the user must initiate the ‘Add years to calculation’ macro. This macro can
be initiated using the button in the TAB input sheet (or RAB input sheet). Regardless of
whether the user runs the macro from the TAB input sheet or the RAB input sheet, the
outcome will be the same. 120




120 Note that this is different to the ‘Insert additional RAB tracking period’ and ‘Insert additional TAB tracking period’ macros
    which only modify the sheets for which they are pressed.



Roll forward model handbook | Electricity distribution network service providers                                                    85

## Powercor_RFM_inputs.xlsx
SHA256: 928075d8ee6ec4b1cd8c310c41a8a9ff893f6130b2859c928986e58c22c2b6ed
来源类型: derived

### 工作表 RFM input
E2=Powercor - RFM Input - DNSP RFM - version 3 | G2=Input cells are in blue
J3=Modifications to base AER model | K3=AER final decision
E5=Opening Regulatory Asset Base for 2020-21 and Opening Tax Asset Base for 2021-22 ($m Nominal)
F6=Asset Class Name | I6=Opening Asset Value (2020) | J6=Average Remaining Life (Year) | K6=Standard Life (Year) | L6=Forecast Net Capex (2020) | M6=Forecast Regulatory Depreciation (2020) | N6=Forecast Capital Contributions (2020) | O6=Forecast Net Capex (HY2021) | P6=Forecast Regulatory Depreciation (HY2021) | Q6=Forecast Capital Contributions (HY2021) | R6=Difference in Final Year (2015) Capex in 2020 terms | S6=Return on Difference in Final Year (2015) Capex in 2020 terms | T6=Other Final Year Adjustments | U6=Opening Tax Asset Value
E7=Asset Class 1 | F7=Subtransmission | I7=556.6499893944305 | J7=n/a | K7=50 | L7=3.430646381427779 | M7=8.048571208074417 | N7=1.429657594281996 | O7=32.14758979460987 | P7=2.701662173295119 | Q7=6.985232329617985 | R7=-0.4629394049551649 | S7=-0.1343388414966863 | T7=0 | U7=525.7773699378637
E8=Asset Class 2 | F8=Distribution system assets | I8=2939.294830207256 | J8=n/a | K8=51 | L8=279.6600947254131 | M8=84.01638471600054 | N8=134.6286917537145 | O8=147.4311542015692 | P8=23.15177980271295 | Q8=31.65267534205357 | R8=-2.758256396789477 | S8=-0.8004092218751807 | T8=-30.33122120492094 | U8=2940.000245480311
E9=Asset Class 3 | F9=Public lighting | I9=6.844000631047956 | J9=n/a | K9=n/a | L9=0 | M9=1.580695641134343 | N9=0 | O9=0 | P9=0.7909740548649413 | Q9=0 | R9=0 | S9=0 | T9=0 | U9=0
E10=Asset Class 4 | F10=SCADA/Network control | I10=73.17248919085556 | J10=n/a | K10=13 | L10=22.62047707800938 | M10=9.205452626341438 | N10=0 | O10=12.21895068831694 | P10=2.989572248186043 | Q10=0 | R10=0 | S10=0 | T10=0 | U10=93.11374486011043
E11=Asset Class 5 | F11=Non-network general assets - IT | I11=88.33312273887549 | J11=n/a | K11=6 | L11=36.86465196632263 | M11=36.17845880918529 | N11=0 | O11=17.76539664161371 | P11=12.57016503385121 | Q11=0 | R11=0 | S11=0 | T11=0 | U11=76.67911827205585
E12=Asset Class 6 | F12=Non-network general assets - Other | I12=224.0589756538664 | J12=n/a | K12=15 | L12=42.52701479772985 | M12=18.51063820409703 | N12=0 | O12=22.13227456416298 | P12=7.429928298134662 | Q12=0 | R12=0 | S12=0 | T12=0 | U12=203.5165507555338
E13=Asset Class 7 | F13=VBRC | I13=154.7946068145716 | J13=n/a | K13=n/a | L13=25.40376371880166 | M13=4.130567258761753 | N13=0 | O13=0 | P13=1.553600278176748 | Q13=0 | R13=0 | S13=0 | T13=0 | U13=147.3066763345617
E14=Asset Class 8 | F14=Land | I14=23.89067175990299 | J14=n/a | K14=n/a | L14=1.000822151768884 | M14=-0.3805593731665979 | N14=0 | O14=0 | P14=-0.3081957717663231 | Q14=0 | R14=0 | S14=0 | T14=0 | U14=33.30517960712559
E15=Asset Class 9 | F15=Accelerated depreciation assets | I15=0 | J15=n/a | K15=n/a | L15=0 | M15=0 | N15=0 | O15=0 | P15=0 | Q15=0 | R15=0 | S15=0 | T15=30.33122120492094 | U15=25.48314732612209
E16=Asset Class 10 | F16=Old SWER ACRs | I16=3.09729065123842 | J16=n/a | K16=n/a | M16=3.097290651238421
E17=Asset Class 11 | F17=0
E18=Asset Class 12 | F18=0
E19=Asset Class 13 | F19=0
E20=Asset Class 14 | F20=0
E21=Asset Class 15 | F21=0
E22=Asset Class 16 | F22=0
E23=Asset Class 17 | F23=0
E24=Asset Class 18 | F24=0
E25=Asset Class 19 | F25=0
E26=Asset Class 20 | F26=0
E27=Asset Class 21 | F27=0
E28=Asset Class 22 | F28=0
E29=Asset Class 23 | F29=0
E30=Asset Class 24 | F30=0
E31=Asset Class 25 | F31=0
E32=Asset Class 26 | F32=0
E33=Asset Class 27 | F33=0
E34=Asset Class 28 | F34=0
E35=Asset Class 29 | F35=0
E36=Asset Class 30 | F36=0
E37=Asset Class 31 | F37=0
E38=Asset Class 32 | F38=0
E39=Asset Class 33 | F39=0
E40=Asset Class 34 | F40=0
E41=Asset Class 35 | F41=0
E42=Asset Class 36 | F42=0
E43=Asset Class 37 | F43=0
E44=Asset Class 38 | F44=0
E45=Asset Class 39 | F45=0
E46=Asset Class 40 | F46=0
E47=Asset Class 41 | F47=0
E48=Asset Class 42 | F48=0
E49=Asset Class 43 | F49=0
E50=Asset Class 44 | F50=0
E51=Asset Class 45 | F51=0
E52=Asset Class 46 | F52=0
E53=Asset Class 47 | F53=0
E54=Asset Class 48 | F54=0
E55=Asset Class 49 | F55=in-house software | I55=0 | J55=n/a | K55=5 | L55=0 | M55=0 | N55=0 | O55=0 | P55=0 | Q55=0 | R55=0 | S55=0 | T55=0 | U55=0
E56=Asset Class 50 | F56=Equity raising costs | I56=19.0875947903976 | J56=n/a | K56=n/a | L56=0 | M56=0.1993828677256921 | N56=0 | O56=1.785406706344591 | P56=0.02444219099723866 | Q56=0 | R56=0 | S56=0 | T56=0 | U56=3.139088545711336
E57=Total | I57=4089.223571832443 | L57=411.5074708194733 | M57=164.5868826093923 | N57=136.0583493479965 | O57=233.4807725966172 | P57=50.90392830845259 | Q57=38.63790767167156 | R57=-3.221195801744642 | S57=-0.934748063371867 | T57=0 | U57=4048.321121119395
E59=Actual Capital Expenditure – As Incurred ($m Nominal)
E60=Year | F60=2020 | G60=HY2021 | H60=2021-22 | I60=2022-23 | J60=2023-24 | K60=2024-25 | L60=2025-26 | M60=2026-27 | N60=2027-28 | O60=2028-29 | P60=2029-30 | Q60=2030-31
E61=Subtransmission | F61=7.077317030000001 | G61=30.4915315763405 | H61=131.21318402 | I61=1.50547982 | J61=0.46842118 | K61=84.52598110999999 | L61=72.88054131492781
E62=Distribution system assets | F62=420.48420874 | G62=185.3733435000197 | H62=292.95641208 | I62=451.59225278 | J62=467.66128295 | K62=459.9760303899999 | L62=487.73900726144
E63=Public lighting | F63=0 | G63=0 | H63=0 | I63=0 | J63=0 | K63=0 | L63=0
E64=SCADA/Network control | F64=20.18786627 | G64=10.78579627660649 | H64=4.12580955 | I64=6.94577102 | J64=6.945864889999999 | K64=0.39697996 | L64=8.73104516489145
E65=Non-network general assets - IT | F65=34.80915085 | G65=17.82582329062194 | H65=5.5161709 | I65=7.768108859999999 | J65=7.71809356 | K65=7.1004551 | L65=9.56735159415531
E66=Non-network general assets - Other | F66=43.43735354 | G66=30.23968453540937 | H66=34.38954712 | I66=63.21257378 | J66=58.27981210000001 | K66=56.88018015 | L66=31.67208201417084
E67=VBRC | F67=13.71430507 | G67=2.048014498329731 | H67=0 | I67=0 | J67=0 | K67=0 | L67=0
E68=Land | F68=0 | G68=0 | H68=0 | I68=0 | J68=0 | K68=0 | L68=0
E69=Accelerated depreciation assets | F69=0 | G69=0 | H69=0 | I69=0 | J69=0 | K69=0 | L69=0
E70=Old SWER ACRs
E71=0
E72=0
E73=0
E74=0
E75=0
E76=0
E77=0
E78=0
E79=0
E80=0
E81=0
E82=0
E83=0
E84=0
E85=0
E86=0
E87=0
E88=0
E89=0
E90=0
E91=0
E92=0
E93=0
E94=0
E95=0
E96=0
E97=0
E98=0
E99=0
E100=0
E101=0
E102=0
E103=0
E104=0
E105=0
E106=0
E107=0
E108=0
E109=in-house software | F109=0 | G109=0 | H109=21.98819423 | I109=31.07243544 | J109=30.87237421 | K109=28.4018214 | L109=30.04003621016085
E110=Equity raising costs | F110=0 | G110=1.76444421337755 | H110=0 | I110=0 | J110=0 | K110=0 | L110=0
E111=Total | F111=539.7102015 | G111=278.5286378907053 | H111=490.1893179 | I111=562.0966217 | J111=571.94584889 | K111=637.2814481099999 | L111=640.6300635597463 | M111=0 | N111=0 | O111=0 | P111=0 | Q111=0
R112=3180.671938050451
E113=Actual Asset Disposal – As Incurred ($m Nominal)
E114=Year | F114=2020 | G114=HY2021 | H114=2021-22 | I114=2022-23 | J114=2023-24 | K114=2024-25 | L114=2025-26 | M114=2026-27 | N114=2027-28 | O114=2028-29 | P114=2029-30 | Q114=2030-31
E115=Subtransmission | F115=0 | G115=0 | H115=0 | I115=0 | J115=0 | K115=0 | L115=0
E116=Distribution system assets | F116=0 | G116=0 | H116=19.39434845 | I116=60.5951 | J116=30.46907452 | K116=0.019079 | L116=3.96690112856998
E117=Public lighting | F117=0 | G117=0 | H117=0 | I117=0 | J117=0 | K117=0 | L117=0
E118=SCADA/Network control | F118=0 | G118=0 | H118=0 | I118=0 | J118=0 | K118=0 | L118=0
E119=Non-network general assets - IT | F119=0 | G119=0 | H119=0 | I119=0 | J119=0 | K119=0 | L119=0
E120=Non-network general assets - Other | F120=0.96249947 | G120=2.04062765 | H120=3.05522495 | I120=1.33387998 | J120=1.01834844 | K120=1.312684 | L120=1.355151052239107
E121=VBRC | F121=0 | G121=0 | H121=0 | I121=0 | J121=0 | K121=0 | L121=0
E122=Land | F122=0 | G122=0 | H122=0 | I122=0 | J122=0 | K122=0 | L122=0
E123=Accelerated depreciation assets | F123=0 | G123=0 | H123=0 | I123=0 | J123=0 | K123=0 | L123=0
E124=Old SWER ACRs
E125=0
E126=0
E127=0
E128=0
E129=0
E130=0
E131=0
E132=0
E133=0
E134=0
E135=0
E136=0
E137=0
E138=0
E139=0
E140=0
E141=0
E142=0
E143=0
E144=0
E145=0
E146=0
E147=0
E148=0
E149=0
E150=0
E151=0
E152=0
E153=0
E154=0
E155=0
E156=0
E157=0
E158=0
E159=0
E160=0
E161=0
E162=0
E163=in-house software | F163=0 | G163=0 | H163=0 | I163=0 | J163=0 | K163=0 | L163=0
E164=Equity raising costs | F164=0 | G164=0 | H164=0 | I164=0 | J164=0 | K164=0 | L164=0
E165=Total | F165=0.96249947 | G165=2.04062765 | H165=22.4495734 | I165=61.92897998 | J165=31.48742296 | K165=1.331763 | L165=5.322052180809088 | M165=0 | N165=0 | O165=0 | P165=0 | Q165=0
R166=124.5604191708091
E167=Actual Capital Contributions – As Incurred ($m Nominal)
E168=Year | F168=2020 | G168=HY2021 | H168=2021-22 | I168=2022-23 | J168=2023-24 | K168=2024-25 | L168=2025-26 | M168=2026-27 | N168=2027-28 | O168=2028-29 | P168=2029-30 | Q168=2030-31
E169=Subtransmission | F169=1.42965759 | G169=7.456049503901446 | H169=31.88367714 | I169=1.9565832 | J169=0.41864911 | K169=24.790398 | L169=17.08390876245572
E170=Distribution system assets | F170=134.62869175 | G170=48.1057894190564 | H170=49.80556179 | I170=86.25364654 | J170=95.91157856999999 | K170=135.021562 | L170=114.3307740256652
E171=Public lighting | F171=0 | G171=0 | H171=0 | I171=0 | J171=0 | K171=0 | L171=0
E172=SCADA/Network control | F172=0 | G172=0 | H172=0 | I172=0 | J172=0 | K172=0 | L172=0
E173=Non-network general assets - IT | F173=0 | G173=0 | H173=0 | I173=0 | J173=0 | K173=0 | L173=0
E174=Non-network general assets - Other | F174=0 | G174=0 | H174=0 | I174=0 | J174=0 | K174=0 | L174=0
E175=VBRC | F175=0 | G175=0 | H175=0 | I175=0 | J175=0 | K175=0 | L175=0
E176=Land | F176=0 | G176=0 | H176=0 | I176=0 | J176=0 | K176=0 | L176=0
E177=Accelerated depreciation assets | F177=0 | G177=0 | H177=0 | I177=0 | J177=0 | K177=0 | L177=0
E178=Old SWER ACRs
E179=0
E180=0
E181=0
E182=0
E183=0
E184=0
E185=0
E186=0
E187=0
E188=0
E189=0
E190=0
E191=0
E192=0
E193=0
E194=0
E195=0
E196=0
E197=0
E198=0
E199=0
E200=0
E201=0
E202=0
E203=0
E204=0
E205=0
E206=0
E207=0
E208=0
E209=0
E210=0
E211=0
E212=0
E213=0
E214=0
E215=0
E216=0
E217=in-house software | F217=0 | G217=0 | H217=0 | I217=0 | J217=0 | K217=0 | L217=0
E218=Equity raising costs | F218=0 | G218=0 | H218=0 | I218=0 | J218=0 | K218=0 | L218=0
E219=Total | F219=136.05834934 | G219=55.56183892295785 | H219=81.68923893 | I219=88.21022974 | J219=96.33022768 | K219=159.81196 | L219=131.4146827881209 | M219=0 | N219=0 | O219=0 | P219=0 | Q219=0
R220=613.0181780610787
E275=Lagged Inflation Option
G276=Partially-lagged Inflation
E277=All-lagged Inflation | G277=All-lagged Inflation
G278=All-lagged
E280=Inflation and Rate of Return
E281=Year | F281=2020 | G281=HY2021 | H281=2021-22 | I281=2022-23 | J281=2023-24 | K281=2024-25 | L281=2025-26 | M281=2026-27 | N281=2027-28 | O281=2028-29 | P281=2029-30 | Q281=2030-31
E282=Lagged Actual CPI Inflation Rate | F282=0.01592920353982308 | G282=0.01219512195121952 | H282=0.008605851979345935 | I282=0.03498293515358353 | J282=0.07831821929101412 | K282=0.04051987767584087 | L282=0.02424687729610597
E283=Actual CPI (one year lagged) | F283=0.9879518072289156 | G283=1 | H283=1.008605851979346 | I283=1.043889845094664 | J283=1.125645438898451 | K283=1.171256454388984 | L283=1.199655765920826 | M283=1.199655765920826 | N283=1.199655765920826 | O283=1.199655765920826 | P283=1.199655765920826 | Q283=1.199655765920826
E284=Forecast Inflation Rate | F284=0.0234949725108347 | G284=0.01118103794611125 | H284=0.01999387250484763 | I284=0.01999387250484763 | J284=0.01999387250484763 | K284=0.01999387250484763 | L284=0.01999387250484763 | M284=0.01999387250484763 | N284=0.01999387250484763 | O284=0.01999387250484763 | P284=0.01999387250484763 | Q284=0.01999387250484763
E285=Forecast Inflation Cumulative Index | G285=1 | H285=1.019993872504848 | I285=1.040387499947435 | J285=1.061188874977022 | K285=1.082406150046875 | L285=1.104047640609375 | M285=1.126121828374997 | N285=1.148637364636452 | O285=1.171603073659298 | P285=1.195027956140329 | Q285=1.218921192735128
E287=Nominal Vanilla WACC | F287=0.05790594216202211 | G287=0.0228763488611472 | H287=0.04726714774933895 | I287=0.04636135438647948 | J287=0.0468620984033168 | K287=0.04705443751223788 | L287=0.04724967736252034
