Yep—I’m with you. By “Insight Engine” you mean the email you send (from KNIME) with two buttons—“Open in Gemini View” and “View Prompt Generator”—that open a Google Drive-hosted report (plus helper pages). You replaced old PDF attachments with Drive links and keep copies in a Drive “reports” space; the KNIME job finds the latest file and injects its link into the email body. 👍

If your seniors want click/usage metrics, here are solid options (from easiest to most robust), plus a ready-to-use pattern:

# 1) Easiest + reliable: Apps Script “redirect logger” (recommended)

Wrap every Drive link in a tiny Apps Script Web App URL that logs the click, then immediately 302-redirects to the real Drive URL.

**How it works**

* KNIME generates a *unique* link per recipient/button:
  `https://script.google.com/macros/s/<DEPLOYMENT_ID>/exec?cid=<campaign>&email=<hash>&btn=<open|prompt>&dest=<encoded_drive_url>`
* The script writes a row to a Google Sheet (timestamp, campaign, hashed email/user id, button, user-agent, IP region if desired), then redirects.
* You still share the file in Drive as usual (no extra friction for users with access). If they don’t have access, you still capture the click.

**Minimal Apps Script (Code.gs)**

1. Apps Script → New project → *Deploy as Web App*

   * **Execute as:** Me
   * **Who has access:** Anyone with the link (this doesn’t expose your Drive file; it only runs the logger)
2. Add this code and deploy:

```javascript
function doGet(e) {
  const p = e.parameter || {};
  const dest = decodeURIComponent(p.dest || "");
  const campaign = p.cid || "default";
  const button = p.btn || "open";
  const user = p.email || "anon"; // pass a hash/token, not raw email for privacy

  // Log to a Google Sheet (create a sheet and paste its ID here)
  const SHEET_ID = "YOUR_SHEET_ID";
  const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName("clicks") || SpreadsheetApp.openById(SHEET_ID).insertSheet("clicks");

  // Header init (idempotent)
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(["timestamp","campaign","user","button","destination","userAgent"]);
  }

  const ua = e?.request?.headers?.["User-Agent"] || "unknown";
  sheet.appendRow([new Date(), campaign, user, button, dest, ua]);

  // 302 redirect to actual Drive file
  if (dest) {
    return HtmlService.createHtmlOutput(
      `<html><head>
        <meta http-equiv="refresh" content="0;url=${sanitize_(dest)}">
      </head><body>Redirecting…</body></html>`
    );
  } else {
    return HtmlService.createHtmlOutput("Missing destination.");
  }
}

function sanitize_(url){
  // Minimal guard—keep to https only
  if (!/^https:\/\/.+/.test(url)) return "https://www.google.com";
  return url.replace(/"/g, "");
}
```

**What you’ll get**

* A clean **Click Log** in Sheets you can pivot by campaign, user, and button for CTR, unique clicks, etc.
* Works with your existing KNIME job: just build the redirect URL around the actual Drive link and include a per-recipient token (hash the email in KNIME to avoid storing PII).

**Notes / gotchas**

* Set Web App to “Anyone with the link”; it’s only the logger. Your Drive file still enforces access.
* If your org blocks script URLs in emails, consider a short vanity domain (Apps Script + Cloud Run/Functions work too).

# 2) Drive Activity API (org-level “views”)

If everyone is on the same Workspace domain and opens the **file**, you can count **file views** via the Drive Activity API or Admin audit logs. Pros: it measures actual opens. Cons: requires admin/API setup, won’t count users who click but get blocked, and attribution can be coarse.

Use this as a *supplement* to the redirect logger when you want “unique viewers” or “time of first open” on the specific Drive file.

# 3) Firebase Dynamic Links (FDL) / Link shorteners

FDL gives built-in analytics for clicks (and deep linking if you ever go mobile). Bitly/others can also work, but many enterprises block external shorteners, and you’ll still need to pass tokens/UTM-style params for per-recipient attribution. Usually more overhead than the Apps Script approach.

---

## Data model & reporting (quick template)

Create a Google Sheet `Insight_Eng_Campaigns` with tabs:

* **clicks**: `timestamp, campaign, user (hashed), button, destination, userAgent`
* **recipients** (optional): `campaign, user_hashed, department, segment`
* **report**: pivot tables →

  * CTR = unique users clicked / recipients sent
  * Button split: Open vs Prompt
  * Heatmap by hour/day
  * Top files/destinations

## KNIME hookup (what to change)

* Before sending email, build the **redirect URL**:

  * `dest = encodeURIComponent(drive_link)`
  * `email_hash = SHA256(lower(email))` (or your internal ID)
  * `campaign = "IE_2025-09-Launch"`
  * Final: `webapp_url + "?cid=" + campaign + "&email=" + email_hash + "&btn=open&dest=" + dest`
* Insert that into the email buttons instead of the raw Drive link.

## Privacy & compliance

* Hash emails (don’t store raw addresses in the Sheet).
* Communicate internal analytics in your campaign brief if required by policy.
* Only log what you need (timestamp, token, button, destination).

If you want, I can also give you a tiny KNIME snippet (String Manipulation + Column Expressions) to generate those URLs, and a ready-made Google Sheet with a pivot report—just say the word and I’ll drop both.
