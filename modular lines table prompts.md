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


You are a Verizon data analyst.
Use the Top 10 metrics already written above in this document (from the takeaways summary) to perform a root cause analysis.

Do not analyze any metrics not mentioned in the previous section.

Now analyze only those 10 metrics by using the following reference sources to identify causes and contributors to their performance:


Lines Source Data:
https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit

Data Dictionary:
https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit

Promotions Docs:
https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit  
https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc

Price Plans Docs:
https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit  
https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc

Business Knowledge:
https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit

News Tracker:
https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit
📌 Additional Guidance:
Focus on variance explanations (vs Forecast / Prior Year / CV).

Match logic to prior patterns in business knowledge or promotions.

Link each metric’s change back to specific root drivers (price plan, promotion, news, etc.).

Do not restate summary from Prompt 2 — build upon it.

Keep all responses grounded in the Top 10 list above.

✍️ Output Format (Repeat Per Metric):
[Metric Name]

Movement Summary: Favorable/unfavorable vs. Forecast / PY / CV. Total variance: [X].

Root Cause Analysis:

Main driver: [Sub-metric or plan], delta: [X].

Supported by: [Promo / Price Plan / News / Channel trend].

Cross-referenced in Data Dictionary as: [logic].

Reference Documents Used:

[Tracker URL or relevant evidence]

