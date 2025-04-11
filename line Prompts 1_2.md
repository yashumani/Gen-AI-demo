

You are tasked with generating a comprehensive, contextual, and insight-driven commentary for the **Lines** data table. This task should follow a structured analytical journey — beginning with the summary-level data provided in the Lines table, and progressively uncovering root causes of changes by referencing supporting business documentation.

Use the following documents as sources:
- Lines Table: https://docs.google.com/document/d/1JE8mJpvbd5vlWc7E8H6TrX4Xab2gtbXPjikfb8uPZY4/edit?tab=t.0
- Source Spreadsheet: https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit?gid=1313153917#gid=1313153917
- Data Dictionary: https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit?tab=t.0
- Promotions Tracker: https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit?tab=t.0
- Price Plans Tracker: https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit?tab=t.0
- Business Knowledge for Lines: https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit
- News Headlines Table : https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit?gid=0#gid=0



---

### Root-Cause Analysis Flow:
Begin by examining the **summary data in the Lines Table**, identifying the most significant weekly and month-to-date (MTD) changes.

Then, for each major movement or variance:
1. Identify the metric(s) responsible.
2. Investigate relevant root causes using:
   - **Business Logic** from the Data Dictionary
   - **Price Plan and Product-Level shifts**
   - **Promotions that could have influenced customer behavior**
   - **External Events or News Items** that provide market context
3. Establish **interdependencies and correlations** between metrics, benchmarks (Forecast, Prior Year, CV), and business drivers.

---

### Metrics for Detailed Analysis (Restrict all further analysis only to those metrics that appear in the Top 5 Takeaways):

- **Phone Gross Adds**
  - Breakdown by Price Plans (*only those with largest positive/negative impact*):
    - Unlimited Welcome
    - Unlimited Plus
    - Unlimited Ultimate
    - Other Premium
    - Other Unlimited/Metered
  - Premium Unlimited Mix %
  - Components:
    - New Phone Lines
    - Add a Line Phone

- **Phone Upgrades**

- **Phone Disconnects** *(Clarify that disconnects are inherently negative; comparisons must use "favorable/unfavorable" or "better/worse")*
  - Voluntary Disconnects
  - Involuntary Disconnects

- **Phone Net Adds** *(Calculated as: Phone Gross Adds minus Phone Disconnects)*

---

### Commentary Requirements:

**Length:**
- Provide a complete and thorough commentary with no word limit.
- Ensure that every section is fully developed with supporting evidence.

**Tone:**
- Professional, analytical, and insight-oriented.
- Language should resemble the style of a senior analyst writing for an executive audience.

**Vocabulary:**
- Use precise comparative language: "favorable/unfavorable", "better/worse", "gained/missed".
- Avoid ambiguous terms like "increase/decrease".
- Always clarify which benchmark is being referenced (Forecast, Prior Year, CV).

---

### Output Structure:

**1. Top 5 Takeaways:**
- Clearly bulletized and prioritized.
- Highlight the most critical changes in the week and MTD.

**2. Metric-Specific Insights:**
- Provide commentary only for metrics referenced in the Top 5 Takeaways.
- Bulletized insights per applicable metric.
- Highlight only largest drivers or movers (positive/negative).
- Use explicit math to describe impact (e.g., "missed forecast by 9.5K, driven by 6.3K shortfall in Unlimited Plus").
- Support insights with the appropriate benchmark reference.

**3. Interdependency Section:**
- Identify and explain causal relationships between the Top 5 metrics.
- Example: "Gross Adds softness led to Net Adds decline, amplified by steady Disconnect volume."
- Draw reasoning from Data Dictionary and Business Knowledge documents.

**4. Correlation Section:**
- Present 5 logical connections across metrics in the Top 5 Takeaways, supported by:
  - Promotions (e.g., impact of $200 trade-in on Upgrades)
  - Price Plans (e.g., shift from Premium to Entry-level)
  - News Events (e.g., traffic surge due to competitor outage)
- Each sub-source should have its own bulletized summary.

---

**Exclude:**
- Do not include a Business Implications section in this output.

