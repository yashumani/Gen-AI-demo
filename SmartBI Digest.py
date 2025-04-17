import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv("config.env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini Pro model
model = genai.GenerativeModel("gemini-pro")

# References
LINES_DOC = "https://docs.google.com/document/d/1yvRtixQ0sCV2_XUK_tpYbq1P8O-BatEM5-cjNKd5zEA/edit?tab=t.0"
SOURCE_DATA = "https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit"
DATA_DICTIONARY = "https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit"
PROMO_DOC = "https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit"
PROMO_SHEET = "https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc/edit?gid=181065931"
PRICE_PLAN_DOC = "https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit"
PRICE_PLAN_SHEET = "https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc"
BUSINESS_KNOWLEDGE = "https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit"
NEWS_TRACKER = "https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit?gid=0"

# Step 1: Surface-Level Analysis
def generate_surface_analysis(lines_df):
    prompt = f"""
You are a Verizon data analyst. Based on the Lines table from this source: {LINES_DOC}, and data provided below, identify the top Week-over-Week and Month-to-Date changes.

{lines_df.to_markdown()}

List the 5 most material movements.
"""
    return model.generate_content(prompt).text

# Step 2: Top 5 Takeaways Summary
def generate_top_5_takeaways(surface_summary):
    prompt = f"""
Using the top metric changes summary below, extract a bulletized list of the top 5 takeaways.

{surface_summary}

Be concise but insightful. Indicate if each takeaway is relative to Forecast, Prior Year, or CV.
"""
    return model.generate_content(prompt).text

# Step 3: Deep Dive Analysis (Per Top Metric)
def generate_metric_deep_dive(metric_name, metric_data):
    prompt = f"""
Perform a root cause analysis for the metric: **{metric_name}** using data below:

Metric Table:
{metric_data.to_markdown()}

Use these reference documents for context:
- Data Dictionary: {DATA_DICTIONARY}
- Promotions Tracker: {PROMO_DOC}, {PROMO_SHEET}
- Price Plans: {PRICE_PLAN_DOC}, {PRICE_PLAN_SHEET}
- Channel Tables: {LINES_DOC}
- News Events: {NEWS_TRACKER}
- Business Knowledge: {BUSINESS_KNOWLEDGE}

Explain what caused the change. Include:
- Specific drivers with supporting math (e.g., "missed forecast by 9.2K")
- Reference the type of comparison (Forecast, PY, CV)
- Only focus on the key sub-drivers
"""
    return model.generate_content(prompt).text

# Step 4: Channel Attribution Logic
def generate_channel_attribution(channel_df):
    prompt = f"""
Based on channel-level data extracted from this document: {LINES_DOC}, attribute performance across FWA, Retail, Digital, and Indirect.

{channel_df.to_markdown()}

Explain whether the trend was specific to a channel or systemic.
"""
    return model.generate_content(prompt).text

# Step 5: Interdependency & Correlation
def generate_interdependency_section(top_5_text):
    prompt = f"""
Using the following Top 5 Takeaways summary, describe logical interdependencies and cross-document correlations:

{top_5_text}

Establish:
- How one metric influenced another (e.g., Gross Adds drove Net Adds)
- 5 cross-source correlations grouped under:
  • Promotions ({PROMO_SHEET})
  • Price Plans ({PRICE_PLAN_SHEET})
  • News Events ({NEWS_TRACKER})
  • Channel Tables ({LINES_DOC})
  • Business Knowledge ({BUSINESS_KNOWLEDGE})
"""
    return model.generate_content(prompt).text

# Example Usage with KNIME table data
lines_df = pd.DataFrame()  # Load this from KNIME
channel_df = pd.DataFrame()  # Load this from KNIME

# Execute sequential Gemini-powered flow
surface_summary = generate_surface_analysis(lines_df)
top_5_takeaways = generate_top_5_takeaways(surface_summary)

# Deep Dive Loop for each top metric
top_metrics = ["Phone Gross Adds", "Phone Disconnects"]  # Replace with dynamic list later
deep_dive_outputs = [generate_metric_deep_dive(metric, lines_df) for metric in top_metrics]

channel_output = generate_channel_attribution(channel_df)
interdependency_output = generate_interdependency_section(top_5_takeaways)

# Outputs ready to store as KNIME flow variables or assemble final document
print(top_5_takeaways)
print("\n".join(deep_dive_outputs))
print(channel_output)
print(interdependency_output)
