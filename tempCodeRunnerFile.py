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