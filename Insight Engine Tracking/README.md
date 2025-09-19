# Insight Engine Tracking

A sophisticated Google Apps Script web application that provides an enhanced document portal experience with dynamic animations and floating news headlines.

## 🚀 Features

### Core Functionality
- **Dynamic Document Portal**: Displays document names and content dynamically
- **Enhanced User Interface**: Modern design with smooth animations
- **Floating News Container**: Collapsible news headlines with expandable stories
- **Google Search Integration**: Direct search links for news items
- **Responsive Design**: Works seamlessly across desktop and mobile devices

### Animation System
- **Anime.js Integration**: Advanced animations with staggered effects
- **Interactive Elements**: Hover and click animations for buttons
- **Smooth Transitions**: CSS-based transitions for UI elements
- **Loading Animations**: Professional loading states

### News Headlines System
- **Google Sheets Integration**: Real-time news data from external sheets
- **Expandable Stories**: Click headlines to read full articles
- **Share Functionality**: Built-in sharing capabilities
- **Search Integration**: Google search buttons for each headline

## 📁 Project Structure

```
Insight Engine Tracking/
├── code.gs                 # Google Apps Script backend logic
├── welcome-template.html   # Main UI template with animations
└── README.md              # This documentation file
```

## 🛠️ Technical Implementation

### Backend (code.gs)
- Google Apps Script functions for data processing
- Integration with Google Sheets for news data
- Template rendering and data binding

### Frontend (welcome-template.html)
- **HTML Structure**: Semantic markup with accessibility features
- **CSS Styling**: Modern design with glass-morphism effects
- **JavaScript Logic**: 
  - Anime.js animations
  - News container functionality
  - Responsive behavior
  - Google search integration

### Key Technologies
- Google Apps Script
- HTML5/CSS3
- JavaScript (ES6+)
- Anime.js animation library
- CSS Grid and Flexbox
- Google Sheets API integration

## 🎨 Design Features

### Visual Elements
- **Glass-morphism UI**: Semi-transparent containers with backdrop blur
- **Gradient Backgrounds**: Modern color schemes
- **Smooth Animations**: Professional transitions and effects
- **Responsive Layout**: Optimized for all screen sizes

### Interactive Components
- **Animated Buttons**: Hover effects with smooth transitions
- **Collapsible News**: Expandable headlines container
- **Dynamic Headers**: Document-specific titles
- **Loading States**: Professional loading animations

## 📱 Mobile Optimization

- Responsive grid layout
- Touch-friendly interactions
- Optimized font sizes
- Adaptive spacing and padding
- Mobile-specific news container positioning

## 🔧 Configuration

### News Headlines Setup
1. Ensure Google Sheets contains `NEWS_HEADLINES` data
2. Configure `window.templateData.NEWS_HEADLINES` in the backend
3. Headlines should include: `title`, `source`, `date`, `summary`, `fullStory`

### Animation Settings
- Customizable anime.js parameters
- Adjustable timing and easing functions
- Configurable stagger effects

## 🚀 Deployment

1. **Google Apps Script Setup**:
   - Upload `code.gs` to Google Apps Script
   - Configure necessary permissions
   - Set up web app deployment

2. **Template Configuration**:
   - Ensure `welcome-template.html` is properly linked
   - Configure data sources for news integration
   - Test responsive behavior

3. **Testing**:
   - Verify animations work correctly
   - Test news container functionality
   - Confirm mobile responsiveness

## 🔄 Updates & Maintenance

### Recent Enhancements
- Added floating news headlines container
- Integrated anime.js for smooth animations
- Improved responsive design
- Enhanced user interface elements
- Added Google search integration

### Performance Optimizations
- Optimized CSS animations
- Efficient JavaScript execution
- Responsive image handling
- Clean, semantic HTML structure

## 📊 Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

This is a production system. Any modifications should be:
1. Thoroughly tested
2. Documented
3. Reviewed for performance impact
4. Compatible with existing functionality

---

**Last Updated**: September 2025  
**Version**: Production  
**Status**: Active Development