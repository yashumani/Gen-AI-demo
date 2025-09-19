Thanks for the detailed explanation! Based on your summary, here's a **comprehensive list of the new and enhanced requirements** we should incorporate into the upgraded prompt for the **Lines Table** commentary generation:

---

### **Updated Requirements for Lines Table Prompt (Based on Feedback)**

#### **What’s Working Well (To Retain & Expand Upon):**
1. **Accurate Focus on Key Metrics**:
   - Emphasize metrics like *Phone Gross Adds, Disconnects, Net Adds*.
   - Continue tracking *Premium Unlimited Mix%* and *Upgrades* as supporting metrics.

2. **Interdependencies Are Appreciated**:
   - The correlation between metrics (e.g., *Phone Gross Adds → Disconnects → Net Adds*, *Phone Upgrades → Disconnects*) should be retained.
   - Add a dedicated section titled **“Metric Interdependencies”** to structure these insights clearly.

3. **Human Tone & Executive-Ready Style**:
   - Maintain the natural tone resembling analyst commentary.
   - Keep output easily digestible, as if crafted by a business analyst.

---

#### **Areas to Improve (Action Items):**

1. **Condense and Prioritize**:
   - **Avoid redundancies**: Do not report each price plan unless it's responsible for the **largest variance** (either favorable or unfavorable).
   - Focus on **top insights only**: e.g., major drivers of Phone Gross Adds.
   - Present **only the most significant positive or negative driver** per sub-metric group (e.g., only 1–2 price plans max).

2. **Focus on Business Relevance / Logic**:
   - Weave in **business knowledge** and context that explains *why* the changes matter to the business.
   - For example, when disconnects go up and upgrades go down, what could it mean for retention strategy?

3. **Supportive Knowledge Links / Documents**:
   - Prompt should ingest & leverage:
     - **Lines Table (Google Doc)**
     - **Data Dictionary**
     - **Promotions Tracker / List**
     - **Business Context for Lines**
   - These should be linked in the prompt and cross-referenced where needed.

4. **Trend Analysis**:
   - Highlight *WoW* and *MTD* metrics distinctly.
   - Mention directionality of trends (improving/declining/stable).
   - If available later: Incorporate **daily phasing** to show weekday performance.

5. **Insightful Summaries, Not Just Data Readouts**:
   - Add commentary that connects changes to strategy, customer behavior, or business goals.

6. **Top 5 Takeaways (Refined)**:
   - Present Top 5 insights across *all line metrics*.
   - Each insight should be:
     - Specific
     - Backed by data
     - Tied to a business implication or hypothesis (but no business implication section required in the output).

7. **Simplified Benchmarks**:
   - Make sure comparisons to **Forecast, Prior Year, and Commit View (CV)** are clearly stated.
   - Use **only** the relevant comparison in each insight—don’t overload with all three unless needed.

---

Would you like me to now proceed to **rewrite the Lines Table Prompt** using these upgraded requirements?
