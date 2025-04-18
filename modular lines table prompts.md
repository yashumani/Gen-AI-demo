**PROMPT 1**

You are a Verizon Business Analyst.
Analyze the Lines Table provided below to extract the Top 5 metrics that exhibited the most significant movement, based on all available benchmark comparisons and week-over-week trends.

📄 Lines Table Document:
https://docs.google.com/document/d/1yvRtixQ0sCV2_XUK_tpYbq1P8O-BatEM5-cjNKd5zEA/edit?tab=t.0

🔽 What to Analyze:

Current Week vs Forecast

Current Week vs Prior Year

Current Week vs Commit View (CV)

Month-to-Date (MTD) vs Forecast

MTD vs CV

MTD vs Prior Year

Weekly Trend (movement from previous weeks)

🔽 What to Consider:

Focus on the absolute size of the variance across all benchmarks.

Prioritize metrics that appear to have consistent trend movement or sudden spikes/reversals.

Avoid redundancy — if multiple rows represent the same driver (e.g., disaggregated price plans), summarize them under the most representative metric.

Disconnect metrics are inherently negative. Fewer disconnects is favorable; more is unfavorable.

🔽 Output Format (Bullet Style):

📌 [Metric Name] — Missed Forecast by 87K and CV by 75K; WoW reversal observed from last 3-week decline.

📌 [Metric Name] — MTD variance against PY is +45K; double-digit mix growth in recent trend.

📌 [Metric Name] — Strong surge this week, exceeding all benchmarks; needs deeper attribution next.

⚠️ Do not include:

Root cause

Channel impact

Business implications



**PROMPT 2**


Prompt 2 – Top 5 Takeaways Summary (Contextual Continuation)
You are a Verizon business analyst.
Use the existing content already written in this document, which includes Lines Table trends and surface-level benchmarking summaries.
Your task now is to:

Extract and summarize the Top 5 most impactful takeaways based on:

WoW changes

MTD vs Forecast

MTD vs Commit View (CV)

MTD vs Prior Year (PY)

Focus on takeaways that exhibit the highest material movement, either favorable or unfavorable.
You may consider Weekly trends separately if impactful.

Ensure the takeaways are written in a professional, executive-ready tone with clear quantification and context.

Output Structure (Use this exact format):
Top 5 Takeaways Summary

[Metric Name] showed a favorable/unfavorable shift of [X] when compared to [Forecast / PY / CV], contributing to the overall movement in the Lines Table this week.

[Metric Name] experienced a WoW change of [X], indicating an acceleration / deceleration / reversal from previous trends.

[Metric Name] was better/worse than CV by [X], driven by consistent gains / unexpected drop observed across multiple channels.

[Metric Name] had the largest variance vs Forecast among all metrics, missing/exceeding expectations by [X].

[Metric Name] continues a [2/3]-week trend and is now [up/down] by [X] YoY, signaling a shift in customer behavior / channel performance / pricing response.
