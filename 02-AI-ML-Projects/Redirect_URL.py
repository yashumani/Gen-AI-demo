/*** CONFIG ***/
const SHEET_ID = 'PUT_YOUR_SHEET_ID_HERE'; // e.g. 1AbC... from the Sheet URL
const CLICKS_TAB = 'clicks';

/*** UTILITIES ***/
function sheet_() {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  let sh = ss.getSheetByName(CLICKS_TAB);
  if (!sh) {
    sh = ss.insertSheet(CLICKS_TAB);
    sh.appendRow(['timestamp','campaign','user_h','button','destination','extra']);
  }
  return sh;
}

function safe_(s) { return (s || '').toString(); }

function logClick_(p) {
  const sh = sheet_();
  const row = [
    new Date(),                // timestamp
    safe_(p.cid),              // campaign
    safe_(p.email),            // user_h (hashed id from KNIME)
    safe_(p.btn),              // open|prompt
    safe_(p.dest),             // full destination URL
    safe_(p.x)                 // optional extra: anything you pass as &x=
  ];
  sh.appendRow(row);
}

/*** WEB ENTRY ***/
function doGet(e) {
  const p = (e && e.parameter) || {};
  // minimally require destination & campaign
  if (!p.dest) {
    return HtmlService.createHtmlOutput('<p>Missing destination.</p>');
  }
  // log first
  try { logClick_(p); } catch (err) { /* fail-soft: still redirect */ }

  // fast client-side redirect (works in most email clients)
  const dest = encodeURI(decodeURIComponent(p.dest));
  const html = `
    <html><head>
      <meta http-equiv="refresh" content="0; url=${dest}">
      <script>location.replace("${dest}");</script>
    </head>
    <body>Redirecting…</body></html>
  `;
  return HtmlService.createHtmlOutput(html);
}

/*** OPTIONAL: one-time setup to make headers if missing ***/
function ensureSetup() { sheet_(); }
