// == Configuration ==
const GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY'; // Replace with your actual Gemini API Key
const GEMINI_ENDPOINT = 'https://generativelanguage.googleapis.com/v1/models/gemini-1.0-pro:generateContent';

// Preset Prompt (modify as required)
const PRESET_PROMPT = `Write a concise summary of key insights from the latest Verizon earnings report.`;

// == Function to create custom menu ==
function onOpen() {
  DocumentApp.getUi().createMenu('✨ Gemini AI')
      .addItem('Generate Gemini Content', 'runGeminiAndAppendToDoc')
      .addToUi();
}

// == Main Function (Triggered by menu click) ==
function runGeminiAndAppendToDoc() {
  try {
    const aiContent = callGemini(PRESET_PROMPT);
    appendContentToDoc(aiContent);
    DocumentApp.getUi().alert('✅ Gemini content appended successfully.');
  } catch (e) {
    DocumentApp.getUi().alert('❌ Error: ' + e.message);
  }
}

// == Call Gemini API ==
function callGemini(prompt) {
  const payload = {
    contents: [{ parts: [{ text: prompt }] }]
  };

  const options = {
    method: 'POST',
    contentType: 'application/json',
    headers: {
      'x-goog-api-key': GEMINI_API_KEY
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch(GEMINI_ENDPOINT, options);
  const json = JSON.parse(response.getContentText());

  if (json.candidates && json.candidates[0].content.parts[0].text) {
    return json.candidates[0].content.parts[0].text.trim();
  } else {
    throw new Error('Gemini API error: ' + JSON.stringify(json));
  }
}

// == Append Generated Content to Current Google Doc ==
function appendContentToDoc(content) {
  const doc = DocumentApp.getActiveDocument();
  const body = doc.getBody();
  
  body.appendParagraph("\n--- Gemini AI Generated Content ---\n").setBold(true);
  body.appendParagraph(content);
  body.appendParagraph("\n--- End of Generated Content ---\n").setBold(true);
  
  doc.saveAndClose();
}
