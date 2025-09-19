# 🚀 Insight Engine Tracking - PRODUCTION READY

A Google Apps Script web application that provides secure document access and analytics tracking through Google Drive integration.

## 📋 Production Files

### Core Application
- **`code.gs`** - Main backend application (2,099 lines)
  - Document access portal with Google Drive integration
  - Template processing with fixed data injection
  - Usage analytics and logging
  - URL parameter handling for multiple formats

### HTML Templates
- **`welcome-template.html`** - Primary user interface (2,822 lines)
- **`error-template.html`** - Error handling page
- **`whats-inside-template.html`** - Content preview template

### Report Templates
- **`template-default.html`** - Default report layout
- **`template-executive-summary.html`** - Executive summary format
- **`template-inflow-outflow.html`** - Financial flow analysis
- **`template-negative-ga.html`** - Negative analytics template
- **`template-sales-performance.html`** - Sales performance dashboard

## 🔧 Key Features

### ✅ Fixed Template Data Injection
- **Issue**: `{{TEMPLATE_DATA_JSON}}` placeholders showing instead of data
- **Solution**: Enhanced `loadTemplateSimple()` function with improved regex pattern
- **Result**: Reliable template data injection in production

### ✅ Google Drive Integration
- Supports multiple URL formats:
  - `https://drive.google.com/file/d/FILE_ID/view`
  - `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
  - `https://drive.google.com/open?id=FILE_ID`

### ✅ Analytics & Logging
- Google Sheets integration for usage tracking
- Comprehensive error handling and logging
- Performance monitoring and optimization

### ✅ Professional UI
- Responsive design with animations
- Multiple template layouts for different report types
- Clean, modern interface

## 🚀 Deployment Instructions

### 1. Google Apps Script Setup
1. Create a new Google Apps Script project
2. Upload all files from this directory
3. Set up the web app deployment:
   - **Execute as**: Me
   - **Who has access**: Anyone

### 2. Google Sheets Configuration
The app expects a Google Sheet with these tabs:
- `Usage Log` - User activity tracking
- `Usage_Metrics` - Analytics data
- `News Headlines` - Content updates

### 3. Testing the Deployment
Test with a Google Drive URL:
```
https://your-web-app-url?URL=https://drive.google.com/file/d/YOUR_FILE_ID/view
```

## 📊 Usage Examples

### Basic Document Access
```
https://your-web-app-url?URL=https://drive.google.com/file/d/123ABC/view
```

### Specific View Mode
```
https://your-web-app-url?URL=https://drive.google.com/file/d/123ABC/view&view=simple
```

### Report Type Selection
```
https://your-web-app-url?URL=https://drive.google.com/file/d/123ABC/view&report=executive-summary
```

## 🔍 Technical Implementation

### Template Processing
The `loadTemplateSimple()` function handles:
- JSON data injection into HTML templates
- Placeholder replacement (`{{VARIABLE_NAME}}`)
- Error handling with fallback templates
- Performance optimization

### URL Parameter Extraction
Supports various Google Drive URL formats and extracts:
- File ID for Drive API access
- Document metadata
- Access permissions

### Error Handling
- Comprehensive try-catch blocks
- Fallback templates for failed loads
- Detailed console logging for debugging

## 📈 Performance Optimizations

- **Template Caching**: Reduces load times
- **Efficient Regex**: Optimized pattern matching
- **Error Recovery**: Graceful degradation
- **Console Logging**: Production debugging support

## 🛠️ Maintenance

### Monitoring
- Check Google Apps Script logs for errors
- Monitor Google Sheets for usage patterns
- Verify template data injection is working

### Updates
- Template modifications: Edit HTML files
- Backend changes: Modify `code.gs`
- New features: Add to `doGet()` function

## 📞 Support

For technical issues:
1. Check Google Apps Script execution logs
2. Verify Google Drive file permissions
3. Test with known working file IDs
4. Review template data injection in browser console

---

**Production Version**: September 2025
**Status**: ✅ Ready for Production Deployment
**Last Updated**: Fixed template data injection issue
