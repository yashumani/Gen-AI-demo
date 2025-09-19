**PROMPT 1**

You are a Verizon Data Analyst.

Using the Lines Table below, identify the **Top 10 metrics** with the most significant changes based on:

- Current Week vs Forecast
- Current Week vs Prior Year (PY)
- Current Week vs Commit View (CV)
- Month-to-Date (MTD) vs Forecast
- MTD vs CV
- MTD vs PY
- Weekly trend (WoW movement compared to prior weeks)

📄 Source Data:  
https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit

🔍 What to Focus On:
- Metrics with largest absolute variances across benchmarks
- Consistent or surprising trend shifts
- Only one row per driver (e.g., avoid listing every price plan)
- Disconnects: Favorability = fewer, Unfavorable = more

📝 Output Format (Bullet Style):
[Metric Name] — Missed Forecast by 87K and CV by 75K; WoW reversal observed from 3-week decline.  
[Metric Name] — MTD variance vs PY is +45K; strong premium plan mix lift observed.  
[Metric Name] — Exceeded all benchmarks with sudden spike; warrants deeper attribution.  





**PROMPT 2**


You are a Verizon business analyst.

Use the **Top 10 metrics already listed above** as your fixed reference list.

Do NOT re-analyze or introduce new metrics. Build upon the metrics already identified to summarize key insights with benchmark context.

📄 Reference Data:  
Lines Table: https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit  
Data Dictionary: https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit

📝 Output Structure:
**Top 10 Takeaways Summary**

- [Metric Name] showed a favorable/unfavorable shift of [X] vs [Forecast / PY / CV].
- [Metric Name] experienced a WoW change of [X], reversing 3-week prior trend.
- [Metric Name] exceeded Forecast by [X], with strong gains across Retail and FWA.
- [Metric Name] was below CV by [X] despite week-over-week gains.
- [Metric Name] is now up/down [X] YoY, indicating [trend insight].

Ensure tone is concise, professional, and ready for executive reporting.






** PROMPT 3**


You are a Verizon data analyst.

For each metric already listed in the Top 10 above, perform **root cause analysis** to explain the underlying drivers behind the variance.

Do not restate the summary — instead, build deeper understanding using analytics and business references.

📄 References:
Lines Source Data: https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit  
Data Dictionary: https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit  
Promotions Docs: https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit  
Promotions Data: https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc  
Price Plans Docs: https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit  
Price Plan Data: https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc  
Business Knowledge: https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit  
News Tracker: https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit

📝 Output Format:
**[Metric Name] Movement Summary:**  
- Favorable/unfavorable vs Forecast / PY / CV. Total variance: [X]  
**Root Cause Analysis:**  
- Main driver: [Subcomponent or price plan], variance: [X]  
- Supporting trigger: [Promotion / Channel shift / News Event]  
- Dictionary logic: [Driver explanation]  
- Business context: [Strategic insight]  
**Supporting References:**  
[Raw URL 1]  
[Raw URL 2]  




**PROMPT 4**


You are a Verizon analyst.

Using the same Top 10 metrics previously analyzed, break down each one’s performance **by channel**.

Use the embedded channel-level tables in the Lines Table document to explain which distribution paths (Retail, Digital, FWA, Indirect) are contributing to the movement.

📄 Reference:  
Lines Table (includes Channel Tables): https://docs.google.com/document/d/1yvRtixQ0sCV2_XUK_tpYbq1P8O-BatEM5-cjNKd5zEA/edit

📝 Output Format:
**[Metric Name] Channel Attribution:**  
- Retail: [X variance], trend: [stable/growth/decline]  
- Digital: [X variance], trend: [stable/growth/decline]  
- Indirect: [X variance], possibly impacted by [context]  
- FWA: [X variance], tied to [promotion or mix]  

Only attribute based on observed patterns. Do not speculate.




**PROMPT 5**


You are a Verizon analyst.

Your task is to identify **interdependencies and correlations** between the previously listed Top 10 metrics using available documents.

Do NOT create new metrics or retell prior summaries.

📄 Use:
Data Dictionary: https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit  
Business Knowledge: https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit  
Promotions: https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc  
News Tracker: https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit

📝 Output Structure:

**Metric Interdependencies**  
- [Metric A] influenced [Metric B] due to [behavioral/business relationship]  
- [Metric C] fluctuation typically results in [Metric D] reaction, confirmed by historical logic  
- Net Adds is a direct function of [GA – Disconnects]; this week’s change reflects [X]

**Cross-Source Correlation (5 bullets per category)**  
- **Promotions**:  
  - [Metric] aligned with [Promo], began [date], drove [X impact]  
- **Price Plans**:  
  - Shifts in [plan] directly affected [Metric], due to [mix / pricing change]  
- **News Events**:  
  - [Metric] moved favorably after [event headline]  
- **Channels**:  
  - [Channel] pushed [Metric] above forecast due to [campaign / allocation change]  
- **Business Knowledge**:  
  - [Metric] behavior consistent with [expected seasonal / policy trend]


**PROMPT 6**

Assemble the final executive report using the following sections from this document only:

- Top 10 Takeaways
- Root Cause Analysis
- Channel Attribution
- Interdependencies & Correlations

Do NOT create new summaries or metrics. This is a formatting and organization task.

🎯 Output Structure:
1. Executive Summary  
   - 3-sentence overview of the week’s major movement

2. Top 10 Takeaways (copied directly)  

3. Deep Dive Commentary (copy Prompt 3 output in order)  

4. Channel-Level Breakdown  

5. Interdependency Map  

6. Cross-Source Correlation Bullets  

Ensure professional tone and clean formatting suitable for leadership-level reporting.

