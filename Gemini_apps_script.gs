const PROJECT_ID = 'your-project-id';
const REGION = 'us-central1';
const MODEL_NAME = 'gemini-1.0-pro';
const VERTEX_AI_API_KEY = 'YOUR_VERTEX_AI_API_KEY';

// Vertex AI endpoint construction
const GEMINI_ENDPOINT = `https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/publishers/google/models/${MODEL_NAME}:generateContent?key=${VERTEX_AI_API_KEY}`;

/**
 * Calls Gemini API via Vertex AI using API key
 */
function callGeminiAPI(prompt) {
  const payload = {
    contents: [
      {
        parts: [{ text: prompt }]
      }
    ]
  };

  const options = {
    method: "POST",
    contentType: "application/json",
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch(GEMINI_ENDPOINT, options);
  const json = JSON.parse(response.getContentText());

  if (json.candidates && json.candidates[0].content.parts[0].text) {
    return json.candidates[0].content.parts[0].text;
  } else {
    throw new Error('Gemini API Error: ' + JSON.stringify(json));
  }
}

/**
 * Reads prompts from "PromptInput" sheet, calls Gemini, and writes responses to "GeminiResponses"
 */
function runGeminiPromptAutomation() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const inputSheet = ss.getSheetByName('PromptInput');
  const outputSheetName = 'GeminiResponses';

  let outputSheet = ss.getSheetByName(outputSheetName);
  if (!outputSheet) {
    outputSheet = ss.insertSheet(outputSheetName);
  } else {
    outputSheet.clear();
  }

  const prompts = inputSheet.getRange('A2:A' + inputSheet.getLastRow()).getValues().flat();
  const results = [['Prompt', 'Gemini Response']];

  prompts.forEach(prompt => {
    if (prompt) {
      try {
        const response = callGeminiAPI(prompt);
        results.push([prompt, response]);
      } catch (e) {
        results.push([prompt, `Error: ${e.message}`]);
      }
    }
  });

  outputSheet.getRange(1, 1, results.length, results[0].length).setValues(results);
}
