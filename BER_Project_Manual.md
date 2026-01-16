# Budget Execution Report (BER) Automation Project
## Introductory Manual for Implementation

### Project Overview
This project automates the creation of a comprehensive Budget Execution Report for the Government of Pakistan (Punjab Province) by extracting data from Excel files, storing it in a database, and using AI to generate detailed analytical content formatted as a Word document.

---

## Phase 1: Data Preparation & Extraction

### 1.1 Source Data Collection
- **Obtain Excel files** containing budget execution data from relevant government departments
- These files contain tables with: 
  - Revenue receipts (tax and non-tax)
  - Expenditure data (current, capital, development)
  - Macroeconomic indicators
  - Fiscal statements

### 1.2 Excel to CSV Conversion
- **Convert all Excel files to CSV format**
  - Use Excel's "Save As" function or automated tools
  - Ensure proper encoding (UTF-8 recommended)
  - Preserve all numerical data without formatting loss
  - Save each sheet as a separate CSV file if multiple sheets exist

### 1.3 Define Table Schemas
- **Create a standardized table structure** for each data category: 
  - Provincial Tax Revenue (department-wise)
  - Provincial Non-Tax Revenue
  - Federal Divisible Pool data
  - General Revenue Receipts
  - Capital Receipts (current and development)
  - Expenditure categories (by category, object, function)
  - Macroeconomic assumptions
  - Budget management/fiscal statements

- **Column naming convention:**
  - Use snake_case (e.g., `Actual_Collection_2022-23`, `B.E_2023-24`)
  - Include year identifiers
  - Use consistent metric names across tables

---

## Phase 2: Database Setup & Data Loading

### 2.1 Database Creation
- **Set up a SQLite database** (lightweight, file-based)
  - Create database file: `budget_analysis.db`
  - Design schema to match your table structures

### 2.2 Create Tables
- **Define tables for each data category:**
  - `macroeconomic_assumptions`
  - `General_Revenue_Receipts`
  - `Federal_Divisible_Pool`
  - `Provincial_Tax_Revenue___Department_wise`
  - `Provincial_Non_Tax_Revenue___Department_wise`
  - `Total_Provincial_Receipts`
  - `Total_Capital_Receipts`
  - `Total_Capital_Receipts_Account_wise`
  - `Table_4_1_Total_Provincial_Expenditure_by_Category`
  - `Table_4_1_A_Total_Provincial_Expenditure_Component_wise`
  - `Table_4_1_B_Total_Provincial_Expenditure_by_Function`
  - `Table_4_1_1_A_Total_Provincial_Current_Expenditure_Category_wise`
  - `Table_4_1_1_B_Total_Current_Expenditure_by_Object`
  - `Table_4_1_1_C_Total_Current_Expenditure_by_Function`
  - `Total_Current_Capital_Expenditure_Account_wise`
  - `Current_Capital_Expenditure_A_C_I`
  - `Current_Capital_Expenditure_A_C_II`
  - `Total_Development_Expenditure_by_Object`
  - `Total_Development_Expenditure_by_Function`
  - `budget_management`

### 2.3 Import CSV Data into Database
- **Write Python scripts to:**
  - Read CSV files using pandas
  - Clean data (handle nulls, format numbers)
  - Insert data into corresponding database tables
  - Validate data integrity after import

---

## Phase 3: SQL Query Design

### 3.1 Analyze Report Requirements
- **Understand what metrics each section needs:**
  - Previous year actuals
  - Current year budget estimates (B.E)
  - Current year actual collections
  - Percentage collection vs budget
  - Year-over-year (YoY) growth percentages
  - Budget utilization rates

### 3.2 Write SQL Queries for Each Section
- **Create complex SQL queries using:**
  - `CASE` statements to pivot data
  - `MAX` aggregations to extract specific rows
  - `CROSS JOIN` to combine multiple data perspectives
  - Common Table Expressions (CTEs) for readability
  - `json_group_array` for nested data structures

- **Example structure:**
  ```sql
  SELECT 
      MAX(CASE WHEN indicator = 'X' THEN value_column END) AS x_value,
      MAX(CASE WHEN indicator = 'Y' THEN value_column END) AS y_value
  FROM table_name
  WHERE indicator IN ('X', 'Y', 'Z');
  ```

### 3.3 Test Queries
- **Verify each query returns:**
  - Correct data values
  - Proper column names (matching placeholder names)
  - All required metrics for analysis
  - Formatted numbers (2 decimal places)

---

## Phase 4: AI Prompt Engineering

### 4.1 Design Section Structure
- **Create a Python dictionary** defining all report sections with: 
  - Section name/title
  - SQL query (or None for intro sections)
  - Detailed prompt for AI content generation
  - Parameters (like fiscal year)

### 4.2 Write Comprehensive Prompts
- **Each prompt should specify:**
  - **Format requirements:** "formal, structured, analytical language"
  - **Length expectations:** "long and highly detailed, spanning multiple pages"
  - **Content structure:**
    1. Overview of the topic
    2. Performance vs. budget targets
    3. Analysis of key indicators with specific metrics
    4. Causes and implications
    5. Future outlook and policy considerations
  
- **Include explicit instructions:**
  - "Do not summarize—discuss each indicator in full detail"
  - "Use only extracted SQL data, no fabricated numbers"
  - "Integrate all data points seamlessly"
  - "Multiple paragraphs per section"
  - "Free of placeholders"

### 4.3 Define Placeholders
- **Use curly braces for variable substitution:**
  - `{fiscal_year}`: e.g., "2023-24"
  - `{grr_actual}`: Actual general revenue receipts
  - `{grr_target}`: Budgeted target
  - `{grr_previous}`: Previous year actual
  - `{grr_yoy_growth}`: Year-over-year growth percentage

---

## Phase 5: AI Integration Setup

### 5.1 Choose AI Model
- **Select a suitable LLM (Large Language Model):**
  - Google Gemini (as used in this project)
  - OpenAI GPT-4
  - Claude, etc. 

### 5.2 Configure API Access
- **Set up configuration file (`config.py`):**
  - Store API keys securely (use environment variables)
  - Initialize the LLM client
  - Set model parameters (temperature, max tokens)

### 5.3 Create Utility Functions
- **Develop helper functions (`utils.py`):**
  - `run_sql_query(query)`: Execute SQL and return results
  - `replace_placeholders(text, data)`: Replace {placeholders} with actual values
  - `extract_json_from_output()`: Parse structured data from responses
  - Database connection management

---

## Phase 6: Report Generation Engine

### 6.1 Build Section Generator
- **Create function to process each section:**
  1. Execute SQL query to extract data
  2. Format numbers to 2 decimal places
  3. Replace placeholders in prompt with actual data
  4. Send prompt + data to AI model
  5. Receive generated analytical text
  6. Create styled data tables as images
  7. Generate bar graphs for sections with 25+ data points
  8. Combine text + images into markdown format

### 6.2 Implement Table Visualization
- **Convert data to visual tables:**
  - Use pandas DataFrame for data manipulation
  - Apply styling (color gradients, formatting)
  - Export as PNG images using `dataframe_image`
  - Support both normal and transposed layouts
  - Save to `tables/` folder

### 6.3 Implement Graph Generation
- **Create bar graphs for large datasets:**
  - Use matplotlib for visualization
  - Create grouped bar charts comparing multiple metrics
  - Configure size (16x8 inches for readability)
  - Export as PNG images
  - Only generate when data has 25+ rows

### 6.4 Enable Concurrent Processing
- **Use ThreadPoolExecutor for parallel section generation:**
  - Process multiple sections simultaneously (4 workers)
  - Significantly reduces total generation time
  - Collect all section outputs

---

## Phase 7: Document Formatting & Export

### 7.1 Generate Markdown Report
- **Compile all sections into markdown:**
  - Add title page with centered formatting
  - Include page breaks between major sections
  - Embed table images using `![alt](path){width=35%}`
  - Embed graph images similarly
  - Apply consistent heading hierarchy (# for main sections)

### 7.2 Number Formatting
- **Enforce consistent decimal places:**
  - Regex pattern to find all numbers
  - Format to exactly 2 decimal places
  - Preserve titles and headers without modification

### 7.3 Convert to Word Document
- **Use pypandoc for conversion:**
  - Convert markdown to `.docx` format
  - Add table of contents (`--toc`)
  - Set TOC depth to 2 levels (`--toc-depth=2`)
  - Output file: `Budget_Execution_Report.docx`

---

## Phase 8: Quality Assurance & Validation

### 8.1 Data Verification
- **Cross-check generated content:**
  - Verify all numbers match database values
  - Ensure no placeholders remain unreplaced
  - Confirm calculations (YoY growth, percentages) are accurate

### 8.2 Format Review
- **Check document structure:**
  - Table of contents is complete
  - All images display correctly
  - Page breaks are appropriate
  - Headings follow hierarchy
  - Professional formatting maintained

### 8.3 Content Review
- **Assess analytical quality:**
  - AI-generated text is coherent and analytical
  - Explanations align with data
  - Government reporting tone is maintained
  - No fabricated information
  - All required sections present

---

## Phase 9: Execution & Maintenance

### 9.1 Run the Project
- **Execute main script:**
  ```bash
  python main.py
  ```
- Monitor console output for progress
- Check for errors in SQL queries or AI generation
- Review generated images in `tables/` folder

### 9.2 Update for New Fiscal Years
- **When new data arrives:**
  - Update CSV files with new fiscal year data
  - Reload database tables
  - Update fiscal year parameter in prompts
  - Update SQL queries if column names change
  - Regenerate report

### 9.3 Troubleshooting
- **Common issues:**
  - **Missing data:** Check CSV import and database integrity
  - **API errors:** Verify API keys and rate limits
  - **Formatting issues:** Review pypandoc installation and markdown syntax
  - **Incorrect numbers:** Validate SQL queries and data cleaning logic

---

## Key Technical Components Summary

### Required Libraries
- **Data Processing:** pandas, sqlite3
- **AI Integration:** google-generativeai (or openai, anthropic)
- **Visualization:** matplotlib, dataframe_image
- **Document Conversion:** pypandoc
- **Concurrency:** concurrent.futures (built-in)
- **Utilities:** os, shutil, re

### File Structure
```
project/
├── main.py                          # Section definitions & orchestration
├── report_generator.py              # Core generation logic
├── utils.py                         # Helper functions
├── config.py                        # API configuration
├── budget_analysis.db               # SQLite database
├── tables/                          # Generated images folder
├── final_report.md                  # Intermediate markdown output
└── Budget_Execution_Report.docx     # Final Word document
```

### Workflow Summary
**Input:** Excel/CSV files → **Process:** Extract to DB → **Query:** SQL data extraction → **Generate:** AI content creation → **Visualize:** Tables & graphs → **Format:** Markdown compilation → **Output:** Word document

---

## Success Criteria

A successful replication achieves:
1. ✅ All budget data accurately imported into database
2. ✅ SQL queries return correct, complete datasets
3. ✅ AI generates detailed, coherent analytical text
4. ✅ All placeholders replaced with actual values
5. ✅ Tables and graphs render correctly
6. ✅ Final Word document is professionally formatted
7. ✅ Content aligns with government reporting standards
8. ✅ No manual intervention required for generation

---

## Tips for Success

1. **Start small:** Test with one or two sections before scaling to full report
2. **Validate data early:** Ensure database accuracy before generation
3. **Test prompts iteratively:** Refine AI prompts based on output quality
4. **Document assumptions:** Keep track of data transformations and business logic
5. **Version control:** Use Git to track changes in queries and prompts
6. **Error handling:** Add try-catch blocks for robust execution
7. **Logging:** Implement comprehensive logging for debugging
8. **Backup data:** Keep original Excel files and database backups

---

**End of Manual**