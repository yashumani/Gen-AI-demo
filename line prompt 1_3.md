**Prompt for Lines Table Commentary Generation (5000 characters version):**

Act as a Verizon Data Analyst. Generate a contextual, executive-ready commentary for the **Lines** data table by analyzing weekly and MTD trends, followed by a root cause investigation using embedded business references. 

The input document now includes: 
- Lines Table & Lines by Channel (https://docs.google.com/document/d/1yvRtixQ0sCV2_XUK_tpYbq1P8O-BatEM5-cjNKd5zEA/edit?tab=t.0)
- Source Data: https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit
- Data Dictionary: https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit
- Promo Docs: https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit
- Promo Data: https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc
- Price Plans Docs: https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit
- Price Plan Data: https://docs.google.com/spreadsheets/d/1uMUwBS7SyQiWMbpasQXDix5-sBFBXxNL2ar-4OZRQIc
- Business Knowledge: https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit
- News Events: https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit

---

### Reasoning Strategy
Use **Chain-of-Thought** and **Tree-of-Thought** approaches:
1. Identify major changes.
2. Branch into potential causes across data sources.
3. Trace logic to supporting evidence.
4. Consolidate a validated root cause narrative.

---

### Step-by-Step Flow

**1. Surface-Level Analysis**
- Identify biggest WoW and MTD movements using Lines Table.

**2. Prioritize Top 5 Takeaways**
- Select highest-impact observations. Avoid redundancy. 

**3. Deep Dive on Top 5 Metrics Only**
Use the following references:
- Data Dictionary
- Promotions (Docs/Sheets)
- Price Plan Docs
- Channel-Level Tables
- News Tracker
- Business Knowledge Sheets

Include:
- Key metric driver breakdown (e.g., "Phone disconnects missed forecast by 96.5K, due to 85.1K miss in voluntary")
- Mention if compared vs Forecast, Prior Year, or Commit View (CV)
- Avoid full price plan breakdowns unless significant

**4. Channel Attribution Logic**
- Attribute performance by channel (FWA, Retail, Digital, Indirect)
- Explain if issue/opportunity is channel-driven or systemic

**5. Interdependency & Correlation**
- Explain how one metric influenced another (e.g., Gross Adds ↔ Disconnects ↔ Net Adds)
- Identify 5 logical cross-source correlations (e.g., promotions driving Phone Net Adds)

---

### Output Structure

**Top 5 Takeaways**
- Bulletized, impactful, WoW and MTD combined

**Metric Deep Dive (Top 5 only)**
- Root cause analysis for each
- Include supporting math
- Use minimum 2 data sources for justification

**Interdependency Section**
- Describe metric-to-metric relationships
- Pull logic from dictionary and channel tables

**Correlation Section**
- 5 bullets per category:
  - Promotions
  - Price Plans
  - News
  - Business Knowledge
  - Channel Tables

Group findings by source.

---

**Exclude:**
- No Business Implications
- No metrics outside the Top 5

**Goal:**
Walk the reader through what changed and why — using sequential, evidence-based analysis across business dimensions.

