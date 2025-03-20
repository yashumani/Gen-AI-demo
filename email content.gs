function extractFullNewsletter() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var searchQuery = 'subject:"Verizon Daily Newsletter"'; // Modify as needed

  var threads = GmailApp.search(searchQuery);
  var emails = GmailApp.getMessagesForThreads(threads);

  // Clear the sheet before adding new data (overwrite mode)
  sheet.clear();

  // Define headers
  var headers = ["Timestamp", "Sender", "Recipient", "Subject", "Email Body"];
  sheet.appendRow(headers);

  emails.forEach(thread => {
    thread.forEach(email => {
      var timestamp = email.getDate();
      var sender = email.getFrom();
      var recipient = email.getTo();
      var subject = email.getSubject();
      var body = email.getPlainBody(); // Capture the FULL email body (no truncation)

      // Append to Google Sheet
      sheet.appendRow([timestamp, sender, recipient, subject, body]);
    });
  });

  Logger.log("Emails extracted successfully!");
}
