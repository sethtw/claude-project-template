---
name: ux-workflow-analysis
description: UI/UX analysis, user journey, workflow validation, z-index issues, layout problems, accessibility, responsive design
allowed-tools: Read, Grep, Glob, WebFetch
model: sonnet
---

# UX Workflow Analysis Skill

> Walk through user interactions to identify UI/UX issues.

## When Activated

User mentions: "user workflow", "user journey", "UI issues", "UX review", "layout problems", "z-index", "responsive", "mobile", "accessibility", "a11y", "interaction flow"

## Analysis Categories

### 1. Visual Layer Issues

#### Z-Index Scale
```css
--z-dropdown: 100;
--z-sticky: 200;
--z-modal-backdrop: 300;
--z-modal: 400;
--z-tooltip: 500;
--z-toast: 600;
```

#### Overflow Conflicts
```css
/* Problem: Dropdown clipped */
.container { overflow: hidden; }
.dropdown { position: absolute; } /* Clipped! */
```

### 2. Interaction Issues

#### Click Target Sizes
```css
/* Minimum touch target: 44x44px */
.button {
  min-width: 44px;
  min-height: 44px;
}
```

#### Focus Management
```typescript
useEffect(() => {
  if (isOpen) {
    modalRef.current?.querySelector('button')?.focus();
  }
}, [isOpen]);
```

### 3. Accessibility Issues

#### Color Contrast
WCAG AA requires 4.5:1 for normal text, 3:1 for large text.

#### Keyboard Navigation
```typescript
<div
  role="button"
  tabIndex={0}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') handleClick();
  }}
>
```

### 4. Responsive Design

#### Touch vs Hover
```css
@media (hover: hover) {
  .card:hover .actions { display: block; }
}
@media (hover: none) {
  .card .actions { display: block; }
}
```

## Used By

### Commands
- `/architect` - UX planning
- `/review` - Quick UX scan
- `/code-review` - Comprehensive review

### Agents
- **analyzer** - Component analysis

## Integration

- Uses sonnet for pattern analysis
- References testing.md for E2E patterns
- Focus on user experience first
