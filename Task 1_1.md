Based on a detailed analysis of the uploaded document, "Consumer Insights & Perspectives Brief," and aligning it with the **expected output** you previously shared, here are the detailed requirements you should consider for Task 1.1 (Target Commentary Style and Criteria):

---

## Task 1.1 Target Commentary Style and Criteria:
Based on your detailed feedback, here's a structured synthesis of areas to address and corresponding improvements to make within your Zero-Shot prompt for better alignment with business expectations and analytical clarity:

---

## 📝 **Revised Prompt Requirements & Recommendations:**

### **General Instructions:**
- Clearly specify comparisons:
  - Primary comparison: **Forecast** (`vs Fct`)
  - Secondary comparisons: **Prior Year (PY)**, **Prior Week (PW)**, and/or **Commit View (CV)** clearly labeled.
- Connect performance across metrics explicitly (e.g., **Accounts ↔ Lines ↔ Disconnects**), illustrating clear causal relationships or correlations between related metrics.
- Emphasize consistency, clarity, and specificity:
  - Use terms like **favorable/unfavorable**, **better/worse**, rather than generic terms like increased/decreased.
  - Explicitly clarify if statements are referring to absolute metric changes or variances from forecasts.
  - Structure commentary to explicitly state cause-effect relationships.

---

### 📊 **Lines & Accounts Sections:**

#### **Length & Detail:**
- Commentary: **150-250 words** per section (Accounts and Lines separately).
- Clearly structured into brief paragraphs with logical flow (Metric → Insight → Implication).

#### **Content Expectations:**
- **Explicit linkage** between metrics, clearly stating causal implications.  
  **Example:** "The unfavorable variance in **new accounts** has directly impacted **gross adds**, as fewer account activations naturally constrain overall phone adds growth."
- Clearly state what comparison is used (Forecast, PY, or Week-over-week)  
  **Example:** "Phone disconnects were **unfavorably higher than forecast**, negating the positive performance in **phone gross adds**, leading to unfavorable net adds."
- Consideration for historical anomalies (e.g., ATT outage YoY), if prompted or data provided.
  - Instruct the model to reference prior briefs or known historical anomalies if relevant data is provided for historical context.

---

### 🏠 **Verizon Home Internet (VHI) Section:**

#### **Length & Detail:**
- Commentary: Approximately **100-150 words** for top takeaways.
- Break down clearly by **Fios and FWA segments separately**.

#### **Content Expectations:**
- Directly align commentary with the 5 core metrics (**Sales, Cancels, Gross Adds, Disconnects, Net Adds**).
- Clearly indicate benchmarks (**Forecast, PY, Commit View**):
  - Example: "Fios **sales** were **favorable against forecast**, primarily driven by strong store channel performance; however, Fios **disconnects** worsened compared to PY."
- Exclude generic insights, and emphasize direct, actionable callouts:
  - Example: "FWA's **net adds** were unfavorable primarily due to higher-than-expected disconnects, particularly driven by recent pricing actions by competitors."

---

### 💰 **Value Segment Section:**

#### **Length & Detail:**
- Commentary: Approximately **150-250 words**, clearly separated into sections:
  - **Gross Adds**
  - **Disconnects**
  - **Net Adds**

#### **Content Expectations:**
- Clearly label performance as **favorable/unfavorable** rather than increase/decrease.
- Identify top **1-3 brands** driving performance variances within each section clearly.
- Explain net adds as a direct result of gross adds and disconnect trends:
  - **Example:**  
    > "**Gross adds** outperformed forecast by 18K primarily driven by **Visible** and **Straight Talk**. However, **disconnects** were slightly unfavorable by 16K, led by higher involuntary churn in **Tracfone**, resulting in an overall favorable **net adds** variance of 2K."
- Comparative analysis to previous week’s MTD to highlight shifts in momentum clearly:
  - Example: "Compared to last week's performance, **Visible** has significantly improved its gross adds, driving increased MTD favorability."

---

### 🚩 **Business Implications (across all sections):**
- Generate deeper insights beyond generic conclusions:
  - Clearly link short-term performance to longer-term trends or strategic impacts.
  - Highlight intramonth or intra-quarter momentum changes.
- Include clear, actionable recommendations or explicitly identify areas needing attention:
  - **Example:** "Given recent increased involuntary disconnects in **Tracfone**, consider proactive retention promotions to mitigate further churn risk."

---

### 🔗 **Enhanced Prompt Template (Zero-Shot):**

**Example Prompt:**
> “Using the provided numeric data, generate a structured commentary for **Lines, Accounts, VHI, and Value** segments separately. Clearly indicate primary comparisons (**Forecast**), secondary benchmarks (**PY, PW, CV**), and explicitly connect performance across metrics. Commentary should use terms like favorable/unfavorable, better/worse, and explicitly state causal relationships (e.g., how new accounts impact gross adds, how gross adds and disconnects impact net adds).  
> 
> Specifically:
> - **Lines & Accounts**: Clearly illustrate relationships between new accounts, disconnects, and gross adds.  
> - **VHI**: Provide separate takeaways for Fios and FWA segments, focusing explicitly on Sales, Cancels, Gross Adds, Disconnects, and Net Adds metrics.  
> - **Value**: Structure commentary separately by Gross Adds, Disconnects, and Net Adds. Clearly identify top brands influencing variance. Use Core Value Brands as the total benchmark (exclude SafeLink).  
> 
> For all segments, include business implications and actionable insights clearly derived from the numeric variances and trends, highlighting recent shifts in momentum and recommending actionable considerations."

---

## **Additional Recommendations:**
- Enable your AI pipeline or prompt to access historical context or metadata (e.g., previous year's briefs or known anomalies), as suggested by your feedback (e.g., ATT outage impact).
- Clearly define terms and business rules upfront within your prompt, particularly exclusions (e.g., SafeLink) or special considerations.

---

Implementing these structured enhancements within your Zero-Shot prompts will address the critical feedback points and significantly increase the quality, clarity, and strategic usefulness of your generated insights.
