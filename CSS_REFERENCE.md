# CSS Quick Reference Guide

## File Structure

```
app/static/css/
├── main.css                 # Core layout, sidebar, navbar, dashboard
├── glassmorphism.css        # Glass effects and variants
├── animations.css           # Animation keyframes and effects
├── stats-cards.css          # Statistics card components
├── modern-components.css    # Buttons, forms, tables, modals
└── utilities.css            # Helper classes
```

## Color Variables

### Primary Colors
```css
var(--primary)           /* #6366f1 - Indigo 500 */
var(--primary-dark)      /* #4f46e5 - Indigo 600 */
var(--primary-light)     /* #818cf8 - Indigo 400 */
var(--secondary)         /* #8b5cf6 - Violet 500 */
var(--success)           /* #10b981 - Emerald 500 */
var(--warning)           /* #f59e0b - Amber 500 */
var(--danger)            /* #ef4444 - Red 500 */
var(--info)              /* #3b82f6 - Blue 500 */
var(--purple)            /* #a855f7 - Purple 500 */
```

### Background Colors
```css
var(--bg-primary)        /* Main background */
var(--bg-secondary)      /* Secondary background */
var(--bg-card)           /* Card background */
```

### Text Colors
```css
var(--text-primary)      /* Primary text */
var(--text-secondary)    /* Secondary text */
var(--text-muted)        /* Muted text */
```

### Other
```css
var(--border-color)      /* Border color */
var(--shadow-color)      /* Shadow color */
var(--shadow-lg)         /* Large shadow color */
```

## Spacing Variables

```css
var(--spacing-xs)        /* 0.5rem */
var(--spacing-sm)        /* 0.75rem */
var(--spacing-md)        /* 1rem */
var(--spacing-lg)        /* 1.5rem */
var(--spacing-xl)        /* 2rem */
```

## Border Radius

```css
var(--radius-sm)         /* 10px */
var(--radius-md)         /* 14px */
var(--radius-lg)         /* 18px */
var(--radius-xl)         /* 24px */
```

## Transitions

```css
var(--transition-fast)   /* 0.2s cubic-bezier(0.4, 0, 0.2, 1) */
var(--transition-normal) /* 0.3s cubic-bezier(0.4, 0, 0.2, 1) */
var(--transition-slow)   /* 0.5s cubic-bezier(0.4, 0, 0.2, 1) */
```

## Common Classes

### Text Utilities
```html
<h1 class="text-gradient">Gradient text</h1>
<p class="text-shadow">Text with shadow</p>
<span class="font-weight-800">Extra bold</span>
<span class="font-weight-900">Black weight</span>
```

### Background Utilities
```html
<div class="bg-gradient-primary">Primary gradient</div>
<div class="bg-gradient-success">Success gradient</div>
<div class="bg-gradient-danger">Danger gradient</div>
```

### Shadow Utilities
```html
<div class="shadow-sm-custom">Small shadow</div>
<div class="shadow-md-custom">Medium shadow</div>
<div class="shadow-lg-custom">Large shadow</div>
<div class="shadow-xl-custom">Extra large shadow</div>
```

### Hover Effects
```html
<div class="hover-lift">Lifts on hover</div>
<div class="hover-scale">Scales on hover</div>
<div class="hover-glow">Glows on hover</div>
```

### Icon Wrappers
```html
<div class="icon-wrapper">
    <i class="bi bi-check"></i>
</div>
<div class="icon-wrapper-sm">Small icon</div>
<div class="icon-wrapper-lg">Large icon</div>
```

### Status Indicators
```html
<span class="status-dot success"></span> Active
<span class="status-dot warning"></span> Pending
<span class="status-dot danger"></span> Error
<span class="status-dot info"></span> Info
```

### Loading States
```html
<div class="skeleton-loader" style="height: 20px;"></div>
<div class="pulse-animation">Pulsing content</div>
```

### Flex Utilities
```html
<div class="flex-center">Centered content</div>
<div class="flex-between">Space between</div>
<div class="flex-start">Flex start</div>
<div class="flex-end">Flex end</div>
```

### Grid Utilities
```html
<div class="grid-auto-fit">Auto-fit grid</div>
<div class="grid-auto-fill">Auto-fill grid</div>
```

## Component Classes

### Buttons
```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-outline-primary">Outline</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-lg">Large</button>
<button class="btn btn-sm">Small</button>
```

### Cards
```html
<div class="card glass-card">
    <div class="card-header">Header</div>
    <div class="card-body">Body</div>
    <div class="card-footer">Footer</div>
</div>
```

### Badges
```html
<span class="badge bg-primary">Primary</span>
<span class="badge bg-success">Success</span>
<span class="badge bg-danger">Danger</span>
<span class="badge bg-warning">Warning</span>
```

### Alerts
```html
<div class="alert alert-success">Success message</div>
<div class="alert alert-danger">Error message</div>
<div class="alert alert-warning">Warning message</div>
<div class="alert alert-info">Info message</div>
```

### Forms
```html
<div class="form-group">
    <label class="form-label">Label</label>
    <input type="text" class="form-control">
    <small class="form-text">Helper text</small>
</div>
```

### Tables
```html
<table class="table table-striped table-hover">
    <thead>
        <tr><th>Header</th></tr>
    </thead>
    <tbody>
        <tr><td>Data</td></tr>
    </tbody>
</table>
```

## Glass Effects

```html
<div class="glass">Standard glass</div>
<div class="glass-card">Glass card</div>
<div class="glass-dark">Dark glass</div>
<div class="glass-light">Light glass</div>
<div class="glass-form">Glass form</div>
<div class="glass-table">Glass table</div>
```

## Animation Classes

```html
<div class="fade-in">Fade in</div>
<div class="slide-in-left">Slide from left</div>
<div class="slide-in-right">Slide from right</div>
<div class="scale-in">Scale in</div>
<div class="pulse">Pulse animation</div>
<div class="bounce">Bounce animation</div>
<div class="floating">Floating animation</div>
```

## AOS Attributes

```html
<div data-aos="fade-up">Fade up on scroll</div>
<div data-aos="fade-down">Fade down on scroll</div>
<div data-aos="fade-left">Fade from left</div>
<div data-aos="fade-right">Fade from right</div>
<div data-aos="zoom-in">Zoom in on scroll</div>
<div data-aos="flip-up">Flip up on scroll</div>

<!-- With delay -->
<div data-aos="fade-up" data-aos-delay="100">Delayed</div>
<div data-aos="fade-up" data-aos-delay="200">More delayed</div>
```

## Responsive Classes

### Bootstrap Breakpoints
```
xs: < 576px   (mobile)
sm: ≥ 576px   (mobile landscape)
md: ≥ 768px   (tablet)
lg: ≥ 992px   (desktop)
xl: ≥ 1200px  (large desktop)
xxl: ≥ 1400px (extra large)
```

### Usage
```html
<div class="d-none d-md-block">Hidden on mobile</div>
<div class="d-block d-md-none">Visible on mobile only</div>
<div class="col-12 col-md-6 col-lg-4">Responsive columns</div>
```

## Custom Scrollbar

Automatically styled for all scrollable elements:
- Width: 10px
- Gradient thumb (primary to secondary)
- Rounded corners
- Hover effect

## Selection Styling

Automatically styled text selection:
- Background: Primary color
- Text: White

## Dark Mode

Toggle between themes:
```javascript
// Automatically handled by theme toggle button
// Stored in localStorage as 'theme'
```

Check current theme:
```javascript
const theme = document.documentElement.getAttribute('data-bs-theme');
// Returns 'light' or 'dark'
```

## Best Practices

### 1. Use CSS Variables
```css
/* Good */
color: var(--primary);

/* Avoid */
color: #6366f1;
```

### 2. Use Utility Classes
```html
<!-- Good -->
<div class="hover-lift shadow-md-custom">

<!-- Avoid -->
<div style="transform: translateY(-4px); box-shadow: ...">
```

### 3. Combine Classes
```html
<button class="btn btn-primary btn-lg hover-lift">
    <i class="bi bi-check"></i> Submit
</button>
```

### 4. Use Semantic HTML
```html
<!-- Good -->
<button class="btn btn-primary">Click</button>

<!-- Avoid -->
<div class="btn btn-primary" onclick="...">Click</div>
```

### 5. Responsive Design
```html
<!-- Always consider mobile first -->
<div class="col-12 col-md-6 col-lg-4">
    <div class="glass-card hover-lift">
        Content
    </div>
</div>
```

## Common Patterns

### Card with Hover Effect
```html
<div class="glass-card hover-lift">
    <div class="card-header">
        <h4><i class="bi bi-star"></i> Title</h4>
    </div>
    <div class="card-body">
        Content here
    </div>
</div>
```

### Gradient Button
```html
<button class="btn btn-primary btn-lg">
    <i class="bi bi-check"></i> Action
</button>
```

### Status Badge
```html
<span class="badge bg-success">
    <span class="status-dot success"></span>
    Active
</span>
```

### Icon with Wrapper
```html
<div class="icon-wrapper">
    <i class="bi bi-check-circle"></i>
</div>
```

### Gradient Text Heading
```html
<h1 class="text-gradient font-weight-900">
    Amazing Title
</h1>
```

## Performance Tips

1. **Use transform and opacity** for animations (hardware accelerated)
2. **Avoid animating** width, height, top, left
3. **Use will-change** sparingly for critical animations
4. **Minimize repaints** by batching DOM changes
5. **Use CSS containment** for isolated components

## Debugging

### Check Theme
```javascript
console.log(document.documentElement.getAttribute('data-bs-theme'));
```

### Check CSS Variables
```javascript
const styles = getComputedStyle(document.documentElement);
console.log(styles.getPropertyValue('--primary'));
```

### Inspect Animations
```javascript
// Check if element has animation
const element = document.querySelector('.my-element');
console.log(getComputedStyle(element).animation);
```

---

**Quick Reference Version**: 1.0  
**Last Updated**: December 2024
