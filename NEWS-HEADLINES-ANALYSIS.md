# 📰 News Headlines Feature - Technical Analysis & Configuration Guide

## 🔍 **Current Status: NOT WORKING** ❌

The News Headlines feature in your Insight Engine is **currently non-functional** because the news data is not being passed to the template. Here's a complete analysis of what's happening and how to fix it.

---

## 🎯 **What the News Headlines Feature Is Supposed to Do**

### **Purpose**
The News Headlines sidebar is designed to display **real-time Verizon company news** in the right sidebar of your Insight Engine portal, keeping users informed about the latest company updates while they access documents.

### **Data Source**
- **External Google Sheet**: `1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM`
- **Sheet Name**: "Verizon Daily Newsletter"
- **Content**: Email body content from Verizon's daily newsletter
- **Processing**: The system parses email newsletters to extract individual headlines

---

## 🔧 **How It's Supposed to Work**

### **Data Flow**
1. **External Google Sheet** contains Verizon Daily Newsletter emails
2. **`getNewsHeadlines()` function** reads from column E (Email Body)
3. **`parseNewsletterContent()` function** extracts individual news items from email content
4. **Template receives data** via `NEWS_HEADLINES` property
5. **Frontend displays** news items in the sidebar with animations

### **Expected Output Format**
```javascript
NEWS_HEADLINES: [
  {
    title: "Verizon CFO discusses turning AI into a revenue source",
    summary: "CFO explains strategy for monetizing AI capabilities...",
    fullStory: "Complete article text here...",
    date: "Sep 16, 2025",
    source: "Fortune"
  },
  // ... more news items
]
```

---

## ❌ **Why It's Not Working**

### **ROOT CAUSE: Missing Data Integration**

The `NEWS_HEADLINES` is **NOT being added** to the `templateData` object in the main `doGet()` function.

**Current templateData (lines 280-295):**
```javascript
const templateData = {
  DOCUMENT_NAME: fileName || 'Executive Report Document',
  DOCUMENT_TYPE: documentDetails.documentType || 'Executive Report',
  LAST_MODIFIED: documentDetails.lastModified || new Date().toLocaleDateString(),
  FILE_ID: fileId,
  FILE_URL: finalFileUrl,
  // ... other properties
  WHATS_INSIDE_HTML: whatsInsideHtml
  // ❌ NEWS_HEADLINES is MISSING!
};
```

**What happens:**
1. ✅ `getNewsHeadlines()` function exists and works
2. ✅ Frontend template expects `window.templateData.NEWS_HEADLINES`
3. ❌ **`NEWS_HEADLINES` never gets added to templateData**
4. ❌ Frontend falls back to mock data (the sample news you see)

---

## 🏥 **Current Fallback Behavior**

Since `NEWS_HEADLINES` is missing, the frontend shows **mock/sample data**:

```javascript
// From welcome-template.html lines 410-420
newsItems = [
  { title: "Verizon CFO discusses turning AI into a revenue source", source: "Fortune", date: "Sep 16, 2025" },
  { title: "Settlement reached with California on Frontier deal", source: "Light Reading", date: "Sep 16, 2025" },
  { title: "19th consecutive year of dividend growth announced", source: "VZMail", date: "Sep 05, 2025" },
  // ... more mock items
];
```

**This is why you see news items but they're static/fake data!**

---

## 🔧 **How to Fix It**

### **Option 1: Enable Real News Data** ✅ (Recommended)

Add this line to the `templateData` object in `code.gs` (around line 295):

```javascript
const templateData = {
  DOCUMENT_NAME: fileName || 'Executive Report Document',
  DOCUMENT_TYPE: documentDetails.documentType || 'Executive Report',
  LAST_MODIFIED: documentDetails.lastModified || new Date().toLocaleDateString(),
  FILE_ID: fileId,
  FILE_URL: finalFileUrl,
  FILE_URL_DIRECT: fileUrls.direct,
  FILE_URL_VIEW: fileUrls.view,
  FILE_URL_EDIT: fileUrls.edit || finalFileUrl,
  FILE_URL_PREVIEW: fileUrls.preview,
  VIEW_MODE: viewMode,
  TIMESTAMP: new Date().toLocaleString(),
  REPORT_TYPE: reportConfig.displayName,
  REPORT_CONFIG_KEY: reportConfig.configKey,
  WHATS_INSIDE_HTML: whatsInsideHtml,
  NEWS_HEADLINES: getNewsHeadlines()  // ✅ ADD THIS LINE
};
```

### **Option 2: Disable News Feature** ⚠️

If you don't want news headlines, remove the entire news sidebar from `welcome-template.html`:

```html
<!-- Remove this entire section (lines ~330-365) -->
<div class="sidebar">
  <div class="column-header">
    <span>📰</span>
    <h4>Latest Headlines</h4>
  </div>
  <!-- ... entire news sidebar content ... -->
</div>
```

And update the CSS grid to 2 columns instead of 3:
```css
.document-container {
  grid-template-columns: 320px 1fr; /* Instead of 320px 1fr 300px */
}
```

---

## 📊 **External Google Sheet Structure**

The news system expects this structure in Google Sheet `1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM`:

| Column A | Column B | Column C | Column D | **Column E** |
|----------|----------|----------|----------|-------------|
| Timestamp | Subject | From | To | **Email Body** |
| Date | Newsletter Subject | sender@verizon.com | recipients | **Full newsletter content with headlines** |

**The system reads Column E (Email Body) and parses it to extract individual news items.**

---

## 🔐 **Permissions Required**

For the news feature to work, your Google Apps Script needs:
- **Read access** to the external Google Sheet `1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM`
- **Access to the "Verizon Daily Newsletter" tab**

If you get permission errors, you'll need the sheet owner to grant access to your Apps Script service account.

---

## 🧪 **Testing the Fix**

### **1. Add the NEWS_HEADLINES line** to templateData
### **2. Deploy your updated Apps Script**
### **3. Test with a document URL**
### **4. Check browser console for errors:**

```javascript
// Open browser console and check:
console.log(window.templateData.NEWS_HEADLINES);
```

**Expected results:**
- ✅ **If working**: Array of real news objects
- ❌ **If broken**: `undefined` or error messages

---

## 📈 **Performance Impact**

Adding `getNewsHeadlines()` to every page load:
- **Additional API call** to external Google Sheet
- **~1-2 second delay** for news parsing
- **Fallback to mock data** if external sheet is unavailable

**Recommendation**: Consider caching news data or loading it asynchronously after page load.

---

## 🎯 **Summary**

| Component | Status | Notes |
|-----------|--------|--------|
| **Backend Function** | ✅ Working | `getNewsHeadlines()` and parsing logic exist |
| **External Data Source** | ❓ Unknown | Google Sheet may have permission issues |
| **Data Integration** | ❌ Broken | `NEWS_HEADLINES` not added to templateData |
| **Frontend Template** | ✅ Working | Displays mock data when real data unavailable |
| **Fallback System** | ✅ Working | Shows sample news when external source fails |

**TO FIX**: Simply add `NEWS_HEADLINES: getNewsHeadlines()` to the templateData object in code.gs line ~295.

---

## 🚀 **Recommendation**

**Enable the real news feature** by adding the missing line to templateData. This will provide users with actual Verizon company news updates, making the Insight Engine portal more valuable and engaging.

If you don't need company news, consider removing the entire sidebar to simplify the interface and improve performance.

---

*Document created: September 19, 2025*
*Analysis of: Insight Engine News Headlines Feature*
*Status: Ready for Implementation*
