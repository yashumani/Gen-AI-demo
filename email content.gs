function extractFullNewsletterCleaned() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var searchQuery = 'subject:"Verizon Daily Newsletter"'; // Modify as needed

  var threads = GmailApp.search(searchQuery);
  var emails = GmailApp.getMessagesForThreads(threads);

  // Clear the sheet before adding new data (overwrite mode)
  sheet.clear();

  // Define headers
  var headers = ["Timestamp", "Sender", "Recipient", "Subject", "Cleaned Email Body"];
  sheet.appendRow(headers);

  emails.forEach(thread => {
    thread.forEach(email => {
      var timestamp = email.getDate();
      var sender = email.getFrom();
      var recipient = email.getTo();
      var subject = email.getSubject();
      var body = cleanEmailBody(email.getPlainBody()); // Process email body

      // Append to Google Sheet
      sheet.appendRow([timestamp, sender, recipient, subject, body]);
    });
  });

  Logger.log("Emails extracted and cleaned successfully!");
}

/**
 * Cleans the email body by:
 * - Removing Proofpoint-protected URLs
 * - Removing unnecessary footers or signatures
 * - Keeping only the main content
 */
function cleanEmailBody(body) {
  // Remove Proofpoint URLs (pattern based)
  body = body.replace(/https:\/\/urldefense\.proofpoint\.com[^\s]+/g, "[Removed Link]");

  // Remove footer and unsubscribe messages (modify this pattern based on common footers)
  var footerPattern = /----------------------\nThis email was sent to[^\n]+/g;
  body = body.replace(footerPattern, "").trim();

  return body;
}
