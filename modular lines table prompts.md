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


You are a Verizon data analyst. Use the existing content about Line Data Table already in this document (which includes summary-level analysis and Top 10 takeaways). For each metric identified in the Top 10, perform a detailed root cause analysis to explain what contributed to the movement.

In addition to what’s already written, reference the following supporting materials to explain the drivers of change:

Lines Source Data: https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit
Data Dictionary: https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit
Promo Docs: https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit
Promo Data: https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc
Price Plans Docs: https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit
Price Plan Data: https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc
Business Knowledge: https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit
News Events: https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit
What to Consider: Use data-backed and contextual reasoning only.
Reference related metrics (e.g., Gross Adds → Disconnects → Net Adds).
Include channel-specific influences when applicable.
Pull in promo, pricing, or event-related causes if relevant.
Focus on largest drivers per metric.
Rank the Takeaways from Most to least impacting.
Be specific (e.g., “Voluntary Disconnects drove 85.1K of the 96.5K forecast miss in total Disconnects”).

✍️ Output Format (Repeat for Each Top 5 Metric): [Metric Name]
Movement Summary: Favorable/unfavorable vs. Forecast / PY / CV. Total variance: [X].
Root Cause Analysis:
Main driver: [Sub-metric or price plan], variance: [X].
This aligns with context from [Promotion/Price Plan/Channel/News/Event].
Business Dictionary confirms such patterns are expected due to [logic].
Additional supporting signals: [News headline/channel table shifts].
Supporting References Used:
[Raw URL to relevant tracker]
[Raw URL to supporting promo/event/business doc]


