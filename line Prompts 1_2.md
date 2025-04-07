**Prompt for Lines Table Commentary Generation:**

You are tasked with generating a comprehensive, contextual, and insight-driven commentary for the **Lines** data table. Use the table data provided in this Google Doc: [Insert Google Doc Link - Lines Table], and reference the associated business logic definitions in this Data Dictionary: [Insert Google Doc Link - Data Dictionary].

Additionally, consider any relevant promotions listed in: [Insert Google Doc Link - Promotions], and apply business understanding from this reference: [Insert Google Doc Link - Business Knowledge for Lines].

---

### Metrics for Detailed Analysis (Analyze from top to bottom, prioritize highly impactful insights):

- **Phone Gross Adds**
  - Breakdown by Price Plans (report only on largest variances):
    - Unlimited Welcome
    - Unlimited Plus
    - Unlimited Ultimate
    - Other Premium
    - Other Unlimited/Metered
  - Premium Unlimited Mix%
  - Components:
    - New Phone Lines
    - Add a Line Phone

- **Phone Upgrades**

- **Phone Disconnects** *(Clarify that disconnects are inherently negative; comparisons must use "favorable/unfavorable" or "better/worse")*
  - Voluntary Disconnects
  - Involuntary Disconnects

- **Phone Net Adds** *(Explicitly calculated as Phone Gross Adds minus Phone Disconnects)*

---

### Commentary Requirements:

**Length:**
- Be as detailed as possible with no word count restriction.

**Tone:**
- Professional, analytical, and insightful.
- Use clear language to define variances and their implications.

**Vocabulary:**
- Use terms like "favorable/unfavorable," "better/worse," and "gained/missed" instead of "increase/decrease."
- Always specify if the insight is vs forecast, prior year, or commit view (CV).

**Content Expectations:**

- **Top 5 Takeaways:**
  - Bulletized top 5 insights identifying the most impactful weekly and MTD observations from the Lines table.

- **Metric-Specific Insights:**
  - Bulletized insights under each metric.
  - Report only the largest positive or negative drivers under each price plan or subcomponent to reduce redundancy.
  - Clearly show interdependencies between metrics (e.g., how Gross Adds influenced Disconnects, or how Upgrades may suppress Disconnects).
  - Include explicit calculations (e.g., "Phone disconnects missed their forecast by (96.5K), primarily due to the (85.1K) miss in voluntary disconnects.")
  - Include context for YoY comparisons (e.g., one-time events like the ATT outage from 2/20/24).
  - Add a distinct **Interdependency Section** summarizing logical connections between metrics.

Exclude commentary on business implications from this analysis.

