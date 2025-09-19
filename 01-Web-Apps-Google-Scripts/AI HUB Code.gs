// ===============================================================
// | Intelligent Analytics Template - Backend (Code.gs) |
// ===============================================================

// --- CONFIGURATION ---

// IMPORTANT: Replace with your Google Cloud Project ID
const PROJECT_ID = 'smartbi-digest';
const LOCATION = 'us-east4'; // e.g., 'us-central1', 'us-east4'


// --- MODEL SELECTION ---

// Choose which Gemini model to use. Simply copy one of the options into the MODEL_ID variable.
//
// 1. "gemini-1.5-pro" -> Best for complex reasoning, deep analysis, and high-quality responses.
// 2. "gemini-1.5-flash" -> Much faster and lower cost, great for everyday quick questions and summarization.
//

const MODEL_ID = 'gemini-2.5-pro';

// ===============================================================
// |                  CORE WEB APP ROUTING                       |
// ===============================================================

/**
 * Main web app router. Serves 'Project.html' for multi-step analysis
 * or the main 'WebApp.html' for Q&A and automated reports.
 */
function doGet(e) {
  if (e.parameter.page === 'project') {
    return HtmlService.createTemplateFromFile('Project')
      .evaluate()
      .setTitle('Gemini Analysis Project')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.DEFAULT);
  }
  return HtmlService.createTemplateFromFile('WebApp')
    .evaluate()
    .setTitle('Gemini Analytics Engine')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.DEFAULT);
}

/**
 * Helper to include CSS in HTML templates.
 */
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}


// ===============================================================
// |            PRIMARY WORKFLOW & AGENT FUNCTIONS               |
// ===============================================================

/**
 * FINAL CORRECTED WORKFLOW: Finds the NEXT un-analyzed sheet, gets its
 * columns, and sends only those to the AI for analysis.
 */
function generateDictionaryProposal() {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let dictionarySheet = ss.getSheetByName('_DataDictionary');
    
    // Create the dictionary sheet if it doesn't exist
    if (!dictionarySheet) {
      dictionarySheet = ss.insertSheet('_DataDictionary');
      dictionarySheet.getRange('A1:D1').setValues([['Sheet Name', 'Column Header', 'Data Type', 'Description']]);
    }
    
    // Find which sheets are already in the dictionary
    const analyzedSheets = dictionarySheet.getLastRow() > 1 ?
      [...new Set(dictionarySheet.getRange(2, 1, dictionarySheet.getLastRow() - 1, 1).getValues().flat())] : [];

    // Find the first data sheet that has not been analyzed yet
    const allDataSheets = ss.getSheets().filter(sheet => !sheet.getName().startsWith('_'));
    const sheetToAnalyze = allDataSheets.find(sheet => !analyzedSheets.includes(sheet.getName()));

    // If no new sheet is found, the process is complete.
    if (!sheetToAnalyze) {
      return { status: 'complete', message: "All sheets have been successfully analyzed and added to the Data Dictionary. You can now use the Q&A and Automated Report features." };
    }

    let columnsToAnalyze = [];
    if (sheetToAnalyze.getLastRow() > 1 && sheetToAnalyze.getLastColumn() > 0) {
      const headers = sheetToAnalyze.getRange(1, 1, 1, sheetToAnalyze.getLastColumn()).getValues()[0];
      const sampleData = sheetToAnalyze.getRange(2, 1, Math.min(5, sheetToAnalyze.getLastRow() - 1), sheetToAnalyze.getLastColumn()).getValues();

      headers.forEach((header, i) => {
        if (header && header.toString().trim() !== '') {
          const samples = sampleData.map(row => row[i] || '').join(', ');
          columnsToAnalyze.push({ sheetName: sheetToAnalyze.getName(), columnHeader: header, sampleData: samples });
        }
      });
    }

    if (columnsToAnalyze.length === 0) {
      // This sheet might be empty, let's try to find the next one
      return { status: 'complete', message: `Sheet "${sheetToAnalyze.getName()}" was empty or had no headers. Please check other sheets or start your analysis.` };
    }
    
    // --- Send only this sheet's columns to the AI ---
    const prompt = `
      You are a data dictionary generation system. Your only output is a valid JSON array.
      Based on the following list of columns and their sample data from the "${sheetToAnalyze.getName()}" sheet, determine the "dataType" and generate a "description" for each.

      COLUMNS TO ANALYZE: ${JSON.stringify(columnsToAnalyze, null, 2)}
      
      MANDATORY INSTRUCTIONS:
      1.  Return a single JSON array of objects. Each object must have four keys: "sheetName", "columnHeader", "dataType", and "description".
      2.  "dataType" must be one of: 'String', 'Integer', 'Float', 'Date', 'Boolean', 'Categorical', 'ID'.
      3.  Ensure the JSON is perfectly valid. Wrap it in <JSON_OUTPUT> tags.
    `;
    const rawResponseText = callGeminiAPI(prompt);
    
    const parsedObject = extractAndCleanJson(rawResponseText);
    return { status: 'success', proposal: parsedObject };

  } catch (e) {
    Logger.log("Error in generateDictionaryProposal: " + e.toString());
    return { status: 'error', message: e.message };
  }
}

/**
 * WORKFLOW 2: Called by the "Generate Automated Report" button.
 * Performs a full automated analysis, finds trends, and generates a visualization.
 */
function generateAutomatedAnalysis() {
  try {
    const dataDictionary = getSheetDataAsMarkdown('_DataDictionary');
    if (dataDictionary.includes("is empty") || dataDictionary.includes("not found")) {
      throw new Error("Data Dictionary is empty. Please run 'Scan Data & Build Dictionary' first.");
    }
    
    const prompt = `
      You are a Senior Data Analyst reporting to an executive. Your task is to perform an automated analysis of the entire data workspace and present your findings.
      **DATA DICTIONARY (Your available data):**
      ---
      ${dataDictionary}
      ---
      **INSTRUCTIONS:**
      1.  **Analyze Holistically:** Review all datasets. Identify columns that represent time-series data and key business metrics.
      2.  **Find the Most Important Story:** Proactively search for significant patterns, anomalies, or trends. Perform comparisons like month-over-month if date columns are available.
      3.  **Write a Narrative Summary:** Structure your findings in clear Markdown. Start with a main heading '# Key Analytical Findings'.
      4.  **Create a Key Visualization:** After the text summary, create a Google Chart configuration to visualize your single most important finding. Enclose this configuration in a \`\`\`google_chart ... \`\`\` block. The JSON must have "type", "data", and "options" keys.
    `;
    const analysisResult = callGeminiAPI(prompt);
    return { status: 'success', insight: analysisResult };

  } catch(e) {
    Logger.log("Error in generateAutomatedAnalysis: " + e.toString());
    return { status: 'error', message: e.message };
  }
}


/**
 * WORKFLOW 3: Called by the Project page.
 * Executes a single step in a multi-turn conversational analysis project.
 */
function executeAnalysisStep(projectGoal, projectHistory) {
  try {
    const dataDictionary = getSheetDataAsMarkdown('_DataDictionary');
    if (dataDictionary.includes("not found")) {
      throw new Error("Data Dictionary not found. Please run 'Scan Data & Build Dictionary' from the main page first.");
    }

    const prompt = `
      You are an autonomous Senior Data Analyst working on a multi-step project.

      **OVERALL PROJECT GOAL:**
      ---
      ${projectGoal}
      ---
      
      **PROJECT HISTORY (What has been done so far):**
      ---
      ${projectHistory}
      ---

      **AVAILABLE DATA (from the Data Dictionary):**
      ---
      ${dataDictionary}
      ---

      **YOUR TASK:**
      Based on the overall goal, the project history, and the user's latest instruction, determine the single most logical next step to advance the project. Execute that step now. Your response should include two parts:
      1.  **Your Thought Process:** In a blockquote, briefly explain what you decided to do next and why.
      2.  **Your Output:** The full result of the action you just took.

      Structure your entire response in clear Markdown. If a chart is the best output, generate its configuration in a \`\`\`google_chart\`\`\` block.
    `;

    const stepResult = callGeminiAPI(prompt);
    return { status: 'success', insight: stepResult };

  } catch (e) {
    Logger.log("Error in executeAnalysisStep: " + e.toString());
    return { status: 'error', message: e.message };
  }
}

/**
 * The main Q&A function for use after the dictionary is set up.
 */
function getGeminiInsight(userQuery, conversationHistory) {
  try {
    const dataDictionary = getSheetDataAsMarkdown('_DataDictionary');
    const pastInsights = getRelevantPastInsights(userQuery); 
    const configData = getSheetDataAsMarkdown('_Config');
    
    const prompt = `
      You are a world-class business analyst.
      **CORE INSTRUCTIONS:** ${configData}
      **KNOWLEDGE BASE (Past relevant analyses):** ${pastInsights}
      **DATA DICTIONARY (Available data):** ${dataDictionary}
      **CURRENT CONVERSATION:** ${conversationHistory}
      **USER'S NEW QUESTION:** "${userQuery}"
      Analyze the user's question and provide the best possible insight based on ALL context. Use Markdown for clarity.
    `;
    
    const geminiResponse = callGeminiAPI(prompt);
    logInsight(userQuery, geminiResponse);
    return { status: 'success', insight: geminiResponse };
  } catch (e) {
    Logger.log(e.toString());
    return { status: 'error', message: e.toString() };
  }
}

// ===============================================================
// |                  HELPER & UTILITY FUNCTIONS                 |
// ===============================================================

/**
 * Writes the approved dictionary proposals back to the Google Sheet.
 */
/**
 * CORRECTED: Appends the new proposals to the Data Dictionary instead of clearing it,
 * allowing for sheet-by-sheet processing.
 */
function updateDataDictionary(proposals) {
    try {
        const ss = SpreadsheetApp.getActiveSpreadsheet();
        let dictionarySheet = ss.getSheetByName('_DataDictionary');
        if (!dictionarySheet) { 
          dictionarySheet = ss.insertSheet('_DataDictionary');
          dictionarySheet.getRange('A1:D1').setValues([['Sheet Name', 'Column Header', 'Data Type', 'Description']]);
        }
        
        const values = proposals.map(p => [p.sheetName, p.columnHeader, p.dataType, p.description]);
        
        if (values.length > 0) {
          // Append data to the end of the sheet, starting at the next available row.
          dictionarySheet.getRange(dictionarySheet.getLastRow() + 1, 1, values.length, 4).setValues(values);
        }
        return { status: 'success' };
    } catch(e) {
        Logger.log("Error in updateDataDictionary: " + e.toString());
        return { status: 'error', message: e.message };
    }
}


/**
 * Generates contextual follow-up questions for the suggestion banner.
 */
function getSuggestedActions(lastQuery, lastResponse) {
  try {
    const prompt = `Suggest three brief, insightful follow-up questions based on the last interaction. LAST USER QUERY: "${lastQuery}" LAST AI RESPONSE: "${lastResponse}". Return ONLY a valid JSON array of strings.`;
    const suggestionsJson = callGeminiAPI(prompt);
    return extractAndCleanJson(suggestionsJson);
  } catch (e) {
    Logger.log("Error generating suggestions: " + e.toString());
    return [];
  }
}

/**
 * FINAL ROBUST FUNCTION: Finds, cleans, and parses a JSON object/array 
 * from a raw AI response using a two-stage approach.
 */
function extractAndCleanJson(rawText) {
  try {
    let jsonString;

    // 1. First, try the most reliable method: look for our specific tags.
    const tagMatch = rawText.match(/<JSON_OUTPUT>([\s\S]*)<\/JSON_OUTPUT>/);
    if (tagMatch && tagMatch[1]) {
      jsonString = tagMatch[1].trim();
    } else {
      // 2. If tags are not found, fall back to finding the first opening brace/bracket.
      // This handles cases where the model forgets the tags but still outputs JSON.
      const fallbackMatch = rawText.match(/\{[\s\S]*\}|\[[\s\S]*\]/);
      if (fallbackMatch) {
        jsonString = fallbackMatch[0].trim();
      } else {
        // If neither method works, there's no recoverable JSON.
        throw new Error("No JSON object or array could be found in the model's response.");
      }
    }

    // 3. Aggressively clean the found string to fix common AI mistakes
    // This removes trailing commas that break JSON.parse()
    jsonString = jsonString.replace(/,\s*([\}\]])/g, "$1");
    
    // 4. Attempt to parse the cleaned string
    return JSON.parse(jsonString);

  } catch (e) {
    // This log is critical for debugging any future, unknown formatting errors.
    Logger.log("CRITICAL PARSE FAILURE. Raw text was: " + rawText);
    throw new Error("The model's response could not be parsed, even after advanced extraction and cleaning. Check logs for details.");
  }
}

/**
 * Calls the Vertex AI Gemini API endpoint using the selected model.
 * This version enforces a JSON response MIME type for reliability.
 */
function callGeminiAPI(prompt) {
  const accessToken = ScriptApp.getOAuthToken();
  const url = `https://us-central1-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/publishers/google/models/${MODEL_ID}:streamGenerateContent`;
  
  const requestBody = {
    "contents": [{ "role": "user", "parts": [{ "text": prompt }] }],
    "generation_config": {
      "temperature": 0.3,
      "top_p": 1.0,
      "max_output_tokens": 8192,
      // NEW: Force the model to output structured JSON
      "response_mime_type": "application/json", 
    }
  };

  const options = { 'method': 'post', 'contentType': 'application/json', 'headers': { 'Authorization': 'Bearer ' + accessToken }, 'payload': JSON.stringify(requestBody), 'muteHttpExceptions': true };
  const response = UrlFetchApp.fetch(url, options);
  const responseText = response.getContentText();
  if (response.getResponseCode() !== 200) { throw new Error(`Gemini API Error: ${responseText}`); }
  
  // Since we force a JSON response, we can be more confident in the structure.
  // The streaming response is an array of objects.
  try {
    const chunks = JSON.parse(responseText);
    let combinedText = '';
    chunks.forEach(chunk => {
      if (chunk.candidates && chunk.candidates[0].content && chunk.candidates[0].content.parts && chunk.candidates[0].content.parts[0].text) {
        combinedText += chunk.candidates[0].content.parts[0].text;
      }
    });

    if (combinedText.trim() === '') { return "{\"error\": \"The model returned an empty response.\"}"; }
    return combinedText.trim();
  } catch(e) {
    Logger.log("Could not parse streaming chunks. Raw Response: " + responseText);
    // If it's not a streaming array, it might be a single error object.
    return responseText;
  }
}

/**
 * Logs a new insight into the _InsightsLog sheet.
 */
function logInsight(query, insight) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const logSheet = ss.getSheetByName('_InsightsLog');
    if (logSheet) { 
      const insightString = typeof insight === 'object' ? JSON.stringify(insight) : insight;
      logSheet.appendRow([new Date(), query, insightString, '']); 
    }
  } catch (e) { Logger.log('Failed to log insight: ' + e.toString()); }
}

/**
 * Finds relevant past insights from the log.
 */
function getRelevantPastInsights(userQuery) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const logSheet = ss.getSheetByName('_InsightsLog');
    if (!logSheet || logSheet.getLastRow() < 2) return "No past insights available.";
  
    const data = logSheet.getRange(2, 1, logSheet.getLastRow() - 1, 3).getValues();
    const queryKeywords = userQuery.toLowerCase().split(/\s+/).filter(w => w.length > 3);
    if(queryKeywords.length === 0) return "No relevant insights found.";

    const relevantInsights = data
      .map(row => ({ query: row[1].toString().toLowerCase(), insight: row[2].toString() }))
      .filter(item => queryKeywords.some(keyword => item.query.includes(keyword)))
      .slice(-3);

    if(relevantInsights.length === 0) return "No specific past insights found for this topic.";

    let markdown = "Here are some relevant past insights from the knowledge base:\n";
    relevantInsights.forEach(item => {
      markdown += `- Based on a past query about "${item.query}", the finding was: "${item.insight.substring(0, 150)}..."\n`;
    });
    return markdown;
  } catch (e) {
    Logger.log("Error in getRelevantPastInsights: " + e.toString());
    return "Could not retrieve past insights due to an error.";
  }
}

/**
 * Converts the data of a given sheet into a markdown table format for prompts.
 */
function getSheetDataAsMarkdown(sheetName) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(sheetName);
    if (!sheet) return `Sheet "${sheetName}" not found.`;
    const data = sheet.getDataRange().getValues();
    if (data.length === 0) return `Sheet "${sheetName}" is empty.`;
    let markdown = `| ${data[0].join(' | ')} |\n`;
    markdown += `| ${data[0].map(() => '---').join(' | ')} |\n`;
    data.slice(1).forEach(row => { markdown += `| ${row.join(' | ')} |\n`; });
    return markdown;
  } catch (e) { return `Error reading sheet ${sheetName}: ${e.toString()}`; }
}


/**
 * HELPER FUNCTION: This runs only if the dictionary is completely empty.
 */
function initializeDictionaryFromSheets() {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const dictionarySheet = ss.getSheetByName('_DataDictionary');
    const allSheets = ss.getSheets().filter(sheet => !sheet.getName().startsWith('_'));
    
    let dictionaryData = [];
    allSheets.forEach(sheet => {
      if (sheet.getLastRow() > 0 && sheet.getLastColumn() > 0) {
        const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
        headers.forEach(header => {
          if (header && header.toString().trim() !== '') {
            dictionaryData.push([sheet.getName(), header, '', '']);
          }
        });
      }
    });

    if (dictionaryData.length > 0) {
      dictionarySheet.getRange(2, 1, dictionaryData.length, 4).setValues(dictionaryData);
    }
}
