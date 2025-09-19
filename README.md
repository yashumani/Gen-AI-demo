# 📊 Insight Engine Document Portal

A modern, responsive Google Apps Script web application that provides an enhanced document access portal for Google Drive files with advanced analytics tracking and report-specific UI templates.

## 🌟 Features

- **Smart URL Detection**: Automatically extracts file IDs from various Google Drive URL formats
- **Modern Responsive UI**: Professional interface with smooth animations and mobile optimization
- **Report-Specific Templates**: Dynamic content templates for different report types (Executive Summary, Sales Performance, GA Reports, etc.)
- **Advanced Analytics**: Comprehensive usage tracking and user interaction analytics
- **Multiple Access Methods**: Supports various URL parameter formats for flexible integration
- **Error Handling**: User-friendly error pages with troubleshooting guidance
- **File Compatibility**: Works with Google Docs, Sheets, PDFs, and other document types

## 🚀 Quick Start

### Prerequisites
- Google Apps Script project
- Google Drive access for target documents
- Basic knowledge of Google Apps Script deployment

### Installation

1. **Create Apps Script Project**:
   - Go to [script.google.com](https://script.google.com)
   - Click "New Project"

2. **Upload Core Files**:
   ```
   📁 Apps Script Project/
   ├── 📄 code.gs                    ← Main backend logic
   ├── 📄 welcome-template            ← Primary UI template
   ├── 📄 error-template              ← Error handling page
   └── 📄 whats-inside-template       ← Content display template
   ```

3. **Deploy as Web App**:
   - Click "Deploy" → "New deployment"
   - Type: Web app
   - Execute as: Me
   - Who has access: Anyone (or as needed)

### Usage

Access your webapp with this URL format:
```
https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec?fileUrl=GOOGLE_DRIVE_URL
```

**Example**:
```
https://script.google.com/macros/s/ABC123.../exec?fileUrl=https://drive.google.com/file/d/1ABC123.../view
```

## 📁 Project Structure

```
Gen-AI-VZ/
├── 📂 Insight Engine Tracking/           ← Main application directory
│   ├── 📄 code.gs                        ← Backend logic and API handlers
│   ├── 📄 welcome-template.html          ← Primary UI template
│   ├── 📄 error-template.html            ← Error page template
│   ├── 📄 whats-inside-template.html     ← Content display template
│   ├── 📄 template-*.html                ← Report-specific templates
│   ├── 📄 README.md                      ← Detailed documentation
│   ├── 📄 PRODUCTION-USAGE-GUIDE.md      ← Deployment instructions
│   └── 📄 FINAL-DEPLOYMENT-CHECKLIST.md  ← Pre-deployment checklist
├── 📄 code.gs                            ← Legacy file (for reference)
├── 📄 WebApp.html                        ← Legacy file (for reference)
└── 📄 README.md                          ← This file
```

## 🎯 Core Components

### Backend (`code.gs`)
- **URL Processing**: Multi-format parameter support and file ID extraction
- **Template System**: Dynamic template loading with data injection
- **Analytics Tracking**: Comprehensive user interaction and usage metrics
- **Error Handling**: Graceful error management with detailed logging

### Frontend Templates
- **Welcome Template**: Modern Document Access Portal interface
- **Error Template**: User-friendly error pages with troubleshooting
- **Content Templates**: Report-specific content displays
- **Report Templates**: Specialized layouts for different document types

### Supported URL Parameters
- `?fileUrl=GOOGLE_DRIVE_URL`
- `?url=GOOGLE_DRIVE_URL` 
- `?file=GOOGLE_DRIVE_URL`
- `?URL=GOOGLE_DRIVE_URL`
- `?id=GOOGLE_DRIVE_FILE_ID`
- `?view=simple` (optional view mode)

## 📊 Analytics & Tracking

The system includes comprehensive analytics tracking:

- **Usage Metrics**: Page views, clicks, session duration
- **User Interactions**: Button clicks, navigation patterns
- **Report Analytics**: Report type popularity and access patterns  
- **Performance Metrics**: Page load times and system performance
- **Error Tracking**: Detailed error logging and troubleshooting data

## 🔧 Configuration

### Report Type Configuration
The system automatically detects report types based on filename patterns:

- **Negative GA Reports**: `/Negative GA/i`
- **Inflow/Outflow Reports**: `/Inflow.*Outflow|Port.*Activity/i`
- **Sales Performance**: `/Sales.*Performance|Revenue.*Report/i`
- **Executive Summary**: `/Executive.*Summary|Management.*Report/i`

### Customization
- Modify `REPORT_CONFIG` in `code.gs` to add new report types
- Update template files to customize UI and branding
- Adjust analytics tracking in the usage metrics functions

## 🚀 Deployment

See the detailed deployment guides:
- **[Production Usage Guide](Insight%20Engine%20Tracking/PRODUCTION-USAGE-GUIDE.md)** - Complete deployment instructions
- **[Final Deployment Checklist](Insight%20Engine%20Tracking/FINAL-DEPLOYMENT-CHECKLIST.md)** - Pre-deployment verification

## 🔒 Security & Privacy

- **Permission-Based Access**: Respects Google Drive file permissions
- **No Data Storage**: File URLs are processed but not permanently stored
- **Secure Analytics**: User data is anonymized in tracking systems
- **HTTPS Encryption**: All communications are encrypted via Google's infrastructure

## 📈 Performance

- **Optimized Loading**: Template caching and efficient file access
- **Responsive Design**: Mobile and desktop optimized
- **Fast Processing**: Minimal API calls and streamlined data handling
- **Error Recovery**: Graceful fallbacks for edge cases

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues and questions:
- Check the [Production Usage Guide](Insight%20Engine%20Tracking/PRODUCTION-USAGE-GUIDE.md)
- Review the [Final Deployment Checklist](Insight%20Engine%20Tracking/FINAL-DEPLOYMENT-CHECKLIST.md)
- Open an issue in this repository

## 🎯 Status

**Current Status**: ✅ **Production Ready**

- ✅ Template data injection system working
- ✅ All core templates tested and verified
- ✅ Analytics and tracking implemented
- ✅ Error handling and fallbacks in place
- ✅ Deployment documentation complete

---

**Built with ❤️ for enhanced document management and analytics**
