import gspread
from google import genai
from google.genai import types
from google.api_core import retry
import pandas as pd

# Define a retry mechanism for API calls
is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})
genai.models.Models.generate_content = retry.Retry(predicate=is_retriable)(genai.models.Models.generate_content)

# API Key and client initialization
GOOGLE_API_KEY = "AIzaSyBzKOM5LQpkvCjyA3Yzyf1NLcg4Jlcjcds"
client = genai.Client(api_key=GOOGLE_API_KEY)

# Google Sheets API setup
gc = gspread.service_account(filename='path_to_service_account.json')  # Replace with your service account JSON file
sheet_url = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"  # Replace with your Google Sheet URL
sh = gc.open_by_url(sheet_url)
worksheet = sh.sheet1  # Access the first sheet

# Fetch data from Google Sheets into a Pandas DataFrame
data = worksheet.get_all_records()
df = pd.DataFrame(data)

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

... (rest of the prompt remains unchanged)
"""

# Generate content using the enhanced prompt
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=few_shot_prompt
)

# Print the response
print(response.text)
