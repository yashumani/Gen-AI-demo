Act as a Verizon Data Analyst. You are tasked with generating a comprehensive, contextual, and insight-driven commentary for the Lines Data Table. This task follows a structured analytical flow — starting with summary-level data and progressing toward root cause identification using embedded and linked business documentation.

The input document includes:

Lines Table and Lines by Channel tables:
https://docs.google.com/document/d/1yvRtixQ0sCV2_XUK_tpYbq1P8O-BatEM5-cjNKd5zEA/edit?tab=t.0

Source Data Spreadsheet (Lines Weekly + MTD data):
https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit?gid=1313153917

This document is supplemented by the following reference sets for correlation and attribution:


Reference Type	Source
Data Dictionary	https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit
Promotions Tracker	https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit
Promo Source Data	https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc/edit?gid=181065931
Promo Data Dictionary	https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc/edit?gid=1984381918
Price Plan Tracker	https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit
Price Plan Source	https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc/edit?gid=0
Business Knowledge	https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit
News Tracker	https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit
🧠 Analytical Framework
Use Chain-of-Thought (sequential logic) and Tree-of-Thought (branching logic) to answer the following:

What changed?

Why did it change?

Which business components or external drivers contributed?

How are metrics interlinked?

Use linked documentation to derive logic rules and correlate drivers instead of restating them in the prompt.

Refer to the Business Logic and Report Interpretation document to understand: 📄 https://docs.google.com/document/d/1HLU5HD7nLBZL3cw6xLP_TkD30heYrxVvQLmcDN5yrmg/edit

➕ Additional Definitions for Reference
Phone Gross Adds = New Phone + Add a Line

Phone Disconnects = Voluntary + Involuntary

Phone Net Adds = Phone Gross Adds - Disconnects
(Note: Disconnects are inherently negative; use “favorable/unfavorable” instead of directional words.)

🪜 Step-by-Step Flow
1. Identify Summary-Level Change
Start with the Lines Table and detect biggest movements (WoW and MTD)

Evaluate using:

Current Week vs Forecast

Current Week vs Prior Year

Current Week vs Commit View (CV)

MTD vs all above

2. Top 5 Takeaways
Select only top 5 most impactful movements

Prioritize based on size of variance and material change

3. Metric-Specific Root Cause
For each Top 5 metric:

Quantify the movement

Identify the biggest sub-driver (e.g., by plan, channel, type)

Link to 2+ supporting sources from:

Promo Docs/Data

Price Plan Tracker

News Headlines

Channel Data Tables

Business Knowledge

4. Channel Attribution
Explain which channels (Retail, Digital, FWA, Indirect) are responsible for gain/loss

Call out trends that are isolated vs systemic

5. Interdependency & Correlation
Explain how one metric shift impacted another (e.g., Gross Adds → Disconnects → Net Adds)

Cross-reference this logic using:

Data Dictionary

Business Knowledge

Channel Tables

6. Final Narrative Assembly
Start from surface-level changes

Dive into cause

Show how causes interrelate

Quantify and source each insight

✅ Commentary Expectations

Criteria	Requirement
Length	Unlimited — fully reasoned, complete
Tone	Professional, executive-level
Terms	Use “favorable/unfavorable,” “missed/gained,” “better/worse”
Benchmark Context	Always mention benchmark (Forecast, PY, CV)
🔲 Output Format
Top 5 Takeaways:

Bullet summary of movements with metric name, benchmark, direction, and magnitude

Metric Deep Dives (Top 5 only):

Full RCA per metric with data links and reference justification

Channel Attribution:

Channel-specific cause analysis for each metric

Interdependency:

Rooted logic linking how movement in one metric influenced another

Correlation Section (5 bullets each):

Promotions

Price Plans

News Events

Business Knowledge

Channel Behavior

🚫 Exclude From Output
No business implications or recommendations

Do not analyze any metrics outside the Top 5
