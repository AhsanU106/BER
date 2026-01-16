from report_generator import generate_report

# Define sections
sections = {
    "Foreword": {
        "query": None,
        "prompt": """
Generate an introduction for a Budget Execution Report (BER) for the fiscal year {fiscal_year}.
**Instructions:**
- Clearly state the purpose of the BER.
- Mention legal compliance (Punjab Public Financial Management Act 2022, Section-41).
- Explain the BER’s role in comparing **actual vs budgeted** revenue & expenditure.
- Highlight its importance in assessing budgetary performance and informing future fiscal decisions.
- Emphasize **government commitment to transparency**.
""",
        "params": {"fiscal_year": "2023-24"}
    },
   "Macroeconomic Assumptions": {
    "query": """
    SELECT 
        MAX(CASE WHEN Indicator = 'Size of GDP (market prices) (Rs Billion)' THEN "Actual FY 2022-23" END) AS nominal_gdp_previous,
        MAX(CASE WHEN Indicator = 'Inflation (%)' THEN "Actual FY 2022-23" END) AS inflation_previous
    FROM macroeconomic_assumptions
    WHERE Indicator IN ('Size of GDP (market prices) (Rs Billion)', 'Inflation (%)');
    """,
    "prompt": """
Generate a "Macroeconomic Assumptions" section for the Budget Execution Report for FY {fiscal_year}.
The section must be long and detailed and discuss each indicator in depth.

*Instructions:*
- Start with an overview of the macroeconomic context for FY {fiscal_year}.
- Use the extracted data (nominal_gdp_previous, inflation_previous) to provide insights into:
  - The size of the GDP and its implications for economic growth.
  - The inflation rate and its impact on purchasing power and fiscal policy.
- Discuss trends compared to previous years and their relevance to the current fiscal year.
- Maintain a formal tone and ensure the content is analytical and data-driven.

*Example Structure:*
1. *Overview*: Briefly describe the macroeconomic environment for FY {fiscal_year}.
2. *GDP Analysis*:
   - Discuss the size of the GDP (nominal_gdp_previous) for the previous fiscal year.
   - Explain its implications for economic growth and fiscal planning.
3. *Inflation Analysis*:
   - Analyze the inflation rate (inflation_previous) for the previous fiscal year.
   - Highlight its impact on consumer spending, monetary policy, and government finances.
4. *Trends and Outlook*:
   - Compare these indicators with historical data to identify trends.
   - Discuss how these trends might influence fiscal decisions in FY {fiscal_year}.
"""
},
   "Analysis of Receipts - 3.1.1 Provincial General Revenue Receipts": {
    "query": """
    WITH grr_data AS (
        SELECT 
            MAX(CASE WHEN col_0 = 'Federal Divisible Pool Transfers' THEN "Actual_Collection_2022-23" END) AS fdp_previous,
            MAX(CASE WHEN col_0 = 'Federal Divisible Pool Transfers' THEN "B.E_2023-24" END) AS fdp_target,
            MAX(CASE WHEN col_0 = 'Federal Divisible Pool Transfers' THEN "Actual_Collection__2023-24" END) AS fdp_actual,
            MAX(CASE WHEN col_0 = 'Federal Divisible Pool Transfers' THEN "%_Collection_w.r.t._BE_2023-24" END) AS fdp_achievement,
            MAX(CASE WHEN col_0 = 'Federal Divisible Pool Transfers' THEN "YoY-_growth" END) AS fdp_yoy_growth,

            MAX(CASE WHEN col_0 = 'Provincial tax' THEN "Actual_Collection_2022-23" END) AS prov_tax_previous,
            MAX(CASE WHEN col_0 = 'Provincial tax' THEN "B.E_2023-24" END) AS prov_tax_target,
            MAX(CASE WHEN col_0 = 'Provincial tax' THEN "Actual_Collection__2023-24" END) AS prov_tax_actual,
            MAX(CASE WHEN col_0 = 'Provincial tax' THEN "%_Collection_w.r.t._BE_2023-24" END) AS prov_tax_achievement,
            MAX(CASE WHEN col_0 = 'Provincial tax' THEN "YoY-_growth" END) AS prov_tax_yoy_growth,

            MAX(CASE WHEN col_0 = 'Provincial non-tax' THEN "Actual_Collection_2022-23" END) AS prov_non_tax_previous,
            MAX(CASE WHEN col_0 = 'Provincial non-tax' THEN "B.E_2023-24" END) AS prov_non_tax_target,
            MAX(CASE WHEN col_0 = 'Provincial non-tax' THEN "Actual_Collection__2023-24" END) AS prov_non_tax_actual,
            MAX(CASE WHEN col_0 = 'Provincial non-tax' THEN "%_Collection_w.r.t._BE_2023-24" END) AS prov_non_tax_achievement,
            MAX(CASE WHEN col_0 = 'Provincial non-tax' THEN "YoY-_growth" END) AS prov_non_tax_yoy_growth,

            MAX(CASE WHEN col_0 = 'General Revenue Receipts' THEN "Actual_Collection_2022-23" END) AS grr_previous,
            MAX(CASE WHEN col_0 = 'General Revenue Receipts' THEN "B.E_2023-24" END) AS grr_target,
            MAX(CASE WHEN col_0 = 'General Revenue Receipts' THEN "Actual_Collection__2023-24" END) AS grr_actual,
            MAX(CASE WHEN col_0 = 'General Revenue Receipts' THEN "%_Collection_w.r.t._BE_2023-24" END) AS grr_achievement,
            MAX(CASE WHEN col_0 = 'General Revenue Receipts' THEN "YoY-_growth" END) AS grr_yoy_growth
        FROM General_Revenue_Receipts
    ),
    fdp_data AS (
        SELECT 
            SUM("Actual_Collection_2022-23") AS fbr_total_collection_previous,
            SUM("B.E_2023-24") AS fbr_total_collection_target,
            SUM("Actual_Collection__2023-24") AS fbr_total_collection_actual
        FROM Federal_Divisible_Pool
    )
    SELECT 
        grr_data.*, 
        fdp_data.fbr_total_collection_previous, 
        fdp_data.fbr_total_collection_target, 
        fdp_data.fbr_total_collection_actual,
        (fdp_data.fbr_total_collection_actual * 0.2874) AS fdp_expected,  
        (fdp_data.fbr_total_collection_actual * 0.2874 - grr_data.fdp_actual) AS fdp_shortfall  
    FROM grr_data, fdp_data;
    """,
    "prompt": """
    Generate a "Provincial General Revenue Receipts" section for the Budget Execution Report for FY {fiscal_year}.  

    *Very Important:*  
    - The section must be long and highly detailed, spanning multiple pages.  
    - Do not summarize—discuss each revenue category in full detail.  
    - Use formal, structured, and analytical language in line with government budget reports.  
    - Focus on clear paragraph transitions, ensuring that every metric and trend is fully analyzed.  

    *Required Analysis*  

    1. *General Overview of Provincial General Revenue Receipts*  
    - Discuss the significance of *General Revenue Receipts (GRR)* in the provincial budget.  
    - Highlight how GRR contributes to fiscal stability and government spending capacity.  
    - Explain the *three main sources* of GRR:  
      - *Federal Divisible Pool (FDP)*  
      - *Provincial Tax Revenue*  
      - *Provincial Non-Tax Revenue*  
    - Provide a historical perspective on revenue trends and their impact on fiscal policy.  

    2. *Performance vs. Budget Targets*  
    - Compare actual revenue collection against budget estimates for *FY {fiscal_year}*.  
    - Explain *revenue shortfalls or overperformance* in FDP, provincial tax, and non-tax revenue.  
    - Evaluate *budgeted vs. actual growth* in each revenue stream:  
      - *FDP Growth*: [insert fdp_yoy_growth]% vs. budgeted target  
      - *Provincial Tax Growth*: [insert prov_tax_yoy_growth]% vs. budgeted target  
      - *Provincial Non-Tax Growth*: [insert prov_non_tax_yoy_growth]% vs. budgeted target  
    - Discuss *% of Budget Achieved*:  
      - *FDP*: [insert fdp_achievement]%  
      - *Provincial Tax*: [insert prov_tax_achievement]%  
      - *Provincial Non-Tax*: [insert prov_non_tax_achievement]%  
    - Assess the impact of *economic conditions and policy decisions* on revenue collection.  

    3. *Analysis of Key Indicators*  
    - *Federal Divisible Pool (FDP)*: Rs. [insert fdp_actual] billion (Target: Rs. [insert fdp_target] billion, Previous: Rs. [insert fdp_previous] billion).  
    - *Provincial Tax Revenue*: Rs. [insert prov_tax_actual] billion (Target: Rs. [insert prov_tax_target] billion, Previous: Rs. [insert prov_tax_previous] billion).  
    - *Provincial Non-Tax Revenue*: Rs. [insert prov_non_tax_actual] billion (Target: Rs. [insert prov_non_tax_target] billion, Previous: Rs. [insert prov_non_tax_previous] billion).  
    - *Total General Revenue Receipts*: Rs. [insert grr_actual] billion (Target: Rs. [insert grr_target] billion, Previous: Rs. [insert grr_previous] billion).  
    - *FDP Shortfall*: Rs. [insert fdp_shortfall] billion.  
    - Explain how these numbers compare to *historical performance and trends*.  

    4. *Causes and Implications*  
    - *FDP Revenue Trends*: Why did FDP revenue deviate from expectations?  
    - *Provincial Tax Revenue Performance*:  
      - Were tax collection targets realistic?  
      - How did tax reforms or enforcement impact actual revenue?  
    - *Provincial Non-Tax Revenue Challenges*:  
      - What factors influenced non-tax revenue collection?  
      - Were there policy shifts affecting revenue from fees, royalties, or services?  
    - *Budget Planning Implications*:  
      - How does revenue performance affect government spending?  
      - What adjustments are needed in future fiscal planning?  

    5. *Future Outlook and Policy Considerations*  
    - *Projected revenue trends for next fiscal year*.  
    - *Expected policy adjustments* to improve revenue collection.  
    - *Potential risks* that could impact revenue performance (economic downturns, tax evasion, administrative inefficiencies).  

    *Final Output Must Be:*  
    - Extremely detailed, providing deep insight into each revenue source.  
    - Multiple paragraphs per section, written in a formal, structured tone.  
    - Free of placeholders—real data must be incorporated seamlessly into the analysis.  
    """
},
   "Analysis of Receipts - 3.1.1.A Provincial Tax Revenue": {
    "query": """
    SELECT 
        -- Total Provincial Tax Revenue
        MAX(CASE WHEN col_0 = 'Provincial Tax Revenue' THEN "Actual_Collection_2022-23" END) AS prov_tax_previous,
        MAX(CASE WHEN col_0 = 'Provincial Tax Revenue' THEN "B.E_2023-24" END) AS prov_tax_target,
        MAX(CASE WHEN col_0 = 'Provincial Tax Revenue' THEN "Actual_Collection__2023-24" END) AS prov_tax_actual,
        MAX(CASE WHEN col_0 = 'Provincial Tax Revenue' THEN "%_Collection_w.r.t._BE_2023-24" END) AS prov_tax_achievement,
        MAX(CASE WHEN col_0 = 'Provincial Tax Revenue' THEN "YoY-_growth" END) AS prov_tax_yoy_growth,

        -- Board of Revenue (BOR)
        MAX(CASE WHEN col_0 = 'Board of Revenue' THEN "Actual_Collection_2022-23" END) AS bor_previous,
        MAX(CASE WHEN col_0 = 'Board of Revenue' THEN "B.E_2023-24" END) AS bor_target,
        MAX(CASE WHEN col_0 = 'Board of Revenue' THEN "Actual_Collection__2023-24" END) AS bor_actual,
        MAX(CASE WHEN col_0 = 'Board of Revenue' THEN "%_Collection_w.r.t._BE_2023-24" END) AS bor_achievement,
        MAX(CASE WHEN col_0 = 'Board of Revenue' THEN "YoY-_growth" END) AS bor_yoy_growth,

        -- Excise, Taxation & Narcotics Control (ET&NCD)
        MAX(CASE WHEN col_0 = 'Excise & Taxation' THEN "Actual_Collection_2022-23" END) AS etncd_previous,
        MAX(CASE WHEN col_0 = 'Excise & Taxation' THEN "B.E_2023-24" END) AS etncd_target,
        MAX(CASE WHEN col_0 = 'Excise & Taxation' THEN "Actual_Collection__2023-24" END) AS etncd_actual,
        MAX(CASE WHEN col_0 = 'Excise & Taxation' THEN "%_Collection_w.r.t._BE_2023-24" END) AS etncd_achievement,
        MAX(CASE WHEN col_0 = 'Excise & Taxation' THEN "YoY-_growth" END) AS etncd_yoy_growth,

        -- Punjab Revenue Authority (PRA)
        MAX(CASE WHEN col_0 = 'Punjab Revenue Authority- PRA' THEN "Actual_Collection_2022-23" END) AS pra_previous,
        MAX(CASE WHEN col_0 = 'Punjab Revenue Authority- PRA' THEN "B.E_2023-24" END) AS pra_target,
        MAX(CASE WHEN col_0 = 'Punjab Revenue Authority- PRA' THEN "Actual_Collection__2023-24" END) AS pra_actual,
        MAX(CASE WHEN col_0 = 'Punjab Revenue Authority- PRA' THEN "%_Collection_w.r.t._BE_2023-24" END) AS pra_achievement,
        MAX(CASE WHEN col_0 = 'Punjab Revenue Authority- PRA' THEN "YoY-_growth" END) AS pra_yoy_growth,

        -- Transport Department
        MAX(CASE WHEN col_0 = 'Transport' THEN "Actual_Collection_2022-23" END) AS transport_previous,
        MAX(CASE WHEN col_0 = 'Transport' THEN "B.E_2023-24" END) AS transport_target,
        MAX(CASE WHEN col_0 = 'Transport' THEN "Actual_Collection__2023-24" END) AS transport_actual,
        MAX(CASE WHEN col_0 = 'Transport' THEN "%_Collection_w.r.t._BE_2023-24" END) AS transport_achievement,
        MAX(CASE WHEN col_0 = 'Transport' THEN "YoY-_growth" END) AS transport_yoy_growth

    FROM Provincial_Tax_Revenue___Department_wise
    WHERE col_0 IN (
        'Provincial Tax Revenue',
        'Board of Revenue',
        'Excise & Taxation',
        'Punjab Revenue Authority- PRA',
        'Transport'
    );
    """,
    "prompt": """
    Generate a "Provincial Tax Revenue" section for the Budget Execution Report for FY {fiscal_year}.  

    *Very Important:*  
    - The section must be long and highly detailed, spanning multiple pages.  
    - Do not summarize—discuss each revenue category in full detail.  
    - Use formal, structured, and analytical language in line with government budget reports.  
    - Focus on clear paragraph transitions, ensuring that every metric and trend is fully analyzed.  

    *Required Analysis*  

    1. *Overview of Provincial Tax Revenue*  
    - Define *Provincial Tax Revenue* and its role in provincial fiscal management.  
    - Discuss the *three major contributors*:  
      - *Punjab Revenue Authority (PRA)*  
      - *Board of Revenue (BOR)*  
      - *Excise, Taxation & Narcotics Control Dept. (ET&NCD)*  
    - Explain the *budgeted target vs actual performance* for FY {fiscal_year}.  

    2. *Performance vs. Budget Targets*  
    - Compare actual tax collection against budget estimates.  
    - Highlight *YoY growth* and how it compares to the *5-year average growth rate*.  
    - Assess the *% of Budget Achieved*:  
      - *Total Provincial Tax Revenue*: [insert prov_tax_achievement]%  
      - *PRA*: [insert pra_achievement]%  
      - *BOR*: [insert bor_achievement]%  
      - *ET&NCD*: [insert etncd_achievement]%  
    - Discuss factors impacting *tax collection efficiency and policy changes*.  

    3. *Analysis of Key Indicators*  
    - *Total Provincial Tax Revenue*: Rs. [insert prov_tax_actual] billion (Target: Rs. [insert prov_tax_target] billion, Previous: Rs. [insert prov_tax_previous] billion).  
    - *Punjab Revenue Authority (PRA) Contribution*: Rs. [insert pra_actual] billion (Target: Rs. [insert pra_target] billion).  
    - *Board of Revenue (BOR) Contribution*: Rs. [insert bor_actual] billion (Target: Rs. [insert bor_target] billion).  
    - *ET&NCD Contribution*: Rs. [insert etncd_actual] billion (Target: Rs. [insert etncd_target] billion).  
    - *Transport Contribution*: Rs. [insert transport_actual] billion (Target: Rs. [insert transport_target] billion).  
    - Explain how these numbers compare to *historical performance and trends*.  

    4. *Causes and Implications*  
    - *PRA Performance*: Why did PRA revenue exceed or fall short of expectations?  
    - *Board of Revenue Trends*:  
      - Did property taxes meet expectations?  
      - Were there any legal or policy changes affecting revenue?  
    - *Excise & Taxation Department's Performance*:  
      - Did tax compliance improve?  
      - Were there enforcement issues or tax rate adjustments?  
    - *Budget Planning Implications*:  
      - How will these tax trends influence future fiscal policy?  

    5. *Future Outlook and Policy Considerations*  
    - *Projected trends for provincial tax collection in the next fiscal year*.  
    - *Proposed reforms* to enhance tax revenue collection.  
    - *Potential risks* that could impact future tax revenue (economic downturns, policy shifts, enforcement challenges).  

    *Final Output Must Be:*  
    - Extremely detailed, providing deep insight into each tax revenue source.  
    - Multiple paragraphs per section, written in a formal, structured tone.  
    - Free of placeholders—real data must be incorporated seamlessly into the analysis.  
    """
}
}

sections["Analysis of Receipts - 3.1 Total Provincial Receipts"] = {
    "query": """
SELECT 
    MAX(CASE WHEN col_0 = 'General Revenue Receipts' THEN "Actual_Collection_2022-23" END) AS grr_previous,
    MAX(CASE WHEN col_0 = 'General Revenue Receipts' THEN "B.E_2023-24" END) AS grr_target,
    MAX(CASE WHEN col_0 = 'General Revenue Receipts' THEN "Budgeted_Growth_%" END) AS grr_budgeted_growth,
    MAX(CASE WHEN col_0 = 'General Revenue Receipts' THEN "Actual_Collection__2023-24" END) AS grr_actual,
    MAX(CASE WHEN col_0 = 'General Revenue Receipts' THEN "%_Collection_w.r.t._BE_2023-24" END) AS grr_achievement,
    MAX(CASE WHEN col_0 = 'General Revenue Receipts' THEN "YoY_growth" END) AS grr_yoy_growth,
    
    MAX(CASE WHEN col_0 = 'Total Capital Receipts' THEN "Actual_Collection_2022-23" END) AS capital_previous,
    MAX(CASE WHEN col_0 = 'Total Capital Receipts' THEN "B.E_2023-24" END) AS capital_target,
    MAX(CASE WHEN col_0 = 'Total Capital Receipts' THEN "Budgeted_Growth_%" END) AS capital_budgeted_growth,
    MAX(CASE WHEN col_0 = 'Total Capital Receipts' THEN "Actual_Collection__2023-24" END) AS capital_actual,
    MAX(CASE WHEN col_0 = 'Total Capital Receipts' THEN "%_Collection_w.r.t._BE_2023-24" END) AS capital_achievement,
    MAX(CASE WHEN col_0 = 'Total Capital Receipts' THEN "YoY_growth" END) AS capital_yoy_growth,
    
    MAX(CASE WHEN col_0 = 'Total Provincial Consolidated Fund' THEN "Actual_Collection_2022-23" END) AS tpr_previous,
    MAX(CASE WHEN col_0 = 'Total Provincial Consolidated Fund' THEN "B.E_2023-24" END) AS tpr_target,
    MAX(CASE WHEN col_0 = 'Total Provincial Consolidated Fund' THEN "Budgeted_Growth_%" END) AS tpr_budgeted_growth,
    MAX(CASE WHEN col_0 = 'Total Provincial Consolidated Fund' THEN "Actual_Collection__2023-24" END) AS tpr_actual,
    MAX(CASE WHEN col_0 = 'Total Provincial Consolidated Fund' THEN "%_Collection_w.r.t._BE_2023-24" END) AS tpr_achievement,
    MAX(CASE WHEN col_0 = 'Total Provincial Consolidated Fund' THEN "YoY_growth" END) AS tpr_yoy_growth
FROM Total_Provincial_Receipts;
""",
    "prompt": """
Generate an **Analysis of Receipts** section for the Budget Execution Report, focusing on **Total Provincial Receipts (TPR)** for FY {fiscal_year}.

**Very Important:**
- The section must be long and highly detailed, spanning multiple pages.
- Do not summarize—provide an in-depth breakdown of each component.
- Use formal, structured, and analytical language in line with government budget reports.
- Ensure smooth paragraph transitions and provide historical context.

**Required Analysis**

1. **Overview of Total Provincial Receipts (TPR)**
   - Define **TPR** and its two main components:
     - **General Revenue Receipts (GRR)** (Federal Divisible Pool, Provincial Tax & Non-Tax Revenue).
     - **Total Capital Receipts** (domestic loans, recoveries, borrowings for State Trading).
   - Explain their respective shares in total receipts and historical trends.
   - Provide a breakdown of **budgeted vs. actual** performance and expected growth.

2. **Performance vs. Budget Targets**
   - Compare actual revenue performance against budget estimates for **FY {fiscal_year}**.
   - Explain deviations: What caused revenue shortfalls or overperformance?
   - Analyze **Budgeted Growth vs. Actual Growth** for GRR ({grr_budgeted_growth}% vs {grr_yoy_growth}%), Capital Receipts ({capital_budgeted_growth}% vs {capital_yoy_growth}%), and TPR ({tpr_budgeted_growth}% vs {tpr_yoy_growth}%).
   - Address external and internal factors affecting collections (e.g., economic conditions, policy changes, tax reforms).
   - Evaluate the **% of Budget Achieved**:
     - **GRR**: {grr_achievement}%
     - **Capital Receipts**: {capital_achievement}%
     - **TPR**: {tpr_achievement}%

3. **Analysis of Key Indicators**
   - General Revenue Receipts (GRR): Rs. {grr_actual} billion (Target: Rs. {grr_target} billion, Previous: Rs. {grr_previous} billion).
   - Total Capital Receipts: Rs. {capital_actual} billion (Target: Rs. {capital_target} billion, Previous: Rs. {capital_previous} billion).
   - Total Provincial Receipts: Rs. {tpr_actual} billion (Target: Rs. {tpr_target} billion, Previous: Rs. {tpr_previous} billion).
   - Breakdown of key trends:
     - **GRR Growth**: {grr_yoy_growth}% YoY vs. budgeted {grr_budgeted_growth}%.
     - **Capital Receipts Growth**: {capital_yoy_growth}% vs. budgeted {capital_budgeted_growth}%.
     - **TPR Growth**: {tpr_yoy_growth}% vs. budgeted {tpr_budgeted_growth}%.
   - Compare historical revenue trends over the last five years.

4. **Causes and Implications**
   - **GRR Performance**: What drove the revenue growth or shortfall? How did tax administration reforms impact collections?
   - **Capital Receipts Challenges**: Did the province secure expected domestic and foreign loans? How did recoveries impact revenue?
   - **Budget Achievement**: Were revenue targets realistic? If not, what policy adjustments are needed?
   - **Fiscal Stability**: What are the implications of these revenue trends on provincial financial sustainability?

5. **Future Outlook & Policy Considerations**
   - Projected revenue trends for the next fiscal year.
   - Recommendations for improving revenue collection efficiency.
   - Risks that may impact revenue inflows (economic conditions, policy shifts, global funding trends).

**Final Output Must Be:**
- Extremely detailed, providing deep insight into each revenue category.
- Multiple paragraphs per section, structured in a formal government reporting style.
- Free of placeholders—real data must be incorporated seamlessly into the analysis.
"""
}

sections["Provincial Non-Tax Revenue"] = {
    "query": """
SELECT 
    MAX(CASE WHEN col_0 = 'Total' THEN "Actual_Collection_2022-23" END) AS non_tax_previous,
    MAX(CASE WHEN col_0 = 'Total' THEN "B.E_2023-24" END) AS non_tax_target,
    MAX(CASE WHEN col_0 = 'Total' THEN "Actual_Collection__2023-24" END) AS non_tax_actual,
    MAX(CASE WHEN col_0 = 'Total' THEN "%_Collection_w.r.t._BE_2023-24" END) AS non_tax_achievement,
    MAX(CASE WHEN col_0 = 'Total' THEN "YoY_growth" END) AS non_tax_yoy_growth,

    MAX(CASE WHEN col_0 = 'Finance' THEN "Actual_Collection_2022-23" END) AS finance_previous,
    MAX(CASE WHEN col_0 = 'Finance' THEN "B.E_2023-24" END) AS finance_target,
    MAX(CASE WHEN col_0 = 'Finance' THEN "Actual_Collection__2023-24" END) AS finance_actual,
    MAX(CASE WHEN col_0 = 'Finance' THEN "%_Collection_w.r.t._BE_2023-24" END) AS finance_achievement,
    MAX(CASE WHEN col_0 = 'Finance' THEN "YoY_growth" END) AS finance_yoy_growth,

    MAX(CASE WHEN col_0 = 'Irrigation' THEN "Actual_Collection_2022-23" END) AS irrigation_previous,
    MAX(CASE WHEN col_0 = 'Irrigation' THEN "B.E_2023-24" END) AS irrigation_target,
    MAX(CASE WHEN col_0 = 'Irrigation' THEN "Actual_Collection__2023-24" END) AS irrigation_actual,
    MAX(CASE WHEN col_0 = 'Irrigation' THEN "%_Collection_w.r.t._BE_2023-24" END) AS irrigation_achievement,
    MAX(CASE WHEN col_0 = 'Irrigation' THEN "YoY_growth" END) AS irrigation_yoy_growth,

    MAX(CASE WHEN col_0 = 'Mines & Minerals' THEN "Actual_Collection_2022-23" END) AS mines_previous,
    MAX(CASE WHEN col_0 = 'Mines & Minerals' THEN "B.E_2023-24" END) AS mines_target,
    MAX(CASE WHEN col_0 = 'Mines & Minerals' THEN "Actual_Collection__2023-24" END) AS mines_actual,
    MAX(CASE WHEN col_0 = 'Mines & Minerals' THEN "%_Collection_w.r.t._BE_2023-24" END) AS mines_achievement,
    MAX(CASE WHEN col_0 = 'Mines & Minerals' THEN "YoY_growth" END) AS mines_yoy_growth,

    MAX(CASE WHEN col_0 = 'Police' THEN "Actual_Collection_2022-23" END) AS police_previous,
    MAX(CASE WHEN col_0 = 'Police' THEN "B.E_2023-24" END) AS police_target,
    MAX(CASE WHEN col_0 = 'Police' THEN "Actual_Collection__2023-24" END) AS police_actual,
    MAX(CASE WHEN col_0 = 'Police' THEN "%_Collection_w.r.t._BE_2023-24" END) AS police_achievement,
    MAX(CASE WHEN col_0 = 'Police' THEN "YoY_growth" END) AS police_yoy_growth,

    MAX(CASE WHEN col_0 = 'Miscellaneous' THEN "Actual_Collection_2022-23" END) AS misc_previous,
    MAX(CASE WHEN col_0 = 'Miscellaneous' THEN "B.E_2023-24" END) AS misc_target,
    MAX(CASE WHEN col_0 = 'Miscellaneous' THEN "Actual_Collection__2023-24" END) AS misc_actual,
    MAX(CASE WHEN col_0 = 'Miscellaneous' THEN "%_Collection_w.r.t._BE_2023-24" END) AS misc_achievement,
    MAX(CASE WHEN col_0 = 'Miscellaneous' THEN "YoY_growth" END) AS misc_yoy_growth

FROM Provincial_Non_Tax_Revenue___Department_wise
WHERE col_0 IN ('Total', 'Finance', 'Irrigation', 'Mines & Minerals', 'Police', 'Miscellaneous');
""",
    "prompt": """
            Generate a **Provincial Non-Tax Revenue** section for the Budget Execution Report for FY {fiscal_year}.  

            **Very Important:**  
            - The section must be long and highly detailed, spanning multiple pages.  
            - Do not summarize—analyze each indicator comprehensively.  
            - Use formal, structured, and analytical language in line with government budget reports.  
            - Ensure smooth paragraph transitions and provide historical comparisons.  

            **Required Analysis**  

            1. **Overview of Provincial Non-Tax Revenue (NTR)**  
            - Define **Provincial Non-Tax Revenue (NTR)** and its role in fiscal sustainability.  
            - Discuss its **composition**, major revenue sources, and reliance on federal transfers.  
            - Provide a breakdown of revenue targets vs actual collections.  

            2. **Performance vs. Budget Estimates**  
            - Compare **actual non-tax revenue performance against budget targets**.  
            - Highlight **% of budget achieved** for each revenue source:  
              - Finance: {finance_achievement}%  
              - Irrigation: {irrigation_achievement}%  
              - Mines & Minerals: {mines_achievement}%  
              - Police: {police_achievement}%  
              - Miscellaneous: {misc_achievement}%  
            - Explain deviations: What caused revenue shortfalls or overperformance?  
            - Address external and internal factors affecting collections (e.g., economic conditions, policy changes).  

            3. **Analysis of Key Indicators**  
            - Total Provincial Non-Tax Revenue: Rs. {non_tax_actual} billion (Target: Rs. {non_tax_target} billion).  
            - Breakdown of revenue composition:  
              - **Finance Department**: Rs. {finance_actual} billion (Target: Rs. {finance_target} billion).  
              - **Irrigation (Abiyana Receipts)**: Rs. {irrigation_actual} billion (Target: Rs. {irrigation_target} billion).  
              - **Mines & Minerals Royalties**: Rs. {mines_actual} billion (Target: Rs. {mines_target} billion).  
              - **Police (Fines & Licensing Fees)**: Rs. {police_actual} billion (Target: Rs. {police_target} billion).  
              - **Miscellaneous Receipts**: Rs. {misc_actual} billion (Target: Rs. {misc_target} billion).  
            - Compare **YoY growth rates**:  
              - Finance: {finance_yoy_growth}%  
              - Irrigation: {irrigation_yoy_growth}%  
              - Mines & Minerals: {mines_yoy_growth}%  
              - Police: {police_yoy_growth}%  
              - Miscellaneous: {misc_yoy_growth}%  

            4. **Causes and Implications**  
            - Finance Department: Impact of federal transfers and hydropower royalties.  
            - Irrigation: Challenges in abiyana collection and historical trends.  
            - Mines & Minerals: Fluctuations in royalties and lease agreements.  
            - Police: Effectiveness of fine collection and revenue administration.  
            - Miscellaneous: Variability in smaller revenue sources and sustainability concerns.  
            - Fiscal Stability: How do non-tax revenue trends impact the province’s financial management?  

            5. **Future Outlook and Policy Recommendations**  
            - Expected trends in non-tax revenue growth.  
            - Proposed reforms to enhance revenue collection efficiency.  
            - Risks and external factors that may impact non-tax revenue streams.  

            **Final Output Must Be:**  
            - Highly detailed, covering all revenue components thoroughly.  
            - Multiple paragraphs per section, structured formally.  
            - Free of placeholders—real data must be seamlessly incorporated.
        """
}

sections["Analysis of Receipts - 3.1.2 Total Capital Receipts"] = {
    "query": """
WITH capital_receipts AS (
    SELECT 
        MAX(CASE WHEN col_0 = 'Current Capital Receipts' THEN "Actual_Collection_2022-23" END) AS current_capital_previous,
        MAX(CASE WHEN col_0 = 'Current Capital Receipts' THEN "B.E_2023-24" END) AS current_capital_target,
        MAX(CASE WHEN col_0 = 'Current Capital Receipts' THEN "Actual_Collection__2023-24" END) AS current_capital_actual,
        MAX(CASE WHEN col_0 = 'Current Capital Receipts' THEN "%_Collection_w.r.t._BE_2023-24" END) AS current_capital_achievement,
        MAX(CASE WHEN col_0 = 'Current Capital Receipts' THEN "YoY_growth" END) AS current_capital_yoy_growth,

        MAX(CASE WHEN col_0 = 'Development Capital Receipts' THEN "Actual_Collection_2022-23" END) AS dev_capital_previous,
        MAX(CASE WHEN col_0 = 'Development Capital Receipts' THEN "B.E_2023-24" END) AS dev_capital_target,
        MAX(CASE WHEN col_0 = 'Development Capital Receipts' THEN "Actual_Collection__2023-24" END) AS dev_capital_actual,
        MAX(CASE WHEN col_0 = 'Development Capital Receipts' THEN "%_Collection_w.r.t._BE_2023-24" END) AS dev_capital_achievement,
        MAX(CASE WHEN col_0 = 'Development Capital Receipts' THEN "YoY_growth" END) AS dev_capital_yoy_growth,

        MAX(CASE WHEN col_0 = 'Total Capital Receipts' THEN "Actual_Collection_2022-23" END) AS total_capital_previous,
        MAX(CASE WHEN col_0 = 'Total Capital Receipts' THEN "B.E_2023-24" END) AS total_capital_target,
        MAX(CASE WHEN col_0 = 'Total Capital Receipts' THEN "Actual_Collection__2023-24" END) AS total_capital_actual,
        MAX(CASE WHEN col_0 = 'Total Capital Receipts' THEN "%_Collection_w.r.t._BE_2023-24" END) AS total_capital_achievement,
        MAX(CASE WHEN col_0 = 'Total Capital Receipts' THEN "YoY_growth" END) AS total_capital_yoy_growth
    FROM Total_Capital_Receipts
),
capital_receipts_account AS (
    SELECT 
        MAX(CASE WHEN col_0 = 'Recoveries of Loans & Advances and Others' THEN "Actual_Collection_2022-23" END) AS recoveries_previous,
        MAX(CASE WHEN col_0 = 'Recoveries of Loans & Advances and Others' THEN "B.E_2023-24" END) AS recoveries_target,
        MAX(CASE WHEN col_0 = 'Recoveries of Loans & Advances and Others' THEN "Actual_Collection__2023-24" END) AS recoveries_actual,
        MAX(CASE WHEN col_0 = 'Recoveries of Loans & Advances and Others' THEN "%_Collection_w.r.t._BE_2023-24" END) AS recoveries_achievement,
        MAX(CASE WHEN col_0 = 'Recoveries of Loans & Advances and Others' THEN "YoY_growth" END) AS recoveries_yoy_growth,

        MAX(CASE WHEN col_0 = 'Debt Financing' THEN "Actual_Collection_2022-23" END) AS debt_financing_previous,
        MAX(CASE WHEN col_0 = 'Debt Financing' THEN "B.E_2023-24" END) AS debt_financing_target,
        MAX(CASE WHEN col_0 = 'Debt Financing' THEN "Actual_Collection__2023-24" END) AS debt_financing_actual,
        MAX(CASE WHEN col_0 = 'Debt Financing' THEN "%_Collection_w.r.t._BE_2023-24" END) AS debt_financing_achievement,
        MAX(CASE WHEN col_0 = 'Debt Financing' THEN "YoY_growth" END) AS debt_financing_yoy_growth,

        MAX(CASE WHEN col_0 = 'Account I' THEN "Actual_Collection_2022-23" END) AS account_i_previous,
        MAX(CASE WHEN col_0 = 'Account I' THEN "B.E_2023-24" END) AS account_i_target,
        MAX(CASE WHEN col_0 = 'Account I' THEN "Actual_Collection__2023-24" END) AS account_i_actual,
        MAX(CASE WHEN col_0 = 'Account I' THEN "%_Collection_w.r.t._BE_2023-24" END) AS account_i_achievement,
        MAX(CASE WHEN col_0 = 'Account I' THEN "YoY_growth" END) AS account_i_yoy_growth,

        MAX(CASE WHEN col_0 = 'Commodity Financing' THEN "Actual_Collection_2022-23" END) AS commodity_financing_previous,
        MAX(CASE WHEN col_0 = 'Commodity Financing' THEN "B.E_2023-24" END) AS commodity_financing_target,
        MAX(CASE WHEN col_0 = 'Commodity Financing' THEN "Actual_Collection__2023-24" END) AS commodity_financing_actual,
        MAX(CASE WHEN col_0 = 'Commodity Financing' THEN "%_Collection_w.r.t._BE_2023-24" END) AS commodity_financing_achievement,
        MAX(CASE WHEN col_0 = 'Commodity Financing' THEN "YoY_growth" END) AS commodity_financing_yoy_growth
    FROM Total_Capital_Receipts_Account_wise
)
SELECT * FROM capital_receipts, capital_receipts_account;
""",
    "prompt": """
            Generate a **Total Capital Receipts** section for the Budget Execution Report for FY {fiscal_year}.  

            **Very Important:**  
            - The section must be long and highly detailed, spanning multiple pages.  
            - Do not summarize—discuss each indicator in full detail.  
            - Use formal, structured, and analytical language in line with government budget reports.  
            - Focus on clear paragraph transitions, ensuring that every metric and trend is fully analyzed.  

            **Required Analysis**  

            1. **Overview of Capital Receipts**  
            - Define **Total Capital Receipts (TCR)** and its components.  
            - Explain how TCR differs from general revenue receipts.  
            - Discuss the role of capital receipts in **financing development projects, public sector investment, and fiscal sustainability**.  

            2. **Performance vs. Budget Targets**  
            - Compare **actual receipts vs budget estimates** for **FY {fiscal_year}**.  
            - Explain **deviations**—what caused capital receipts to be higher or lower than expected?  
            - Address external influences such as **global credit conditions, government borrowing policies, and investment inflows**.  

            #### **3. Analysis of Key Indicators**  
            - **Total Capital Receipts**: Rs. {total_capital_actual} billion (Target: Rs. {total_capital_target} billion, Previous: Rs. {total_capital_previous} billion).  
            - **Current Capital Receipts**: Rs. {current_capital_actual} billion (Target: Rs. {current_capital_target} billion, Previous: Rs. {current_capital_previous} billion).  
            - **Development Capital Receipts**: Rs. {dev_capital_actual} billion (Target: Rs. {dev_capital_target} billion, Previous: Rs. {dev_capital_previous} billion).  
            - **Recoveries of Loans & Advances**: Rs. {recoveries_actual} billion (Target: Rs. {recoveries_target} billion, Previous: Rs. {recoveries_previous} billion).  
            - **Debt Financing**: Rs. {debt_financing_actual} billion (Target: Rs. {debt_financing_target} billion, Previous: Rs. {debt_financing_previous} billion).  
            - **Account I & II Contributions**:  
              - **Account I**: Rs. {account_1_actual} billion (Target: Rs. {account_1_target} billion).  
              - **Account II (Commodity Financing)**: Rs. {account_2_actual} billion (Target: Rs. {account_2_target} billion).  
            - Discuss **YoY Growth Trends**:  
              - **TCR Growth**: {total_capital_yoy_growth}% YoY.  
              - **Recoveries Growth**: {recoveries_yoy_growth}% YoY.  
              - **Debt Financing Growth**: {debt_financing_yoy_growth}% YoY.  
              - **Current Capital Receipts Growth**: {current_capital_yoy_growth}% YoY.  
              - **Development Capital Receipts Growth**: {dev_capital_yoy_growth}% YoY.  
            - Compare to **historical performance over the last five years**.  

            4. **Causes and Implications**  
            - **Debt Financing Performance**: Did the government secure planned borrowing? How does debt financing compare to budget targets?  
            - **Recoveries of Loans & Advances**: Were projected recoveries met? What factors influenced repayment rates?  
            - **Budget Achievement**: How well did actual collections align with budget estimates?  
            - **Fiscal Stability**: What are the implications of these revenue trends on provincial financial sustainability?  

            5. **Future Outlook & Policy Considerations**  
            - Projected capital receipt trends for the next fiscal year.  
            - Recommendations for **enhancing debt financing efficiency** and **improving recoveries**.  
            - Risks that may impact capital receipts (interest rate fluctuations, macroeconomic conditions, government borrowing capacity).  

            **Final Output Must Be:**  
            - Extremely detailed, providing deep insight into each capital receipt category.  
            - Multiple paragraphs per section, structured in a formal government reporting style.  
            - Free of placeholders—real data must be incorporated seamlessly into the analysis.  
        """
}

sections["Analysis of Expenses - 4.1 Total Provincial Expenditure"] = {
    "query": """
            WITH expenditure_category AS (
                SELECT
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Expenditure' THEN "Actual Expenditure 2022-23" END) AS current_previous,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Expenditure' THEN "B.E 2023-24" END) AS current_target,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Expenditure' THEN "Actual Expenditure 2023-24" END) AS current_actual,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Expenditure' THEN "% Utilization w.r.t. BE 2023-24" END) AS current_achievement,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Expenditure' THEN "YoY- growth" END) AS current_yoy_growth,

                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Capital Expenditure A/C-I' THEN "Actual Expenditure 2022-23" END) AS capital_1_previous,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Capital Expenditure A/C-I' THEN "B.E 2023-24" END) AS capital_1_target,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Capital Expenditure A/C-I' THEN "Actual Expenditure 2023-24" END) AS capital_1_actual,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Capital Expenditure A/C-I' THEN "% Utilization w.r.t. BE 2023-24" END) AS capital_1_achievement,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Capital Expenditure A/C-I' THEN "YoY- growth" END) AS capital_1_yoy_growth,

                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Capital Expenditure A/C-II' THEN "Actual Expenditure 2022-23" END) AS capital_2_previous,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Capital Expenditure A/C-II' THEN "B.E 2023-24" END) AS capital_2_target,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Capital Expenditure A/C-II' THEN "Actual Expenditure 2023-24" END) AS capital_2_actual,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Capital Expenditure A/C-II' THEN "% Utilization w.r.t. BE 2023-24" END) AS capital_2_achievement,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Current Capital Expenditure A/C-II' THEN "YoY- growth" END) AS capital_2_yoy_growth,

                    MAX(CASE WHEN "Total Expenditure by Category" = 'Development Expenditure' THEN "Actual Expenditure 2022-23" END) AS development_previous,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Development Expenditure' THEN "B.E 2023-24" END) AS development_target,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Development Expenditure' THEN "Actual Expenditure 2023-24" END) AS development_actual,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Development Expenditure' THEN "% Utilization w.r.t. BE 2023-24" END) AS development_achievement,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Development Expenditure' THEN "YoY- growth" END) AS development_yoy_growth,

                    MAX(CASE WHEN "Total Expenditure by Category" = 'Total Provincial Expenditure' THEN "Actual Expenditure 2022-23" END) AS expenditure_previous,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Total Provincial Expenditure' THEN "B.E 2023-24" END) AS expenditure_target,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Total Provincial Expenditure' THEN "Actual Expenditure 2023-24" END) AS expenditure_actual,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Total Provincial Expenditure' THEN "% Utilization w.r.t. BE 2023-24" END) AS budget_utilization,
                    MAX(CASE WHEN "Total Expenditure by Category" = 'Total Provincial Expenditure' THEN "YoY- growth" END) AS expenditure_yoy_growth
                FROM "Table_4_1_Total_Provincial_Expenditure_by_Category"
            ),
            expenditure_component AS (
                SELECT 
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Salary' THEN "Actual Expenditure 2022-23" END) AS salary_previous,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Salary' THEN "B.E 2023-24" END) AS salary_target,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Salary' THEN "Actual Expenditure 2023-24" END) AS salary_actual,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Salary' THEN "% Utilization w.r.t. BE 2023-24" END) AS salary_achievement,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Salary' THEN "YoY- growth" END) AS salary_yoy_growth,
        
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Pension' THEN "Actual Expenditure 2022-23" END) AS pension_previous,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Pension' THEN "B.E 2023-24" END) AS pension_target,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Pension' THEN "Actual Expenditure 2023-24" END) AS pension_actual,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Pension' THEN "% Utilization w.r.t. BE 2023-24" END) AS pension_achievement,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Pension' THEN "YoY- growth" END) AS pension_yoy_growth,
        
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Transfers (to LGs and others)' THEN "Actual Expenditure 2022-23" END) AS transfers_previous,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Transfers (to LGs and others)' THEN "B.E 2023-24" END) AS transfers_target,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Transfers (to LGs and others)' THEN "Actual Expenditure 2023-24" END) AS transfers_actual,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Transfers (to LGs and others)' THEN "% Utilization w.r.t. BE 2023-24" END) AS transfers_achievement,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Transfers (to LGs and others)' THEN "YoY- growth" END) AS transfers_yoy_growth,
        
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Non-Salary (Service Delivery Expenditure)' THEN "Actual Expenditure 2022-23" END) AS non_salary_previous,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Non-Salary (Service Delivery Expenditure)' THEN "B.E 2023-24" END) AS non_salary_target,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Non-Salary (Service Delivery Expenditure)' THEN "Actual Expenditure 2023-24" END) AS non_salary_actual,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Non-Salary (Service Delivery Expenditure)' THEN "% Utilization w.r.t. BE 2023-24" END) AS non_salary_achievement,
                    MAX(CASE WHEN "Total Expenditure by Major Components" = 'Non-Salary (Service Delivery Expenditure)' THEN "YoY- growth" END) AS non_salary_yoy_growth
                FROM "Table_4_1_A_Total_Provincial_Expenditure_Component_wise"
            ),
expenditure_function AS (
    SELECT
        (SELECT "Actual Expenditure 2022-23" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '01 - General Public Service') AS gps_previous,
        (SELECT "B.E 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '01 - General Public Service') AS gps_target,
        (SELECT "Budgeted Growth %" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '01 - General Public Service') AS gps_budgeted_growth,
        (SELECT "Actual Expenditure 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '01 - General Public Service') AS gps_actual,
        (SELECT "% Utilization w.r.t. BE 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '01 - General Public Service') AS gps_utilization,
        (SELECT "YoY- growth" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '01 - General Public Service') AS gps_yoy_growth,

        (SELECT "Actual Expenditure 2022-23" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '03 - Public Order and Safety Affairs') AS pos_previous,
        (SELECT "B.E 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '03 - Public Order and Safety Affairs') AS pos_target,
        (SELECT "Budgeted Growth %" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '03 - Public Order and Safety Affairs') AS pos_budgeted_growth,
        (SELECT "Actual Expenditure 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '03 - Public Order and Safety Affairs') AS pos_actual,
        (SELECT "% Utilization w.r.t. BE 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '03 - Public Order and Safety Affairs') AS pos_utilization,
        (SELECT "YoY- growth" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '03 - Public Order and Safety Affairs') AS pos_yoy_growth,

        (SELECT "Actual Expenditure 2022-23" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '04 - Economic Affairs') AS eco_previous,
        (SELECT "B.E 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '04 - Economic Affairs') AS eco_target,
        (SELECT "Budgeted Growth %" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '04 - Economic Affairs') AS eco_budgeted_growth,
        (SELECT "Actual Expenditure 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '04 - Economic Affairs') AS eco_actual,
        (SELECT "% Utilization w.r.t. BE 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '04 - Economic Affairs') AS eco_utilization,
        (SELECT "YoY- growth" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '04 - Economic Affairs') AS eco_yoy_growth,

        (SELECT "Actual Expenditure 2022-23" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '05 - Environment Protection') AS env_previous,
        (SELECT "B.E 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '05 - Environment Protection') AS env_target,
        (SELECT "Budgeted Growth %" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '05 - Environment Protection') AS env_budgeted_growth,
        (SELECT "Actual Expenditure 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '05 - Environment Protection') AS env_actual,
        (SELECT "% Utilization w.r.t. BE 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '05 - Environment Protection') AS env_utilization,
        (SELECT "YoY- growth" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '05 - Environment Protection') AS env_yoy_growth,

        (SELECT "Actual Expenditure 2022-23" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '06 - Housing and Community Amenities') AS house_previous,
        (SELECT "B.E 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '06 - Housing and Community Amenities') AS house_target,
        (SELECT "Budgeted Growth %" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '06 - Housing and Community Amenities') AS house_budgeted_growth,
        (SELECT "Actual Expenditure 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '06 - Housing and Community Amenities') AS house_actual,
        (SELECT "% Utilization w.r.t. BE 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '06 - Housing and Community Amenities') AS house_utilization,
        (SELECT "YoY- growth" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '06 - Housing and Community Amenities') AS house_yoy_growth,

        (SELECT "Actual Expenditure 2022-23" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '07 – Health') AS health_previous,
        (SELECT "B.E 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '07 – Health') AS health_target,
        (SELECT "Budgeted Growth %" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '07 – Health') AS health_budgeted_growth,
        (SELECT "Actual Expenditure 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '07 – Health') AS health_actual,
        (SELECT "% Utilization w.r.t. BE 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '07 – Health') AS health_utilization,
        (SELECT "YoY- growth" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '07 – Health') AS health_yoy_growth,

        (SELECT "Actual Expenditure 2022-23" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '08 - Recreational, Culture and Religion') AS rec_previous,
        (SELECT "B.E 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '08 - Recreational, Culture and Religion') AS rec_target,
        (SELECT "Budgeted Growth %" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '08 - Recreational, Culture and Religion') AS rec_budgeted_growth,
        (SELECT "Actual Expenditure 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '08 - Recreational, Culture and Religion') AS rec_actual,
        (SELECT "% Utilization w.r.t. BE 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '08 - Recreational, Culture and Religion') AS rec_utilization,
        (SELECT "YoY- growth" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '08 - Recreational, Culture and Religion') AS rec_yoy_growth,

        (SELECT "Actual Expenditure 2022-23" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '09 - Education Affairs and Services') AS edu_previous,
        (SELECT "B.E 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '09 - Education Affairs and Services') AS edu_target,
        (SELECT "Budgeted Growth %" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '09 - Education Affairs and Services') AS edu_budgeted_growth,
        (SELECT "Actual Expenditure 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '09 - Education Affairs and Services') AS edu_actual,
        (SELECT "% Utilization w.r.t. BE 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '09 - Education Affairs and Services') AS edu_utilization,
        (SELECT "YoY- growth" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '09 - Education Affairs and Services') AS edu_yoy_growth,

        (SELECT "Actual Expenditure 2022-23" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '10 - Social Protection') AS sp_previous,
        (SELECT "B.E 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '10 - Social Protection') AS sp_target,
        (SELECT "Budgeted Growth %" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '10 - Social Protection') AS sp_budgeted_growth,
        (SELECT "Actual Expenditure 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '10 - Social Protection') AS sp_actual,
        (SELECT "% Utilization w.r.t. BE 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '10 - Social Protection') AS sp_utilization,
        (SELECT "YoY- growth" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = '10 - Social Protection') AS sp_yoy_growth,

        (SELECT "Actual Expenditure 2022-23" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = 'Total Provincial Expenditure') AS func_total_previous,
        (SELECT "B.E 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = 'Total Provincial Expenditure') AS func_total_target,
        (SELECT "Budgeted Growth %" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = 'Total Provincial Expenditure') AS func_total_budgeted_growth,
        (SELECT "Actual Expenditure 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = 'Total Provincial Expenditure') AS func_total_actual,
        (SELECT "% Utilization w.r.t. BE 2023-24" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = 'Total Provincial Expenditure') AS func_total_utilization,
        (SELECT "YoY- growth" FROM "Table_4_1_B_Total_Provincial_Expenditure_by_Function" 
         WHERE "Total Provincial Expenditure by Function" = 'Total Provincial Expenditure') AS func_total_yoy_growth
)
SELECT *
FROM expenditure_category
CROSS JOIN expenditure_component
CROSS JOIN expenditure_function;
""",
        "prompt": """
            Generate a **Total Provincial Expenditure** section for the Budget Execution Report for FY {fiscal_year}.

            **Very Important:**
            - The section must be long and highly detailed, spanning multiple pages.
            - Do not summarize—discuss each indicator in full detail.
            - Use formal, structured, and analytical language in line with government budget reports.
            - Ensure clear paragraph transitions and incorporate all extracted data into the analysis.

            **Required Analysis**

            1. **Overview of Provincial Expenditure**
            - Define **Total Provincial Expenditure (TPE)** and discuss its significance in fiscal management.
            - Explain how TPE is composed of current, capital (split into two accounts), and development expenditures.
            - Emphasize the role of expenditure in meeting fiscal targets and ensuring efficient public service delivery.

            2. **Performance vs. Budget Targets**
            - Compare the actual expenditure against the budgeted estimates for FY {fiscal_year}.
            - Highlight deviations between the actual spending and the budgeted allocations.
            - Discuss external factors (e.g., economic conditions, administrative constraints, policy shifts) influencing these variances.

            #### **3. Analysis of Key Expenditure Categories**
            - **Current Expenditure:** Rs. {current_actual} billion (Budgeted: Rs. {current_target} billion, Previous: Rs. {current_previous} billion)
                - Analyze the performance in service delivery maintenance and improvements.
                - Examine the YoY growth of {current_yoy_growth}% and the budget achievement of {current_achievement}%, noting any trends.
            - **Current Capital Expenditure A/C-I:** Rs. {capital_1_actual} billion (Budgeted: Rs. {capital_1_target} billion, Previous: Rs. {capital_1_previous} billion)
                - Discuss the impact of loans, equity investments, and pension liabilities on this category.
                - Analyze its YoY growth of {capital_1_yoy_growth}% and the achieved {capital_1_achievement}% of the budget.
            - **Current Capital Expenditure A/C-II:** Rs. {capital_2_actual} billion (Budgeted: Rs. {capital_2_target} billion, Previous: Rs. {capital_2_previous} billion)
                - Focus on issues like delays in fund allocations and loan repayments.
                - Evaluate the YoY growth of {capital_2_yoy_growth}% and the budget utilization of {capital_2_achievement}%.
            - **Development Expenditure:** Rs. {development_actual} billion (Budgeted: Rs. {development_target} billion, Previous: Rs. {development_previous} billion)
                - Assess investments in capacity building and infrastructure projects.
                - Review its YoY growth of {development_yoy_growth}% and the budget achievement of {development_achievement}%.
            - **Total Provincial Expenditure:** Rs. {expenditure_actual} billion (Budgeted: Rs. {expenditure_target} billion, Previous: Rs. {expenditure_previous} billion)
                - Analyze the overall YoY growth of {expenditure_yoy_growth}% and the overall budget utilization of {budget_utilization}%.

            4. **Functional Classification of Expenditure**
            - Break down the expenditure by function and analyse changes in explanatory form; highlight any increases or decreases, covering:
                - **General Public Service:** Actual: {gps_actual} billion (Target: {gps_target} billion, Previous: {gps_previous} billion), Utilization: {gps_utilization}%, YoY Growth: {gps_yoy_growth}%.
                - **Public Order & Safety Affairs:** Actual: {pos_actual} billion (Target: {pos_target} billion, Previous: {pos_previous} billion), Utilization: {pos_utilization}%, YoY Growth: {pos_yoy_growth}%.
                - **Economic Affairs:** Actual: {eco_actual} billion (Target: {eco_target} billion, Previous: {eco_previous} billion), Utilization: {eco_utilization}%, YoY Growth: {eco_yoy_growth}%.
                - **Environment Protection:** Actual: {env_actual} billion (Target: {env_target} billion, Previous: {env_previous} billion), Utilization: {env_utilization}%, YoY Growth: {env_yoy_growth}%.
                - **Housing and Community Amenities:** Actual: {house_actual} billion (Target: {house_target} billion, Previous: {house_previous} billion), Utilization: {house_utilization}%, YoY Growth: {house_yoy_growth}%.
                - **Health:** Actual: {health_actual} billion (Target: {health_target} billion, Previous: {health_previous} billion), Utilization: {health_utilization}%, YoY Growth: {health_yoy_growth}%.
                - **Recreational, Culture and Religion:** Actual: {rec_actual} billion (Target: {rec_target} billion, Previous: {rec_previous} billion), Utilization: {rec_utilization}%, YoY Growth: {rec_yoy_growth}%.
                - **Education Affairs and Services:** Actual: {edu_actual} billion (Target: {edu_target} billion, Previous: {edu_previous} billion), Utilization: {edu_utilization}%, YoY Growth: {edu_yoy_growth}%.
                - **Social Protection:** Actual: {sp_actual} billion (Target: {sp_target} billion, Previous: {sp_previous} billion), Utilization: {sp_utilization}%, YoY Growth: {sp_yoy_growth}%.
                - **Overall (Function Total):** Actual: {func_total_actual} billion (Target: {func_total_target} billion, Previous: {func_total_previous} billion), Utilization: {func_total_utilization}%, YoY Growth: {func_total_yoy_growth}%.
        
            5. **Causes, Implications, and Policy Considerations**
            - Identify the key factors behind the expenditure variances, including administrative challenges and economic conditions.
            - Discuss the implications of these variances on fiscal sustainability and service delivery.
            - Provide recommendations to improve budget utilization and align spending with fiscal targets.

            **Final Output Must Be:**
            - Extremely detailed, offering deep insight into each expenditure category.
            - Structured in multiple paragraphs with a formal government reporting style.
            - Free of placeholders—each extracted data point must be seamlessly integrated.
        """
    }

sections["Analysis of Expenses - 4.1.1 Current Expenditure"] = {
    "query": """
            WITH current_expenditure_category AS (
                SELECT
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Salary' THEN "Actual Expenditure 2022-23" END), 0) AS salary_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Salary' THEN "B.E 2023-24" END), 0) AS salary_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Salary' THEN "Actual Expenditure 2023-24" END), 0) AS salary_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Salary' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS salary_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Salary' THEN "YoY- growth" END), 0) AS salary_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Pension' THEN "Actual Expenditure 2022-23" END), 0) AS pension_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Pension' THEN "B.E 2023-24" END), 0) AS pension_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Pension' THEN "Actual Expenditure 2023-24" END), 0) AS pension_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Pension' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS pension_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Pension' THEN "YoY- growth" END), 0) AS pension_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Transfers (to LGs and others)' THEN "Actual Expenditure 2022-23" END), 0) AS transfers_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Transfers (to LGs and others)' THEN "B.E 2023-24" END), 0) AS transfers_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Transfers (to LGs and others)' THEN "Actual Expenditure 2023-24" END), 0) AS transfers_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Transfers (to LGs and others)' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS transfers_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Transfers (to LGs and others)' THEN "YoY- growth" END), 0) AS transfers_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Non-Salary (Service Delivery Expenditure)' THEN "Actual Expenditure 2022-23" END), 0) AS service_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Non-Salary (Service Delivery Expenditure)' THEN "B.E 2023-24" END), 0) AS service_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Non-Salary (Service Delivery Expenditure)' THEN "Actual Expenditure 2023-24" END), 0) AS service_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Non-Salary (Service Delivery Expenditure)' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS service_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Non-Salary (Service Delivery Expenditure)' THEN "YoY- growth" END), 0) AS service_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Total Current Expenditure' THEN "Actual Expenditure 2022-23" END), 0) AS current_previous_total,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Total Current Expenditure' THEN "B.E 2023-24" END), 0) AS current_target_total,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Total Current Expenditure' THEN "Actual Expenditure 2023-24" END), 0) AS current_actual_total,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Total Current Expenditure' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS budget_utilization,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Category" = 'Total Current Expenditure' THEN "YoY- growth" END), 0) AS current_yoy_growth_total
                FROM "Table_4_1_1_A_Total_Provincial_Current_Expenditure_Category_wise"
            ),
            current_expenditure_object AS (
                SELECT
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A01-Employee Related Expenses' THEN "Actual Expenditure 2022-23" END), 0) AS employee_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A01-Employee Related Expenses' THEN "B.E 2023-24" END), 0) AS employee_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A01-Employee Related Expenses' THEN "Actual Expenditure 2023-24" END), 0) AS employee_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A01-Employee Related Expenses' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS employee_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A01-Employee Related Expenses' THEN "YoY- growth" END), 0) AS employee_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A02-Project Pre-investment Analysis' THEN "Actual Expenditure 2022-23" END), 0) AS preinv_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A02-Project Pre-investment Analysis' THEN "B.E 2023-24" END), 0) AS preinv_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A02-Project Pre-investment Analysis' THEN "Actual Expenditure 2023-24" END), 0) AS preinv_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A02-Project Pre-investment Analysis' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS preinv_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A02-Project Pre-investment Analysis' THEN "YoY- growth" END), 0) AS preinv_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A03-Operating Expenses' THEN "Actual Expenditure 2022-23" END), 0) AS operating_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A03-Operating Expenses' THEN "B.E 2023-24" END), 0) AS operating_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A03-Operating Expenses' THEN "Actual Expenditure 2023-24" END), 0) AS operating_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A03-Operating Expenses' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS operating_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A03-Operating Expenses' THEN "YoY- growth" END), 0) AS operating_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A04-Employees Retirement Benefits' THEN "Actual Expenditure 2022-23" END), 0) AS pension_obj_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A04-Employees Retirement Benefits' THEN "B.E 2023-24" END), 0) AS pension_obj_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A04-Employees Retirement Benefits' THEN "Actual Expenditure 2023-24" END), 0) AS pension_obj_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A04-Employees Retirement Benefits' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS pension_obj_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A04-Employees Retirement Benefits' THEN "YoY- growth" END), 0) AS pension_obj_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" LIKE 'A05-%' THEN "Actual Expenditure 2022-23" END), 0) AS grants_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" LIKE 'A05-%' THEN "B.E 2023-24" END), 0) AS grants_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" LIKE 'A05-%' THEN "Actual Expenditure 2023-24" END), 0) AS grants_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" LIKE 'A05-%' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS grants_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" LIKE 'A05-%' THEN "YoY- growth" END), 0) AS grants_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A06-Transfers' THEN "Actual Expenditure 2022-23" END), 0) AS obj_transfers_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A06-Transfers' THEN "B.E 2023-24" END), 0) AS obj_transfers_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A06-Transfers' THEN "Actual Expenditure 2023-24" END), 0) AS obj_transfers_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A06-Transfers' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS obj_transfers_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A06-Transfers' THEN "YoY- growth" END), 0) AS obj_transfers_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A07-Interest Payment' THEN "Actual Expenditure 2022-23" END), 0) AS interest_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A07-Interest Payment' THEN "B.E 2023-24" END), 0) AS interest_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A07-Interest Payment' THEN "Actual Expenditure 2023-24" END), 0) AS interest_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A07-Interest Payment' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS interest_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A07-Interest Payment' THEN "YoY- growth" END), 0) AS interest_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A09-Expenditure on Acquiring of Physical Assets' THEN "Actual Expenditure 2022-23" END), 0) AS physical_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A09-Expenditure on Acquiring of Physical Assets' THEN "B.E 2023-24" END), 0) AS physical_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A09-Expenditure on Acquiring of Physical Assets' THEN "Actual Expenditure 2023-24" END), 0) AS physical_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A09-Expenditure on Acquiring of Physical Assets' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS physical_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A09-Expenditure on Acquiring of Physical Assets' THEN "YoY- growth" END), 0) AS physical_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A12-Civil Works' THEN "Actual Expenditure 2022-23" END), 0) AS civil_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A12-Civil Works' THEN "B.E 2023-24" END), 0) AS civil_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A12-Civil Works' THEN "Actual Expenditure 2023-24" END), 0) AS civil_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A12-Civil Works' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS civil_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A12-Civil Works' THEN "YoY- growth" END), 0) AS civil_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A13-Repairs and Maintenance' THEN "Actual Expenditure 2022-23" END), 0) AS repairs_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A13-Repairs and Maintenance' THEN "B.E 2023-24" END), 0) AS repairs_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A13-Repairs and Maintenance' THEN "Actual Expenditure 2023-24" END), 0) AS repairs_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A13-Repairs and Maintenance' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS repairs_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A13-Repairs and Maintenance' THEN "YoY- growth" END), 0) AS repairs_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A14-Suspence and Clearing' THEN "Actual Expenditure 2022-23" END), 0) AS suspence_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A14-Suspence and Clearing' THEN "B.E 2023-24" END), 0) AS suspence_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A14-Suspence and Clearing' THEN "Actual Expenditure 2023-24" END), 0) AS suspence_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A14-Suspence and Clearing' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS suspence_achievement,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'A14-Suspence and Clearing' THEN "YoY- growth" END), 0) AS suspence_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'Total Current Expenditure' THEN "Actual Expenditure 2022-23" END), 0) AS obj_total_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'Total Current Expenditure' THEN "B.E 2023-24" END), 0) AS obj_total_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'Total Current Expenditure' THEN "Actual Expenditure 2023-24" END), 0) AS obj_total_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'Total Current Expenditure' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS obj_total_utilization,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Object" = 'Total Current Expenditure' THEN "YoY- growth" END), 0) AS obj_total_yoy_growth
                FROM "Table_4_1_1_B_Total_Current_Expenditure_by_Object"
            ),
            current_expenditure_function AS (
                SELECT
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '01 - General Public Service' THEN "Actual Expenditure 2022-23" END), 0) AS gps_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '01 - General Public Service' THEN "B.E 2023-24" END), 0) AS gps_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '01 - General Public Service' THEN "Budgeted Growth %" END), 0) AS gps_budgeted_growth,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '01 - General Public Service' THEN "Actual Expenditure 2023-24" END), 0) AS gps_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '01 - General Public Service' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS gps_utilization,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '01 - General Public Service' THEN "YoY- growth" END), 0) AS gps_yoy_growth,
        
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '03 - Public Order and Safety Affairs' THEN "Actual Expenditure 2022-23" END), 0) AS pos_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '03 - Public Order and Safety Affairs' THEN "B.E 2023-24" END), 0) AS pos_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '03 - Public Order and Safety Affairs' THEN "Budgeted Growth %" END), 0) AS pos_budgeted_growth,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '03 - Public Order and Safety Affairs' THEN "Actual Expenditure 2023-24" END), 0) AS pos_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '03 - Public Order and Safety Affairs' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS pos_utilization,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '03 - Public Order and Safety Affairs' THEN "YoY- growth" END), 0) AS pos_yoy_growth,
        
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '04 - Economic Affairs' THEN "Actual Expenditure 2022-23" END), 0) AS eco_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '04 - Economic Affairs' THEN "B.E 2023-24" END), 0) AS eco_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '04 - Economic Affairs' THEN "Budgeted Growth %" END), 0) AS eco_budgeted_growth,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '04 - Economic Affairs' THEN "Actual Expenditure 2023-24" END), 0) AS eco_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '04 - Economic Affairs' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS eco_utilization,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '04 - Economic Affairs' THEN "YoY- growth" END), 0) AS eco_yoy_growth,
        
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '05 - Environment Protection' THEN "Actual Expenditure 2022-23" END), 0) AS env_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '05 - Environment Protection' THEN "B.E 2023-24" END), 0) AS env_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '05 - Environment Protection' THEN "Budgeted Growth %" END), 0) AS env_budgeted_growth,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '05 - Environment Protection' THEN "Actual Expenditure 2023-24" END), 0) AS env_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '05 - Environment Protection' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS env_utilization,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '05 - Environment Protection' THEN "YoY- growth" END), 0) AS env_yoy_growth,
        
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '06 - Housing and Community Amenities' THEN "Actual Expenditure 2022-23" END), 0) AS house_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '06 - Housing and Community Amenities' THEN "B.E 2023-24" END), 0) AS house_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '06 - Housing and Community Amenities' THEN "Budgeted Growth %" END), 0) AS house_budgeted_growth,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '06 - Housing and Community Amenities' THEN "Actual Expenditure 2023-24" END), 0) AS house_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '06 - Housing and Community Amenities' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS house_utilization,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '06 - Housing and Community Amenities' THEN "YoY- growth" END), 0) AS house_yoy_growth,
        
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '07 – Health' THEN "Actual Expenditure 2022-23" END), 0) AS health_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '07 – Health' THEN "B.E 2023-24" END), 0) AS health_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '07 – Health' THEN "Budgeted Growth %" END), 0) AS health_budgeted_growth,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '07 – Health' THEN "Actual Expenditure 2023-24" END), 0) AS health_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '07 – Health' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS health_utilization,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '07 – Health' THEN "YoY- growth" END), 0) AS health_yoy_growth,
        
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '08 - Recreational, Culture and Religion' THEN "Actual Expenditure 2022-23" END), 0) AS rec_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '08 - Recreational, Culture and Religion' THEN "B.E 2023-24" END), 0) AS rec_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '08 - Recreational, Culture and Religion' THEN "Budgeted Growth %" END), 0) AS rec_budgeted_growth,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '08 - Recreational, Culture and Religion' THEN "Actual Expenditure 2023-24" END), 0) AS rec_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '08 - Recreational, Culture and Religion' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS rec_utilization,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '08 - Recreational, Culture and Religion' THEN "YoY- growth" END), 0) AS rec_yoy_growth,
        
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '09 - Education Affairs and Services' THEN "Actual Expenditure 2022-23" END), 0) AS edu_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '09 - Education Affairs and Services' THEN "B.E 2023-24" END), 0) AS edu_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '09 - Education Affairs and Services' THEN "Budgeted Growth %" END), 0) AS edu_budgeted_growth,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '09 - Education Affairs and Services' THEN "Actual Expenditure 2023-24" END), 0) AS edu_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '09 - Education Affairs and Services' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS edu_utilization,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '09 - Education Affairs and Services' THEN "YoY- growth" END), 0) AS edu_yoy_growth,
        
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '10 - Social Protection' THEN "Actual Expenditure 2022-23" END), 0) AS sp_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '10 - Social Protection' THEN "B.E 2023-24" END), 0) AS sp_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '10 - Social Protection' THEN "Budgeted Growth %" END), 0) AS sp_budgeted_growth,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '10 - Social Protection' THEN "Actual Expenditure 2023-24" END), 0) AS sp_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '10 - Social Protection' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS sp_utilization,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = '10 - Social Protection' THEN "YoY- growth" END), 0) AS sp_yoy_growth,
        
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = 'Total Current Expenditure' THEN "Actual Expenditure 2022-23" END), 0) AS func_total_previous,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = 'Total Current Expenditure' THEN "B.E 2023-24" END), 0) AS func_total_target,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = 'Total Current Expenditure' THEN "Budgeted Growth %" END), 0) AS func_total_budgeted_growth,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = 'Total Current Expenditure' THEN "Actual Expenditure 2023-24" END), 0) AS func_total_actual,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = 'Total Current Expenditure' THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS func_total_utilization,
                    COALESCE(MAX(CASE WHEN "Current Expenditure by Function" = 'Total Current Expenditure' THEN "YoY- growth" END), 0) AS func_total_yoy_growth
                FROM "Table_4_1_1_C_Total_Current_Expenditure_by_Function"
            )
            SELECT *
            FROM current_expenditure_category
            CROSS JOIN current_expenditure_object
            CROSS JOIN current_expenditure_function;
        """,
        "prompt": """
            Generate a **Current Expenditure** section for the Budget Execution Report for FY {fiscal_year}.

            **Very Important:**
            - The section must be long and highly detailed, spanning multiple pages.
            - Do not summarize—discuss each indicator in full detail.
            - Use formal, structured, and analytical language consistent with government budget reports.
            - Integrate all extracted data from category, object, and function levels into the analysis.

            **Required Analysis**

            1. **Overview of Current Expenditure**
            - Define **Current Expenditure** and explain its importance as the largest component of provincial spending.
            - Clarify that it includes salaries, pensions, transfers to local governments, and non-salary (service delivery) expenses.
            - Emphasize its role in ensuring effective public service delivery and operational governance.

            2. **Performance vs. Budget Targets**
            - Compare the actual current expenditure of Rs. {current_actual_total} billion against the budgeted target of Rs. {current_target_total} billion for FY {fiscal_year}.
            - Discuss key variances and identify factors—such as inflation, high interest rates, or policy constraints—that contributed to these deviations.
            - Note the overall budget utilization rate of {budget_utilization}% for current expenditure.

            #### **3. Analysis of Key Expenditure Categories**
            - **Salary Expenditure:** Rs. {salary_actual} billion (Budgeted: Rs. {salary_target} billion, Previous: Rs. {salary_previous} billion)
                - Analyze trends in employee-related spending.
                - Evaluate a YoY growth of {salary_yoy_growth}% and a budget achievement of {salary_achievement}%.
            - **Pension Expenditure:** Rs. {pension_actual} billion (Budgeted: Rs. {pension_target} billion, Previous: Rs. {pension_previous} billion)
                - Discuss the impact of mandatory pension payments and inflation.
                - Review a YoY growth of {pension_yoy_growth}% and a budget achievement of {pension_achievement}%.
            - **Transfers to Local Governments:** Rs. {transfers_actual} billion (Budgeted: Rs. {transfers_target} billion, Previous: Rs. {transfers_previous} billion)
                - Explain how transfers support local governance.
                - Analyze a YoY growth of {transfers_yoy_growth}% and a budget utilization of {transfers_achievement}%.
            - **Non-Salary (Service Delivery) Expenditure:** Rs. {service_actual} billion (Budgeted: Rs. {service_target} billion, Previous: Rs. {service_previous} billion)
                - Examine spending on operational costs and service delivery functions.
                - Discuss a YoY growth of {service_yoy_growth}% and a budget achievement of {service_achievement}%.
            - **Total Current Expenditure:** Rs. {current_actual_total} billion (Budgeted: Rs. {current_target_total} billion, Previous: Rs. {current_previous_total} billion)
                - Summarize overall performance with a YoY growth of {current_yoy_growth_total}% and overall budget utilization of {budget_utilization}%.

            3. **Object-Level Analysis**
            - Provide detailed analysis of object-level expenditure and analyse changes in explanatory form; highlight any increases or decreases such as:
                - **Employee-Related Expenses:** Actual: {employee_actual} billion, Target: {employee_target} billion, Previous: {employee_previous} billion, YoY: {employee_yoy_growth}%, Achievement: {employee_achievement}%.
                - **Project Pre-investment Analysis:** Actual: {preinv_actual} billion, etc.
                - **Operating Expenses:** Actual: {operating_actual} billion, etc.
                - **Employees Retirement Benefits:** Actual: {pension_obj_actual} billion, etc.
                - **Grants/Subsidies/Write-offs:** Actual: {grants_actual} billion, etc.
                - **Transfers (object level):** Actual: {obj_transfers_actual} billion, etc.
                - **Interest Payments:** Actual: {interest_actual} billion, etc.
                - **Acquisitions of Physical Assets:** Actual: {physical_actual} billion, etc.
                - **Civil Works:** Actual: {civil_actual} billion, etc.
                - **Repairs & Maintenance:** Actual: {repairs_actual} billion, etc.
                - **Suspence and Clearing:** Actual: {suspence_actual} billion, etc.
                - **Total (object level):** Actual: {obj_total_actual} billion, Utilization: {obj_total_utilization}%, YoY Growth: {obj_total_yoy_growth}%.

            4. **Functional Classification of Current Expenditure**
            - Break down current expenditure by function and analyse changes in explanatory form; highlight any increases or decreases:
                - **General Public Service:** Actual: {gps_actual} billion (Target: {gps_target} billion, Previous: {gps_previous} billion), Utilization: {gps_utilization}%, YoY Growth: {gps_yoy_growth}%.
                - **Public Order & Safety Affairs:** Actual: {pos_actual} billion (Target: {pos_target} billion, Previous: {pos_previous} billion), Utilization: {pos_utilization}%, YoY Growth: {pos_yoy_growth}%.
                - **Economic Affairs:** Actual: {eco_actual} billion (Target: {eco_target} billion, Previous: {eco_previous} billion), Utilization: {eco_utilization}%, YoY Growth: {eco_yoy_growth}%.
                - **Environment Protection:** Actual: {env_actual} billion (Target: {env_target} billion, Previous: {env_previous} billion), Utilization: {env_utilization}%, YoY Growth: {env_yoy_growth}%.
                - **Housing and Community Amenities:** Actual: {house_actual} billion (Target: {house_target} billion, Previous: {house_previous} billion), Utilization: {house_utilization}%, YoY Growth: {house_yoy_growth}%.
                - **Health:** Actual: {health_actual} billion (Target: {health_target} billion, Previous: {health_previous} billion), Utilization: {health_utilization}%, YoY Growth: {health_yoy_growth}%.
                - **Recreational, Culture and Religion:** Actual: {rec_actual} billion (Target: {rec_target} billion, Previous: {rec_previous} billion), Utilization: {rec_utilization}%, YoY Growth: {rec_yoy_growth}%.
                - **Education Affairs and Services:** Actual: {edu_actual} billion (Target: {edu_target} billion, Previous: {edu_previous} billion), Utilization: {edu_utilization}%, YoY Growth: {edu_yoy_growth}%.
                - **Social Protection:** Actual: {sp_actual} billion (Target: {sp_target} billion, Previous: {sp_previous} billion), Utilization: {sp_utilization}%, YoY Growth: {sp_yoy_growth}%.
                - **Overall (Function Total):** Actual: {func_total_actual} billion (Target: {func_total_target} billion, Previous: {func_total_previous} billion), Utilization: {func_total_utilization}%, YoY Growth: {func_total_yoy_growth}%.

            5. **Causes, Implications, and Policy Considerations**
            - Identify the primary drivers behind current expenditure variances, such as inflation, high interest rates, or policy constraints.
            - Discuss the implications of these variances on fiscal sustainability and public service delivery.
            - Provide recommendations for enhancing budget utilization and aligning current expenditure with fiscal targets.

            **Final Output Must Be:**
            - Extremely detailed, offering deep insights into every component of current expenditure.
            - Structured in multiple paragraphs in a formal government reporting style.
            - Free of placeholders—each extracted data point must be seamlessly integrated.
        """
    }

sections["Analysis of Expenses - 4.1.2 Total Current Capital Expenditure"] = {
    "query": """
            WITH capital_expenditure AS (
                SELECT
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Current Capital Expenditure A/C-I' 
                                      THEN "Actual Expenditure 2022-23" END), 0) AS capital_1_previous,
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Current Capital Expenditure A/C-I' 
                                      THEN "B.E 2023-24" END), 0) AS capital_1_target,
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Current Capital Expenditure A/C-I' 
                                      THEN "Actual Expenditure 2023-24" END), 0) AS capital_1_actual,
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Current Capital Expenditure A/C-I' 
                                      THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS capital_1_achievement,
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Current Capital Expenditure A/C-I' 
                                      THEN "YoY- growth" END), 0) AS capital_1_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Current Capital Expenditure A/C-II' 
                                      THEN "Actual Expenditure 2022-23" END), 0) AS capital_2_previous,
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Current Capital Expenditure A/C-II' 
                                      THEN "B.E 2023-24" END), 0) AS capital_2_target,
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Current Capital Expenditure A/C-II' 
                                      THEN "Actual Expenditure 2023-24" END), 0) AS capital_2_actual,
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Current Capital Expenditure A/C-II' 
                                      THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS capital_2_achievement,
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Current Capital Expenditure A/C-II' 
                                      THEN "YoY- growth" END), 0) AS capital_2_yoy_growth,

                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Total Current Capital Expenditure' 
                                      THEN "Actual Expenditure 2022-23" END), 0) AS capital_previous,
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Total Current Capital Expenditure' 
                                      THEN "B.E 2023-24" END), 0) AS capital_target,
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Total Current Capital Expenditure' 
                                      THEN "Actual Expenditure 2023-24" END), 0) AS capital_actual,
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Total Current Capital Expenditure' 
                                      THEN "% Utilization w.r.t. BE 2023-24" END), 0) AS budget_utilization,
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Total Current Capital Expenditure' 
                                      THEN "YoY- growth" END), 0) AS capital_yoy_growth,
                    
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Debt Repayments & Loans Disbursed' 
                                      THEN "Actual Expenditure 2023-24" END), 0) AS debt_actual,
                    COALESCE(MAX(CASE WHEN "Total Current Capital Expenditure" = 'Commodity Financing Expenditure' 
                                      THEN "Actual Expenditure 2023-24" END), 0) AS commodity_actual
                FROM "Total_Current_Capital_Expenditure_Account_wise"
            ),
            ac_i AS (
                SELECT
                    COALESCE(MAX("Actual Expenditure 2022-23"), 0) AS ac_i_previous,
                    COALESCE(MAX("B.E 2023-24"), 0) AS ac_i_target,
                    COALESCE(MAX("Actual Expenditure 2023-24"), 0) AS ac_i_actual,
                    COALESCE(MAX("% Utilization w.r.t. BE 2023-24"), 0) AS ac_i_achievement,
                    COALESCE(MAX("YoY- growth"), 0) AS ac_i_yoy_growth
                FROM "Current_Capital_Expenditure_A_C_I"
            ),
            ac_ii AS (
                SELECT
                    COALESCE(MAX("Actual Expenditure 2022-23"), 0) AS ac_ii_previous,
                    COALESCE(MAX("B.E 2023-24"), 0) AS ac_ii_target,
                    COALESCE(MAX("Actual Expenditure 2023-24"), 0) AS ac_ii_actual,
                    COALESCE(MAX("% Utilization w.r.t. BE 2023-24"), 0) AS ac_ii_achievement,
                    COALESCE(MAX("YoY- growth"), 0) AS ac_ii_yoy_growth
                FROM "Current_Capital_Expenditure_A_C_II"
            )
            SELECT *
            FROM capital_expenditure
            CROSS JOIN ac_i
            CROSS JOIN ac_ii;
        """,
        "prompt": """
            Generate a **Total Current Capital Expenditure** section for the Budget Execution Report for FY {fiscal_year}.

            **Overview of Current Capital Expenditure:**
            - Total current capital expenditure for FY {fiscal_year} was Rs. {capital_actual} billion.
            - The budget target was Rs. {capital_target} billion with an overall budget utilization of {budget_utilization}%.
            - Year-on-year growth was {capital_yoy_growth}%, reflecting significant fiscal adjustments in capital spending.

            **Breakdown of Expenditure Categories:**
            - **Current Capital Expenditure A/C-I:**
              Fully Break it down and analyse changes in explanatory form; highlight any increases or decreases
              - Includes debt repayments, government loans, and public sector investments.
              - Actual expenditure was Rs. {capital_1_actual} billion versus a target of Rs. {capital_1_target} billion.
              - Achieved {capital_1_achievement}% of its budget with a YoY growth of {capital_1_yoy_growth}%.
              - Notably, debt repayments accounted for Rs. {debt_actual} billion, emphasizing efforts to reduce fiscal liabilities.
            - **Current Capital Expenditure A/C-II:**
              - Pertains primarily to commodity financing operations.
              - Actual spending was Rs. {capital_2_actual} billion against a target of Rs. {capital_2_target} billion.
              - Budget utilization in this category was {capital_2_achievement}% with a YoY growth of {capital_2_yoy_growth}%.
              - Commodity financing expenditure reached Rs. {commodity_actual} billion, influenced by revised market policies.

            **Performance vs. Budget Targets:**
            - Overall, the province’s current capital expenditure increased compared to the previous fiscal year (from Rs. {capital_previous} billion).
            - The strong performance in A/C-I demonstrates an aggressive approach to debt reduction, while A/C-II’s performance reflects a more cautious strategy in commodity financing.
            - The combined results underscore a dual-track fiscal strategy focused on reducing high-cost debt while adapting commodity financing to volatile market conditions.

            **Implications and Future Policy Considerations:**
            - The robust growth in A/C-I, especially with significant debt repayments, signals a clear commitment to fiscal consolidation.
            - The underperformance in A/C-II suggests that market conditions and policy shifts have led to more conservative commodity financing.
            - Future policies should aim to balance aggressive debt reduction with adaptive commodity financing strategies to ensure long-term fiscal sustainability.
        """
    }

sections["Analysis of Expenses - 4.1.3 Development Expenditure"] = {
    "query": """
SELECT json_group_array(
         json_object(
           'category', t.category,
           'previous', t.previous,
           'target', t.target,
           'actual', t.actual,
           'utilization', t.utilization,
           'yoy', t.yoy
         )
       ) AS result
FROM (
    SELECT 
        "Development Expenditure by Object" AS category,
        SUM("Actual Expenditure 2022-23") AS previous,
        SUM("B.E 2023-24") AS target,
        SUM("Actual Expenditure 2023-24") AS actual,
        SUM("% Utilization w.r.t. BE 2023-24") AS utilization,
        SUM("YoY- growth") AS yoy
    FROM "Total_Development_Expenditure_by_Object"
    WHERE "Development Expenditure by Object" IN (
        'A01-Employee Related Expenses', 'A02-Project Pre-investment Analysis', 'A03-Operating Expenses',
        'A04-Employees Retirement Benefits', 'A05-Grants, Subsidies and Writeoffs of Loans/Advances/Others',
        'A06-Transfers', 'A08-Loans and Advances', 'A09-Expenditure on Acquiring of Physical Assets',
        'A11-Investments', 'A12-Civil Works', 'A13-Repairs and Maintenance', 'Total'
    )
    GROUP BY "Development Expenditure by Object"
    UNION ALL
    SELECT 
        "Development Expenditure by Function" AS category,
        SUM("Actual Expenditure 2022-23") AS previous,
        SUM("B.E 2023-24") AS target,
        SUM("Actual Expenditure 2023-24") AS actual,
        SUM("% Utilization w.r.t. BE 2023-24") AS utilization,
        SUM("YoY- growth") AS yoy
    FROM "Total_Development_Expenditure_by_Function"
    WHERE "Development Expenditure by Function" IN (
        '01 - General Public Service', '03 - Public Order and Safety Affairs', '04 - Economic Affairs',
        '05 - Environment Protection', '06 - Housing and Community Amenities', '07 - Health',
        '08 - Recreational, Culture and Religion', '09 - Education Affairs and Services', '10 - Social Protection', 'Total'
    )
    GROUP BY "Development Expenditure by Function"
) t;
    """,
    "prompt": """
            Generate a **Development Expenditure** section for the Budget Execution Report for FY {fiscal_year}.

            **Very Important:**
            - The section must be long and highly detailed, spanning multiple pages.
            - Do not summarize—discuss each indicator in full detail.
            - Use formal, structured, and analytical language consistent with government budget reports.
            - Integrate all extracted data from both the object and function tables into the analysis.

            **Required Analysis**

            1. **Overview of Development Expenditure**
            - Define **Development Expenditure** as government spending aimed at improving service delivery and building infrastructure.
            - Emphasize its role in long-term public service improvements and economic development.
            - State that in FY {fiscal_year}, total development expenditure was Rs. {development_actual} billion (Target: Rs. {development_target} billion), with a budget utilization rate of {budget_utilization}% and a YoY growth of {development_yoy_growth}%.

            2. **Analysis by Object**
            - Examine each object-level category:
                - **Employee Related Expenses:** Actual 2022-23: Rs. {a01_previous} billion, Budget 2023-24: Rs. {a01_target} billion, Actual 2023-24: Rs. {a01_actual} billion, Utilization: {a01_utilization}%, YoY Growth: {a01_yoy}%.
                - **Project Pre-investment Analysis:** Actual 2022-23: Rs. {a02_previous} billion, Budget 2023-24: Rs. {a02_target} billion, Actual 2023-24: Rs. {a02_actual} billion, Utilization: {a02_utilization}%, YoY Growth: {a02_yoy}%.
                - **Operating Expenses:** Actual 2022-23: Rs. {a03_previous} billion, Budget 2023-24: Rs. {a03_target} billion, Actual 2023-24: Rs. {a03_actual} billion, Utilization: {a03_utilization}%, YoY Growth: {a03_yoy}%.
                - **Employees Retirement Benefits:** Actual 2022-23: Rs. {a04_previous} billion, Budget 2023-24: Rs. {a04_target} billion, Actual 2023-24: Rs. {a04_actual} billion, Utilization: {a04_utilization}%, YoY Growth: {a04_yoy}%.
                - **Grants, Subsidies and Writeoffs:** Actual 2022-23: Rs. {a05_previous} billion, Budget 2023-24: Rs. {a05_target} billion, Actual 2023-24: Rs. {a05_actual} billion, Utilization: {a05_utilization}%, YoY Growth: {a05_yoy}%.
                - **Transfers:** Actual 2022-23: Rs. {a06_previous} billion, Budget 2023-24: Rs. {a06_target} billion, Actual 2023-24: Rs. {a06_actual} billion, Utilization: {a06_utilization}%, YoY Growth: {a06_yoy}%.
                - **Loans and Advances:** Actual 2022-23: Rs. {a08_previous} billion, Budget 2023-24: Rs. {a08_target} billion, Actual 2023-24: Rs. {a08_actual} billion, Utilization: {a08_utilization}%, YoY Growth: {a08_yoy}%.
                - **Expenditure on Acquiring Physical Assets:** Actual 2022-23: Rs. {a09_previous} billion, Budget 2023-24: Rs. {a09_target} billion, Actual 2023-24: Rs. {a09_actual} billion, Utilization: {a09_utilization}%, YoY Growth: {a09_yoy}%.
                - **Investments:** Actual 2022-23: Rs. {a11_previous} billion, Budget 2023-24: Rs. {a11_target} billion, Actual 2023-24: Rs. {a11_actual} billion, Utilization: {a11_utilization}%, YoY Growth: {a11_yoy}%.
                - **Civil Works:** Actual 2022-23: Rs. {a12_previous} billion, Budget 2023-24: Rs. {a12_target} billion, Actual 2023-24: Rs. {a12_actual} billion, Utilization: {a12_utilization}%, YoY Growth: {a12_yoy}%.
                - **Repairs and Maintenance:** Actual 2022-23: Rs. {a13_previous} billion, Budget 2023-24: Rs. {a13_target} billion, Actual 2023-24: Rs. {a13_actual} billion, Utilization: {a13_utilization}%, YoY Growth: {a13_yoy}%.
                - **Total (Object Level):** Actual 2022-23: Rs. {total_obj_previous} billion, Budget 2023-24: Rs. {total_obj_target} billion, Actual 2023-24: Rs. {total_obj_actual} billion, Utilization: {total_obj_utilization}%, YoY Growth: {total_obj_yoy}%.

            3. **Analysis by Function**
            - Evaluate performance by function:
                - **General Public Service:** Actual 2022-23: Rs. {gp_previous} billion, Budget 2023-24: Rs. {gp_target} billion, Actual 2023-24: Rs. {gp_actual} billion, Utilization: {gp_utilization}%, YoY Growth: {gp_yoy}%.
                - **Public Order & Safety Affairs:** Actual 2022-23: Rs. {pos_previous} billion, Budget 2023-24: Rs. {pos_target} billion, Actual 2023-24: Rs. {pos_actual} billion, Utilization: {pos_utilization}%, YoY Growth: {pos_yoy}%.
                - **Economic Affairs:** Actual 2022-23: Rs. {eco_previous} billion, Budget 2023-24: Rs. {eco_target} billion, Actual 2023-24: Rs. {eco_actual} billion, Utilization: {eco_utilization}%, YoY Growth: {eco_yoy}%.
                - **Environment Protection:** Actual 2022-23: Rs. {env_previous} billion, Budget 2023-24: Rs. {env_target} billion, Actual 2023-24: Rs. {env_actual} billion, Utilization: {env_utilization}%, YoY Growth: {env_yoy}%.
                - **Housing and Community Amenities:** Actual 2022-23: Rs. {house_previous} billion, Budget 2023-24: Rs. {house_target} billion, Actual 2023-24: Rs. {house_actual} billion, Utilization: {house_utilization}%, YoY Growth: {house_yoy}%.
                - **Health:** Actual 2022-23: Rs. {health_previous} billion, Budget 2023-24: Rs. {health_target} billion, Actual 2023-24: Rs. {health_actual} billion, Utilization: {health_utilization}%, YoY Growth: {health_yoy}%.
                - **Recreational, Culture and Religion:** Actual 2022-23: Rs. {rec_previous} billion, Budget 2023-24: Rs. {rec_target} billion, Actual 2023-24: Rs. {rec_actual} billion, Utilization: {rec_utilization}%, YoY Growth: {rec_yoy}%.
                - **Education Affairs and Services:** Actual 2022-23: Rs. {edu_previous} billion, Budget 2023-24: Rs. {edu_target} billion, Actual 2023-24: Rs. {edu_actual} billion, Utilization: {edu_utilization}%, YoY Growth: {edu_yoy}%.
                - **Social Protection:** Actual 2022-23: Rs. {sp_previous} billion, Budget 2023-24: Rs. {sp_target} billion, Actual 2023-24: Rs. {sp_actual} billion, Utilization: {sp_utilization}%, YoY Growth: {sp_yoy}%.
                - **Total (Function Level):** Actual 2022-23: Rs. {total_func_previous} billion, Budget 2023-24: Rs. {total_func_target} billion, Actual 2023-24: Rs. {total_func_actual} billion, Utilization: {total_func_utilization}%, YoY Growth: {total_func_yoy}%.

            4. **Causes, Implications, and Policy Considerations**
            - Analyze the factors behind deviations in development expenditure, such as delays caused by the interim government, policy changes, or market conditions.
            - Discuss how these spending patterns have affected service delivery and infrastructure projects.
            - Offer recommendations for optimizing future development spending and improving budget utilization.

            **Final Output Must Be:**
            - Extremely detailed, offering deep insights into every component of development expenditure.
            - Structured in multiple paragraphs in a formal government reporting style.
            - Free of placeholders—each extracted data point must be seamlessly integrated.
        """
    }

sections["Analysis of Budget Management - 5.1"] = {
    "query": """
            WITH bm AS (
                SELECT
                    MAX(CASE WHEN "Fiscal Statement" = 'General Revenue Receipts' THEN "Actual 2022-23" END) AS receipts_previous,
                    MAX(CASE WHEN "Fiscal Statement" = 'General Revenue Receipts' THEN "BE 2023-24" END) AS receipts_target,
                    MAX(CASE WHEN "Fiscal Statement" = 'General Revenue Receipts' THEN "Actual 2023-24" END) AS receipts_actual,

                    MAX(CASE WHEN "Fiscal Statement" = 'Total Current Expenditure' THEN "Actual 2022-23" END) AS expenditure_previous,
                    MAX(CASE WHEN "Fiscal Statement" = 'Total Current Expenditure' THEN "BE 2023-24" END) AS expenditure_target,
                    MAX(CASE WHEN "Fiscal Statement" = 'Total Current Expenditure' THEN "Actual 2023-24" END) AS expenditure_actual,

                    MAX(CASE WHEN "Fiscal Statement" = 'Revenue Balance (A-B)' THEN "Actual 2022-23" END) AS revenue_previous,
                    MAX(CASE WHEN "Fiscal Statement" = 'Revenue Balance (A-B)' THEN "BE 2023-24" END) AS revenue_target,
                    MAX(CASE WHEN "Fiscal Statement" = 'Revenue Balance (A-B)' THEN "Actual 2023-24" END) AS revenue_actual,

                    MAX(CASE WHEN "Fiscal Statement" = 'Net Capital Receipts (E-F)' THEN "Actual 2022-23" END) AS net_capital_previous,
                    MAX(CASE WHEN "Fiscal Statement" = 'Net Capital Receipts (E-F)' THEN "BE 2023-24" END) AS net_capital_target,
                    MAX(CASE WHEN "Fiscal Statement" = 'Net Capital Receipts (E-F)' THEN "Actual 2023-24" END) AS net_capital_actual,

                    MAX(CASE WHEN "Fiscal Statement" = 'Capital Receipt (A/C-I & A/C-II)' THEN "Actual 2022-23" END) AS capital_receipt_previous,
                    MAX(CASE WHEN "Fiscal Statement" = 'Capital Receipt (A/C-I & A/C-II)' THEN "BE 2023-24" END) AS capital_receipt_target,
                    MAX(CASE WHEN "Fiscal Statement" = 'Capital Receipt (A/C-I & A/C-II)' THEN "Actual 2023-24" END) AS capital_receipt_actual,

                    MAX(CASE WHEN "Fiscal Statement" = 'Capital Exp. (A/C-I & A/C-II)' THEN "Actual 2022-23" END) AS capital_expenditure_previous,
                    MAX(CASE WHEN "Fiscal Statement" = 'Capital Exp. (A/C-I & A/C-II)' THEN "BE 2023-24" END) AS capital_expenditure_target,
                    MAX(CASE WHEN "Fiscal Statement" = 'Capital Exp. (A/C-I & A/C-II)' THEN "Actual 2023-24" END) AS capital_expenditure_actual,

                    MAX(CASE WHEN "Fiscal Statement" = 'Net Resources for Development (C+D)' THEN "Actual 2022-23" END) AS development_resources_previous,
                    MAX(CASE WHEN "Fiscal Statement" = 'Net Resources for Development (C+D)' THEN "BE 2023-24" END) AS development_resources_target,
                    MAX(CASE WHEN "Fiscal Statement" = 'Net Resources for Development (C+D)' THEN "Actual 2023-24" END) AS development_resources_actual,

                    MAX(CASE WHEN "Fiscal Statement" = 'Development Exp.' THEN "Actual 2022-23" END) AS development_expenditure_previous,
                    MAX(CASE WHEN "Fiscal Statement" = 'Development Exp.' THEN "BE 2023-24" END) AS development_expenditure_target,
                    MAX(CASE WHEN "Fiscal Statement" = 'Development Exp.' THEN "Actual 2023-24" END) AS development_expenditure_actual,

                    MAX(CASE WHEN "Fiscal Statement" = 'Fiscal Balance (G-H)' THEN "Actual 2022-23" END) AS fiscal_previous,
                    MAX(CASE WHEN "Fiscal Statement" = 'Fiscal Balance (G-H)' THEN "BE 2023-24" END) AS fiscal_target,
                    MAX(CASE WHEN "Fiscal Statement" = 'Fiscal Balance (G-H)' THEN "Actual 2023-24" END) AS fiscal_actual,

                    MAX(CASE WHEN "Fiscal Statement" = 'Interest Expense' THEN "Actual 2022-23" END) AS interest_expense_previous,
                    MAX(CASE WHEN "Fiscal Statement" = 'Interest Expense' THEN "BE 2023-24" END) AS interest_expense_target,
                    MAX(CASE WHEN "Fiscal Statement" = 'Interest Expense' THEN "Actual 2023-24" END) AS interest_expense_actual,

                    MAX(CASE WHEN "Fiscal Statement" = 'Primary Balance (I-J)' THEN "Actual 2022-23" END) AS primary_balance_previous,
                    MAX(CASE WHEN "Fiscal Statement" = 'Primary Balance (I-J)' THEN "BE 2023-24" END) AS primary_balance_target,
                    MAX(CASE WHEN "Fiscal Statement" = 'Primary Balance (I-J)' THEN "Actual 2023-24" END) AS primary_balance_actual
                FROM "budget_management"
            )
            SELECT * FROM bm;
        """,
    "prompt": """
            Generate a **Budget Management** section for the Budget Execution Report for FY {fiscal_year}.  

            **Very Important:**  
            - The section must be long and highly detailed, spanning multiple pages.  
            - Do not summarize—discuss each indicator in full detail.  
            - Use formal, structured, and analytical language in line with government budget reports.  
            - Ensure clear paragraph transitions and incorporate all extracted data into the analysis.  

            **Required Analysis**  

            1. **Overview of Budget Management**  
            - Define **Budget Management** and its role in ensuring fiscal discipline, efficient resource allocation, and financial sustainability.  
            - Explain how budgetary performance is assessed by comparing actual receipts and expenditures against budget estimates.  
            - Highlight key fiscal metrics, including revenue balance, net capital receipts, development expenditure, and fiscal balance, to evaluate financial health.  

            2. **Performance vs. Budget Targets**  
            - Compare **actual receipts vs. budget estimates** for **FY {fiscal_year}**, highlighting any over- or under-performance.  
            - Discuss major factors influencing revenue collection, such as economic conditions, tax compliance, and external financing.  
            - Examine **total provincial expenditure**, analyzing variances between actual and budgeted spending.  
            - Assess deviations in revenue balance, net capital receipts, and fiscal balance to determine fiscal performance trends.  

            #### **3. Analysis of Key Fiscal Indicators**  
            - **Total Provincial Receipts**: Rs. {receipts_actual} billion (Target: Rs. {receipts_target} billion, Previous: Rs. {receipts_previous} billion).  
            - **Total Provincial Expenditure**: Rs. {expenditure_actual} billion (Target: Rs. {expenditure_target} billion, Previous: Rs. {expenditure_previous} billion).  
            - **Revenue Balance**: Rs. {revenue_actual} billion (Target: Rs. {revenue_target} billion, Previous: Rs. {revenue_previous} billion).  
            - **Net Capital Receipts**: Rs. {net_capital_actual} billion (Target: Rs. {net_capital_target} billion, Previous: Rs. {net_capital_previous} billion).  
            - **Capital Receipts**: Rs. {capital_receipt_actual} billion (Target: Rs. {capital_receipt_target} billion, Previous: Rs. {capital_receipt_previous} billion).  
            - **Capital Expenditure**: Rs. {capital_expenditure_actual} billion (Target: Rs. {capital_expenditure_target} billion, Previous: Rs. {capital_expenditure_previous} billion).  
            - **Development Resources Available**: Rs. {development_resources_actual} billion (Target: Rs. {development_resources_target} billion, Previous: Rs. {development_resources_previous} billion).  
            - **Development Expenditure**: Rs. {development_expenditure_actual} billion (Target: Rs. {development_expenditure_target} billion, Previous: Rs. {development_expenditure_previous} billion).  
            - **Fiscal Balance**: Rs. {fiscal_actual} billion (Target: Rs. {fiscal_target} billion, Previous: Rs. {fiscal_previous} billion).  
            - **Interest Expense**: Rs. {interest_expense_actual} billion (Target: Rs. {interest_expense_target} billion, Previous: Rs. {interest_expense_previous} billion).  
            - **Primary Balance**: Rs. {primary_balance_actual} billion (Target: Rs. {primary_balance_target} billion, Previous: Rs. {primary_balance_previous} billion).  

            4. **Causes, Implications, and Policy Considerations**  
            - Analyze the factors driving budget shortfalls and surpluses.  
            - Assess fiscal sustainability in light of current revenue-expenditure trends.  
            - Recommend policy interventions for improving fiscal management.  

            **Final Output Must Be:**  
            - Extremely detailed, offering deep insights into every budget component.  
            - Structured in multiple paragraphs with a formal government reporting style.  
            - Free of placeholders—each extracted data point must be seamlessly integrated.  
        """
    }










if __name__ == "__main__":
    generate_report(sections)