Based on your deep dive prompt and analytical expectations, here's the **enhanced "Report Reading & Business Logic Guide for Lines Table Analysis"** — now expanded to cover **missing logic and reference alignment** required to support Gemini’s prompts for RCA and interdependencies:

---

## 📘 **Report Reading & Business Logic Guide for Lines Table Analysis**

This guide serves as the foundational reference for all Gemini prompt executions. It reduces prompt complexity and centralizes the logic for interpreting Lines Table data, ensuring **consistency**, **accuracy**, and **valid RCA** (root cause analysis).

---

### 🔹 1. **Benchmark Interpretation Logic**

For **each metric** (e.g., Phone Gross Adds, Disconnects, Upgrades, Net Adds):

| Benchmark | Interpretation Logic |
|----------|----------------------|
| **Current Week vs Forecast** | Compares actual performance to target set for the current week. Large unfavorable variances (misses) require immediate analysis. |
| **Current Week vs Prior Year (PY)** | Measures YoY change. Consider seasonal events and one-time incidents (e.g., ATT outage on 2/20/24). |
| **Current Week vs Commit View (CV)** | CV = Executively approved forecast post mid-month. Missing CV indicates performance deterioration. |
| **MTD vs Forecast / PY / CV** | Aggregated version of the above. Stronger indication of sustained trend. |
| **Weekly Trend (WoW)** | Week-over-week shifts. Used to detect inflection points or reversals. |

**Disconnects:** Always treated as **negative metrics**. Fewer disconnects = *favorable*, more disconnects = *unfavorable*. Never say "disconnects increased" — use "worsened" or "missed target".

---

### 🔹 2. **Metric Composition Logic**

To break down aggregate metrics during RCA:

- **Phone Gross Adds = New Phone + Add-a-Line Phone**
- **Phone Disconnects = Voluntary + Involuntary**
- **Phone Net Adds = Gross Adds - Disconnects**

Each of these rollups must be confirmed using **Source Data Spreadsheet** (Google Sheets), and validated against **Data Dictionary** definitions.

---

### 🔹 3. **Reference Matching Protocol (Manual RAG Logic)**

For every metric, search these references to justify RCA:

| Reference Type        | Purpose |
|-----------------------|---------|
| **Data Dictionary**   | Business logic for metric definitions, inter-metric dependencies. |
| **Promotions Tracker + Data** | Attribute gains or losses to campaign timing and eligible audiences. |
| **Price Plans Tracker** | Segment mix shifts (e.g., Unlimited Welcome vs Premium Unlimited). |
| **Business Knowledge Sheet** | Qualitative context like churn reasons, past behaviors. |
| **Channel Tables (Document)** | Disaggregates performance by channel (Retail, Digital, Indirect, etc.). |
| **News Headlines Table** | Look for spikes caused by external events (e.g., competitor outages, weather). |

Use **at least two sources per insight**. Prioritize *triangulated logic* over single-source assumptions.

---

### 🔹 4. **Root Cause Analysis (RCA) Protocol**

For each of the Top 5 metrics from the Lines Table prompt:

1. **Quantify** the deviation (e.g., “Missed forecast by 45.8K”).
2. **Decompose** the metric (e.g., voluntary disconnects drove 85% of total).
3. **Validate with References** (e.g., promo eligibility, price plan shift).
4. **Attribute by Channel**, if clear in the Channel Table.
5. **Link with Business Events**, only if a news trigger or known change occurred.
6. **Explain if Trend is Structural or One-Time**.

Avoid repeating surface commentary from summary prompts.

---

### 🔹 5. **Interdependency & Correlation Matrix**

Always validate links between metrics using both **business logic and data trail**.

| Relationship Type         | Example |
|---------------------------|---------|
| **Metric ↔ Metric**       | Upgrades reduce disconnects → impacts Net Adds |
| **Promo ↔ Metric**        | Trade-in campaign boosts Gross Adds |
| **Channel ↔ Metric**      | Retail driving 70% of favorable Disconnects trend |
| **Price Plan ↔ Metric**   | Migration to Unlimited Plus lowers churn |
| **News ↔ Metric**         | ATT outage causing spike in Gross Adds YoY |

Each correlation should have a **line of evidence**, either data-based or event-based.

---

### 🔹 6. **Standard Output Vocabulary**

| Instead of… | Use this… |
|-------------|-----------|
| “Increase/Decrease” | “Favorable/Unfavorable” |
| “Up/Down” | “Better/Worse than [Benchmark]” |
| “Higher/Lower” | “Exceeded/Missed [Forecast/PY/CV]” |
| “Performance Change” | “Variance of X vs [Benchmark]” |

---

### 🔹 7. **Final Commentary Format Template**

Use this structure for each metric deep dive:

**[Metric Name] Movement Summary:**  
- Favorable/Unfavorable vs Forecast/PY/CV  
- Variance: [X]

**Root Cause Analysis:**  
- Driver: [e.g., Voluntary Disconnects]  
- Supporting Data: [X] from Lines Table  
- Confirmed by: [Promo X, Price Plan Y, Business Doc Z]

**Attribution & Correlation:**  
- Channel Influence: [Retail/Digital etc.]  
- Correlation with [Related Metric]  
- News or Promo Tie-in: [If applicable]

---

