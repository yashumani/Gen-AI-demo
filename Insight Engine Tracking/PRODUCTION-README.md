# 🚀 Insight Engine Tracking - PRODUCTION READY (Enhanced)

A Google Apps Script web application that provides secure document access and analytics tracking through Google Drive integration, **now enhanced with dynamic headers, anime.js animations, and interactive user experience**.

## 📋 Production Files (Updated September 2025)

### Core Application
- **`code.gs`** - Enhanced backend application (2,100+ lines)
  - Document access portal with Google Drive integration
  - **Fixed template processing** with improved placeholder replacement
  - **Dynamic header system** showing actual document names
  - Usage analytics and logging
  - URL parameter handling for multiple formats

### HTML Templates (Enhanced)
- **`welcome-template.html`** - **Enhanced responsive UI with anime.js animations** (1,000+ lines)
- **`error-template.html`** - Error handling page
- **`whats-inside-template.html`** - Content preview template

---

## ✨ **NEW FEATURES (September 2025)**

### 🎪 **Advanced Animation System**
- **Anime.js Integration**: Professional animations with staggered effects
- **Header Animations**: Scale + elastic bounce (1000ms duration)
- **Content Sections**: Slide-up with exponential easing
- **Interactive Buttons**: Hover and click feedback with smooth transitions
- **Sidebar Effects**: Slide-in from left/right (1000ms duration)
- **News Feed**: Individual fade-in with staggered timing

### 🎯 **Dynamic UI Enhancements**
- **Document Name Headers**: Headers display actual file names instead of "Secure Document Portal"
- **Insight Engine Branding**: "Welcome to Insight Engine" messaging
- **Enhanced Buttons**: "🚀 Launch Document & Start Analysis" and "⚡ Open AI Prompt Generator"
- **Pulsing Title Effects**: Continuous glow animation with brand colors
- **Responsive Animations**: Optimized for all screen sizes

---

## 🔧 **Core Features** (Enhanced)

### ✅ **Enhanced Template Data Injection**
- **Issue Resolved**: `{{DOCUMENT_NAME}}` and `{{LAST_MODIFIED}}` placeholders now properly replaced
- **Solution**: Enhanced `loadTemplateSimple()` function with improved regex pattern and HTML escaping
- **Dynamic Headers**: Headers now show actual document names instead of generic text
- **Result**: Reliable template data injection with professional user experience

### ✅ **Advanced Animation System**
- **Anime.js Integration**: Professional staggered animations with multiple easing types
- **Interactive Elements**: Buttons respond with hover and click feedback
- **Performance Optimized**: Smooth animations across all devices and screen sizes
- **Responsive Design**: All animations scale appropriately for mobile and desktop

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
