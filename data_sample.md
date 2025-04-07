Here’s a concise **Minutes of Meeting (MoM)** summary with bullets and action items from your discussion:

---

### **Minutes of Meeting – 1x Data Transition Discussion**
**Date:** [Insert Today’s Date]  
**Attendees:**  
- Onshore: Yashu, Mark  
- Offshore (VDSI Team)

---

### **Meeting Purpose:**  
To align on the transition of 1x and related reports/workflows from onshore to offshore (VDSI), validate data parity, and clarify the data source migration from EDW to GCP.

---

### **Discussion Summary:**

1. **1x Data Validation – Onshore vs Offshore**
   - Validated if VDSI has same data source and row counts.
   - Some discrepancies identified; e.g., **Track Phone Table** is **missing** in the VDSI environment.

2. **1x Report Components & Required Tables**
   - **Four main tables** for 1x:
     1. Summary Table (Actuals)
     2. Summary Table (Targets)
     3. Track Phone Table (Targets) – **Missing in VDSI**
     4. Wireline Table – **Available in VDSI** (already mirrored and transitioned)

3. **GCP Transition Clarification**
   - Need clarity if VDSI GCP mirrors Onshore GCP or is a customized/governed version.
   - Some CP&I and GSAM data are **excluded** in VDSI version.

4. **Future GCP Strategy for VDSI**
   - Need to confirm if VDSI will follow the **same transition pattern** as Onshore for GCP.
   - Clarify long-term governance and data source plans for both environments.

---

### **Action Items:**

| # | Action Item | Owner |
|---|-------------|-------|
| 1 | Investigate and resolve missing **Track Phone Table** in VDSI | VDSI Team |
| 2 | Provide **summary tables** (actuals and targets) for 1x to VDSI | Onshore Team |
| 3 | Confirm whether **VDSI GCP** will be identical to **Onshore GCP** or governed version | VDSI & Data Governance Team |
| 4 | Get clarity on **future GCP transition plan** for VDSI | VDSI & Onshore Architecture |
| 5 | Share **modified wireline workflow** with VDSI for reference | Yashu |

---

Let me know if you want this in a Word doc or email format too.
