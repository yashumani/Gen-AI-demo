/**
 * Creates a custom menu in the Google Sheet UI when the spreadsheet is opened.
 */
function onOpen() {
  SpreadsheetApp.getUi()
      .createMenu('Gemini Assistant')
      .addItem('Launch Prompt Generator', 'showWebApp')
      .addToUi();
}

/**
 * Shows the web app in a sidebar in the Google Sheet.
 */
function showWebApp() {
  const html = HtmlService.createHtmlOutputFromFile('WebApp')
      .setTitle('Gemini Prompt Generator')
      .setWidth(850); // Set a suitable width for the dashboard
  SpreadsheetApp.getUi().showSidebar(html);
}

function doGet() {
  // This function serves the main HTML page of the prompt generator web app.
  return HtmlService.createTemplateFromFile('WebApp')
      .evaluate()
      .setTitle('Gemini Prompt Generator & Feedback')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * Fetches and structures the suggested prompts from the active Google Sheet.
 * @param {string} reportName The name of the sheet (tab) to read from.
 * @return {Object} A structured object of prompts categorized by question type.
 */
function getSuggestedPrompts(reportName) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(reportName);
    
    if (!sheet) {
      // Return an explicit error object if the sheet is not found.
      return { error: `A sheet (tab) named '${reportName}' was not found in your Google Sheet. Please check the name.` };
    }

    const dataRange = sheet.getDataRange();
    const values = dataRange.getValues();
    const headers = values[0];
    const prompts = {};

    // Initialize an array for each question type (header)
    headers.forEach(header => {
      if (header) { // Ensure header is not empty
        prompts[header] = [];
      }
    });

    // Populate the arrays with prompts from the corresponding columns
    for (let i = 1; i < values.length; i++) {
      for (let j = 0; j < headers.length; j++) {
        const header = headers[j];
        if (header && values[i][j]) {
          prompts[header].push(values[i][j]);
        }
      }
    }
    
    return prompts;
  } catch (error) {
    // Return an error object to be handled by the client-side script
    return { error: error.toString() };
  }
}

/**
 * Handles the submission of user questions and feedback.
 */
function submitUserQuestion(formData) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const reportName = formData.reportName;
    const submissionType = formData.submissionType;
    const submissionText = formData.submissionText;
    const userEmail = Session.getActiveUser().getEmail() || "anonymous";

    let sheet = ss.getSheetByName(reportName + " Submissions");
    if (!sheet) {
      sheet = ss.insertSheet(reportName + " Submissions");
      sheet.getRange("A1").setValue("Timestamp");
    }

    const headers = sheet.getRange("1:1").getValues()[0];
    let columnIndex = headers.indexOf(submissionType) + 1;

    if (columnIndex === 0) {
      columnIndex = sheet.getLastColumn() + 1;
      sheet.getRange(1, columnIndex).setValue(submissionType);
    }

    const columnValues = sheet.getRange(1, columnIndex, sheet.getMaxRows()).getValues();
    let lastRow = columnValues.filter(String).length;
    
    sheet.getRange(lastRow + 1, columnIndex).setValue(submissionText);
    sheet.getRange(lastRow + 1, 1).setValue(new Date());
    if (sheet.getRange("B1").getValue() !== "UserEmail") {
        sheet.getRange("B1").setValue("UserEmail");
    }
    sheet.getRange(lastRow + 1, 2).setValue(userEmail);

    return { success: true, message: "Thank you! Your submission has been received." };
  } catch (error) {
    return { success: false, message: "An error occurred: " + error.toString() };
  }
}
