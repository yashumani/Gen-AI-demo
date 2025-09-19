# GitHub Copilot Instructions - Insight Engine Document Portal

## Project Overview
This is a **Google Apps Script Web Application** that provides a modern, responsive document access portal for Google Drive files. The webapp processes URL parameters to detect and open Google Drive documents with enhanced user experience and analytics tracking.

## Current Architecture & Status

### ✅ Production-Ready Components
- **Backend**: `code.gs` - Fully functional with template system fixes
- **Frontend**: `welcome-template.html` - Modern responsive UI with URL detection
- **Error handling**: `error-template.html` - User-friendly error pages
- **Content display**: `whats-inside-template.html` - Document content template

### 🔧 Key Technical Implementations
1. **URL Parameter Processing**: Supports multiple parameter formats (`fileUrl`, `url`, `file`, `URL`)
2. **Template System**: Fixed to use proper Apps Script `HtmlService.createTemplateFromFile()`
3. **File ID Extraction**: Robust pattern matching for various Google Drive URL formats
4. **Multiple URL Generation**: Creates direct, view, edit, and preview URLs for better compatibility
5. **JSON Data Injection**: Uses `{{TEMPLATE_DATA_JSON}}` for reliable frontend data transfer

## Core Functionality

### Backend (`code.gs`)
```javascript
// Main request handler with enhanced URL parameter support
function doGet(e) {
  // Processes: fileUrl, url, file, URL parameters
  // Extracts file IDs from various Google Drive URL formats
  // Generates multiple URL formats for compatibility
  // Injects template data via JSON
}

// Fixed template loading system
function loadTemplate(templateName, data) {
  // Uses HtmlService.createTemplateFromFile() for Apps Script compatibility
  // Falls back to Drive-based templates if needed
  // Injects JSON data using {{TEMPLATE_DATA_JSON}} placeholder
}
```

### Frontend (`welcome-template.html`)
```javascript
// Template data from backend (injected as JSON)
window.templateData = {{TEMPLATE_DATA_JSON}};

// Enhanced URL detection with multiple fallback sources
function getFileUrl() {
  // 1. Check window.templateData (primary source from backend)
  // 2. Check template variables (fallback)
  // 3. Check URL parameters (testing)
  // 4. Multiple other fallback mechanisms
}
```

## Development Guidelines

### When Working with This Project:

#### 🎯 **Primary Focus Areas**
1. **URL Parameter Processing** - Core functionality for detecting file URLs
2. **Template System** - Proper data injection from backend to frontend
3. **Google Drive Integration** - File access, permissions, and URL generation
4. **Responsive UI** - Modern, mobile-friendly interface design
5. **Error Handling** - User-friendly error messages and troubleshooting

#### 🚫 **Avoid These Patterns**
- Loading HTML templates from Google Drive (use Apps Script project files)
- Using `{{placeholder}}` syntax directly in JavaScript objects
- Complex client-side URL parameter parsing (backend handles this)
- Blocking popup windows for file opening
- Hard-coded file IDs or URLs

#### ✅ **Preferred Patterns**
- Use `HtmlService.createTemplateFromFile()` for template loading
- Inject data via `{{TEMPLATE_DATA_JSON}}` for complex objects
- Use `window.templateData` for frontend data access
- Implement multiple fallback mechanisms for robustness
- Generate multiple URL formats for better compatibility

### Code Style & Standards

#### Apps Script Specific
```javascript
// Proper template loading
const template = HtmlService.createTemplateFromFile('welcome-template');
template.FILE_URL = fileUrl;
const html = template.evaluate().getContent();

// JSON data injection
const templateDataJson = JSON.stringify(data, null, 2);
htmlContent = htmlContent.replace(/\{\{TEMPLATE_DATA_JSON\}\}/g, templateDataJson);

// File access with error handling
try {
  const file = DriveApp.getFileById(fileId);
  const fileName = file.getName();
} catch (fileError) {
  throw new Error(`File not accessible: ${fileError.message}`);
}
```

#### Frontend JavaScript
```javascript
// Use template data from backend
const fileUrl = window.templateData?.FILE_URL_DIRECT || 
                window.templateData?.FILE_URL || 
                getFileUrlFallback();

// Implement progressive enhancement
function openDocument() {
  // 1. Try primary URL
  // 2. Fall back to alternative formats
  // 3. Show user-friendly error if all fail
}
```

### Testing & Validation

#### Essential Test Cases
1. **URL Parameter Detection**: Test with various Google Drive URL formats
2. **Template Data Injection**: Verify `window.templateData` is populated
3. **File Access**: Test with different file types and permissions
4. **Error Handling**: Test with invalid URLs and inaccessible files
5. **Responsive Design**: Test on mobile and desktop devices

#### Debug Functions Available
```javascript
// Backend testing
testTemplateSystemFix()        // Test template loading and data injection
testUrlParameterProcessing()   // Test URL parameter handling
testFileIdExtraction()         // Test file ID extraction patterns

// Frontend testing (browser console)
console.log('Template data:', window.templateData);
console.log('Detected URL:', getFileUrl());
console.log('All URL formats:', getFileUrls());
```

## Deployment & Configuration

### Apps Script Project Structure
```
Project Root/
├── code.gs                 # Main backend logic
├── welcome-template.html   # Primary UI (no .html extension in Apps Script)
├── error-template.html     # Error handling page
└── whats-inside-template.html # Content display template
```

### Environment Variables & Configuration
```javascript
// Spreadsheet integration
const LOG_SHEET_NAME = "Usage Log";
const USAGE_METRICS_SHEET_NAME = "Usage_Metrics";

// External integrations
const NEWSLETTER_SHEET_ID = "1X2kUhOYtaIdkCnptDPAYbu6AYdCwHYhsqsdEB3QEsXM";
```

### Deployment Checklist
1. ✅ Upload all 4 essential files to Apps Script project
2. ✅ Deploy as web app with proper permissions
3. ✅ Test with sample URL parameter
4. ✅ Verify template data injection in browser console
5. ✅ Test file opening functionality

## Known Issues & Solutions

### ❌ Common Problems
- **"No URL parameters found"** → Fixed with proper template system
- **Template placeholders not replaced** → Use JSON injection method
- **File URLs not detected** → Check `window.templateData` population
- **Permission errors** → Ensure proper file sharing and access

### ✅ Current Status
All major issues resolved. System is production-ready with:
- ✅ Robust URL parameter detection
- ✅ Proper template data injection
- ✅ Multiple fallback mechanisms
- ✅ Comprehensive error handling
- ✅ Modern responsive UI

## Integration Points

### Google Services Used
- **Google Apps Script**: Web app hosting and backend logic
- **Google Drive API**: File access and metadata retrieval
- **Google Sheets API**: Usage logging and analytics
- **HTML Service**: Template processing and frontend delivery

### External Dependencies
- **Anime.js**: UI animations and transitions
- **Modern CSS**: Responsive design and styling
- **Verizon Design System**: Brand-compliant styling

## Performance Considerations
- Template data is loaded once per request
- File metadata cached during request processing
- Minimal external API calls
- Optimized for mobile and desktop performance
- Progressive enhancement for better user experience

---

**When suggesting code changes or improvements, always consider:**
1. Apps Script environment limitations
2. Google Drive API rate limits and permissions
3. Template system requirements
4. Mobile responsiveness
5. User experience and accessibility
6. Error handling and edge cases

## Production File Structure
The project is now clean and production-ready with only essential files:

```
Insight Engine Tracking/
├── code.gs                     # Main backend with URL processing & analytics
├── welcome-template.html       # Modern responsive UI with file detection
├── error-template.html         # User-friendly error handling
├── whats-inside-template.html  # Document content display
├── README.md                   # Project documentation
├── TEMPLATE-SYSTEM-FIX.md     # Critical template system fixes
└── PRODUCTION-READY.md         # Production status & validation
```

**✅ CLEANUP COMPLETED**: All debug files, test scripts, and redundant documentation have been removed for production use.

**🎯 PRODUCTION FOCUS**: The system is now streamlined with only the 4 core templates + 3 essential documentation files needed for deployment and maintenance.
