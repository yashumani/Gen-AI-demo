**PROMPT 1**

You are a Verizon Data Analyst.
Analyze the Lines Table provided below to extract the Top 10 metrics that exhibited the most significant movement, based on all available benchmark comparisons and week-over-week trends.
Lines Source Data: https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit
What to Analyze:
Current Week vs Forecast
Current Week vs Prior Year
Current Week vs Commit View (CV)
Month-to-Date (MTD) vs Forecast
MTD vs CV
MTD vs Prior Year
Weekly Trend (movement from previous weeks)
What to Consider:
Focus on the absolute size of the variance across all benchmarks.
Prioritize metrics that appear to have consistent trend movement or sudden spikes/reversals.
Avoid redundancy — if multiple rows represent the same driver (e.g., disaggregated price plans), summarize them under the most representative metric.
Disconnect metrics are inherently negative. Fewer disconnects is favorable; more is unfavorable.
Rank the Takeaways from Most to least impacting.
Output Format (Bullet Style):

For Example:-
[Metric Name] — Missed Forecast by 87K and CV by 75K; WoW reversal observed from last 3-week decline.
[Metric Name] — MTD variance against PY is +45K; double-digit mix growth in recent trend.
[Metric Name] — Strong surge this week, exceeding all benchmarks; needs deeper attribution next.
Do not include:
Root cause
Channel impact
Business implications





**PROMPT 2**


Top 10 Takeaways Summary (Contextual Continuation) You are a Verizon business analyst. Use the existing content already written in this document, which includes Lines Table trends and surface-level benchmarking summaries. 
Source Data: https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit
Data Dictionary: https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit
Your task now is to:
Extract and summarize the Top 10 most impactful takeaways based on:
WoW changes
MTD vs Forecast
MTD vs Commit View (CV)
MTD vs Prior Year (PY)
Focus on takeaways that exhibit the highest material movement, either favorable or unfavorable. You may consider Weekly trends separately if impactful.
Ensure the takeaways are written in a professional, executive-ready tone with clear quantification and context.
Output Structure (Use this exact format): Top 10 Takeaways Summary
[Metric Name] showed a favorable/unfavorable shift of [X] when compared to [Forecast / PY / CV], contributing to the overall movement in the Lines Table this week.
[Metric Name] experienced a WoW change of [X], indicating an acceleration / deceleration / reversal from previous trends.
[Metric Name] was better/worse than CV by [X], driven by consistent gains / unexpected drop observed across multiple channels.
[Metric Name] had the largest variance vs Forecast among all metrics, missing/exceeding expectations by [X].
[Metric Name] continues a [2/3]-week trend and is now [up/down] by [X] YoY, signaling a shift in customer behavior / channel performance / pricing response.





** PROMPT 3**


Root Cause Analysis – Metric Deep Dives
You are a Verizon data analyst.
Use the Top 10 Takeaways already documented in this file as the foundation for this next phase.
Your task is to perform a Root Cause Analysis (RCA) for each metric listed, based specifically on:

The Lines Table data

Weekly and MTD performance benchmarks

Supporting reference documentation

The goal is to analytically explain why each change occurred — identifying the main drivers, quantifying the variance, and linking the insight to business context where applicable.

Use the following reference documents to support your RCA:

Lines Table Source Data:
https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit

Data Dictionary:
https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit

Promotions:
https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit  
https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc

Price Plans:
https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit  
https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc

Business Knowledge:
https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit

News Tracker:
https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit
✍️ RCA Output Format for Each Metric:
[Metric Name]

Movement Summary: [Favorable/unfavorable] vs [Forecast / Prior Year / CV].
Total variance: [X].

Analytical Root Cause:

Main driver: [Sub-metric or channel], contributing [X].

Supporting source: [Promo / Price Plan / Business Knowledge / News].

Reference logic: As defined in Data Dictionary – [short summary].

Relevant References Used:

[Paste applicable links]



**PROMPT 4**


Title: Channel Attribution Analysis (Based on Top 10 Takeaways)

You are a Verizon data analyst. This document already includes the Lines Table data, summary-level analysis, and the Top 10 Takeaways. Your task now is to analyze those Top 10 metrics and determine which sales channels were responsible for the performance changes.

Use the following references for attribution insights:

Lines Table & Channel-Level Tables:
https://docs.google.com/document/d/1yvRtixQ0sCV2_XUK_tpYbq1P8O-BatEM5-cjNKd5zEA/edit?tab=t.0

Source Data Sheet (Channel Views Tab):
https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit

Business Knowledge – Channel Strategy Notes:
https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit

What to do:

For each metric in the Top 10 Takeaways:

Attribute the movement to the appropriate channel(s): Retail, Indirect, Digital, FWA.

Identify which channel(s) performed above or below forecast or trend.

Clarify whether the performance was consistent across all channels or driven by a few.

Pull in any relevant data from the business knowledge tracker for deeper context.

What to consider:

Compare Week-over-Week and MTD changes by channel.

Include variance math if available (e.g., "Retail channel exceeded forecast by 18.4K").

Highlight trends that differ between channels (e.g., “FWA declined, while Retail improved”).

Output Format (Repeat for each relevant Top 10 metric):

[Metric Name] — Channel Attribution Summary

• Primary channel contributor: [Retail / Indirect / Digital / FWA]
• Movement vs Forecast: [Favorable/Unfavorable] by [X]
• Channel disparities: [Example — Digital underperformed, while Retail drove gains]
• Supporting channel-level insight: [Quote trend or delta]
• Interpretation: [Summarize why the movement occurred, e.g., promo traction, digital lag]

Do not restate Top 10 summaries. Instead, enhance the analysis with channel-level context using the references above.



**PROMPT 5**


Title: Interdependency & Correlation Mapping

Use the existing content already present in this document, which includes:

The Top 10 Takeaways Summary

Detailed Root Cause Analyses (RCA) for each of the top metrics

Now, perform a cross-metric and cross-reference correlation analysis using the context from the Lines Table and the following support documents:

Lines Source Data: https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit

Data Dictionary: https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit

Promotions Tracker: https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit

Price Plans Data: https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc

Business Knowledge: https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit

News Headlines Table: https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit

Channel-Level Tables (included in source data document)

Instructions:

Review the Top 10 metrics that were analyzed in the RCA section.

Identify how those metrics influenced or were influenced by each other.

Use supporting documents to find correlation signals, triggers, or event-based anomalies.

Apply business logic to validate each relationship.

Focus on highlighting cause-effect insights backed by evidence.

What to Include:

Interdependencies between metrics (e.g., Gross Adds drove Net Adds; Upgrades may have suppressed Disconnects).

Correlation logic across the following reference categories:

Promotions

Price Plans

News Events

Business Knowledge

Channel Performance

Output Format:

Interdependency Mapping

[Metric A] is strongly linked to [Metric B] due to [reason], which aligns with patterns explained in [data dictionary or business logic reference].

[Metric X] and [Metric Y] showed simultaneous variance due to [channel impact or promo effect], confirming directional influence.

Cross-Source Correlation Summary

Promotions

[Metric] was impacted by [Promo Name], launched in [week], which aligned with performance spikes in [channel or metric].

Price Plans

[Metric] shift was associated with [Price Plan] movement, supported by share of mix increase in [Lines Table].

News

[Metric] trend may relate to the [Event/Headline] reported on [Date], suggesting reactive customer behavior.

Business Knowledge

[Metric] performance followed an expected seasonal pattern as documented in [Business Knowledge tab].

Channel Tables

[Metric] gain/loss was mostly driven by [Channel Name], with [X]% of the movement isolated to that channel in the source data.

Be specific, use actual variance figures where applicable, and group by document type. Only include the most defensible and material relationships.
