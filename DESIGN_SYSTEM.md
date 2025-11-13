# Health Care - Professional Design System

## 🎨 Design Overview

A modern, professional medical UI design system with a clean, trustworthy aesthetic perfect for healthcare applications.

## Color Palette

### Primary Colors (Medical Blue)
- **Primary 500**: `#1677ff` - Main brand color
- **Primary 600**: `#0958d9` - Hover states
- **Primary 700**: `#003eb3` - Active states

### Accent Colors (Medical Green)
- **Accent 500**: `#2cbd69` - Success, wellness
- **Accent 600**: `#24a557` - Hover states
- **Accent 700**: `#1d8d45` - Active states

### Neutral Colors
- **Gray 50-900**: Complete grayscale for text and backgrounds
- **White**: `#ffffff` - Cards and surfaces

### Semantic Colors
- **Success**: `#10b981` - Positive actions
- **Warning**: `#f59e0b` - Caution
- **Error**: `#ef4444` - Errors and alerts
- **Info**: `#3b82f6` - Information

## Typography

### Font Family
- **Primary**: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
- **Display**: Inter (for headings)

### Font Sizes
- **H1**: 2.5rem (40px)
- **H2**: 2rem (32px)
- **H3**: 1.5rem (24px)
- **Body**: 1rem (16px)
- **Small**: 0.875rem (14px)

### Font Weights
- **Regular**: 400
- **Medium**: 600
- **Bold**: 700
- **Extra Bold**: 800

## Components

### Buttons
- **Primary**: Gradient blue, white text
- **Secondary**: White background, blue border
- **Success**: Gradient green, white text
- **Outline**: Transparent, gray border

**Sizes**:
- Small: 8px 16px padding
- Medium: 12px 24px padding (default)
- Large: 16px 32px padding

### Cards
- **Background**: White
- **Border Radius**: 16px (large), 10px (medium)
- **Shadow**: Soft elevation shadows
- **Border**: 1px solid gray-100
- **Hover**: Lift effect with increased shadow

### Forms
- **Input Height**: 48px
- **Border**: 2px solid gray-300
- **Focus**: Blue border with light blue glow
- **Border Radius**: 10px

### Navigation
- **Background**: White with blur effect
- **Height**: Auto (responsive)
- **Sticky**: Yes
- **Shadow**: Subtle bottom shadow

## Layout

### Container Widths
- **Small**: 640px
- **Medium**: 960px
- **Large**: 1280px (default)

### Spacing Scale
- **XS**: 4px
- **SM**: 8px
- **MD**: 16px
- **LG**: 24px
- **XL**: 32px
- **2XL**: 48px

### Grid System
- **Columns**: 1, 2, 3, 4 (responsive)
- **Gap**: 24px (default)

## Shadows

- **SM**: Subtle shadow for small elements
- **MD**: Standard card shadow
- **LG**: Elevated card shadow
- **XL**: High elevation shadow
- **2XL**: Maximum elevation

## Border Radius

- **SM**: 6px
- **MD**: 10px
- **LG**: 16px
- **XL**: 24px
- **Full**: 9999px (pills/circles)

## Animations

### Transitions
- **Duration**: 0.2s - 0.3s
- **Easing**: ease, ease-out, ease-in-out

### Keyframes
- **Fade In**: Opacity + translateY
- **Slide In**: translateX
- **Pulse**: Opacity oscillation
- **Shimmer**: Gradient animation

## Page-Specific Styles

### Login Page
- Full-screen gradient background (purple gradient)
- Centered card with brand logo
- Password toggle functionality
- Smooth animations

### Home Page
- Hero section with gradient background
- Feature grid with hover effects
- Quick stats section
- CTA section with gradient

### Dashboard
- Wellness score ring with animation
- Stats cards with icons
- Recent consultations list
- Quick action buttons
- Two-column responsive layout

### Symptom Checker
- Checkbox grid for symptoms
- Visual feedback on selection
- Results with condition matching
- Urgency alerts
- Specialist recommendations

## Responsive Breakpoints

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

### Mobile Optimizations
- Single column layouts
- Stacked navigation
- Full-width buttons
- Reduced padding and font sizes

## Accessibility

- **Color Contrast**: WCAG AA compliant
- **Focus States**: Visible focus indicators
- **Keyboard Navigation**: Full support
- **Screen Readers**: Semantic HTML

## Best Practices

1. **Consistency**: Use design tokens (CSS variables)
2. **Spacing**: Follow the spacing scale
3. **Colors**: Use semantic color names
4. **Typography**: Maintain hierarchy
5. **Shadows**: Use appropriate elevation
6. **Animations**: Keep subtle and purposeful
7. **Responsive**: Mobile-first approach
8. **Performance**: Optimize images and animations

## Usage Examples

### Button
```html
<button class="btn btn-primary">Primary Action</button>
<button class="btn btn-secondary">Secondary Action</button>
<button class="btn btn-success btn-lg">Large Success</button>
```

### Card
```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Title</h3>
    <p class="card-subtitle">Subtitle</p>
  </div>
  <div class="card-body">
    Content here
  </div>
  <div class="card-footer">
    <button class="btn btn-primary">Action</button>
  </div>
</div>
```

### Form
```html
<div class="form-group">
  <label class="form-label">Email</label>
  <input type="email" class="form-input" placeholder="Enter email">
  <p class="form-help">We'll never share your email</p>
</div>
```

### Grid
```html
<div class="grid grid-cols-3 gap-4">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>
```

## Future Enhancements

- Dark mode support
- Additional color themes
- More component variants
- Animation library
- Icon system
- Illustration set
