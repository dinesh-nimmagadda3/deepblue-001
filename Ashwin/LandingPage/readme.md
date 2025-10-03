# Ashwin Pillai - Portfolio Website

Hey there! 👋

Welcome to my personal portfolio repository. I'm Ashwin Pillai, an AI & Automation Engineer who loves building intelligent systems that make life easier and businesses more efficient.

This is a modern, single-page portfolio website that I've built to showcase my journey in AI, automation, and software development. It's crafted with vanilla HTML, CSS, and JavaScript - keeping things simple, fast, and easy to customize.

Feel free to fork this repo, use it as inspiration, or reach out if you want to chat about AI, automation, or cool tech projects!

## 🚀 Features

- **Responsive Design**: Fully responsive layout that works on all devices
- **Modern UI/UX**: Dark theme with gradient accents and glassmorphism effects
- **Smooth Animations**: Fade-in effects and smooth scrolling throughout
- **Interactive Elements**: Hover effects and animated components
- **Performance Optimized**: Pure vanilla JavaScript, no dependencies
- **SEO Ready**: Proper meta tags and semantic HTML structure

## 📋 Sections

1. **Hero Section**: Introduction with call-to-action buttons
2. **Stats Section**: Key achievements and metrics
3. **Experience**: Professional background at TCS
4. **Projects**: Featured projects and work samples
5. **Skills**: Technical toolkit organized by category
6. **Contact**: Social media links and contact information

## 🛠️ Setup & Deployment

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/yourusername.github.io.git
cd yourusername.github.io
```

2. Open `index.html` in your browser:
```bash
# On macOS
open index.html

# On Linux
xdg-open index.html

# On Windows
start index.html
```

### Deploy to GitHub Pages

1. Create a new repository named `yourusername.github.io` (replace `yourusername` with your actual GitHub username)

2. Push your code:
```bash
git init
git add .
git commit -m "Initial commit: Portfolio website"
git branch -M main
git remote add origin https://github.com/yourusername/yourusername.github.io.git
git push -u origin main
```

3. Enable GitHub Pages:
   - Go to repository Settings
   - Navigate to "Pages" section
   - Under "Source", select "main" branch
   - Click "Save"

4. Your site will be live at `https://yourusername.github.io` within a few minutes!

## ✏️ Customization

### Update Personal Information

Open `index.html` and modify the following sections:

#### Social Media Links (Line ~550+)
```html
<a href="https://github.com/yourusername" class="social-link" title="GitHub">⚡</a>
<a href="https://linkedin.com/in/yourusername" class="social-link" title="LinkedIn">💼</a>
<a href="mailto:your.email@example.com" class="social-link" title="Email">📧</a>
<a href="https://twitter.com/yourusername" class="social-link" title="Twitter">🐦</a>
```

Replace:
- `yourusername` with your actual GitHub/LinkedIn/Twitter username
- `your.email@example.com` with your email address

#### Meta Tags (Optional)
Add these in the `<head>` section for better SEO:
```html
<meta name="description" content="Ashwin Pillai - AI & Automation Engineer specializing in RPA, GenAI, and enterprise automation solutions">
<meta name="keywords" content="AI Engineer, Automation, RPA, GenAI, LangChain, Python Developer">
<meta name="author" content="Ashwin Pillai">
```

### Color Scheme

Modify the CSS variables in the `:root` section (around line 14):
```css
:root {
    --primary: #6366f1;      /* Primary color (Indigo) */
    --secondary: #8b5cf6;    /* Secondary color (Purple) */
    --accent: #ec4899;       /* Accent color (Pink) */
    --dark: #0f172a;         /* Background dark */
    --light: #f1f5f9;        /* Light text/background */
    --text: #334155;         /* Text color */
}
```

### Add New Projects

Find the projects grid section (around line 330) and add:
```html
<div class="project-card">
    <h3>Your Project Name</h3>
    <p>
        Project description goes here.
    </p>
</div>
```

### Add New Skills

Find the skills section (around line 380) and add new categories or tags:
```html
<div class="skill-category">
    <h3>Category Name</h3>
    <div class="skill-tags">
        <span class="skill-tag">Skill 1</span>
        <span class="skill-tag">Skill 2</span>
    </div>
</div>
```

## 🎨 Design Philosophy

This portfolio follows modern web design principles:
- **Dark Mode First**: Reduces eye strain and looks professional
- **Gradient Accents**: Creates visual interest without overwhelming
- **Glassmorphism**: Adds depth with frosted glass effects
- **Micro-interactions**: Subtle animations enhance user engagement
- **Minimalist Approach**: Clean, focused content presentation

## 📱 Browser Support

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🔧 Technology Stack

- **HTML5**: Semantic markup
- **CSS3**: Custom properties, Grid, Flexbox, animations
- **Vanilla JavaScript**: Smooth scrolling, intersection observers
- **No frameworks**: Fast loading, no dependencies

## 📈 Performance

- **Lightweight**: Single HTML file (~20KB)
- **Fast Loading**: No external dependencies
- **Optimized Animations**: GPU-accelerated transforms
- **Lazy Loading**: Elements fade in as you scroll

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Connect

- **GitHub**: [github.com/yourusername](https://github.com/yourusername)
- **LinkedIn**: [linkedin.com/in/yourusername](https://linkedin.com/in/yourusername)
- **Email**: your.email@example.com

---

Built with ❤️ by Ashwin Pillai | AI & Automation Engineer
