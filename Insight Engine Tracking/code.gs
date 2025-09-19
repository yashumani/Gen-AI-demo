// Global constants
const LOG_SHEET_NAME = "Usage Log";
const NEWS_SHEET_NAME = "News Headlines"; // Add news sheet name

// NEW: Usage tracking configuration
const USAGE_METRICS_SHEET_NAME = "Usage_Metrics";
const USAGE_SUMMARY_SHEET_NAME = "Usage_Summary";

// NEW: Prompt Generator Integration Constants
const PROMPT_GENERATION_SHEET_NAME = "Prompt_Generation_Log";

/**
 * CENTRALIZED REPORT CONFIGURATION
 * Single source of truth for all report types
 * Each key is a unique report identifier with pattern matching and template file name
 * Templates should be uploaded to Google Drive with these exact file names
 */
const REPORT_CONFIG = {
  'NEGATIVE_GA': {
    pattern: /Negative GA/i,
    templateFileName: 'template-negative-ga.html',
    displayName: 'Negative GA Report'
  },
  'INFLOW_OUTFLOW': {
    pattern: /Inflow.*Outflow|Port.*Activity/i,
    templateFileName: 'template-inflow-outflow.html',
    displayName: 'Inflow and Outflow Report'
  },
  'SALES_PERFORMANCE': {
    pattern: /Sales.*Performance|Revenue.*Report/i,
    templateFileName: 'template-sales-performance.html',
    displayName: 'Sales Performance Report'
  },
  'EXECUTIVE_SUMMARY': {
    pattern: /Executive.*Summary|Management.*Report/i,
    templateFileName: 'template-executive-summary.html',
    displayName: 'Executive Summary Report'
  },
  'DEFAULT': {
    pattern: /.*/,  // Catch-all pattern
    templateFileName: 'template-default.html',
    displayName: 'Standard Report'
  }
};

/**
 * Main function to handle GET requests to the web app.
 * @param {Object} e The event parameter containing URL query parameters.
 * @return {HtmlOutput} An HTML service output for the welcome or error page.
 */
function doGet(e) {
  // Handle special actions first
  const action = e.parameter.action || "";
  if (action === 'test') {
    return handleTestAction(e);
  }
  if (action === 'simple_test') {
    return handleSimpleTestAction(e);
  }
  if (action === 'debug_template') {
    return testTemplateLoading();
  }
  if (action === 'template_test') {
    return testTemplateLoadingSimple();
  }
  if (action === 'diagnostic') {
    return handleDiagnosticAction(e);
  }
  
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(LOG_SHEET_NAME);

  // Create the log sheet if it doesn't exist
  if (!sheet) {
    sheet = ss.insertSheet(LOG_SHEET_NAME);
    sheet.appendRow(["Timestamp", "File ID", "File Name", "User Email", "Action", "Error Details", "User Agent", "Recent Activities Count", "Last Activity"]);
    sheet.setFrozenRows(1);
  }

  // NEW: Support for different view modes
  const viewMode = e.parameter.view || 'simple'; // 'simple' or 'dashboard'
  
  let fileId = e.parameter.id || "";
  // Support multiple URL parameter names for flexibility
  const fileUrlParam = e.parameter.fileUrl || e.parameter.url || e.parameter.file || e.parameter.URL || "";
  const userEmail = Session.getActiveUser().getEmail();
  
  // Initialize fileName early to avoid ReferenceError in catch block
  let fileName = "Unknown File";

  // Extract file ID from a full URL if provided 
  if (fileUrlParam && !fileId) {
    fileId = extractFileIdFromUrl(fileUrlParam);
  }

  let finalFileUrl = fileUrlParam || (fileId ? `https://drive.google.com/file/d/${fileId}/view` : "");
  
  // Convert to a format that opens directly in Google Drive for editing/viewing
  if (finalFileUrl && fileId) {
    // For better compatibility, use the open format which redirects to the appropriate app
    finalFileUrl = `https://drive.google.com/open?id=${fileId}`;
  }

  try {
    // Enhanced validation with user-friendly errors
    if (!fileId && !fileUrlParam) {
      const currentUrl = ScriptApp.getService().getUrl();
      const helpMessage = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Insight Engine - File URL Required</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { 
                    font-family: "Segoe UI", Arial, sans-serif; 
                    line-height: 1.6; 
                    margin: 0; 
                    padding: 20px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }
                .container { 
                    max-width: 700px; 
                    margin: 0 auto; 
                    background: white; 
                    border-radius: 12px; 
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    overflow: hidden;
                }
                .header { 
                    background: #2c3e50; 
                    color: white; 
                    padding: 30px; 
                    text-align: center; 
                }
                .content { padding: 30px; }
                .code-block { 
                    background: #f8f9fa; 
                    padding: 12px; 
                    border-radius: 6px; 
                    border-left: 4px solid #007cba; 
                    font-family: 'Courier New', monospace; 
                    margin: 10px 0;
                    word-break: break-all;
                }
                .example-box { 
                    background: #e8f5e8; 
                    padding: 20px; 
                    border-radius: 8px; 
                    margin: 20px 0;
                    border-left: 4px solid #28a745;
                }
                .step { 
                    background: #fff3cd; 
                    padding: 15px; 
                    border-radius: 8px; 
                    margin: 15px 0;
                    border-left: 4px solid #ffc107;
                }
                .button { 
                    display: inline-block; 
                    padding: 12px 24px; 
                    background: #007cba; 
                    color: white; 
                    text-decoration: none; 
                    border-radius: 6px; 
                    margin: 10px 5px;
                }
                .button:hover { background: #005a87; }
                ul li { margin: 8px 0; }
                h3 { color: #2c3e50; margin-top: 30px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔗 File URL Required</h1>
                    <p>To access your document through the Insight Engine, please provide a Google Drive file URL</p>
                </div>
                
                <div class="content">
                    <h3>🎯 Quick Setup Guide</h3>
                    
                    <div class="step">
                        <strong>Step 1:</strong> Get your Google Drive file's sharing URL<br>
                        <small>Right-click your file in Google Drive → Get link → Copy link</small>
                    </div>
                    
                    <div class="step">
                        <strong>Step 2:</strong> Add it as a URL parameter<br>
                        <small>Append your file URL to the webapp URL using one of the parameter names below</small>
                    </div>
                    
                    <h3>📝 Supported URL Parameter Formats</h3>
                    <ul>
                        <li><code>?URL=YOUR_GOOGLE_DRIVE_URL</code></li>
                        <li><code>?fileUrl=YOUR_GOOGLE_DRIVE_URL</code></li>
                        <li><code>?url=YOUR_GOOGLE_DRIVE_URL</code></li>
                        <li><code>?file=YOUR_GOOGLE_DRIVE_URL</code></li>
                    </ul>
                    
                    <h3>💡 Complete Example</h3>
                    <div class="example-box">
                        <strong>If your webapp URL is:</strong><br>
                        <div class="code-block">${currentUrl}</div>
                        
                        <strong>And your Google Drive file URL is:</strong><br>
                        <div class="code-block">https://drive.google.com/file/d/1ABC123XYZ/view?usp=sharing</div>
                        
                        <strong>Then your complete URL should be:</strong><br>
                        <div class="code-block">${currentUrl}?URL=https://drive.google.com/file/d/1ABC123XYZ/view?usp=sharing</div>
                    </div>
                    
                    <h3>✅ Supported Google Drive File Types</h3>
                    <ul>
                        <li>📄 Google Docs, Sheets, and Slides</li>
                        <li>📊 PDF Documents</li>
                        <li>📈 Excel Files (.xlsx, .xls)</li>
                        <li>📝 Word Documents (.docx, .doc)</li>
                        <li>🖼️ Images and other files</li>
                    </ul>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="mailto:support@yourcompany.com" class="button">📞 Contact Support</a>
                        <a href="${currentUrl}?URL=PASTE_YOUR_DRIVE_URL_HERE" class="button">🔧 Try with Sample URL</a>
                    </div>
                    
                    <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; font-size: 14px; color: #666;">
                        <strong>� Privacy Note:</strong> Your file URL is only used to access and display your document. We don't store or share your Google Drive files.
                    </div>
                </div>
            </div>
        </body>
        </html>
      `;
      
      return HtmlService.createHtmlOutput(helpMessage)
        .setTitle("Insight Engine - File URL Required")
        .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
    }

    // PERFORMANCE OPTIMIZATION: Read log data only once
    const logData = sheet.getDataRange().getValues();

    // Enhanced file validation
    let file;
    fileName = "Unknown File";  // Re-assign, don't re-declare
    
    try {
      file = DriveApp.getFileById(fileId);
      fileName = file.getName();
    } catch (fileError) {
      throw new Error(`File not accessible (ID: ${fileId}). Please check: 1) File exists, 2) You have access permissions, 3) File ID is correct. Error: ${fileError.message}`);
    }

    // Log the initial page view for admin tracking
    logAccessWithActivity(sheet, logData, fileId, fileName, userEmail, "page_view");
    
    // NEW: Identify report type based on filename
    const reportConfig = getReportConfig(fileName);
    console.log(`Report config identified:`, reportConfig);
    
    // NEW: Load the specific "What's Inside" template from Google Drive
    let whatsInsideHtml = '';
    try {
      whatsInsideHtml = loadTemplateFromDrive(reportConfig.templateFileName);
    } catch (templateError) {
      console.error('Template loading failed:', templateError);
      whatsInsideHtml = loadTemplateFromDrive(''); // This will trigger the fallback error template
    }
    
    // Get user-facing document details
    const documentDetails = getUserFacingDocumentDetails(fileId, file);
    
    // Generate multiple URL formats for better compatibility
    const fileUrls = generateFileUrls(fileId, file);
    
    // Enhanced template data with report-specific content
    const templateData = {
      DOCUMENT_NAME: fileName || 'Executive Report Document',
      DOCUMENT_TYPE: documentDetails.documentType || 'Executive Report',
      LAST_MODIFIED: documentDetails.lastModified || new Date().toLocaleDateString(),
      FILE_OWNER: documentDetails.fileOwner || 'Document Owner',
      FILE_ID: fileId,
      FILE_URL: finalFileUrl,
      FILE_URL_DIRECT: fileUrls.direct,
      FILE_URL_VIEW: fileUrls.view,
      FILE_URL_EDIT: fileUrls.edit || finalFileUrl,
      FILE_URL_PREVIEW: fileUrls.preview,
      VIEW_MODE: viewMode, // Pass view mode to template
      TIMESTAMP: new Date().toLocaleString(),
      // NEW: Report-specific data
      REPORT_TYPE: reportConfig.displayName,
      REPORT_CONFIG_KEY: reportConfig.configKey,
      WHATS_INSIDE_HTML: whatsInsideHtml  // Inject the dynamic template content
    };

    // Load and render the appropriate template based on view mode
    // For now, both view modes use the same template (welcome-template)
    const templateName = 'welcome-template';
    const htmlContent = loadTemplateSimple(templateName, templateData);
    
    return HtmlService.createHtmlOutput(htmlContent)
      .setTitle(`Document Access Portal - ${documentDetails.documentType}`)
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL); // Allow embedding

  } catch (err) {
    // For error logging
    logAccessWithActivity(sheet, null, fileId, fileName, userEmail, "page_view", err.message);

    // Enhanced error template with troubleshooting
    const errorTemplateData = {
      ERROR_MESSAGE: err.message,
      FILE_ID: fileId,
      ORIGINAL_URL: fileUrlParam,
      TROUBLESHOOTING_STEPS: generateTroubleshootingSteps(err.message, fileId, fileUrlParam),
      TIMESTAMP: new Date().toLocaleString()
    };
    
    const errorHtmlContent = loadTemplateSimple('error-template', errorTemplateData);
    return HtmlService.createHtmlOutput(errorHtmlContent).setTitle("Document Access Error");
  }
}

/**
 * Server-side function called by the welcome page's button to log the click event.
 * @param {string} fileId The Google Drive file ID.
 * @param {string} action The action being recorded.
 * @return {string} A success or error message.
 */
function recordButtonClick(fileId, action) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(LOG_SHEET_NAME);
    const userEmail = Session.getActiveUser().getEmail();
    let fileName = "File Name Not Found";
    
    try {
      fileName = DriveApp.getFileById(fileId).getName();
    } catch (e) { /* Silently fail */ }
    
    // For button clicks, we don't need to read existing log data
    // since we're just appending a new entry
    logAccessWithActivity(sheet, null, fileId, fileName, userEmail, action);
    return "SUCCESS";
  } catch (error) {
    return "ERROR: " + error.message;
  }
}

/**
 * Loads an HTML template file from Google Drive and injects data.
 * @param {string} templateName The name of the HTML file (e.g., "welcome-template").
 * @param {Object} data The data object with placeholders and their values.
 * @return {string} The processed HTML content.
 */
function loadTemplate(templateName, data) {
  try {
    // Load HTML template from Apps Script project files
    let htmlContent;
    
    try {
      // Try to get the HTML file from the Apps Script project
      const template = HtmlService.createTemplateFromFile(templateName);
      
      // For Apps Script template system, we need to set properties
      for (const key in data) {
        template[key] = data[key];
      }
      
      // Evaluate the template with Apps Script's built-in template system
      htmlContent = template.evaluate().getContent();
      
    } catch (htmlServiceError) {
      // Fallback: Try to read as plain HTML file and do manual replacement
      const fileBlob = DriveApp.getFilesByName(templateName + '.html');
      if (fileBlob.hasNext()) {
        htmlContent = fileBlob.next().getBlob().getDataAsString();
      } else {
        throw new Error(`Template file "${templateName}.html" not found in project or Drive`);
      }
    }
    
    // Manual replacement for both methods (to ensure {{TEMPLATE_DATA_JSON}} is replaced)
    const templateDataJson = JSON.stringify(data, null, 2);
    htmlContent = htmlContent.replace(/\{\{TEMPLATE_DATA_JSON\}\}/g, templateDataJson);
    
    // Manual replacement for other placeholders (as fallback)
    for (const key in data) {
      const placeholder = new RegExp('{{' + key + '}}', 'g');
      const replacementValue = data[key] || '';
      htmlContent = htmlContent.replace(placeholder, replacementValue);
    }
    
    // Verify critical placeholders were replaced
    const remainingCriticalPlaceholders = htmlContent.match(/\{\{(FILE_URL|TEMPLATE_DATA_JSON|DOCUMENT_NAME|DOCUMENT_TYPE|LAST_MODIFIED|TIMESTAMP)\}\}/g);
    if (remainingCriticalPlaceholders) {
      // In production, we'll use fallback values instead of throwing errors
      htmlContent = htmlContent.replace(/\{\{TEMPLATE_DATA_JSON\}\}/g, 'null');
      htmlContent = htmlContent.replace(/\{\{FILE_URL\}\}/g, '');
      htmlContent = htmlContent.replace(/\{\{DOCUMENT_NAME\}\}/g, 'Executive Report Document');
      htmlContent = htmlContent.replace(/\{\{DOCUMENT_TYPE\}\}/g, 'Executive Report');
      htmlContent = htmlContent.replace(/\{\{LAST_MODIFIED\}\}/g, new Date().toLocaleDateString());
      htmlContent = htmlContent.replace(/\{\{TIMESTAMP\}\}/g, new Date().toLocaleString());
    }
    
    return htmlContent;
    
  } catch (error) {
    console.error('Template loading error:', error);
    return `<html><body><h1>Template Error</h1><p>Could not load template "${templateName}": ${error.message}</p><p>Available data: ${JSON.stringify(data, null, 2)}</p></body></html>`;
  }
}

/**
 * PRODUCTION VERSION - Loads and processes an HTML template with data substitution
 * Fixed template data injection for reliable production use
 * @param {string} templateName The name of the template
 * @param {Object} data The data to inject
 * @return {string} The processed HTML content
 */
function loadTemplateSimple(templateName, data) {
  try {
    console.log(`🔄 Loading template: ${templateName}`);
    console.log(`🔄 Template data:`, data);

    // Load the template as raw HTML content
    const template = HtmlService.createTemplateFromFile(templateName);
    let htmlContent = template.evaluate().getContent();

    console.log(`🔄 Template loaded, size: ${htmlContent.length} characters`);

    // Replace the {{TEMPLATE_DATA_JSON}} placeholder with actual JSON data
    const templateDataJson = JSON.stringify(data, null, 2);
    console.log(`🔄 Generated JSON data: ${templateDataJson.substring(0, 200)}...`);

    // FIXED: Corrected regex pattern - the original had extra escaping
    // Look for the exact pattern: eval('window.templateData = {{TEMPLATE_DATA_JSON}};');
    const evalPattern = /eval\('window\.templateData\s*=\s*\{\{TEMPLATE_DATA_JSON\}\};'\);/g;

    // Check if the pattern exists
    const evalMatches = (htmlContent.match(evalPattern) || []).length;
    console.log(`🔄 Found ${evalMatches} eval patterns to replace`);

    if (evalMatches > 0) {
      // Replace the eval statement with direct assignment
      const evalReplacement = `window.templateData = ${templateDataJson};`;
      console.log('🔄 Replacing eval pattern with template data');
      htmlContent = htmlContent.replace(evalPattern, evalReplacement);
      console.log('✅ Eval pattern replacement completed');
    } else {
      console.warn('⚠️ No eval patterns found - checking for standalone placeholders');
    }

    // ALSO handle standalone {{TEMPLATE_DATA_JSON}} placeholders
    const standalonePattern = /\{\{TEMPLATE_DATA_JSON\}\}/g;
    const standaloneMatches = (htmlContent.match(standalonePattern) || []).length;
    console.log(`🔄 Found ${standaloneMatches} standalone {{TEMPLATE_DATA_JSON}} placeholders`);

    if (standaloneMatches > 0) {
      htmlContent = htmlContent.replace(standalonePattern, templateDataJson);
      console.log('✅ Standalone placeholder replacement completed');
    }

    // Replace any other simple placeholders like {{FILE_NAME}}, {{FILE_URL}}, etc.
    let simpleReplacements = 0;
    for (const key in data) {
      const placeholder = new RegExp(`\\{\\{${key}\\}\\}`, 'g');
      const value = data[key];
      const matches = (htmlContent.match(placeholder) || []).length;

      if (matches > 0) {
        simpleReplacements += matches;
        if (typeof value === 'string') {
          // Escape HTML special characters to prevent issues
          const escapedValue = value.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
          htmlContent = htmlContent.replace(placeholder, escapedValue || '');
        } else {
          htmlContent = htmlContent.replace(placeholder, value || '');
        }
        console.log(`🔄 Replaced ${matches} instances of {{${key}}}`);
      }
    }

    console.log(`✅ Template processing completed. ${simpleReplacements} simple replacements made`);
    console.log(`✅ Final template size: ${htmlContent.length} characters`);

    // Final check: ensure no placeholders remain
    const remainingPlaceholders = (htmlContent.match(/\{\{[^}]+\}\}/g) || []).length;
    if (remainingPlaceholders > 0) {
      console.warn(`⚠️ ${remainingPlaceholders} placeholders still remain in template`);
    } else {
      console.log(`✅ All placeholders successfully replaced`);
    }

    return htmlContent;

  } catch (error) {
    console.error(`❌ Template loading failed for ${templateName}:`, error);
    console.error(`❌ Error stack:`, error.stack);

    // Return a simple fallback HTML template
    return generateFallbackTemplate(templateName, data, error.message);
  }
}

/**
 * Generate a fallback template when the main template fails to load
 * @param {string} templateName The name of the failed template
 * @param {Object} data The data that was supposed to be injected
 * @param {string} errorMessage The error message
 * @return {string} Fallback HTML content
 */
function generateFallbackTemplate(templateName, data, errorMessage) {
  const isErrorTemplate = templateName === 'error-template';
  
  if (isErrorTemplate) {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <title>System Error</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
          .container { max-width: 600px; margin: 0 auto; }
          .error { background: #fee; padding: 20px; border-radius: 8px; border-left: 4px solid #e44; }
          .code { background: #f5f5f5; padding: 10px; font-family: monospace; border-radius: 4px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="error">
            <h2>⚠️ System Error</h2>
            <p><strong>Error:</strong> ${data.ERROR_MESSAGE || 'Unknown error occurred'}</p>
            <p><strong>Template Loading Error:</strong> ${errorMessage}</p>
            <p><strong>File ID:</strong> ${data.FILE_ID || 'Not provided'}</p>
            <p><strong>Timestamp:</strong> ${data.TIMESTAMP || new Date().toLocaleString()}</p>
          </div>
          <div style="margin-top: 30px;">
            <h3>Troubleshooting Steps:</h3>
            <ol>
              <li>Check that template files are uploaded to the Apps Script project</li>
              <li>Verify file permissions and access</li>
              <li>Contact your system administrator</li>
            </ol>
          </div>
        </div>
      </body>
      </html>
    `;
  } else {
    // Fallback for welcome template
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Document Access Portal</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          body { 
            font-family: "Segoe UI", Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
          }
          .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 12px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
          }
          .header { 
            background: #2c3e50; 
            color: white; 
            padding: 30px; 
            text-align: center; 
          }
          .content { padding: 30px; }
          .access-btn {
            display: inline-block;
            padding: 15px 30px;
            background: #007cba;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-size: 16px;
            margin: 10px;
            border: none;
            cursor: pointer;
            transition: background 0.3s;
          }
          .access-btn:hover { background: #005a87; }
          .warning { 
            background: #fff3cd; 
            padding: 15px; 
            border-radius: 8px; 
            border-left: 4px solid #ffc107; 
            margin: 20px 0;
          }
        </style>
        <script>
          window.templateData = ${JSON.stringify(data, null, 2)};
          
          function accessDocument() {
            const fileUrl = window.templateData.FILE_URL || window.templateData.FILE_URL_DIRECT;
            if (fileUrl) {
              window.open(fileUrl, '_blank');
            } else {
              alert('No file URL available');
            }
          }
        </script>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>📄 Document Access Portal</h1>
            <p>Fallback template (original template failed to load)</p>
          </div>
          
          <div class="content">
            <div class="warning">
              <strong>⚠️ Template System Notice:</strong> The custom template failed to load (${errorMessage}). Using fallback display.
            </div>
            
            <h2>${data.DOCUMENT_NAME || 'Document'}</h2>
            <p><strong>Type:</strong> ${data.DOCUMENT_TYPE || 'Unknown'}</p>
            <p><strong>Last Modified:</strong> ${data.LAST_MODIFIED || 'Unknown'}</p>
            <p><strong>Owner:</strong> ${data.FILE_OWNER || 'Unknown'}</p>
            
            <div style="text-align: center; margin: 30px 0;">
              <button onclick="accessDocument()" class="access-btn">
                📄 Open Document
              </button>
            </div>
            
            ${data.WHATS_INSIDE_HTML || '<p>This document contains important business information.</p>'}
            
            <div style="margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 8px; font-size: 14px;">
              <strong>Debug Information:</strong><br>
              Report Type: ${data.REPORT_TYPE || 'Unknown'}<br>
              Template Error: ${errorMessage}<br>
              Timestamp: ${data.TIMESTAMP || 'Unknown'}
            </div>
          </div>
        </div>
      </body>
      </html>
    `;
  }
}

/**
 * Extracts file ID from a Google Drive URL.
 * @param {string} url The Google Drive URL.
 * @return {string} The extracted file ID or empty string if not found.
 */
function extractFileIdFromUrl(url) {
  try {
    const patterns = [
      /\/file\/d\/([a-zA-Z0-9-_]+)/,
      /id=([a-zA-Z0-9-_]+)/,
      /\/d\/([a-zA-Z0-9-_]+)/
    ];
    
    for (const pattern of patterns) {
      const match = url.match(pattern);
      if (match) {
        return match[1];
      }
    }
    return "";
  } catch (error) {
    return "";
  }
}

/**
 * Generates multiple URL formats for better Google Drive file compatibility
 * @param {string} fileId - The Google Drive file ID
 * @param {DriveApp.File} file - The Google Drive file object
 * @return {Object} Object containing different URL formats
 */
function generateFileUrls(fileId, file) {
  try {
    return {
      direct: `https://drive.google.com/file/d/${fileId}/view?usp=sharing`,
      view: `https://drive.google.com/file/d/${fileId}/view`,
      edit: `https://drive.google.com/file/d/${fileId}/edit`,
      preview: `https://drive.google.com/file/d/${fileId}/preview`,
      download: `https://drive.google.com/uc?id=${fileId}`,
      open: `https://drive.google.com/open?id=${fileId}`
    };
  } catch (error) {
    console.error('Error generating file URLs:', error);
    // Return basic URLs as fallback
    return {
      direct: `https://drive.google.com/file/d/${fileId}/view`,
      view: `https://drive.google.com/file/d/${fileId}/view`,
      edit: `https://drive.google.com/file/d/${fileId}/edit`,
      preview: `https://drive.google.com/file/d/${fileId}/view`,
      download: `https://drive.google.com/file/d/${fileId}/view`,
      open: `https://drive.google.com/file/d/${fileId}/view`
    };
  }
}

/**
 * Generates troubleshooting steps based on the error message and context
 * @param {string} errorMessage - The error message that occurred
 * @param {string} fileId - The file ID that caused the error
 * @param {string} originalUrl - The original URL parameter provided
 * @return {string} HTML formatted troubleshooting steps
 */
function generateTroubleshootingSteps(errorMessage, fileId, originalUrl) {
  try {
    let troubleshootingHtml = '<div class="troubleshooting-steps">';
    
    // Determine error type and provide specific guidance
    if (errorMessage.includes("File not accessible")) {
      troubleshootingHtml += `
        <h4>🔧 File Access Issues</h4>
        <ol>
          <li><strong>Check File Permissions:</strong>
            <ul>
              <li>Open the file directly in Google Drive</li>
              <li>Verify you have "View" or "Edit" access</li>
              <li>Ask the file owner to share it with you</li>
            </ul>
          </li>
          <li><strong>Verify File Status:</strong>
            <ul>
              <li>Ensure the file hasn't been deleted or moved</li>
              <li>Check if the file is in the Trash</li>
            </ul>
          </li>
          <li><strong>Try Alternative Access:</strong>
            <ul>
              <li>Request "Editor" access if you only have "Viewer"</li>
              <li>Ask for a new sharing link from the owner</li>
            </ul>
          </li>
        </ol>
      `;
    } else if (errorMessage.includes("not found") || errorMessage.includes("does not exist")) {
      troubleshootingHtml += `
        <h4>📂 File Not Found</h4>
        <ol>
          <li><strong>Verify File URL:</strong>
            <ul>
              <li>Double-check the Google Drive URL is correct</li>
              <li>Ensure no extra characters or truncation</li>
              <li>Try copying the link again from Google Drive</li>
            </ul>
          </li>
          <li><strong>Check File ID:</strong>
            <ul>
              <li>File ID detected: <code>${fileId || 'None detected'}</code></li>
              <li>Original URL: <code>${originalUrl || 'None provided'}</code></li>
            </ul>
          </li>
          <li><strong>Alternative Solutions:</strong>
            <ul>
              <li>Try accessing the file directly in Google Drive first</li>
              <li>Get a fresh sharing link from the file owner</li>
            </ul>
          </li>
        </ol>
      `;
    } else if (errorMessage.includes("Template")) {
      troubleshootingHtml += `
        <h4>📄 Template Loading Issues</h4>
        <ol>
          <li><strong>Template System:</strong>
            <ul>
              <li>The system is loading report-specific content</li>
              <li>Some templates may need to be uploaded by the administrator</li>
              <li>Default content will be shown if custom templates aren't available</li>
            </ul>
          </li>
          <li><strong>Contact Support:</strong>
            <ul>
              <li>Report this issue to your system administrator</li>
              <li>Provide the file name and error details</li>
            </ul>
          </li>
        </ol>
      `;
    } else {
      // Generic troubleshooting for unknown errors
      troubleshootingHtml += `
        <h4>⚙️ General Troubleshooting</h4>
        <ol>
          <li><strong>Basic Checks:</strong>
            <ul>
              <li>Refresh the page and try again</li>
              <li>Clear your browser cache and cookies</li>
              <li>Try using a different browser or incognito mode</li>
            </ul>
          </li>
          <li><strong>URL Verification:</strong>
            <ul>
              <li>Ensure the Google Drive URL is complete and correct</li>
              <li>Try different URL parameter formats (URL, fileUrl, url, file)</li>
            </ul>
          </li>
          <li><strong>Network & Access:</strong>
            <ul>
              <li>Check your internet connection</li>
              <li>Verify you're logged into the correct Google account</li>
              <li>Try accessing Google Drive directly first</li>
            </ul>
          </li>
        </ol>
      `;
    }
    
    // Add common footer with support information
    troubleshootingHtml += `
      <div class="support-info" style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
        <h5>📞 Need Additional Help?</h5>
        <p>If these steps don't resolve the issue:</p>
        <ul>
          <li>Contact your system administrator</li>
          <li>Provide the complete error message and file URL</li>
          <li>Include your browser type and version</li>
        </ul>
        <p><strong>Error Details:</strong> ${errorMessage}</p>
        <p><strong>File ID:</strong> ${fileId || 'Not detected'}</p>
        <p><strong>Original URL:</strong> ${originalUrl || 'Not provided'}</p>
      </div>
    `;
    
    troubleshootingHtml += '</div>';
    
    return troubleshootingHtml;
    
  } catch (error) {
    console.error('Error generating troubleshooting steps:', error);
    return `
      <div class="troubleshooting-error">
        <h4>❌ Troubleshooting Guide Error</h4>
        <p>Unable to generate specific troubleshooting steps.</p>
        <p><strong>Original Error:</strong> ${errorMessage}</p>
        <p><strong>Please contact support for assistance.</strong></p>
      </div>
    `;
  }
}

/**
 * Get user-facing document details (no tracking metrics)
 * @param {string} fileId - The file ID
 * @param {DriveApp.File} file - The file object
 * @return {Object} User-facing document details
 */
function getUserFacingDocumentDetails(fileId, file) {
  var details = {
    documentType: 'Document',
    lastModified: 'Unknown',
    fileOwner: 'Unknown'
  };
  
  try {
    // Get file type from MIME type
    var mimeType = file.getMimeType();
    if (mimeType.includes('spreadsheet')) {
      details.documentType = 'Spreadsheet';
    } else if (mimeType.includes('presentation')) {
      details.documentType = 'Presentation';
    } else if (mimeType.includes('document')) {
      details.documentType = 'Document';
    } else if (mimeType.includes('pdf')) {
      details.documentType = 'PDF Document';
    } else {
      details.documentType = 'File';
    }
    
    // Get last modified date
    var lastModified = file.getLastUpdated();
    if (lastModified) {
      details.lastModified = Utilities.formatDate(lastModified, Session.getScriptTimeZone(), 'MMM dd, yyyy');
    }
    
    // Get file owner
    try {
      var owner = file.getOwner();
      if (owner) {
        details.fileOwner = owner.getName() || owner.getEmail();
      }
    } catch (ownerError) {
      details.fileOwner = 'Access Limited';
    }
    
  } catch (error) {
    // Silent error handling for production
  }
  
  return details;
}

/**
 * Gets document insights including type, modification date, and access statistics.
 * @param {string} fileId The Google Drive file ID.
 * @param {DriveApp.File} file The Google Drive file object.
 * @return {Object} An object containing document insights.
 */
function getDocumentInsights(fileId, file) {
  try {
    const mimeType = file.getMimeType();
    const lastModified = file.getLastUpdated();
    
    // Determine document type based on MIME type
    let documentType = "Document";
    if (mimeType.includes('spreadsheet')) {
      documentType = "Spreadsheet";
    } else if (mimeType.includes('presentation')) {
      documentType = "Presentation";
    } else if (mimeType.includes('document')) {
      documentType = "Document";
    } else if (mimeType.includes('pdf')) {
      documentType = "PDF";
    } else if (mimeType.includes('image')) {
      documentType = "Image";
    }

    // Get access count from usage log
    const accessCount = getAccessCount(fileId);
    
    // Get recent activities count (last 7 days)
    const recentActivities = getRecentActivitiesCount(fileId, 7);
    
    return {
      documentType: documentType,
      lastModified: lastModified.toLocaleDateString(),
      accessCount: accessCount,
      recentActivities: recentActivities
    };
  } catch (error) {
    console.error('Error getting document insights: ' + error.toString());
    return {
      documentType: "Unknown",
      lastModified: "Unknown",
      accessCount: 0,
      recentActivities: 0
    };
  }
}

/**
 * Logs access with activity tracking.
 * @param {Sheet} sheet The logging sheet.
 * @param {Array} logData The existing log data (null for button clicks to skip calculations).
 * @param {string} fileId The file ID.
 * @param {string} fileName The file name.
 * @param {string} userEmail The user's email.
 * @param {string} action The action performed.
 * @param {string} errorDetails Optional error details.
 */
function logAccessWithActivity(sheet, logData, fileId, fileName, userEmail, action, errorDetails = "") {
  try {
    const timestamp = new Date();
    const userAgent = "Google Apps Script";
    
    // Only calculate these for page views (when logData is provided)
    // Skip expensive calculations for button clicks
    let recentActivitiesCount = 0;
    let lastActivity = "First visit";
    
    if (logData) {
      recentActivitiesCount = getRecentActivitiesCount(fileId, 7, logData);
      lastActivity = getLastActivity(fileId, userEmail, logData);
    }
    
    sheet.appendRow([
      timestamp,
      fileId,
      fileName,
      userEmail,
      action,
      errorDetails,
      userAgent,
      recentActivitiesCount,
      lastActivity
    ]);
  } catch (error) {
    // Silent error handling for production
  }
}

/**
 * Gets the total access count for a file.
 * @param {string} fileId The file ID.
 * @param {Array} data The log data array (optional, reads from sheet if not provided).
 * @return {number} The total access count.
 */
function getAccessCount(fileId, data = null) {
  try {
    // If data is not provided, read from sheet (fallback for legacy calls)
    if (!data) {
      const ss = SpreadsheetApp.getActiveSpreadsheet();
      const sheet = ss.getSheetByName(LOG_SHEET_NAME);
      if (!sheet) return 0;
      data = sheet.getDataRange().getValues();
    }
    
    let count = 0;
    for (let i = 1; i < data.length; i++) {
      if (data[i][1] === fileId) { // File ID is in column B (index 1)
        count++;
      }
    }
    
    return count;
  } catch (error) {
    console.error('Error getting access count: ' + error.toString());
    return 0;
  }
}

/**
 * Gets the count of recent activities for a file within specified days.
 * @param {string} fileId The file ID.
 * @param {number} days The number of days to look back.
 * @param {Array} data The log data array (optional, reads from sheet if not provided).
 * @return {number} The count of recent activities.
 */
function getRecentActivitiesCount(fileId, days, data = null) {
  try {
    // If data is not provided, read from sheet (fallback for legacy calls)
    if (!data) {
      const ss = SpreadsheetApp.getActiveSpreadsheet();
      const sheet = ss.getSheetByName(LOG_SHEET_NAME);
      if (!sheet) return 0;
      data = sheet.getDataRange().getValues();
    }
    
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    
    let count = 0;
    
    for (let i = 1; i < data.length; i++) {
      if (data[i][1] === fileId && new Date(data[i][0]) >= cutoffDate) {
        count++;
      }
    }
    
    return count;
  } catch (error) {
    console.error('Error getting recent activities count: ' + error.toString());
    return 0;
  }
}

/**
 * Gets the last activity timestamp for a user and file.
 * @param {string} fileId The file ID.
 * @param {string} userEmail The user's email.
 * @param {Array} data The log data array (optional, reads from sheet if not provided).
 * @return {string} The last activity timestamp or "First visit".
 */
function getLastActivity(fileId, userEmail, data = null) {
  try {
    // If data is not provided, read from sheet (fallback for legacy calls)
    if (!data) {
      const ss = SpreadsheetApp.getActiveSpreadsheet();
      const sheet = ss.getSheetByName(LOG_SHEET_NAME);
      if (!sheet) return "First visit";
      data = sheet.getDataRange().getValues();
    }
    
    let lastActivity = null;
    
    for (let i = data.length - 1; i >= 1; i--) {
      if (data[i][1] === fileId && data[i][3] === userEmail) {
        lastActivity = new Date(data[i][0]);
        break;
      }
    }
    
    return lastActivity ? lastActivity.toLocaleString() : "First visit";
  } catch (error) {
    console.error('Error getting last activity: ' + error.toString());
    return "Unknown";
  }
}

/**
 * Fetches news headlines from the Verizon Daily Newsletter Google Sheet
 * @return {Array} Array of news objects with title, summary, date, and source
 */
function getNewsHeadlines() {
  try {
    // External Google Sheet ID for Verizon Daily Newsletter
    const NEWSLETTER_SHEET_ID = "1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM";
    const NEWSLETTER_TAB_NAME = "Verizon Daily Newsletter";
    
    // Open the external spreadsheet
    const newsletterSpreadsheet = SpreadsheetApp.openById(NEWSLETTER_SHEET_ID);
    const newsletterSheet = newsletterSpreadsheet.getSheetByName(NEWSLETTER_TAB_NAME);
    
    if (!newsletterSheet) {
      console.error("Newsletter sheet not found");
      return [];
    }
    
    const data = newsletterSheet.getDataRange().getValues();
    const newsItems = [];
    
    // Process each row (skip header)
    for (let i = 1; i < Math.min(data.length, 6); i++) { // Limit to 5 most recent newsletters
      const row = data[i];
      
      // Column E (index 4) contains the Email Body
      const emailBody = row[4] ? row[4].toString() : "";
      const timestamp = row[0] ? new Date(row[0]) : new Date();
      
      if (emailBody) {
        // Parse the email body to extract headlines
        const headlines = parseNewsletterContent(emailBody, timestamp);
        newsItems.push(...headlines);
      }
    }
    
    // Return the most recent 8 headlines
    return newsItems.slice(0, 8);
    
  } catch (error) {
    console.error("Error fetching news headlines:", error);
    // Return error message instead of sample data
    return getFallbackNewsHeadlines();
  }
}

/**
 * Parses the newsletter email body to extract individual headlines
 * @param {string} emailBody The email body content
 * @param {Date} timestamp The newsletter timestamp
 * @return {Array} Array of parsed news items
 */
function parseNewsletterContent(emailBody, timestamp) {
  const newsItems = [];
  
  try {
    // Split by separator lines to get individual articles
    const sections = emailBody.split(/[-]{10,}/);
    
    for (const section of sections) {
      if (section.trim() && !section.includes("Web Version") && !section.includes("This email was sent")) {
        const lines = section.trim().split('\n').filter(line => line.trim());
        
        if (lines.length >= 2) {
          // First line is usually the headline
          let title = lines[0].trim();
          
          // Second line often contains source and author
          let source = "Verizon Newsletter";
          let summary = "";
          
          if (lines.length > 1) {
            const sourceLine = lines[1];
            if (sourceLine.includes(" by ")) {
              const parts = sourceLine.split(" by ");
              source = parts[0].trim();
            }
          }
          
          // Extract summary from remaining lines
          if (lines.length > 2) {
            summary = lines.slice(2).join(' ').trim();
            // Keep full summary for expandable view, but create excerpt for preview
            let excerpt = summary;
            if (summary.length > 150) {
              excerpt = summary.substring(0, 150) + "...";
            }
            
            // Clean up title
            title = title.replace(/^[-\s]+/, '').replace(/[-\s]+$/, '');
            
            if (title && title.length > 10) {
              // Store both full and excerpt versions
              newsItems.push({
                title: title,
                summary: excerpt,
                fullStory: summary,
                date: timestamp.toLocaleDateString(),
                source: source
              });
            }
          } else {
            // Clean up title
            title = title.replace(/^[-\s]+/, '').replace(/[-\s]+$/, '');
            
            if (title && title.length > 10) {
              newsItems.push({
                title: title,
                summary: "Click to read more...",
                fullStory: title,
                date: timestamp.toLocaleDateString(),
                source: source
              });
            }
          }
        }
      }
    }
    
  } catch (error) {
    console.error("Error parsing newsletter content:", error);
  }
  
  return newsItems;
}

/**
 * Provides error message when external news sheet is not accessible
 * @return {Array} Array with error message
 */
function getFallbackNewsHeadlines() {
  return [
    {
      title: "News Service Unavailable",
      summary: "Unable to load news headlines from the Verizon Daily Newsletter. Please contact your administrator to resolve this issue.",
      fullStory: "The news service is currently experiencing connectivity issues. This could be due to network problems, permission restrictions, or the external Google Sheet being temporarily unavailable. Please contact your system administrator to diagnose and resolve this issue.",
      date: new Date().toLocaleDateString(),
      source: "System Error"
    }
  ];
}

// ========================================
// NEW: ENHANCED USAGE TRACKING SYSTEM
// ========================================

/**
 * Record comprehensive usage metrics for analytics
 * @param {string} metricType - Type of metric (click, feedback, session_end, page_load)
 * @param {Object} data - Tracking data object
 * @return {Object} Success/failure response
 */
function recordUsageMetrics(metricType, data) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = getOrCreateUsageMetricsSheet(ss);
    
    // Common tracking data
    const timestamp = new Date();
    const userEmail = Session.getActiveUser().getEmail() || 'anonymous';
    const sessionId = data.sessionId || 'unknown';
    
    // Prepare row data based on metric type
    let rowData = [
      timestamp,
      sessionId,
      userEmail,
      metricType,
      data.reportType || 'unknown',
      data.reportDate || 'unknown',
      data.fileName || 'unknown',
      data.clickType || '',
      data.elementId || '',
      data.totalClicks || 0,
      data.sessionDuration || 0,
      data.feedback || '',
      data.pageLoadTime || 0,
      data.userAgent || 'unknown'
    ];
    
    // Add the tracking record
    sheet.appendRow(rowData);
    
    // Update summary statistics
    updateUsageSummaryStats(ss, metricType, data);
    
    return { success: true, message: 'Metrics recorded successfully' };
    
  } catch (error) {
    console.error('Error recording usage metrics:', error);
    return { success: false, error: error.toString() };
  }
}

/**
 * Get or create the usage metrics sheet with proper headers
 * @param {SpreadsheetApp.Spreadsheet} ss - The spreadsheet object
 * @return {SpreadsheetApp.Sheet} The usage metrics sheet
 */
function getOrCreateUsageMetricsSheet(ss) {
  let sheet = ss.getSheetByName(USAGE_METRICS_SHEET_NAME);
  
  if (!sheet) {
    sheet = ss.insertSheet(USAGE_METRICS_SHEET_NAME);
    
    // Set up headers
    const headers = [
      'Timestamp',
      'Session ID', 
      'User Email',
      'Event Type',
      'Report Type',
      'Report Date',
      'File Name',
      'Click Type',
      'Element ID',
      'Total Clicks',
      'Session Duration (ms)',
      'User Feedback',
      'Page Load Time (ms)',
      'User Agent'
    ];
    
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
    
    // Auto-resize columns
    sheet.autoResizeColumns(1, headers.length);
  }
  
  return sheet;
}

/**
 * Get or create the usage summary sheet
 * @param {SpreadsheetApp.Spreadsheet} ss - The spreadsheet object
 * @return {SpreadsheetApp.Sheet} The usage summary sheet
 */
function getOrCreateUsageSummarySheet(ss) {
  let sheet = ss.getSheetByName(USAGE_SUMMARY_SHEET_NAME);
  
  if (!sheet) {
    sheet = ss.insertSheet(USAGE_SUMMARY_SHEET_NAME);
    
    // Set up headers
    const headers = ['Date', 'Metric Type', 'Count', 'Details'];
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
    sheet.autoResizeColumns(1, headers.length);
  }
  
  return sheet;
}

/**
 * Update summary statistics for usage metrics
 * @param {SpreadsheetApp.Spreadsheet} ss - The spreadsheet object
 * @param {string} metricType - Type of metric
 * @param {Object} data - Tracking data
 */
function updateUsageSummaryStats(ss, metricType, data) {
  try {
    const summarySheet = getOrCreateUsageSummarySheet(ss);
    const today = new Date().toDateString();
    
    // Update different counters based on metric type
    switch (metricType) {
      case 'click':
        incrementSummaryCounter(summarySheet, today, 'Total Clicks', '');
        if (data.clickType === 'report_access_button') {
          incrementSummaryCounter(summarySheet, today, 'Report Access Clicks', data.reportType || '');
        } else if (data.clickType === 'prompt_generator_link') {
          incrementSummaryCounter(summarySheet, today, 'Prompt Generator Clicks', '');
        }
        break;
        
      case 'feedback':
        incrementSummaryCounter(summarySheet, today, 'Total Feedback', '');
        if (data.feedback === 'thumbs_up') {
          incrementSummaryCounter(summarySheet, today, 'Thumbs Up', '');
        } else if (data.feedback === 'thumbs_down') {
          incrementSummaryCounter(summarySheet, today, 'Thumbs Down', '');
        }
        break;
        
      case 'session_end':
        incrementSummaryCounter(summarySheet, today, 'Total Sessions', '');
        updateAverageMetric(summarySheet, today, 'Average Session Duration', data.sessionDuration || 0);
        break;
        
      case 'page_load':
        incrementSummaryCounter(summarySheet, today, 'Page Views', data.reportType || '');
        updateAverageMetric(summarySheet, today, 'Average Page Load Time', data.pageLoadTime || 0);
        break;
    }
    
  } catch (error) {
    console.error('Error updating summary stats:', error);
  }
}

/**
 * Increment a counter in the summary sheet
 * @param {SpreadsheetApp.Sheet} sheet - The summary sheet
 * @param {string} date - The date string
 * @param {string} metric - The metric name
 * @param {string} details - Additional details
 */
function incrementSummaryCounter(sheet, date, metric, details) {
  const data = sheet.getDataRange().getValues();
  
  // Look for existing entry
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] === date && data[i][1] === metric) {
      const currentCount = data[i][2] || 0;
      sheet.getRange(i + 1, 3).setValue(currentCount + 1);
      return;
    }
  }
  
  // If not found, create new entry
  sheet.appendRow([date, metric, 1, details]);
}

/**
 * Update an average metric in the summary sheet
 * @param {SpreadsheetApp.Sheet} sheet - The summary sheet
 * @param {string} date - The date string
 * @param {string} metric - The metric name
 * @param {number} newValue - The new value to include in average
 */
function updateAverageMetric(sheet, date, metric, newValue) {
  const data = sheet.getDataRange().getValues();
  
  // Look for existing entry
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] === date && data[i][1] === metric) {
      const currentAvg = data[i][2] || 0;
      const currentCount = data[i][3] || 0;
      const newCount = currentCount + 1;
      const newAvg = ((currentAvg * currentCount) + newValue) / newCount;
      
      sheet.getRange(i + 1, 3).setValue(Math.round(newAvg));
      sheet.getRange(i + 1, 4).setValue(newCount);
      return;
    }
  }
  
  // If not found, create new entry
  sheet.appendRow([date, metric, newValue, 1]);
}

/**
 * Generate comprehensive usage analytics report
 * @return {Object} Analytics report object
 */
function generateUsageAnalytics() {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const metricsSheet = ss.getSheetByName(USAGE_METRICS_SHEET_NAME);
    const summarySheet = ss.getSheetByName(USAGE_SUMMARY_SHEET_NAME);
    
    if (!metricsSheet || !summarySheet) {
      return { error: 'Usage tracking sheets not found. Start using the portal to generate data.' };
    }
    
    const data = metricsSheet.getDataRange().getValues();
    const today = new Date().toDateString();
    
    // Calculate key metrics
    const totalSessions = data.filter(row => row[3] === 'session_end').length;
    const totalPageViews = data.filter(row => row[3] === 'page_load').length;
    const totalClicks = data.filter(row => row[3] === 'click').length;
    const reportAccessClicks = data.filter(row => row[7] === 'report_access_button').length;
    const promptGenClicks = data.filter(row => row[7] === 'prompt_generator_link').length;
    
    // Feedback metrics
    const totalFeedback = data.filter(row => row[3] === 'feedback').length;
    const thumbsUp = data.filter(row => row[11] === 'thumbs_up').length;
    const thumbsDown = data.filter(row => row[11] === 'thumbs_down').length;
    
    // Calculate averages
    const sessions = data.filter(row => row[3] === 'session_end');
    const avgSessionDuration = sessions.length > 0 
      ? Math.round(sessions.reduce((sum, row) => sum + (row[10] || 0), 0) / sessions.length)
      : 0;
      
    const pageLoads = data.filter(row => row[3] === 'page_load');
    const avgPageLoadTime = pageLoads.length > 0
      ? Math.round(pageLoads.reduce((sum, row) => sum + (row[12] || 0), 0) / pageLoads.length)
      : 0;
    
    // Report type breakdown
    const reportTypes = {};
    data.filter(row => row[3] === 'page_load' && row[4]).forEach(row => {
      const reportType = row[4];
      reportTypes[reportType] = (reportTypes[reportType] || 0) + 1;
    });
    
    return {
      totalSessions,
      totalPageViews,
      totalClicks,
      reportAccessClicks,
      promptGenClicks,
      totalFeedback,
      thumbsUp,
      thumbsDown,
      avgSessionDuration,
      avgPageLoadTime,
      reportTypes,
      satisfactionRate: totalFeedback > 0 ? Math.round((thumbsUp / totalFeedback) * 100) : 0
    };
    
  } catch (error) {
    console.error('Error generating usage analytics:', error);
    return { error: 'Failed to generate analytics: ' + error.toString() };
  }
}

/**
 * Identifies the report type based on filename using centralized configuration
 * @param {string} fileName - The name of the file to analyze
 * @return {Object} The report configuration object that matches the filename
 */
function getReportConfig(fileName) {
  try {
    // Iterate through REPORT_CONFIG to find the first matching pattern
    for (const [configKey, config] of Object.entries(REPORT_CONFIG)) {
      // Skip DEFAULT for now - it will be our fallback
      if (configKey === 'DEFAULT') continue;
      
      if (config.pattern.test(fileName)) {
        console.log(`Report identified: ${configKey} for file: ${fileName}`);
        return {
          ...config,
          configKey: configKey
        };
      }
    }
    
    // If no specific pattern matches, return DEFAULT
    console.log(`No specific pattern matched for: ${fileName}, using DEFAULT`);
    return {
      ...REPORT_CONFIG.DEFAULT,
      configKey: 'DEFAULT'
    };
    
  } catch (error) {
    console.error('Error in getReportConfig:', error);
    // Always return DEFAULT on error to prevent crashes
    return {
      ...REPORT_CONFIG.DEFAULT,
      configKey: 'DEFAULT'
    };
  }
}

/**
 * Loads an HTML template from Google Drive by file name with improved error handling
 * @param {string} fileName - The name of the HTML file in Google Drive (e.g., "template-negative-ga.html")
 * @return {string} The HTML content of the template
 */
function loadTemplateFromDrive(fileName) {
  try {
    // Validate file name
    if (!fileName || typeof fileName !== 'string') {
      throw new Error('Invalid file name provided');
    }
    
    console.log(`Attempting to load template: ${fileName}`);
    
    // Search for the file by name in Google Drive
    const files = DriveApp.getFilesByName(fileName);
    
    if (!files.hasNext()) {
      console.log(`Template file "${fileName}" not found in Google Drive`);
      // Return a simple fallback template instead of throwing error
      return generateSimpleTemplateHTML(fileName);
    }
    
    // Get the first file with this name
    const file = files.next();
    console.log(`Found template file: ${fileName}`);
    
    // Get the HTML content as string
    const htmlContent = file.getBlob().getDataAsString();
    
    if (!htmlContent || htmlContent.trim().length === 0) {
      console.log(`Template file "${fileName}" is empty`);
      return generateSimpleTemplateHTML(fileName);
    }
    
    console.log(`Successfully loaded template: ${fileName} (${htmlContent.length} characters)`);
    return htmlContent;
    
  } catch (error) {
    console.error(`Error loading template "${fileName}":`, error);
    
    // Return a fallback template instead of the error template
    return generateSimpleTemplateHTML(fileName, error.message);
  }
}

/**
 * Generate a simple template HTML when Google Drive templates are not available
 * @param {string} fileName - The template file name that failed to load
 * @param {string} errorMessage - Optional error message
 * @return {string} Simple HTML template content
 */
function generateSimpleTemplateHTML(fileName, errorMessage = null) {
  // Determine template type from filename
  let templateContent = '';
  
  if (fileName.includes('negative-ga')) {
    templateContent = `
      <div class="report-template negative-ga">
        <h3>📊 Negative GA Analysis</h3>
        <div class="report-highlights">
          <div class="highlight-item">
            <h4>🔍 Key Findings</h4>
            <p>This report contains analysis of negative gross adds and their impact on business performance.</p>
          </div>
          <div class="highlight-item">
            <h4>📈 Metrics Included</h4>
            <ul>
              <li>Negative GA trends and patterns</li>
              <li>Impact analysis on revenue</li>
              <li>Comparison with historical data</li>
              <li>Recommendations for improvement</li>
            </ul>
          </div>
        </div>
      </div>
    `;
  } else if (fileName.includes('inflow-outflow')) {
    templateContent = `
      <div class="report-template inflow-outflow">
        <h3>🌊 Inflow and Outflow Analysis</h3>
        <div class="report-highlights">
          <div class="highlight-item">
            <h4>📊 Traffic Analysis</h4>
            <p>Comprehensive analysis of customer inflow and outflow patterns.</p>
          </div>
          <div class="highlight-item">
            <h4>🔢 Key Metrics</h4>
            <ul>
              <li>Customer acquisition rates</li>
              <li>Churn analysis and patterns</li>
              <li>Net customer flow</li>
              <li>Seasonal trends and variations</li>
            </ul>
          </div>
        </div>
      </div>
    `;
  } else if (fileName.includes('sales-performance')) {
    templateContent = `
      <div class="report-template sales-performance">
        <h3>💰 Sales Performance Dashboard</h3>
        <div class="report-highlights">
          <div class="highlight-item">
            <h4>🎯 Performance Overview</h4>
            <p>Detailed analysis of sales performance across all channels and regions.</p>
          </div>
          <div class="highlight-item">
            <h4>📊 Key Performance Indicators</h4>
            <ul>
              <li>Revenue growth and trends</li>
              <li>Sales target achievement</li>
              <li>Channel performance comparison</li>
              <li>Team and individual metrics</li>
            </ul>
          </div>
        </div>
      </div>
    `;
  } else if (fileName.includes('executive-summary')) {
    templateContent = `
      <div class="report-template executive-summary">
        <h3>📋 Executive Summary</h3>
        <div class="report-highlights">
          <div class="highlight-item">
            <h4>🎯 Strategic Overview</h4>
            <p>High-level summary of key business metrics and strategic insights for leadership review.</p>
          </div>
          <div class="highlight-item">
            <h4>📈 Executive Insights</h4>
            <ul>
              <li>Key performance indicators</li>
              <li>Strategic recommendations</li>
              <li>Risk assessment and mitigation</li>
              <li>Market opportunities</li>
            </ul>
          </div>
        </div>
      </div>
    `;
  } else {
    // Default template
    templateContent = `
      <div class="report-template default">
        <h3>� Business Report</h3>
        <div class="report-highlights">
          <div class="highlight-item">
            <h4>📊 Report Overview</h4>
            <p>This document contains important business insights and analytical data for your review.</p>
          </div>
          <div class="highlight-item">
            <h4>🔍 What's Inside</h4>
            <ul>
              <li>Data analysis and insights</li>
              <li>Key performance metrics</li>
              <li>Trends and patterns</li>
              <li>Actionable recommendations</li>
            </ul>
          </div>
        </div>
      </div>
    `;
  }
  
  // Add error notice if there was an error
  if (errorMessage) {
    templateContent += `
      <div class="template-notice" style="margin-top: 20px; padding: 15px; background: #fff3cd; border-radius: 8px; border-left: 4px solid #ffc107;">
        <p><strong>📝 Template Note:</strong> Custom template "${fileName}" could not be loaded. Using built-in template.</p>
        ${errorMessage ? `<p><small>Error: ${errorMessage}</small></p>` : ''}
      </div>
    `;
  }
  
  // Add access button
  templateContent += `
    <div class="access-button-container" style="text-align: center; margin: 30px 0;">
      <button onclick="accessDocument()" class="access-btn" style="
        display: inline-block;
        padding: 15px 30px;
        background: #007cba;
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-size: 16px;
        border: none;
        cursor: pointer;
        transition: background 0.3s;
      ">
        📄 Open Document
      </button>
    </div>
  `;
  
  return templateContent;
}

/**
 * DEBUG: Test template loading functionality
 * @return {string} Debug information about template loading
 */
function debugTemplateLoading() {
  const debugInfo = [];
  
  debugInfo.push("=== TEMPLATE LOADING DEBUG ===");
  
  // Test 1: Check if Apps Script project files exist
  const requiredTemplates = [
    'welcome-template',
    'error-template', 
    'whats-inside-template',
    'template-negative-ga',
    'template-inflow-outflow',
    'template-sales-performance',
    'template-executive-summary',
    'template-default'
  ];
  
  for (const templateName of requiredTemplates) {
    try {
      const template = HtmlService.createTemplateFromFile(templateName);
      const htmlContent = template.evaluate().getContent();
      
      // Check if it contains the {{TEMPLATE_DATA_JSON}} placeholder
      const hasJsonPlaceholder = htmlContent.includes('{{TEMPLATE_DATA_JSON}}');
      const templateSize = htmlContent.length;
      
      debugInfo.push(`✅ ${templateName} - Found (${templateSize} chars, JSON placeholder: ${hasJsonPlaceholder})`);
    } catch (e) {
      debugInfo.push(`❌ ${templateName} - MISSING: ${e.message}`);
    }
  }
  
  // Test 2: Test template processing with sample data
  debugInfo.push("\n=== TEMPLATE PROCESSING TEST ===");
  
  const sampleData = {
    DOCUMENT_NAME: "Test Document",
    DOCUMENT_TYPE: "Test Report", 
    LAST_MODIFIED: "2025-09-16",
    FILE_URL: "https://example.com",
    WHATS_INSIDE_HTML: "<p>Sample content</p>"
  };
  
  try {
    const processedTemplate = loadTemplateSimple('welcome-template', sampleData);
    const hasTemplateData = processedTemplate.includes('window.templateData');
    const hasPlaceholders = processedTemplate.includes('{{');
    const hasEvalPattern = processedTemplate.includes('eval(');
    const templateSize = processedTemplate.length;
    
    debugInfo.push(`✅ Template processing - SUCCESS`);
    debugInfo.push(`   - Template data injection: ${hasTemplateData}`);
    debugInfo.push(`   - Remaining placeholders: ${hasPlaceholders}`);
    debugInfo.push(`   - Eval patterns remaining: ${hasEvalPattern}`);
    debugInfo.push(`   - Processed size: ${templateSize} chars`);
    
    // Test for specific patterns that might cause issues
    const jsonDataMatch = processedTemplate.match(/window\.templateData\s*=\s*\{/);
    if (jsonDataMatch) {
      debugInfo.push(`   - JSON assignment found: ${jsonDataMatch[0]}...`);
    } else {
      debugInfo.push(`   - ❌ JSON assignment not found`);
    }
    
  } catch (e) {
    debugInfo.push(`❌ Template processing - FAILED: ${e.message}`);
  }
  
  // Test 3: Test report configuration
  debugInfo.push("\n=== REPORT CONFIG TEST ===");
  
  const testFiles = [
    "Negative GA Report.xlsx",
    "Inflow Outflow Analysis.docx", 
    "Sales Performance Q3.pdf",
    "Executive Summary 2025.doc",
    "Random Document.txt"
  ];
  
  for (const fileName of testFiles) {
    const config = getReportConfig(fileName);
    debugInfo.push(`📊 "${fileName}" → ${config.configKey} (${config.displayName})`);
  }
  
  return debugInfo.join('\n');
}

/**
 * Simple template loading test that returns HTML
 * @return {HtmlOutput} Test page with template loading results
 */
function testTemplateLoading() {
  const debugResult = debugTemplateLoading();
  
  const testHtml = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Template Loading Debug - Enhanced</title>
      <style>
        body { 
          font-family: 'Courier New', monospace; 
          margin: 20px; 
          line-height: 1.6; 
          background: #f8f9fa;
        }
        .container {
          max-width: 1000px;
          margin: 0 auto;
          background: white;
          padding: 30px;
          border-radius: 8px;
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .success { color: #28a745; font-weight: bold; }
        .error { color: #dc3545; font-weight: bold; }
        .info { color: #007cba; }
        pre { 
          background: #f8f9fa; 
          padding: 20px; 
          border-radius: 8px; 
          border-left: 4px solid #007cba;
          overflow-x: auto;
          white-space: pre-wrap;
        }
        .status-card {
          background: #e9ecef;
          padding: 15px;
          margin: 15px 0;
          border-radius: 6px;
          border-left: 4px solid #ffc107;
        }
        .next-steps {
          background: #d1ecf1;
          padding: 20px;
          border-radius: 8px;
          border-left: 4px solid #17a2b8;
          margin-top: 30px;
        }
        .test-url {
          background: #d4edda;
          padding: 15px;
          border-radius: 6px;
          font-family: monospace;
          margin: 10px 0;
          word-break: break-all;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>🔧 Enhanced Template Loading Debug Results</h1>
        <p><strong>Timestamp:</strong> ${new Date().toLocaleString()}</p>
        
        <div class="status-card">
          <h3>📊 Debug Information</h3>
          <pre>${debugResult}</pre>
        </div>
        
        <div class="next-steps">
          <h3>🚀 Next Steps</h3>
          
          <h4>If Templates Are Missing:</h4>
          <ol>
            <li><strong>Open Apps Script:</strong> Go to script.google.com</li>
            <li><strong>Add Files:</strong> Click "+" → HTML file for each missing template</li>
            <li><strong>Copy Content:</strong> Paste content from your local HTML files</li>
            <li><strong>Save:</strong> Save each file in the Apps Script project</li>
          </ol>
          
          <h4>If Templates Are Found But Processing Fails:</h4>
          <ol>
            <li>Check for syntax errors in the HTML templates</li>
            <li>Verify the {{TEMPLATE_DATA_JSON}} placeholder exists</li>
            <li>Test with a simple document URL</li>
          </ol>
          
          <h4>Test Your Webapp:</h4>
          <div class="test-url">
            <strong>Simple Test:</strong><br>
            YOUR_WEBAPP_URL?action=simple_test
          </div>
          
          <div class="test-url">
            <strong>Document Test (replace FILE_ID):</strong><br>
            YOUR_WEBAPP_URL?URL=https://drive.google.com/file/d/FILE_ID/view
          </div>
        </div>
        
        <div style="margin-top: 30px; text-align: center;">
          <p><small>This debug page updates automatically. Refresh after making changes.</small></p>
        </div>
      </div>
    </body>
    </html>
  `;
  
  return HtmlService.createHtmlOutput(testHtml)
    .setTitle("Enhanced Template Loading Debug")
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * Simple test to verify template loading without full data processing
 * @return {HtmlOutput} Simple test result
 */
function testTemplateLoadingSimple() {
  try {
    // Test if we can load the welcome template
    const template = HtmlService.createTemplateFromFile('welcome-template');
    const rawContent = template.evaluate().getContent();
    
    // More detailed analysis
    const trimmedContent = rawContent.trim();
    const firstNonWhitespace = rawContent.replace(/^\s+/, '').substring(0, 500);
    const lastNonWhitespace = rawContent.replace(/\s+$/, '').slice(-500);
    const lineCount = rawContent.split('\n').length;
    const hasDoctype = rawContent.includes('<!DOCTYPE');
    const hasHtmlTag = rawContent.includes('<html');
    const hasBodyTag = rawContent.includes('<body');
    
    const testHtml = `
      <!DOCTYPE html>
      <html>
      <head><title>Enhanced Template Test</title></head>
      <body>
        <h1>Template Loading Test Results</h1>
        <div style="background:#e8f5e8;padding:15px;border-radius:8px;margin:10px 0;">
          <h3>✅ Basic Checks</h3>
          <p><strong>Template Found:</strong> ✅ YES</p>
          <p><strong>Raw Template Size:</strong> ${rawContent.length} characters</p>
          <p><strong>Trimmed Size:</strong> ${trimmedContent.length} characters</p>
          <p><strong>Line Count:</strong> ${lineCount}</p>
        </div>
        
        <div style="background:#fff3cd;padding:15px;border-radius:8px;margin:10px 0;">
          <h3>🔍 Content Analysis</h3>
          <p><strong>Contains TEMPLATE_DATA_JSON placeholder:</strong> ${rawContent.includes('{{TEMPLATE_DATA_JSON}}') ? '✅ YES' : '❌ NO'}</p>
          <p><strong>Contains eval pattern:</strong> ${rawContent.includes('eval(') ? '✅ YES' : '❌ NO'}</p>
          <p><strong>Has DOCTYPE:</strong> ${hasDoctype ? '✅ YES' : '❌ NO'}</p>
          <p><strong>Has HTML tag:</strong> ${hasHtmlTag ? '✅ YES' : '❌ NO'}</p>
          <p><strong>Has BODY tag:</strong> ${hasBodyTag ? '✅ YES' : '❌ NO'}</p>
        </div>
        
        <div style="background:#f8f9fa;padding:15px;border-radius:8px;margin:10px 0;">
          <h3>📝 Content Preview</h3>
          <p><strong>First 500 non-whitespace characters:</strong></p>
          <pre style="background:#ffffff;padding:10px;border:1px solid #ddd;border-radius:5px;overflow-x:auto;">${firstNonWhitespace.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</pre>
          
          <p><strong>Last 500 characters:</strong></p>
          <pre style="background:#ffffff;padding:10px;border:1px solid #ddd;border-radius:5px;overflow-x:auto;">${lastNonWhitespace.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</pre>
        </div>
        
        <div style="background:#d1ecf1;padding:15px;border-radius:8px;margin:10px 0;">
          <h3>🔧 Troubleshooting</h3>
          ${rawContent.length > 0 && trimmedContent.length === 0 ? 
            '<p><strong>⚠️ Issue:</strong> Template contains only whitespace characters</p>' :
            trimmedContent.length < 1000 ? 
            '<p><strong>⚠️ Issue:</strong> Template content seems too small for a full template</p>' :
            '<p><strong>✅ Content:</strong> Template appears to have substantial content</p>'}
        </div>
      </body>
      </html>
    `;
    
    return HtmlService.createHtmlOutput(testHtml).setTitle("Enhanced Template Test");
    
  } catch (error) {
    const errorHtml = `
      <!DOCTYPE html>
      <html>
      <head><title>Template Test Error</title></head>
      <body>
        <h1>❌ Template Loading Failed</h1>
        <p><strong>Error:</strong> ${error.message}</p>
        <p>This confirms the template is not found in the Apps Script project.</p>
      </body>
      </html>
    `;
    
    return HtmlService.createHtmlOutput(errorHtml).setTitle("Template Test Error");
  }
}

/**
 * Test the complete template processing pipeline
 * This will help us understand why the main template isn't rendering
 */
function testTemplateProcessing() {
  console.log("🔄 Testing Complete Template Processing Pipeline\n");
  
  try {
    // Test 1: Basic template loading
    console.log("1️⃣ Testing basic template loading...");
    const rawTemplate = HtmlService.createTemplateFromFile('welcome-template');
    console.log("✅ Raw template loaded successfully");
    
    // Test 2: Template with data injection
    console.log("\n2️⃣ Testing template with data injection...");
    const testData = {
      FILE_URL: "https://drive.google.com/file/d/1234567890/view",
      FILE_NAME: "Test Document.pdf",
      VIEW_TYPE: "simple",
      ERROR_MESSAGE: null,
      DEBUG_INFO: {
        timestamp: new Date().toISOString(),
        testMode: true
      }
    };
    
    // Use our loadTemplateSimple function
    const processedHtml = loadTemplateSimple('welcome-template', testData);
    console.log("✅ Template processed with data injection");
    console.log(`📊 Processed HTML size: ${processedHtml.length} characters`);
    
    // Test 3: Check for proper data injection
    console.log("\n3️⃣ Checking data injection...");
    const hasTemplateData = processedHtml.includes('window.templateData');
    const hasFileUrl = processedHtml.includes(testData.FILE_URL);
    const hasFileName = processedHtml.includes(testData.FILE_NAME);
    
    console.log(`✅ Has window.templateData: ${hasTemplateData}`);
    console.log(`✅ Has FILE_URL: ${hasFileUrl}`);
    console.log(`✅ Has FILE_NAME: ${hasFileName}`);
    
    // Test 4: Check for fallback indicators
    console.log("\n4️⃣ Checking for fallback indicators...");
    const hasFallbackMarkers = processedHtml.includes('FALLBACK_TEMPLATE') || 
                               processedHtml.includes('Template not found') ||
                               processedHtml.includes('Error loading template');
    console.log(`🔍 Has fallback markers: ${hasFallbackMarkers}`);
    
    // Test 5: Simulate doGet processing
    console.log("\n5️⃣ Testing doGet simulation...");
    const mockRequest = {
      parameter: {
        fileUrl: "https://drive.google.com/file/d/1234567890/view",
        view: "simple"
      }
    };
    
    const response = doGet(mockRequest);
    console.log("✅ doGet executed successfully");
    console.log(`📄 Response content size: ${response.getContent().length} characters`);
    
    // Test 6: Content analysis
    const responseContent = response.getContent();
    const isMainTemplate = responseContent.includes('Document Access Portal') && 
                          responseContent.includes('anime.min.js');
    const isFallback = responseContent.includes('Simple fallback') || 
                      responseContent.includes('FALLBACK_TEMPLATE');
    
    console.log(`\n📋 Final Analysis:`);
    console.log(`✅ Main template rendered: ${isMainTemplate}`);
    console.log(`⚠️  Fallback template used: ${isFallback}`);
    
    if (!isMainTemplate && !isFallback) {
      console.log("❌ Unknown template type - need to investigate");
      console.log("First 500 chars of response:");
      console.log(responseContent.substring(0, 500));
    }
    
    return {
      success: true,
      mainTemplateRendered: isMainTemplate,
      fallbackUsed: isFallback,
      responseSize: responseContent.length,
      testData: testData
    };
    
  } catch (error) {
    console.error("❌ Template processing test failed:");
    console.error(error.toString());
    console.error("Stack trace:", error.stack);
    return {
      success: false,
      error: error.toString()
    };
  }
}

