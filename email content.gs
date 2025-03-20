function extractNewsletterSections() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var searchQuery = 'subject:"Your Newsletter Subject"'; // Modify to match your email search criteria

  var threads = GmailApp.search(searchQuery); // Fetch ALL matching emails
  var emails = GmailApp.getMessagesForThreads(threads);

  // Clear existing data before each execution (overwrite mode)
  sheet.clear();
  
  // Define sections to extract
  var sections = [
    "Verizon's Stock",
    "US Stock Market Closings",
    "Verizon in the News",
    "Verizon in the Local News",
    "Competitor News",
    "Industry News",
    "Verizon News"
  ];

  // Add headers dynamically based on sections
  var headers = ["Timestamp", "Sender", "Recipient", "Subject"].concat(sections);
  sheet.appendRow(headers);

  emails.forEach(thread => {
    thread.forEach(email => {
      var timestamp = email.getDate();
      var sender = email.getFrom();
      var recipient = email.getTo();
      var subject = email.getSubject();
      var body = email.getPlainBody();

      // Parse email body into sections
      var sectionData = extractSections(body, sections);

      // Create row with extracted data
      var rowData = [timestamp, sender, recipient, subject];
      sections.forEach(section => {
        rowData.push(sectionData[section] || ""); // Fill empty sections with blank
      });

      // Append to Google Sheet
      sheet.appendRow(rowData);
    });
  });

  Logger.log("Emails extracted and saved successfully!");
}

/**
 * Extracts content under specific section headers
 */
function extractSections(body, sections) {
  var data = {};
  
  // Create regex pattern to identify headers
  var pattern = new RegExp(sections.map(s => `(${s})`).join("|"), "g");
  var matches = [...body.matchAll(pattern)];

  if (matches.length === 0) {
    return data; // Return empty if no matches
  }

  for (var i = 0; i < matches.length; i++) {
    var section = matches[i][0]; // Get matched section name
    var startIndex = matches[i].index + section.length; // Start of section content
    var endIndex = i + 1 < matches.length ? matches[i + 1].index : body.length; // End of section

    data[section] = body.substring(startIndex, endIndex).trim(); // Extract content
  }

  return data;
}
