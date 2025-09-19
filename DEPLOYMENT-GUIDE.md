# 🚀 Insight Engine - Complete Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the **Insight Engine** with its enhanced animations, dynamic headers, and anime.js integration.

---

## 📋 **Prerequisites**

- Google Account with access to Google Apps Script
- Google Drive with documents to access
- Basic understanding of Google Apps Script deployment
- Modern web browser for testing

---

## 🔧 **Step-by-Step Deployment**

### **1. Google Apps Script Setup**

#### 1.1 Create New Project
1. Go to [Google Apps Script](https://script.google.com)
2. Click **"New Project"**
3. Give your project a meaningful name: `"Insight Engine Portal"`

#### 1.2 Copy Backend Code
1. Replace the default `Code.gs` content with the enhanced `code.gs` from this repository
2. Ensure all 2,100+ lines are copied correctly
3. **Key Features Included:**
   - Dynamic header processing showing document names
   - Fixed template placeholder replacement
   - Google Drive integration with multiple URL formats
   - Analytics and error handling

#### 1.3 Add HTML Templates
1. Click the **"+"** next to Files and select **"HTML"**
2. Create the following files:

**welcome-template.html**
- Copy the enhanced template with anime.js integration
- Includes dynamic headers, staggered animations, and interactive elements
- Features responsive 3-column layout with news feed

**error-template.html**
- Copy the error handling template
- Provides user-friendly error messages and recovery options

**whats-inside-template.html** (optional)
- Copy if you need content preview functionality

### **2. Configuration & Testing**

#### 2.1 Update Configuration (Optional)
In `code.gs`, find and update these settings if needed:

```javascript
// Analytics Configuration (line ~50)
const TRACKING_ENABLED = false; // Set to true to enable analytics
const SPREADSHEET_ID = 'YOUR_GOOGLE_SHEET_ID'; // For analytics logging

// Default settings for animations
const ANIMATION_ENABLED = true; // Anime.js animations
```

#### 2.2 Test the Code
1. In Apps Script, click **"Run"** to test the `doGet` function
2. Authorize the script when prompted
3. Check for any errors in the execution log

### **3. Deploy as Web App**

#### 3.1 Deploy Settings
1. Click **"Deploy"** → **"New deployment"**
2. Click the gear icon next to "Type" and select **"Web app"**
3. Configure deployment settings:
   - **Description**: `"Insight Engine Portal - Enhanced with Animations"`
   - **Execute as**: `"Me (your-email@gmail.com)"`
   - **Who has access**: `"Anyone"` or `"Anyone with the link"`

#### 3.2 Get Deployment URL
1. Click **"Deploy"**
2. Copy the provided Web app URL
3. Save this URL - it's your production endpoint

### **4. Testing & Verification**

#### 4.1 Basic Functionality Test
Test with a Google Drive file URL:
```
https://your-web-app-url/exec?URL=https://drive.google.com/file/d/YOUR_FILE_ID/view
```

#### 4.2 Animation Verification Checklist
✅ **Header shows actual document name** (not "Secure Document Portal")
✅ **"Welcome to Insight Engine" text appears**
✅ **Header scales in with bounce effect**
✅ **Content sections slide up in sequence**
✅ **Buttons appear with staggered timing**
✅ **Sidebars slide in from both sides**
✅ **News items fade in individually**
✅ **Buttons respond to hover with scale effect**
✅ **Click feedback works on buttons**

#### 4.3 Cross-Device Testing
- **Desktop**: Full 3-column layout with all animations
- **Tablet**: 2-column layout (sidebar hidden)
- **Mobile**: Single column with stacked sections

---

## 🎨 **Animation Configuration**

### **Default Animation Sequence**
1. **Header (100ms delay)**: Scale + elastic bounce
2. **File Info (300ms delay)**: Slide up with expo easing
3. **Insight Overview (500ms delay)**: Scale with back easing
4. **Buttons (700ms+ stagger)**: Slide up + scale with 200ms intervals
5. **Sidebars (200ms/400ms delay)**: Slide from sides
6. **News Items (800ms+ stagger)**: Fade in with 100ms intervals

### **Customizing Animations**
To modify animation timing, edit `welcome-template.html`:

```javascript
// Adjust header animation
anime({
    targets: '.header',
    scale: [0.8, 1],           // Scale from 80% to 100%
    duration: 1000,            // Duration in milliseconds
    easing: 'easeOutElastic(1, .6)', // Animation easing
    delay: 100                 // Delay before starting
});

// Modify stagger timing
delay: anime.stagger(200, {start: 700}) // 200ms intervals, start at 700ms
```

### **Disabling Animations**
If you need to disable animations for testing:

```javascript
// At the top of the script section in welcome-template.html
if (typeof anime === 'undefined') {
    console.log('Anime.js not loaded - animations disabled');
    return;
}
```

---

## 📊 **Analytics Setup (Optional)**

### **1. Create Google Sheet**
1. Create a new Google Sheet for analytics
2. Create tabs: `Usage Log`, `Usage_Metrics`, `News Headlines`
3. Copy the sheet ID from the URL

### **2. Enable Analytics**
1. In `code.gs`, update `SPREADSHEET_ID` with your sheet ID
2. Set `TRACKING_ENABLED = true`
3. Deploy the updated version

### **3. Analytics Data**
The system will track:
- Document access attempts
- User interactions
- Error occurrences
- Performance metrics

---

## 🔍 **Troubleshooting**

### **Common Issues**

#### **Animations Not Working**
- Check browser console for anime.js loading errors
- Verify CDN link: `https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js`
- Test on different browsers (Chrome, Firefox, Safari)

#### **Headers Still Show "Secure Document Portal"**
- Verify `{{DOCUMENT_NAME}}` placeholder is in the template
- Check that `loadTemplateSimple()` function is processing correctly
- Test with `testPlaceholderReplacement()` function in Apps Script

#### **File Access Issues**
- Ensure Google Drive file permissions allow public access
- Test with different URL formats
- Check Apps Script execution logs for errors

#### **Mobile Display Problems**
- Verify responsive CSS media queries are working
- Test on actual mobile devices, not just browser resize
- Check that animations scale appropriately

### **Debug Functions**

#### **Test Template Replacement**
Run this function in Apps Script to test placeholder replacement:
```javascript
testPlaceholderReplacement()
```

#### **Check Animation Loading**
Add this to browser console:
```javascript
console.log('Anime.js loaded:', typeof anime !== 'undefined');
```

---

## 🚀 **Production Deployment**

### **Performance Optimization**
- Animations are optimized for 60fps performance
- Staggered timing prevents overwhelming the browser
- Responsive design ensures good performance on all devices

### **Monitoring**
- Monitor Apps Script quotas and usage
- Check execution logs regularly for errors
- Verify animation performance across different browsers

### **Updates & Maintenance**
- Keep anime.js library updated via CDN
- Monitor for Google Apps Script API changes
- Regular testing of core functionality

---

## 📞 **Support**

### **Getting Help**
- Check Apps Script execution logs first
- Test with known working Google Drive files
- Verify all template files are properly uploaded
- Use browser developer tools to debug animations

### **Reporting Issues**
When reporting issues, include:
- Browser type and version
- Device type (desktop/mobile/tablet)
- Specific error messages from console
- Example Google Drive URL that's not working

---

## ✅ **Deployment Checklist**

- [ ] Google Apps Script project created
- [ ] All code files uploaded (`code.gs`, HTML templates)
- [ ] Web app deployed with correct permissions
- [ ] Basic functionality tested with sample file
- [ ] Animation sequence verified
- [ ] Cross-device testing completed
- [ ] Error handling tested
- [ ] Analytics configured (if needed)
- [ ] Performance verified
- [ ] Production URL documented

---

**🎉 Congratulations! Your enhanced Insight Engine with animations is now ready for production use!**

*Last Updated: September 19, 2025*
*Version: 2.0 - Enhanced with Anime.js Animations*
