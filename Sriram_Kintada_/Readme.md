# RESA Landing Page

A production-ready landing page for RESA (Research to Startup AI Agent Swarm) - an AI-powered platform that transforms research papers into investor-ready pitch decks.

## Overview

This landing page showcases RESA's capabilities and converts visitors (researchers, investors, entrepreneurs, and university partners) into users and waitlist signups.

**Live Demo Landing Page:** [https://v0-resa-landing-page.vercel.app/]
**Live Demo App:** [https://resa-web.streamlit.app/](https://resa-web.streamlit.app/)

## Features

- Fully responsive design (mobile, tablet, desktop)
- Single-page application with smooth scrolling navigation
- Optimized for conversion with clear CTAs
- Professional color scheme aligned with trust and innovation
- SEO-ready meta tags
- No external dependencies (pure HTML/CSS/JS)
- Fast loading time (under 50KB)

## Quick Start

### Local Development

1. Clone or download the repository
2. Open `index.html` in any modern browser
3. That's it - no build process required

### Testing Locally

```bash
# If you have Python installed
python -m http.server 8000

# If you have Node.js installed
npx serve

# Then visit http://localhost:8000
```

## Deployment Options

### GitHub Pages (Free)

1. Create a new GitHub repository
2. Upload `index.html`
3. Go to Settings > Pages
4. Select main branch as source
5. Your site will be live at `https://yourusername.github.io/repo-name/`

### Netlify (Free)

1. Sign up at [netlify.com](https://netlify.com)
2. Drag and drop the `index.html` file
3. Get instant custom domain: `your-site.netlify.app`

### Vercel (Free)

1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in your project directory
3. Follow prompts to deploy

## Customization Guide

### Update Contact Information

Replace these placeholders in the HTML:

```html
<!-- Line 580: Email -->
<a href="mailto:hello@resa.ai">Contact</a>

<!-- Line 589: LinkedIn -->
<a href="https://linkedin.com/in/sriramkintada" target="_blank">LinkedIn</a>

<!-- Line 590: Email -->
<a href="mailto:kintada.sriram@students.iiserpune.ac.in">Email</a>

<!-- Line 556: GitHub -->
<a href="https://github.com/yourusername/resa" target="_blank">GitHub</a>
```

### Connect Waitlist Form

The form currently shows an alert. To connect to a backend:

**Option 1: Google Sheets (via Apps Script)**
```javascript
fetch('YOUR_GOOGLE_APPS_SCRIPT_URL', {
    method: 'POST',
    body: JSON.stringify(formData)
});
```

**Option 2: Airtable**
```javascript
fetch('https://api.airtable.com/v0/YOUR_BASE/Waitlist', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({fields: formData})
});
```

**Option 3: Email via FormSpree**
Change form action to:
```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```

### Add Analytics

Before closing `</body>` tag, add:

**Google Analytics:**
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Update Colors

Edit CSS variables in the `<style>` section:

```css
:root {
    --primary: #1E3A8A;    /* Main brand color */
    --accent: #14B8A6;     /* Accent/CTA color */
    --dark: #1F2937;       /* Text color */
    --gold: #F59E0B;       /* Badges/highlights */
}
```

## Project Structure

```
resa-landing-page/
├── index.html          # Complete landing page
└── README.md          # This file
```

## Sections Included

1. **Navigation** - Sticky header with smooth scroll links
2. **Hero** - Main value proposition with dual CTAs
3. **Problem** - Statistics showing India's deep tech crisis
4. **Solution** - 5 AI agents explanation
5. **How It Works** - 3-step process
6. **Social Proof** - Hackathon win, testimonials, waitlist count
7. **Waitlist Form** - Email capture for early access
8. **FAQ** - Common questions about IP, cost, accuracy
9. **Footer** - Links, contact, branding

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- First Contentful Paint: < 1s
- Time to Interactive: < 2s
- Total page weight: ~45KB
- No external dependencies to load

## SEO Optimization

The page includes:
- Semantic HTML5 markup
- Meta description tag
- Proper heading hierarchy (H1 > H2 > H3)
- Alt text ready for images (when you add them)
- Mobile-friendly viewport settings

### Recommended additions:

1. Add Open Graph tags for social sharing:
```html
<meta property="og:title" content="RESA - Transform Research into Reality">
<meta property="og:description" content="AI-powered platform connecting researchers, entrepreneurs, and investors">
<meta property="og:image" content="URL_TO_PREVIEW_IMAGE">
```

2. Add Twitter Card tags:
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="RESA - Transform Research into Reality">
```

## Next Steps After Deployment

1. Set up form backend (Google Sheets, Airtable, or email)
2. Add Google Analytics tracking
3. Create and add logo/favicon
4. Take screenshots of the Streamlit app for visual proof
5. Add GDG winner certificate image
6. Set up custom domain (optional)
7. Submit to Product Hunt for visibility

## Maintenance

### Adding Testimonials

Add to the Social Proof section:
```html
<div class="quote">
    "Your testimonial text here"
    <br><strong>— Name, Title</strong>
</div>
```

### Updating Stats

Modify the stats grid in the Problem section:
```html
<div class="stat-card">
    <span class="stat-number">NEW_NUMBER</span>
    <span class="stat-label">Description</span>
</div>
```

## Technical Notes

- No JavaScript frameworks required
- CSS uses modern features (Grid, Flexbox, Custom Properties)
- Graceful degradation for older browsers
- Form uses basic HTML5 validation
- Smooth scroll uses native CSS `scroll-behavior`

## Troubleshooting

**Form not submitting?**
- Check browser console for errors
- Verify form action URL is correct
- Test with a simple alert first

**Styles not loading?**
- Clear browser cache (Ctrl+Shift+R)
- Check for syntax errors in CSS
- Validate HTML at validator.w3.org

**Links not working?**
- Verify all `href` attributes are correct
- Check for typos in anchor IDs
- Test in multiple browsers

## Contact & Support

- **Email:** kintada.sriram@students.iiserpune.ac.in
- **LinkedIn:** [sriramkintada](https://linkedin.com/in/sriramkintada)
- **GitHub:** [Your GitHub Profile]
- **Demo App:** [https://resa-web.streamlit.app/](https://resa-web.streamlit.app/)

## License

This landing page template is provided as-is for the RESA project. Customize freely for your needs.

---

**Built with passion at IISER Pune | Disrupting India's deep tech landscape**

