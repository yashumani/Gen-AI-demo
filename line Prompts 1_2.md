**Enhanced Prompt for Lines Table Commentary Generation:**

You are tasked with generating a comprehensive, contextual, and insight-driven commentary for the **Lines** data table. This task should follow a structured analytical journey — beginning with the summary-level data provided in the Lines table and progressively uncovering the **root causes** of key metric changes by referencing relevant business documentation and historical archives.

Use the following documents as sources:
- Lines Table: https://docs.google.com/document/d/1JE8mJpvbd5vlWc7E8H6TrX4Xab2gtbXPjikfb8uPZY4/edit?tab=t.0
- Source Spreadsheet: https://docs.google.com/spreadsheets/d/1T4j07mZWPVpq_K3dbAP77W3mejfMBlMNSKe_f10gJcA/edit?gid=1313153917#gid=1313153917
- Data Dictionary: https://docs.google.com/document/d/1h9HFsWp1xJm4s8Ibiui2LcJA2RpN3aLhN9wFCD4anmo/edit?tab=t.0
- Promotions Tracker: https://docs.google.com/document/d/1YVZLbA7zxfwyzW5eNIZl9Bc4UfwruOJZB2sCS1aJ670/edit?tab=t.0
- Price Plans Tracker: https://docs.google.com/document/d/1fdtnMTwcKuiUK0nWjCOIpphIwLbKINRN7yMwhD6rNn4/edit?tab=t.0
- Business Knowledge for Lines: https://docs.google.com/spreadsheets/d/1UHvpzD3DDegkqiY4reM6hPgH4mfrLR5Z/edit
- News Headlines Table : https://docs.google.com/spreadsheets/d/1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM/edit?gid=0#gid=0
- Historical Reports Archive: [Insert Link to Folder with Past CIPB Reports]



---

### Analytical Framework:
This prompt applies a **Tree-of-Thoughts** reasoning strategy. For each metric insight:
1. Branch into **possible causes** across business logic, promotions, news events, price plan trends, and benchmark deviations.
2. Explore each branch with supporting context.
3. Consolidate into the most logical insight pathway.
4. Validate against historical report trends and call out any breaks in seasonal expectation or one-time events.

---

### Step-by-Step Flow:

1. **Start with Lines Table Summary Data:**
   - Identify top changes week-over-week (WoW) and month-to-date (MTD).

2. **Prioritize the Top 5 Takeaways**:
   - Only focus on the **top 5 metrics or observations** with the largest impact or deviation.

3. **Deep Dive on Only Top 5 Metrics**:
   - Use business logic, historical trends, and real-time context to analyze only those metrics referenced in the Top 5 section.

4. **Use Relevant Sources to Explain Root Causes:**
   - Business Logic (Data Dictionary)
   - Promotional Influence (Promo Tracker)
   - External Events (News Tracker)
   - Business Strategy (Business Context)
   - Seasonal and historical expectations (Historical Reports)

5. **Refer to Historical Reports Archive for Contextual Alignment:**
   - Review archived reports to align the tone, vocabulary, and depth of analysis with prior outputs.
   - Use historical data to validate trends, identify recurring patterns, and highlight deviations from past expectations.
   - Incorporate any relevant insights or methodologies from archived reports to enhance the depth of the analysis.

6. **Establish Interdependencies & Correlations:**
   - Link how one metric shift influenced another (e.g., upgrades suppressing disconnects, or gross adds driving net adds).
   - Validate logic through cross-source triangulation.

---

### Commentary Requirements:

**Length:**
- Be as detailed as possible with no word count restrictions.
- Ensure all sections are fully developed with supporting evidence.

**Tone:**
- Professional, analytical, and executive-focused.
- Align with the tone used in historical reports from the archive.

**Vocabulary:**
- Use clear terms like "favorable/unfavorable," "better/worse," "gained/missed."
- Clarify if the comparison is to Forecast, Prior Year, or Commit View (CV).
- Ensure consistency with vocabulary used in archived reports.

---

### Output Structure:

**1. Top 5 Takeaways:**
- Clearly bulletized.
- Highlight the most critical WoW and MTD observations.
- Only select observations with meaningful business movement.

**2. Metric-Specific Analysis (Only for Metrics from Top 5):**
- Provide focused analysis **only** for the metrics appearing in the Top 5.
- For each metric:
  - Highlight the major drivers (positive or negative).
  - Quantify the variance (e.g., missed forecast by 9.5K).
  - Use external documentation and historical archives to explain underlying reasons.

**3. Interdependency Section:**
- Explain cause-effect relationships between the selected top 5 metrics.
- Use cross-references to business logic, past patterns, and archived reports for support.

**4. Correlation Section:**
- Present 5 logical connections across the top 5 metrics, drawing from:
  - Promotions
  - Price Plans
  - News Events
  - Historical Comparisons
- Group bullet points by document source.

---

**Exclude:**
- Do not include a Business Implications section.
- Do not analyze any metrics that were not in the Top 5 Takeaways.

**Additional Note:**
- Use the **Historical Reports Archive** as a benchmark for the expected tone, vocabulary, and depth of analysis. Ensure that the commentary aligns with the standards set in prior reports while incorporating new insights and data.
