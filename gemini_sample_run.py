import pandas as pd
from google import genai
from google.genai import types
from google.api_core import retry

# Define a retry mechanism for API calls
is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})
genai.models.Models.generate_content = retry.Retry(predicate=is_retriable)(genai.models.Models.generate_content)

# API Key and client initialization
GOOGLE_API_KEY = "AIzaSyBzKOM5LQpkvCjyA3Yzyf1NLcg4Jlcjcds"
client = genai.Client(api_key=GOOGLE_API_KEY)

# Read data from a CSV file into a Pandas DataFrame
csv_file_path = "C:/Users/Sharya3/Desktop/GenAI/source_data.csv"  # Replace with the path to your CSV file
df = pd.read_csv(csv_file_path)

# Identify measure columns (numerical) and dimension columns (categorical or date)
measure_columns = df.select_dtypes(include=['number']).columns.tolist()
dimension_columns = df.select_dtypes(exclude=['number']).columns.tolist()

# Check if any date columns exist and convert them to datetime
for col in dimension_columns:
    if pd.api.types.is_string_dtype(df[col]):
        try:
            df[col] = pd.to_datetime(df[col])
            print(f"Identified date column: {col}")
        except (ValueError, TypeError):
            pass

# Update dimension columns after identifying date columns
dimension_columns = [col for col in dimension_columns if not pd.api.types.is_datetime64_any_dtype(df[col])]

print("Measure columns:", measure_columns)
print("Dimension columns:", dimension_columns)

# Perform analysis on the data
if 'RPT_DT' in df.columns:
    df['RPT_DT'] = pd.to_datetime(df['RPT_DT'])
    df = df.sort_values(by='RPT_DT')
    grouped = df.groupby(df['RPT_DT'].dt.to_period('M'))  # Group by month once to avoid redundant calculations
    for measure in measure_columns:
        df[f'{measure}_WoW_change'] = df[measure].diff(7)  # Assuming daily data
        df[f'{measure}_MTD_change'] = df[measure] - grouped[measure].transform('first')

# Prepare the few-shot prompt with dynamic data
data_summary = df.describe().to_string()
top_5_observations = (
    df.nlargest(5, f'{measure_columns[0]}_WoW_change').to_string(index=False)
    if f'{measure_columns[0]}_WoW_change' in df.columns
    else "WoW_change not calculated"
)

few_shot_prompt = f"""
Enhanced Prompt for Lines Table Commentary Generation:

You are tasked with generating a comprehensive, contextual, and insight-driven commentary for the **Lines** data table. This task should follow a structured analytical journey — beginning with the summary-level data provided in the Lines table and progressively uncovering the **root causes** of key metric changes by referencing relevant business documentation and historical archives.

--- Data Summary ---
{data_summary}

--- Measure Columns ---
{measure_columns}

--- Dimension Columns ---
{dimension_columns}

--- Top 5 Observations ---
{top_5_observations}

--- Additional Context ---
Use the following documents as reference inputs:
Lines Table: https://docs.google.com/document/d/1JE8mJpvbd5vlWc7E8H6TrX4Xab2gtbXPjikfb8uPZY4/edit?tab=t.0
Source Spreadsheet: https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit?gid=1313153917#gid=1313153917
Data Dictionary: https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit?tab=t.0
Channel data table:
https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit?gid=2117838166#gid=1313153917
Promotions Tracker: https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit?tab=t.0
Price Plans Tracker: https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit?tab=t.0
Business Knowledge for Lines: https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit
News Headlines Table : https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit?gid=0#gid=0
Historical Reports Archive: https://docs.google.com/document/d/134jbf090H3C56QTDpDEbLmTT1CrMRbuDhXY612Cw10o/edit?tab=t.0#heading=h.osfntl5foqzj

--- Instructions ---
1. Begin with a high-level summary of the Lines table data, highlighting key metrics and trends.
2. Identify and explain the top 5 week-over-week (WoW) changes in the data, providing potential reasons for these changes.
3. Use the provided reference documents to contextualize the changes and identify root causes.
4. Incorporate historical data and business knowledge to provide a deeper understanding of the trends.
5. Ensure the commentary is structured, concise, and actionable, with clear insights and recommendations.

--- Example Commentary ---
"Over the past week, the Lines table data reveals a significant increase in metric X, driven primarily by [reason]. This change aligns with the recent promotion campaign outlined in the Promotions Tracker. Additionally, metric Y has shown a decline, which can be attributed to [reason], as indicated in the News Event Tracker. Historical data from the CIPB Reports suggests that similar trends were observed during [specific period], highlighting the impact of [factor]."

--- Output Format ---
The output should be a well-structured and professional commentary, suitable for presentation to stakeholders. Use bullet points or numbered lists where appropriate to enhance readability.

--- Notes ---
- Ensure the commentary is data-driven and supported by evidence from the provided documents.
- Avoid generic statements; focus on actionable insights and specific observations.
- Maintain a professional tone throughout the commentary.
"""

# Generate content using the enhanced prompt
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=few_shot_prompt
)

# Print the response
print(response.text)
