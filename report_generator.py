import concurrent.futures
import pypandoc
import pandas as pd
import dataframe_image as dfi
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # <<--- Must come first!

from utils import run_sql_query, extract_json_from_output, replace_placeholders
from config import llm

import os
import shutil
import re

def enforce_two_decimal_places(text):
    """Format only numerical values in normal text, avoiding titles and table names."""
    lines = text.split("\n")
    def format_match(match):
        num = float(match.group())
        return f"{num:.2f}"
    formatted_lines = []
    for line in lines:
        if line.startswith("#") or "![Table for" in line:
            formatted_lines.append(line)
        else:
            formatted_line = re.sub(r"\b\d+\.\d+\b", format_match, line)
            formatted_lines.append(formatted_line)
    return "\n".join(formatted_lines)

# Define the folder to save images
IMAGE_FOLDER = "tables"

def format_numbers(obj):
    """Recursively format all numerical values to exactly 2 decimal places."""
    if isinstance(obj, dict):
        return {k: format_numbers(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [format_numbers(item) for item in obj]
    elif isinstance(obj, (int, float)):
        return "{:.2f}".format(float(obj))
    return obj

def clean_image_folder():
    """Deletes all existing images in the folder before saving new ones."""
    if os.path.exists(IMAGE_FOLDER):
        shutil.rmtree(IMAGE_FOLDER)
    os.makedirs(IMAGE_FOLDER)

def get_cleaned_dataframe(data):
    """
    Convert raw data into a DataFrame and clean it by converting columns to numeric
    and dropping rows where all values are NaN.
    """
    # If data is a dict, wrap it in a list.
    if isinstance(data, dict):
        data = [data]
    df = pd.DataFrame(data)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(how="all", inplace=True)
    return df

def create_styled_table_image(data, filename="table.png", layout="multiple_rows"):
    """
    Create a styled table image from SQL result data.
    
    Parameters:
      data: list of dicts from your SQL result.
      filename: output PNG file name.
      layout: "multiple_rows" for normal table or "transpose" for a single-row pivot.
      
    Returns:
      The filename of the generated image.
    """
    if not data:
        print("No data to create a table.")
        return None

    # Ensure data is a list of dictionaries.
    if isinstance(data, dict):
        data = [data]

    # Clean data using the helper function.
    df = get_cleaned_dataframe(data)
    if df.empty:
        print("⚠ No valid rows remain after cleaning. Skipping image generation.")
        return None

    # Prettify column names.
    df.columns = [col.replace("_", " ").strip().title() for col in df.columns]

    # Adjust layout.
    if layout == "transpose":
        if len(df) == 1:
            df = df.T.reset_index()
            df.columns = ["Metric", "Value"]
        else:
            print("⚠ layout='transpose' but data has multiple rows. Using as-is.")

    numeric_cols = df.select_dtypes(include='number').columns
    styled_df = df.style.background_gradient(subset=numeric_cols, cmap='Greens')
    styled_df = styled_df.format({col: "{:.2f}" for col in numeric_cols})
    styled_df.set_table_styles([
        {"selector": "th", "props": [("font-size", "10pt"), ("font-weight", "bold"), 
                                       ("text-align", "center"), ("background-color", "#D3D3D3")]},
        {"selector": "td", "props": [("font-size", "10pt"), ("text-align", "center")]}
    ], overwrite=False)

    output_path = os.path.join(IMAGE_FOLDER, filename)
    try:
        dfi.export(styled_df, output_path, max_rows=-1, max_cols=-1)
        print(f"✅ Table image created: {output_path}")
        return output_path
    except Exception as e:
        print("❌ Error exporting table image:", e)
        return None

def create_bar_graph_image(data, filename="bar_graph.png"):
    """
    Create a grouped bar graph where:
      - Each row in the data becomes a category on the x-axis.
      - Each numeric column becomes a set of bars within each category.
      
    The figure is enlarged and the legend font size is reduced.
    
    Parameters:
      data: list of dictionaries.
      filename: name of the output PNG file.
      
    Returns:
      The output path of the generated bar graph image, or None if creation fails.
    """
    if not data:
        print("No data to create a bar graph.")
        return None

    df = pd.DataFrame(data)
    
    if df.empty or len(df.columns) < 2:
        print("⚠ Not enough columns for a bar graph.")
        return None

    # Assume the first column contains category labels
    category_col = df.columns[0]
    df[category_col] = df[category_col].astype(str)

    # Select numerical columns
    numeric_cols = df.select_dtypes(include='number').columns
    if numeric_cols.empty:
        print("⚠ No numeric columns available for bar graph.")
        return None

    # Bar width and position settings
    num_bars = len(numeric_cols)
    bar_width = 0.2
    x = range(len(df))  # Positions for categories

    # Create a larger figure (e.g., 16 x 8 inches)
    plt.figure(figsize=(16, 8))
    
    for i, col in enumerate(numeric_cols):
        plt.bar(
            [pos + (i * bar_width) for pos in x],  # Shift each set of bars
            df[col],
            width=bar_width,
            label=col.replace("_", " ").title()
        )

    # Formatting
    plt.xlabel(category_col.replace("_", " ").title())
    plt.ylabel("Values")
    plt.title("Grouped Bar Graph")
    plt.xticks([pos + (bar_width * (num_bars / 2)) for pos in x], df[category_col], rotation=45, ha="right")
    
    # Set legend with a smaller font size
    plt.legend(title="Legend", fontsize="small", title_fontsize="small", loc="upper right")
    
    plt.tight_layout()

    # Save the graph
    output_path = os.path.join(IMAGE_FOLDER, filename)
    try:
        plt.savefig(output_path)
        plt.close()
        print(f"✅ Bar graph created: {output_path}")
        return output_path
    except Exception as e:
        print("❌ Error exporting bar graph image:", e)
        plt.close()
        return None

# Clean up the image folder before generating new images.
clean_image_folder()

def generate_section(section_name, section_details):
    """Generate a single section of the report, including a table image and, if applicable, a bar graph image."""
    print(f"Generating {section_name}...")
    print("SECTION DETAILS:", section_details)

    # 1) Extract data from SQL query or fallback to parameters.
    result_data = []
    if section_details.get("query"):
        raw_output = run_sql_query(section_details["query"])
        # Optionally: result_data = extract_json_from_output(str(raw_output))
        result_data = format_numbers(raw_output)
    else:
        result_data = section_details.get("params", [])

    print("RESULT DATA:", result_data)

    # 2) Clean the data using get_cleaned_dataframe.
    df = get_cleaned_dataframe(result_data)
    
    # Determine the final row count from the table that is converted into an image.
    # If using transpose layout and the original data has one row,
    # the final table will have one row per original column.
    table_layout = "transpose"
    if table_layout == "transpose" and len(df) == 1:
        final_table_row_count = df.shape[1]  # number of columns becomes rows after transposition
    else:
        final_table_row_count = df.shape[0]
    print(f"Final table row count (from image): {final_table_row_count}")

    # 3) Generate textual content via LLM.
    placeholders = {"fiscal_year": "2023-24"}
    filled_prompt = replace_placeholders(section_details["prompt"], placeholders)
    strict_instruction = f"""
You are generating a **formal, structured section** for a Budget Execution Report (BER).

**DO NOT create any numerical values yourself. Use only the extracted SQL data.**
- Ensure all placeholders are correctly replaced with real values.
- DO NOT return raw code, tables, or placeholders.
- Write a clear, well-structured, paragraph-based response.
- Maintain a professional, analytical, and data-driven tone.
- Follow the provided prompt exactly without adding extra sections.

**Extracted Data for Reference:**
{result_data}

**Prompt to Follow:**
{filled_prompt}
"""
    section_output = llm.generate_content(strict_instruction).text

    # 4) Create a table image using the cleaned data.
    table_md = ""
    if not df.empty:
        safe_section_name = section_name.replace(" ", "_").replace("/", "_")
        table_filename = f"{safe_section_name}_table.png"
        created_file = create_styled_table_image(df.to_dict('records'), table_filename, layout=table_layout)
        if created_file:
            table_md = f"\n\n![Table for {section_name}]({created_file}){{width=35%}}\n\n"

    # 5) If the final table (i.e. the image) has 25 or more rows, create a bar graph image as well.
    bar_graph_md = ""
    if final_table_row_count >= 25:
        safe_section_name = section_name.replace(" ", "_").replace("/", "_")
        graph_filename = f"{safe_section_name}_bar_graph.png"
        created_graph = create_bar_graph_image(df.to_dict('records'), graph_filename)
        if created_graph:
            bar_graph_md = f"\n\n![Bar Graph for {section_name}]({created_graph}){{width=35%}}\n\n"

    # 6) Return combined text + images.
    return f"# {section_name}\n\n{section_output}\n\n{table_md}{bar_graph_md}"

def generate_report(sections):
    """Generate the full report by processing all sections concurrently."""
    if len(sections) < 1:
        print("⚠️ Warning: The sections dictionary contains no sections.")
        return

    print(f"✅ {len(sections)} section(s) found. Proceeding with report generation...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        section_md_list = list(executor.map(lambda item: generate_section(*item), sections.items()))

    final_report_md = "".join(section_md_list)
    print(final_report_md)

    title_page_md = """
<div style="text-align: center; margin-top: 250px;">
  <h1 style="font-size: 48px; font-weight: bold;">Budget Execution Report</h1>
  <h2 style="font-size: 36px; font-weight: bold;">Fiscal Year 2023-24</h2>
  <p style="font-size: 18px;">December 2023</p>
</div>

<div style="page-break-after: always;"></div>
"""
    final_report_md = title_page_md + "".join(section_md_list)
    final_report_md = enforce_two_decimal_places(final_report_md)

    with open('final_report.md', 'w', encoding='utf-8') as file:
        file.write(final_report_md)

    try:
        output_filename = "Budget_Execution_Report.docx"
        extra_args = ['--toc', '--toc-depth=2']
        pypandoc.convert_text(
            final_report_md,
            'docx',
            format='md',
            outputfile=output_filename,
            extra_args=extra_args
        )
        print(f"Full Budget Execution Report generated successfully in {output_filename}!")
    except Exception as e:
        print("❌ Error during conversion to DOCX:", e)
