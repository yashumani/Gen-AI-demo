**Prompt for Lines Table Commentary Generation:**

Act as a Verizon Data Analyst and you are tasked with generating a comprehensive, contextual, and insight-driven commentary for the **Lines** data table. This task follows a structured analytical journey — starting with the summary-level Lines data and uncovering **root causes** using embedded business documentation.

**Note:** The input document now includes the Lines data table and reference materials (e.g., Promotions, Price Plans, Business Knowledge, News Events, Channel Data Tables). This format is designed to support richer interdependencies and correlation logic. In addition, the Lines data is correlated with Phone Lines and Phone Accounts, since a user can have multiple lines under one account.

**Use the following documents as sources:**
- **Lines Table and Lines by Channel tables**: https://docs.google.com/document/d/1yvRtixQ0sCV2_XUK_tpYbq1P8O-BatEM5-cjNKd5zEA/edit?tab=t.0
- **Source Data Spreadsheet**: https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit?gid=1313153917#gid=1313153917
- **Data Dictionary**: https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit?tab=t.0
- **Promotions Tracker**: https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit?tab=t.0
- **Promotions Source Data Spreadsheet**: https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc/edit?gid=181065931#gid=181065931
- **Promotions Data Dictionary**: https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc/edit?gid=1984381918#gid=1984381918
- **Price Plans Tracker**: https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit?tab=t.0
- **Price Plans Source Data**: https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc/edit?gid=0#gid=0
- **Business Knowledge for Lines**: https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit
- **News Headlines Table**: https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit?gid=0#gid=0

---

### Analytical Framework
Apply a **Chain-of-Thoughts and Tree-of-Thoughts** reasoning strategy:
- Use a sequential problem-solving approach to articulate **what changed**, **why it changed**, and **how different variables contributed**.
- Branch into **possible causes** using embedded references (promotions, news, pricing, business knowledge, channel-level drivers).
- Prioritize logical, data-backed pathways and consolidate into the most defensible narrative.

**Additional Note:**
- **Phone Gross Adds** = New Phone + Add a Line Phone
- **Phone Disconnects** = Voluntary Disconnects + Involuntary Disconnects
- **Phone Net Adds** = Phone Gross Adds - Phone Disconnects (Disconnects are inherently negative; always compare using "favorable/unfavorable" or "better/worse")

---

### Step-by-Step Flow

1. **Start with Summary Data:**
   - Identify largest WoW and MTD changes from the Lines Table.

2. **Prioritize Top 5 Takeaways:**
   - Focus only on **Top 5 observations** with the highest material impact (positive or negative).

3. **Metric-Specific Root Cause Analysis (Only for Top 5 Metrics):**
   - Use:
     - Business Logic (Data Dictionary)
     - Promotions (Docs and Spreadsheets)
     - Price Plan Tracker
     - Channel Tables (within the input document)
     - News Events
     - Business Knowledge for Lines
   - Analyze the components that caused the shift, the direction of change, and its magnitude.

4. **Channel-Level Attribution Logic:**
   - From Channel Data Tables, determine:
     - Which channels contributed most/least to each metric change.
     - Whether the trend is channel-specific or system-wide.
     - Attribute the variances logically across FWA, Retail, Digital, Indirect, etc.

5. **Establish Interdependencies & Correlations:**
   - Identify how one metric shift (e.g., Gross Adds) influenced others (e.g., Disconnects, Net Adds).
   - Validate insights using multiple sources when possible.

---

### Commentary Requirements

**Length:**
- No word count restriction. Be thorough and fully substantiated.

**Tone:**
- Executive-level, professional, and insight-rich.

**Vocabulary:**
- Use precise terminology: "favorable/unfavorable," "better/worse," "gained/missed."
- Always specify if comparisons are against Forecast, Prior Year, or Commit View (CV).

---

### Output Structure

**1. Top 5 Takeaways:**
- Bulletized summary.
- Focus on the most critical WoW and MTD metric movements.

**2. Metric-Specific Deep Dive (Only for Top 5):**
- Detailed breakdown for each metric.
- Quantify the variance (e.g., missed forecast by 9.5K).
- Justify using at least two references (e.g., business logic + promotions).

**3. Interdependency Section:**
- Highlight logical cause-effect chains between the Top 5 metrics.
- Use data dictionary and channel tables to strengthen rationale.

**4. Correlation Section:**
- Provide five bullet points for each of the following categories:
  - Promotions
  - Price Plans
  - News Events
  - Business Knowledge
  - Channel Tables
- Group insights by source to demonstrate multidimensional understanding.

---

**Exclude:**
- No Business Implications.
- Avoid analyzing metrics outside the Top 5.

**Reminder:**
Your final output must walk the reader step-by-step from data summary to root cause — using a chain-of-thought flow enhanced by tree-of-thought logic, validating each key finding with at least two layers of reference material.

