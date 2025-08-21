/** Click Tracking Web App — single-file implementation
 * Sheets created by "Tracking → Setup sheets"
 * Build per-recipient links with "Tracking → Build tracking links (for Link ID)"
 *
 * ─ Sheets ─
 * Links:      [LinkID, TargetURL, Title, Active, Owner]
 * Recipients: [Token, Name, Email, TrackingURL (per-link)]
 * Clicks:     [Timestamp, LogID, LinkID, TargetURL, RecipientToken, RecipientName, RecipientEmail, UserAgent, Language, Screen, Timezone, Referrer, QueryString, Notes]
 */

const SHEETS = {
  LINKS: 'Links',
  RECIPS: 'Recipients',
  CLICKS: 'Clicks',
};

const HEADERS = {
  [SHEETS.LINKS]:  ['LinkID','TargetURL','Title','Active','Owner'],
  [SHEETS.RECIPS]: ['Token','Name','Email','TrackingURL'],
  [SHEETS.CLICKS]: ['Timestamp','LogID','LinkID','TargetURL','RecipientToken','RecipientName','RecipientEmail','UserAgent','Language','Screen','Timezone','Referrer','QueryString','Notes'],
};

// ⬅️ Paste your deployed Web App URL here after deploying (Step 7/8)
const WEB_APP_URL = 'PASTE_WEB_APP_URL_HERE';

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Tracking')
    .addItem('Setup sheets', 'setupSheets_')
    .addItem('Generate recipient tokens', 'generateRecipientTokens_')
    .addItem('Build tracking links (for Link ID)', 'buildLinksForLinkId_')
    .addToUi();
}

/** One-time: create sheets and headers if missing */
function setupSheets_() {
  const ss = SpreadsheetApp.getActive();
  [SHEETS.LINKS, SHEETS.RECIPS, SHEETS.CLICKS].forEach(name => {
    let sh = ss.getSheetByName(name);
    if (!sh) sh = ss.insertSheet(name);
    const hdrs = HEADERS[name];
    const firstRow = sh.getRange(1,1,1,hdrs.length).getValues()[0];
    const needs = JSON.stringify(firstRow) !== JSON.stringify(hdrs);
    if (needs) sh.getRange(1,1,1,hdrs.length).setValues([hdrs]);
    sh.setFrozenRows(1);
    sh.autoResizeColumns(1, hdrs.length);
  });
  SpreadsheetApp.getUi().alert('Sheets ready.\nFill Links, Recipients, then deploy the web app.');
}

/** Assign a unique token to each recipient (if missing) */
function generateRecipientTokens_() {
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEETS.RECIPS);
  if (!sh) throw new Error('Recipients sheet not found.');
  const rng = sh.getDataRange().getValues();
  const hdr = rng[0];
  const colToken = hdr.indexOf('Token');
  if (colToken < 0) throw new Error('Token column missing.');
  let updates = 0;
  for (let r=1; r<rng.length; r++) {
    if (!rng[r][colToken]) {
      rng[r][colToken] = shortToken_();
      updates++;
    }
  }
  if (updates) sh.getRange(1,1,rng.length,hdr.length).setValues(rng);
  SpreadsheetApp.getUi().alert(`Tokens generated for ${updates} recipients.`);
}

/** Build per-recipient tracking URLs for a given LinkID */
function buildLinksForLinkId_() {
  const ui = SpreadsheetApp.getUi();
  const resp = ui.prompt('Build links', 'Enter LinkID exactly as in Links sheet:', ui.ButtonSet.OK_CANCEL);
  if (resp.getSelectedButton() !== ui.Button.OK) return;
  const linkId = resp.getResponseText().trim();
  if (!linkId) return;

  const link = getLinkById_(linkId);
  if (!link || !link.active || !link.url) {
    ui.alert('LinkID not found or not active in Links sheet.');
    return;
  }
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEETS.RECIPS);
  const vals = sh.getDataRange().getValues();
  const hdr = vals[0];
  const idxToken = hdr.indexOf('Token');
  const idxURL   = hdr.indexOf('TrackingURL');
  if (idxToken < 0 || idxURL < 0) throw new Error('Recipients sheet missing Token or TrackingURL columns.');

  for (let r=1; r<vals.length; r++) {
    const token = (vals[r][idxToken] || '').toString().trim();
    if (!token) continue;
    const url = `${WEB_APP_URL}?id=${encodeURIComponent(linkId)}&r=${encodeURIComponent(token)}`;
    vals[r][idxURL] = url;
  }
  sh.getRange(1,1,vals.length,hdr.length).setValues(vals);
  ui.alert('TrackingURL built for all recipients.');
}

/** ───────── Web App endpoints ───────── */

function doGet(e) {
  // Read parameters
  const id = (e.parameter.id || '').toString().trim();
  const r  = (e.parameter.r || '').toString().trim();
  const rawUrl = (e.parameter.url || '').toString().trim();

  let linkId = id;
  let targetUrl = '';

  if (id) {
    const link = getLinkById_(id);
    if (!link || !link.active) {
      return htmlError_('Invalid or inactive LinkID.');
    }
    targetUrl = link.url;
  } else if (rawUrl) {
    // Ad-hoc: direct pass-through if you supply ?url=ENCODED
    targetUrl = decodeURIComponent(rawUrl);
    linkId = '(adhoc)';
  } else {
    return htmlError_('Missing link id or url param.');
  }

  const logId = Utilities.getUuid();

  // Try resolve recipient details from token
  const rec = r ? getRecipientByToken_(r) : null;

  // Minimal server-side log (in case JS/beacon blocked)
  appendClickRow_({
    logId,
    linkId,
    targetUrl,
    r,
    recName: rec?.name || '',
    recEmail: rec?.email || '',
    userAgent: '',
    language: '',
    screen: '',
    timezone: '',
    referrer: '',
    querystring: (e.queryString || ''),
    notes: 'GET',
  });

  // Serve tiny page that beacons extra details then redirects immediately
  return htmlRedirect_(targetUrl, logId);
}

function doPost(e) {
  try {
    const body = (e.postData && e.postData.contents) ? e.postData.contents : '{}';
    const data = JSON.parse(body);
    if (!data || !data.logId) return ContentService.createTextOutput('no logId');

    const sh = SpreadsheetApp.getActive().getSheetByName(SHEETS.CLICKS);
    const range = sh.getDataRange();
    const vals = range.getValues();
    const hdr = vals[0];

    const idxLogId   = hdr.indexOf('LogID');
    const idxUA      = hdr.indexOf('UserAgent');
    const idxLang    = hdr.indexOf('Language');
    const idxScreen  = hdr.indexOf('Screen');
    const idxTZ      = hdr.indexOf('Timezone');
    const idxRef     = hdr.indexOf('Referrer');
    const idxQS      = hdr.indexOf('QueryString');
    const idxNotes   = hdr.indexOf('Notes');

    // Find the row with this logId
    for (let r=1; r<vals.length; r++) {
      if (vals[r][idxLogId] === data.logId) {
        vals[r][idxUA]     = data.ua || '';
        vals[r][idxLang]   = data.lang || '';
        vals[r][idxScreen] = data.screen || '';
        vals[r][idxTZ]     = data.tz || '';
        if (data.ref && !vals[r][idxRef]) vals[r][idxRef] = data.ref;
        // Keep original GET querystring; no need to overwrite
        if (vals[r][idxNotes]) vals[r][idxNotes] += ', POST';
        else vals[r][idxNotes] = 'POST';
        sh.getRange(1,1,vals.length,hdr.length).setValues(vals);
        break;
      }
    }
    return ContentService.createTextOutput('ok');
  } catch (err) {
    return ContentService.createTextOutput('error');
  }
}

/** ───────── Helpers ───────── */

function getLinkById_(id) {
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEETS.LINKS);
  if (!sh) return null;
  const vals = sh.getDataRange().getValues();
  const hdr = vals[0];
  const idxId   = hdr.indexOf('LinkID');
  const idxURL  = hdr.indexOf('TargetURL');
  const idxAct  = hdr.indexOf('Active');
  for (let r=1; r<vals.length; r++) {
    if ((vals[r][idxId] || '').toString().trim() === id) {
      return {
        id,
        url: (vals[r][idxURL] || '').toString().trim(),
        active: String(vals[r][idxAct]).toUpperCase() !== 'FALSE',
      };
    }
  }
  return null;
}

function getRecipientByToken_(token) {
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEETS.RECIPS);
  if (!sh) return null;
  const vals = sh.getDataRange().getValues();
  const hdr = vals[0];
  const idxTok = hdr.indexOf('Token');
  const idxNm  = hdr.indexOf('Name');
  const idxEm  = hdr.indexOf('Email');
  for (let r=1; r<vals.length; r++) {
    if ((vals[r][idxTok] || '').toString().trim() === token) {
      return { token, name: (vals[r][idxNm]||'').toString().trim(), email: (vals[r][idxEm]||'').toString().trim() };
    }
  }
  return null;
}

function appendClickRow_(o) {
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEETS.CLICKS);
  const row = [
    new Date(), // Timestamp
    o.logId || '',
    o.linkId || '',
    o.targetUrl || '',
    o.r || '',
    o.recName || '',
    o.recEmail || '',
    o.userAgent || '',
    o.language || '',
    o.screen || '',
    o.timezone || '',
    o.referrer || '',
    o.querystring || '',
    o.notes || ''
  ];
  sh.appendRow(row);
}

function shortToken_() {
  // 12-char token from UUID (enough uniqueness for this purpose)
  return Utilities.getUuid().replace(/-/g,'').slice(0,12);
}

function htmlError_(msg) {
  return HtmlService.createHtmlOutput(
    `<html><body style="font-family:system-ui;padding:24px">
      <h3>Link error</h3><p>${escapeHtml_(msg)}</p>
    </body></html>`
  ).setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function htmlRedirect_(targetUrl, logId) {
  const safeUrl = escapeAttr_(targetUrl);
  const safeJS  = JSON.stringify(targetUrl);
  const html = `
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Redirecting…</title>
  <meta http-equiv="refresh" content="0; url=${safeUrl}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>
    (function(){
      try {
        var data = {
          logId: ${JSON.stringify(logId)},
          ua: navigator.userAgent || '',
          lang: navigator.language || '',
          screen: (window.screen && screen.width && screen.height) ? (screen.width+'x'+screen.height) : '',
          tz: (Intl && Intl.DateTimeFormat) ? (Intl.DateTimeFormat().resolvedOptions().timeZone || '') : '',
          ref: document.referrer || ''
        };
        var blob = new Blob([JSON.stringify(data)], {type: 'application/json'});
        // Post to same web app URL (no query), using sendBeacon so it survives navigation
        navigator.sendBeacon(window.location.origin + window.location.pathname, blob);
      } catch(e) {}
      // Ensure redirect even if meta refresh blocked
      setTimeout(function(){ window.location.replace(${safeJS}); }, 30);
    })();
  </script>
  <style>body{font:14px/1.5 system-ui;margin:24px;color:#111}</style>
</head>
<body>
  Redirecting to the document…
</body>
</html>`;
  return HtmlService.createHtmlOutput(html).setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function escapeHtml_(s) {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function escapeAttr_(s) {
  // safe for HTML attribute context (like URL in content/meta)
  return escapeHtml_(s).replace(/"/g, '&quot;');
}
