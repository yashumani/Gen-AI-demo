function extractNewsletterEmails() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var searchQuery = 'subject:"Security Alert"'; // Modify this to match your email
  var threads = GmailApp.search(searchQuery, 0, 10); // Fetch latest 10 matching emails
  var emails = GmailApp.getMessagesForThreads(threads);
  
  sheet.appendRow(["Timestamp", "Sender", "Recipient", "Subject", "Body Preview", "Attachments"]);

  emails.forEach(thread => {
    thread.forEach(email => {
      var timestamp = email.getDate();
      var sender = email.getFrom();
      var recipient = email.getTo();
      var subject = email.getSubject();
      var body = email.getPlainBody().substring(0, 500); // First 500 characters (adjust if needed)
      
      var attachments = email.getAttachments();
      var attachmentLinks = attachments.map(att => att.getName()).join(", ");

      sheet.appendRow([timestamp, sender, recipient, subject, body, attachmentLinks]);
    });
  });
  
  Logger.log("Emails extracted successfully!");
}
