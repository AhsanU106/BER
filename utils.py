import json
import re
from sqlalchemy import create_engine, text
from config import DATABASE_URL


def run_sql_query(query):
    """Execute a SQL query and return the result as a dictionary."""
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]


def extract_json_from_output(raw_output):
    """Extract JSON from raw output using regex."""
    print('RAW_OUTPUT:', raw_output)

    # Step 1: Use regex to extract the JSON-like string
    json_match = re.search(r"\{.*\}", raw_output, re.DOTALL)
    if json_match:
        raw_json = json_match.group(0)

        # Step 2: Replace single quotes with double quotes to make it valid JSON
        try:
            valid_json = raw_json.replace("'", '"')

            # Step 3: Parse the valid JSON string
            return json.loads(valid_json)
        except json.JSONDecodeError as e:
            print("❌ JSON Decoding Error:", e)
    return {}

def replace_placeholders(prompt, data):
    """Replace placeholders in the prompt with corresponding values."""
    for key, value in data.items():
        prompt = prompt.replace(f"{{{key}}}", str(value))
    return prompt