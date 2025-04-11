**Prompt for Lines Table Commentary Generation:**

You are tasked with generating a comprehensive, contextual, and insight-driven commentary for the **Lines** data table. This task should follow a structured analytical journey — beginning with the summary-level data provided in the Lines table, and progressively uncovering root causes of changes by referencing supporting business documentation.

Use the following documents as sources:
- Lines Table: [Insert Google Doc Link - Lines Table]
- Source Spreadsheet: [Insert Google Sheets Link - Raw Data]
- Data Dictionary: [Insert Google Doc Link - Data Dictionary]
- Promotions Tracker: [Insert Google Doc Link - Promotions]
- Business Knowledge for Lines: [Insert Google Sheets Link - Business Context]
- News Event Tracker: [Insert Google Sheets Link - News Impacts]

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

### Metrics for Detailed Analysis (Analyze top to bottom, prioritizing highly impactful drivers):

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
- Bulletized commentary per metric.
- Highlight only largest drivers or movers (positive/negative).
- Use explicit math to describe impact (e.g., "missed forecast by 9.5K, driven by 6.3K shortfall in Unlimited Plus").
- Support insights with the appropriate benchmark reference.

**3. Interdependency Section:**
- Identify and explain causal relationships between metrics.
- Example: "Gross Adds softness led to Net Adds decline, amplified by steady Disconnect volume."
- Draw reasoning from Data Dictionary and Business Knowledge documents.

**4. Correlation Section:**
- Present 5 logical connections across metrics, supported by:
  - Promotions (e.g., impact of $200 trade-in on Upgrades)
  - Price Plans (e.g., shift from Premium to Entry-level)
  - News Events (e.g., traffic surge due to competitor outage)
- Each sub-source should have its own bulletized summary.

---

**Exclude:**
- Do not include a Business Implications section in this output.

