Act as a Verizon Data Analyst and you are tasked with generating a comprehensive, contextual, and insight-driven commentary for the Lines data table. This task follows a structured analytical journey — starting with the summary-level Lines data and uncovering root causes using embedded business documentation.
Note: The input document now includes the Lines data table and reference materials (e.g., Promotions, Price Plans, Business Knowledge, News Events, Channel Data Tables). This format is designed to support richer interdependencies and correlation logic. In addition, the Lines data is correlated with Phone Lines and Phone Accounts, since user can have multiple lines under one account.
Use the following documents as sources:
Lines Table and Lines by Channel tables: 
https://docs.google.com/document/d/1yvRtixQ0sCV2_XUK_tpYbq1P8O-BatEM5-cjNKd5zEA/edit?tab=t.0
Source Data Spreadsheet: https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit?gid=1313153917#gid=1313153917
Data Dictionary: https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit?tab=t.0
Promotions Tracker: https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit?tab=t.0
Promotions Source Data Spreadsheet:
https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc/edit?gid=181065931#gid=181065931
Promotions Data Dictionary:
https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc/edit?gid=1984381918#gid=1984381918
Price Plans Tracker: https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit?tab=t.0
Price Plans Source Data: 
https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc/edit?gid=0#gid=0
Business Knowledge for Lines: https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit
News Headlines Table : https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit?gid=0#gid=0

Analytical Framework
Apply a Chain-of-Thoughts and Tree-of-Thoughts reasoning strategy:
Use a sequential problem-solving approach to articulate what changed, why it changed, and how different variables contributed.
Branch into possible causes using embedded references (promotions, news, pricing, business knowledge, channel-level drivers).
Prioritize logical, data-backed pathways and consolidate into the most defensible narrative.
Additional Note:
Phone Gross Adds (Calculated as: New Phone + Add a line Phone)
Components:
New Phone 
Add a Line Phone

Phone Disconnects (Clarify that disconnects are inherently negative; comparisons must use "favorable/unfavorable" or "better/worse")
Voluntary Disconnects
Involuntary Disconnects
Phone Net Adds (Calculated as: Phone Gross Adds minus Phone Disconnects)


Step-by-Step Flow
Start with Summary Data:
Identify largest WoW and MTD changes from the Lines Table.
Prioritize Top 5 Takeaways:
Focus only on Top 5 observations with the highest material impact (positive or negative).
Metric-Specific Root Cause Analysis (Only for Top 5 Metrics):
Perform deep dives using:
Business Logic (Data Dictionary)
Promotions
Price Plan Tracker
Channel Tables (within the document)
News Events
Business Knowledge
Apply analytical breakdown: clarify which sub-drivers caused the change, how each element contributed, and why it matters.
Channel-Level Attribution Logic:
Refer to embedded Channel Data Tables to identify:
Which channel(s) drove or suppressed each metric.
Whether a trend was channel-specific or universal.
Attribute key variances to appropriate channels with logic (e.g., FWA, Retail, Digital, Indirect).
Establish Interdependencies & Correlations:
Describe how shifts in one metric (e.g., Gross Adds) influenced others (e.g., Disconnects, Net Adds, Phone GA AAL, Phone GA New).
Correlate across reference sections to validate observations.


Commentary Requirements
Length:
No word count limit. Be comprehensive, insight-rich, and fully substantiated.
Tone:
Professional, analytical, and suitable for executive reporting.
Vocabulary:
Use: "favorable/unfavorable," "better/worse," "gained/missed."
Always clarify benchmarks: Forecast, Prior Year, Commit View (CV).

Output Structure
1. Top 5 Takeaways:
Bulletized list.
Emphasize most significant WoW and MTD movements.
2. Metric-Specific Deep Dive (Only for Metrics in Top 5):
Break down major drivers.
Include variance math (e.g., missed forecast by 9.5K).
Explain impact using at least two reference sources.
3. Interdependency Section:
Show relationships between Top 5 metrics.
Reference data dictionary and channel tables as support.
Ensure the 
4. Correlation Section:
Provide five bullet points across:
Promotions
Price Plans
News Events
Business Knowledge
Channel Table
Grouped by source to show multi-dimensional insights.

Exclude:
Business Implications section.
Analysis of metrics outside the Top 5.
Reminder:
Your final output should walk the reader step-by-step from surface-level changes to root causes using a chain-of-thought method enhanced by tree-of-thought logic.

