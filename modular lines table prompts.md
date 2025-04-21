**PROMPT 1**

Title: Surface-Level Benchmark Analysis (Initial Discovery)
You are a Verizon Data Analyst. Analyze the Lines Table data (Weekly and MTD) using the Google Sheet provided below:
Lines Source Data:
https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit

🎯 Objective:
Identify Top 10 metrics exhibiting the most significant movement by comparing against all relevant benchmarks:

Current Week vs Forecast

Current Week vs Prior Year (PY)

Current Week vs Commit View (CV)

Month-to-Date (MTD) vs Forecast

MTD vs CV

MTD vs PY

Week-over-Week (WoW) trend change (3-week patterns if applicable)

🧠 What to Consider:
Prioritize material movement (positive or negative).

Highlight strongest variance deltas across any benchmark.

Avoid redundancy – group similar metrics (e.g., plan-level splits under one header).

Treat Disconnect metrics as inherently negative – fewer is better, more is worse.

Look for sustained trends, reversals, or unexpected surges.

Ensure WoW changes are given space to stand alone if compelling.

📝 Output Format (Bullet Style):
[Metric Name] — Missed Forecast by 87K and CV by 75K; WoW reversal observed from last 3-week decline.

[Metric Name] — MTD variance against PY is +45K; double-digit mix growth in recent trend.

[Metric Name] — Strong surge this week, exceeding all benchmarks; needs deeper attribution next.





**PROMPT 2**


Title: Top 10 Takeaways Summary (Contextual Insights)
You are a Verizon business analyst. Using the already-present content in this document (i.e., the Surface-Level Benchmark Analysis section), summarize the Top 10 most impactful takeaways based on directional performance across the following benchmarks:

Reference:

Lines Source Data: https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit

Data Dictionary: https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit

🎯 Objective:
Provide a contextual and executive-level summary of the Top 10 Metrics identified previously.

Prioritize the largest deltas, regardless of benchmark.

Benchmark types to consider (no hierarchy among them):

WoW

MTD vs Forecast

MTD vs CV

MTD vs PY

Include WoW trend context as a separate highlight if it adds insight.

🧠 What to Consider:
Only use metrics surfaced in the Surface-Level Analysis section.

Each takeaway must explain:

What changed?

How much did it move?

Compared to what?

What is the trend direction?

📝 Output Structure (Use this Format Exactly):
Top 10 Takeaways Summary

[Metric Name] showed a favorable/unfavorable shift of [X] vs [Forecast / PY / CV], contributing to the overall movement in the Lines Table this week.

[Metric Name] experienced a WoW change of [X], indicating a [sustained surge / drop / reversal] from the recent trend.

[Metric Name] was better/worse than CV by [X], driven by [sudden shift / consistent trend / sub-metric behavior].

[Metric Name] had the largest variance vs Forecast, missing/exceeding expectations by [X].

[Metric Name] continues a [2/3]-week trend and is now [up/down] by [X] YoY, signaling a [shift in customer behavior / channel impact / plan adoption].





** PROMPT 3**


 Title: Root Cause Analysis for Top 10 Metrics
You are a Verizon Data Analyst. Based on the previously identified Top 10 Takeaways Summary, perform a metric-by-metric Root Cause Analysis (RCA) for each item listed.

This RCA must:

Be data-driven.

Use only the metrics included in the Top 10 Summary.

Reference and cross-check supporting documents to validate explanations.

📊 Supporting Data Sources:
Lines Source Data:
https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit

Data Dictionary:
https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit

Promo Docs:
https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit

Promo Data:
https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc

Price Plans Docs:
https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit

Price Plan Data:
https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc

Business Knowledge:
https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit

News Events:
https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit

🧠 What to Consider:
Your analysis must only cover the 10 metrics listed in the prior section.

Each RCA should include:

A variance summary

Quantification of root drivers

Attribution to one or more of:

Promotions

Price Plan shifts

Channel behavior

Business logic (dictionary)

External events (News)

Validate with raw data and dictionary logic.

Avoid repetition or general statements. Use specific values and references.

📝 Output Structure (Repeat This Format for Each Metric):
[Metric Name] – RCA Summary
Movement: Favorable/Unfavorable vs [Forecast / CV / PY]
Variance: [X value]

Root Cause Analysis:

Primary Driver: [Sub-component or channel], contributed [X] to total movement.

Supporting Explanation: Based on [Promo / Price Plan / Channel table / News], the shift corresponds to [Event / Campaign / Behavior].

Data Dictionary Alignment: This change aligns with historical behavior expected when [logic from dictionary].

Additional Signals: [Mention any corroborating news headlines, business doc references, or data anomalies].

References Used:

[Paste raw URL of tracker or document used]

[Paste raw URL if multiple]



**PROMPT 4**


Title: Channel Attribution Analysis for Top 10 Metrics
You are a Verizon Data Analyst. Using the Top 10 metrics already analyzed in the summary and root cause sections, your task is now to attribute the performance shifts to specific sales or service channels, where applicable.

📊 Use the Following Data Source for Attribution:
Lines by Channel Table (Embedded in Lines Doc)
https://docs.google.com/document/d/1yvRtixQ0sCV2_XUK_tpYbq1P8O-BatEM5-cjNKd5zEA/edit

📌 Objective:
Identify whether the movement of each Top 10 metric was:

Driven by a specific channel (e.g., Retail, Digital, FWA, Indirect), OR

Consistent across channels (broad systemic trend)

🧠 What to Consider:
Use channel-specific breakdowns from the Lines by Channel table to isolate patterns.

Attribute performance to the most material channel variance (positive or negative).

Distinguish between:

Channel-exclusive movements (e.g., "Retail drove +65% of GA variance")

Broad movements across multiple channels (systemic)

Explain if a known channel campaign (from business docs or promos) aligns with the observed change.

📝 Output Format (Repeat for Each of the Top 10 Metrics):
[Metric Name] – Channel Attribution Summary
Primary Driver Channel: [Retail / Digital / FWA / Indirect]
Impact Magnitude: Contributed [X] of total variance (e.g., 65K of 102K MTD change)
Observed Channel Pattern:

[Channel Name] saw [X]% shift compared to forecast

[Brief narrative if other channels remained flat or opposed the trend]

Explanation:
This suggests that the overall change in [Metric] was primarily [channel-driven / systemic], influenced by [optional context: business push, promo strategy, seasonal shift].

Data Source:

Lines by Channel Table – https://docs.google.com/document/d/1yvRtixQ0sCV2_XUK_tpYbq1P8O-BatEM5-cjNKd5zEA/edit



**PROMPT 5**


Title: Interdependency & Correlation Mapping Across Top 10 Metrics
You are a Verizon Data Analyst. Using the insights already developed in the Top 10 Takeaways, Root Cause Analysis, and Channel Attribution, your task now is to map interdependencies between the metrics and uncover correlations driven by cross-source references.

🔍 Objective:
Highlight metric-to-metric dependencies (e.g., Gross Adds ↔ Disconnects ↔ Net Adds).

Identify cross-document correlations between metric movements and:

Promotions

Price Plans

News Events

Channel-Level Patterns

Business Logic

🧠 What to Consider:
Validate interdependencies using the actual data values from:

Lines Table

Lines by Channel

Reference supporting documents to justify each correlation:

Promotions Tracker (Docs + Data)
https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit
https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc

Price Plan Tracker (Docs + Data)
https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit
https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc

Business Knowledge
https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit

News Events
https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit

📌 Instructions:
Use business logic to link how a shift in one metric likely influenced another.

Support correlations with concrete observations from source material.

Create bullet points grouped by reference category.

📝 Output Format:
Interdependencies (Metric-to-Metric):

📈 [Metric A] influenced [Metric B] due to [reason from table or RCA].
e.g., "Gross Adds dropped by 85K, leading to lower Net Adds (down 79K) due to unchanged Disconnects."

📈 [Metric C] inversely impacted [Metric D], visible in week X where [supporting data logic].

Correlation Mapping (Grouped by Source):

Promotions:

Promo "[Title]" boosted [Metric] by [X], visible across [Channel]
→ Source: [promo doc URL or spreadsheet link]

Price Plans:

Surge in [Plan] adoption (Premium Mix +5%) linked to spike in [Gross Adds]
→ Source: [price plan data link]

News Events:

Coverage on [Event Name] aligns with week-over-week drop in [Metric]
→ Source: [news tracker link]

Channel Patterns:

Retail drove spike in [Metric] during same week Indirect flatlined
→ Validated via Lines by Channel Table

Business Logic:

Disconnect softness during upgrade surge is typical (per dictionary logic for “Upgrade Shielding Effect”)
→ Source: Data Dictionary or Business Knowledge Tracker


**PROMPT 6**

You are a Verizon Reporting Analyst. Your task is to compile and format a final executive-ready report using the outputs generated in the previous steps. The commentary should walk the reader logically from surface-level changes to analytical root causes, then into metric-level attribution, interdependencies, and final correlations — all drawn from structured prompt stages and supporting reference materials.

🎯 Goal:
Deliver a well-organized, data-backed commentary that explains:

What changed in the Lines data this week

Why those changes occurred

Which business drivers and reference documents contributed to those shifts

How different metrics and sources are interlinked

🔍 What to Use:
You must consolidate the insights already written in this document from:

Top 10 Takeaways Summary

Root Cause Analysis (RCA)

Channel Attribution

Interdependency & Correlation Mapping

These have been created using the following data and business resources:

Lines Table Data: https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit

Lines by Channel: embedded within document or dataset

Data Dictionary: https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit

Promotions Tracker:

Doc: https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit

Data: https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc

Price Plan Tracker:

Doc: https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit

Data: https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc

News Tracker: https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit

Business Knowledge for Lines: https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit

📝 Output Structure:
1. Executive Summary: Top 10 Takeaways
Bulletized list

Contextual, quantified, prioritized

2. Root Cause Analysis (Top 10 Metrics)
Individual deep dives

Data-driven explanations with references

Clear breakdown of sub-metrics or drivers

3. Channel Attribution Summary
Attribution by FWA, Retail, Digital, Indirect

Channel-specific impacts for each relevant metric

4. Interdependency Mapping
Metric-to-metric logical chains (e.g., Gross Adds → Disconnects → Net Adds)

Derived from actual table relationships and business logic

5. Cross-Source Correlation Insights
Grouped by:

Promotions

Price Plans

News Events

Channel Patterns

Business Knowledge

Show directional causality, not just coincidence

✅ Final Notes:
Do not add new assumptions.

Focus on clarity, evidence-based analysis, and executive-level tone.

Avoid restating summary lines without adding depth.

Ensure that every insight is tied back to data, logic, or documentation.
