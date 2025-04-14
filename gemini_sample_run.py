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
csv_file_path = "path/to/your/input.csv"  # Replace with the path to your CSV file
df = pd.read_csv(csv_file_path)

# Perform analysis on the data
# Example: Calculate week-over-week (WoW) and month-to-date (MTD) changes
# Replace 'metric_column' and 'date_column' with actual column names
df['date_column'] = pd.to_datetime(df['date_column'])
df = df.sort_values(by='date_column')
df['WoW_change'] = df['metric_column'].diff(7)  # Assuming daily data
df['MTD_change'] = df['metric_column'] - df.groupby(df['date_column'].dt.to_period('M'))['metric_column'].transform('first')

# Few-shot prompt with dynamic data
few_shot_prompt = f"""
Enhanced Prompt for Lines Table Commentary Generation:

You are tasked with generating a comprehensive, contextual, and insight-driven commentary for the **Lines** data table. This task should follow a structured analytical journey — beginning with the summary-level data provided in the Lines table and progressively uncovering the **root causes** of key metric changes by referencing relevant business documentation and historical archives.

--- Data Summary ---
{df.describe().to_string()}

--- Top 5 Observations ---
{df.nlargest(5, 'WoW_change').to_string(index=False)}

--- Additional Context ---
Use the following documents as reference inputs:
- Lines Table: [Insert Google Doc Link - Lines Table]
- Source Spreadsheet: [Insert Google Sheets Link - Raw Data]
- Data Dictionary: [Insert Google Doc Link - Data Dictionary]
- Promotions Tracker: [Insert Google Doc Link - Promotions]
- Business Knowledge for Lines: [Insert Google Sheets Link - Business Context]
- News Event Tracker: [Insert Google Sheets Link - News Impacts]
- Historical Reports Archive: [Insert Link to Folder with Past CIPB Reports]

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
