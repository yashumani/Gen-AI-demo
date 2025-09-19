# Insight Engine Tracking

A sophisticated Google Apps Script web application that provides a comprehensive three-column document portal experience with dynamic animations, content insights, and real-time news integration.

## 🏗️ Three-Column Architecture

The Insight Engine uses a sophisticated three-column layout system:

### 📊 **Center Column - Main Portal** (`welcome-template.html`)
- **Document Information**: Dynamic headers showing actual document names
- **Report Details**: File information, access controls, and metadata
- **Action Buttons**: "Launch Document & Start Analysis" and "Open AI Prompt Generator"
- **Insight Engine Branding**: "Welcome to Insight Engine" messaging
- **Anime.js Animations**: Professional staggered animations and interactive effects

### 📋 **Left Column - Content Overview** (`whats-inside-template.html`)
- **What's Inside Panel**: Detailed breakdown of document contents
- **Content Categorization**: Organized view of document sections
- **Navigation Aid**: Quick access to specific document parts
- **Dynamic Loading**: Content populated based on document type
- **Responsive Design**: Adapts to different document structures

### 📰 **Right Column - News Integration** (Google Sheets Connection)
- **Floating News Container**: Collapsible headlines with expandable stories
- **Real-time Updates**: Direct connection to Google Sheets data source
- **Interactive Features**: Click to expand full stories
- **Google Search Integration**: Direct search links for each headline
- **Share Functionality**: Built-in sharing capabilities
- **Responsive Behavior**: Optimized for mobile and desktop viewing

## 🚀 Features

### Core Functionality
- **Three-Column Layout**: Balanced information architecture
- **Dynamic Document Portal**: Displays document names and content dynamically
- **Enhanced User Interface**: Modern design with smooth animations
- **Content Overview System**: Left panel showing document breakdown
- **News Headlines Integration**: Right panel with real-time news
- **Google Search Integration**: Direct search links for news items
- **Responsive Design**: Works seamlessly across desktop and mobile devices
- **Error Handling**: Comprehensive error management with user-friendly recovery

### Animation System
- **Anime.js Integration**: Advanced animations with staggered effects
- **Interactive Elements**: Hover and click animations for buttons
- **Smooth Transitions**: CSS-based transitions for UI elements
- **Loading Animations**: Professional loading states
- **Column Animations**: Individual animations for each column section

### News Headlines System
- **Google Sheets Integration**: Real-time news data from external sheets
- **Expandable Stories**: Click headlines to read full articles
- **Share Functionality**: Built-in sharing capabilities
- **Search Integration**: Google search buttons for each headline
- **Floating Design**: Non-intrusive overlay that doesn't block content

## 📁 Project Structure

```
Insight Engine Tracking/
├── code.gs                      # Google Apps Script backend logic
├── welcome-template.html        # Main center column with animations & portal
├── whats-inside-template.html   # Left column content overview panel
├── error-template.html          # Error handling and recovery interface
└── README.md                   # This comprehensive documentation
```

## 🛠️ Technical Implementation

### Backend (code.gs)
- Google Apps Script functions for data processing
- Integration with Google Sheets for news data
- Template rendering and data binding
- Three-column layout coordination
- Error handling and recovery systems

### Frontend Templates

#### **Main Portal** (`welcome-template.html`)
- **HTML Structure**: Three-column grid layout with semantic markup
- **CSS Styling**: Modern design with glass-morphism effects
- **JavaScript Logic**: 
  - Anime.js animations coordination
  - News container functionality
  - Responsive behavior management
  - Google search integration
  - Column interaction handling

#### **Content Overview** (`whats-inside-template.html`)
- **Document Breakdown**: Structured content analysis
- **Navigation Elements**: Quick access to document sections
- **Dynamic Loading**: Content adapts to document type
- **Integration**: Seamless coordination with main portal

#### **Error Handling** (`error-template.html`)
- **User-Friendly Error Messages**: Clear problem descriptions
- **Recovery Options**: Actionable steps for users
- **Troubleshooting Guidance**: Built-in diagnostic information
- **Consistent Design**: Matches main portal styling

### Key Technologies
- Google Apps Script
- HTML5/CSS3 with Grid Layout
- JavaScript (ES6+)
- Anime.js animation library
- CSS Grid and Flexbox
- Google Sheets API integration
- Responsive Design Principles

## 🎨 Design Features

### Visual Elements
- **Three-Column Grid**: Balanced information architecture
- **Glass-morphism UI**: Semi-transparent containers with backdrop blur
- **Gradient Backgrounds**: Modern color schemes across all columns
- **Smooth Animations**: Professional transitions and effects
- **Responsive Layout**: Optimized for all screen sizes
- **Consistent Branding**: Unified design language across templates

### Interactive Components
- **Animated Buttons**: Hover effects with smooth transitions
- **Collapsible News**: Expandable headlines container
- **Dynamic Headers**: Document-specific titles
- **Loading States**: Professional loading animations
- **Column Interactions**: Coordinated animations between sections

## 📱 Mobile Optimization

- **Responsive Grid**: Three-column layout adapts to mobile screens
- **Touch-friendly Interactions**: Optimized for mobile gestures
- **Column Stacking**: Intelligent reordering on smaller screens
- **Optimized Font Sizes**: Readable text across all devices
- **Adaptive Spacing**: Mobile-specific padding and margins
- **News Container**: Mobile-optimized floating positioning

## 🔧 Configuration

### Three-Column Setup
1. **Main Portal**: Configure `welcome-template.html` for document handling
2. **Content Overview**: Set up `whats-inside-template.html` for document analysis
3. **News Integration**: Connect Google Sheets data source for news headlines
4. **Error Handling**: Configure `error-template.html` for recovery scenarios

### News Headlines Setup
1. Ensure Google Sheets contains `NEWS_HEADLINES` data
2. Configure `window.templateData.NEWS_HEADLINES` in the backend
3. Headlines should include: `title`, `source`, `date`, `summary`, `fullStory`
4. Set up right-column integration with floating container

### Animation Settings
- Customizable anime.js parameters for each column
- Adjustable timing and easing functions
- Configurable stagger effects between columns
- Responsive animation scaling

## 🚀 Deployment

1. **Google Apps Script Setup**:
   - Upload `code.gs` to Google Apps Script
   - Configure necessary permissions
   - Set up web app deployment

2. **Template Configuration**:
   - Ensure all three templates are properly linked
   - Configure data sources for news integration
   - Test three-column responsive behavior
   - Verify cross-template communication

3. **Testing**:
   - Verify animations work correctly across all columns
   - Test news container functionality
   - Confirm mobile responsiveness for three-column layout
   - Test error handling scenarios

## 🔄 Template Integration

### How the Three Columns Work Together

1. **Center Column (Main)**: 
   - Loads first with document information
   - Triggers loading of left and right columns
   - Coordinates animations across all sections

2. **Left Column (What's Inside)**:
   - Analyzes document content
   - Provides structured overview
   - Links to specific document sections

3. **Right Column (News)**:
   - Loads independently from Google Sheets
   - Provides contextual news updates
   - Operates as floating overlay when needed

### Data Flow
```
Google Sheets (News) → Right Column (Floating Container)
Document Data → Center Column (Main Portal)
Document Analysis → Left Column (Content Overview)
Error Scenarios → Error Template (Full Screen)
```

## 📊 Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

This is a production system with a three-column architecture. Any modifications should be:
1. Thoroughly tested across all three columns
2. Documented with template interactions
3. Reviewed for performance impact
4. Compatible with existing three-column functionality
5. Tested on mobile responsive behavior

---

**Last Updated**: September 2025  
**Version**: Production (Three-Column Architecture)  
**Status**: Active Development