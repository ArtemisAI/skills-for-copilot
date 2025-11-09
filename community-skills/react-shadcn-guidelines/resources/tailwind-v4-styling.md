# Tailwind CSS v4 Styling Guide

## Overview

Tailwind v4 brings powerful features for building modern, maintainable UIs with shadcn/ui components. This guide covers v4-specific patterns, CSS variables, responsive design, and dark mode.

---

## Core Styling Principles

### 1. Always Use className (Never Inline Styles)

```typescript
// ✅ CORRECT - className with Tailwind utilities
<div className="flex items-center gap-4 p-4 bg-background">
  <Button className="px-6 py-2 rounded-md">Click me</Button>
</div>

// ❌ WRONG - inline styles
<div style={{ display: 'flex', gap: '16px', padding: '16px' }}>
  <Button style={{ padding: '8px 24px' }}>Click me</Button>
</div>

// ❌ WRONG - CSS-in-JS (MUI pattern)
<div sx={{ display: 'flex', gap: 2, p: 2 }}>
  <Button sx={{ px: 3, py: 1 }}>Click me</Button>
</div>
```

### 2. Use cn() for Conditional Classes

```typescript
import { cn } from "@/lib/utils"

// Combine base classes with conditional ones
<Button
  className={cn(
    "px-4 py-2 rounded-md transition-colors",
    isPrimary && "bg-primary text-white",
    isDisabled && "opacity-50 cursor-not-allowed",
    isLoading && "animate-pulse"
  )}
>
  Submit
</Button>

// Works great with shadcn components
<Card className={cn(
  "p-6 border shadow-sm",
  isSelected && "ring-2 ring-primary",
  hasError && "border-destructive"
)}>
```

---

## Tailwind v4 CSS Variables

### Theme Colors with CSS Variables

Tailwind v4 integrates seamlessly with shadcn's CSS variable system:

```css
/* globals.css - CSS variables defined */
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 221.2 83.2% 53.3%;
  --primary-foreground: 210 40% 98%;
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  /* ... more variables */
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  /* ... dark mode overrides */
}
```

```typescript
// Use in components via Tailwind classes
<div className="bg-background text-foreground">
  <h1 className="text-primary">Heading</h1>
  <p className="text-muted-foreground">Description</p>
</div>

// These automatically adapt to dark mode!
```

### Custom CSS Variables

Add your own variables when needed:

```css
/* globals.css */
:root {
  --header-height: 64px;
  --sidebar-width: 280px;
  --content-max-width: 1200px;
}
```

```typescript
// Use in arbitrary values
<div className="h-[var(--header-height)]">
<aside className="w-[var(--sidebar-width)]">
<main className="max-w-[var(--content-max-width)]">
```

---

## Responsive Design Patterns

### Mobile-First Breakpoints

Tailwind uses mobile-first breakpoints:

| Breakpoint | Min Width | Example |
|------------|-----------|---------|
| `sm:` | 640px | `sm:text-base` |
| `md:` | 768px | `md:grid-cols-2` |
| `lg:` | 1024px | `lg:px-8` |
| `xl:` | 1280px | `xl:max-w-7xl` |
| `2xl:` | 1536px | `2xl:grid-cols-4` |

### Common Responsive Patterns

#### Responsive Text Sizes
```typescript
<h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold">
  Responsive Heading
</h1>

<p className="text-sm md:text-base lg:text-lg text-muted-foreground">
  Body text that scales with viewport
</p>
```

#### Responsive Layout
```typescript
// Stack on mobile, grid on larger screens
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <Card>Item 1</Card>
  <Card>Item 2</Card>
  <Card>Item 3</Card>
</div>

// Responsive padding
<div className="p-4 md:p-6 lg:p-8">
  Content with responsive spacing
</div>
```

#### Responsive Flexbox
```typescript
// Column on mobile, row on desktop
<div className="flex flex-col md:flex-row gap-4 items-start md:items-center">
  <Avatar className="h-16 w-16 md:h-20 md:w-20" />
  <div className="flex-1">
    <h3 className="text-lg md:text-xl">User Name</h3>
  </div>
</div>
```

#### Show/Hide at Breakpoints
```typescript
// Hide on mobile, show on desktop
<aside className="hidden lg:block w-64">
  Sidebar content
</aside>

// Show on mobile, hide on desktop
<Button className="md:hidden">
  Mobile Menu
</Button>
```

---

## Dark Mode Implementation

### Automatic Dark Mode with CSS Variables

shadcn components automatically support dark mode through CSS variables:

```typescript
// No extra code needed - these adapt automatically!
<Card className="bg-card text-card-foreground">
  <CardHeader>
    <CardTitle className="text-foreground">Title</CardTitle>
    <CardDescription className="text-muted-foreground">
      Description
    </CardDescription>
  </CardHeader>
</Card>
```

### Using dark: Modifier

For custom dark mode styles:

```typescript
<div className="bg-white dark:bg-gray-900">
  <h2 className="text-gray-900 dark:text-gray-100">
    Heading
  </h2>
  <p className="text-gray-700 dark:text-gray-300">
    Body text
  </p>
</div>

// Borders
<div className="border border-gray-200 dark:border-gray-800">

// Shadows
<Card className="shadow-sm dark:shadow-lg">
```

### Dark Mode Toggle Component

```typescript
import { Button } from "@/components/ui/button"
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="hover:bg-muted"
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-transform dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-transform dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  )
}
```

---

## Layout Patterns

### Flexbox Patterns

#### Horizontal Center
```typescript
<div className="flex items-center justify-center">
  <Button>Centered Button</Button>
</div>
```

#### Space Between
```typescript
<div className="flex items-center justify-between">
  <h2>Title</h2>
  <Button>Action</Button>
</div>
```

#### Vertical Stack with Gap
```typescript
<div className="flex flex-col gap-4">
  <Card>Item 1</Card>
  <Card>Item 2</Card>
</div>
```

#### Horizontal List with Gap
```typescript
<div className="flex items-center gap-2">
  <Badge>Tag 1</Badge>
  <Badge>Tag 2</Badge>
  <Badge>Tag 3</Badge>
</div>
```

### Grid Patterns

#### Responsive Grid
```typescript
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
  {items.map(item => (
    <Card key={item.id}>
      {/* Card content */}
    </Card>
  ))}
</div>
```

#### Auto-Fit Grid
```typescript
<div className="grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-4">
  {/* Items automatically wrap */}
</div>
```

#### Dashboard Layout
```typescript
<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
  <Card className="md:col-span-2">
    Main content
  </Card>
  <Card className="md:col-span-1">
    Sidebar
  </Card>
</div>
```

---

## Component Styling Strategies

### shadcn Component Customization

#### Button Variants
```typescript
import { Button } from "@/components/ui/button"

// Use built-in variants
<Button variant="default">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="destructive">Delete</Button>

// Custom styling with className
<Button className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
  Gradient Button
</Button>
```

#### Card Styling
```typescript
import { Card, CardHeader, CardContent } from "@/components/ui/card"

// Default
<Card>
  <CardContent>Content</CardContent>
</Card>

// Custom styling
<Card className="border-2 border-primary shadow-lg hover:shadow-xl transition-shadow">
  <CardHeader className="bg-muted">
    <h3 className="font-semibold">Styled Card</h3>
  </CardHeader>
  <CardContent className="p-6">
    Content with custom padding
  </CardContent>
</Card>
```

### Composing Styles with cn()

```typescript
import { cn } from "@/lib/utils"

interface CustomButtonProps {
  variant?: 'primary' | 'success' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function CustomButton({ variant = 'primary', size = 'md', className }: CustomButtonProps) {
  return (
    <button
      className={cn(
        // Base styles
        "rounded-md font-medium transition-colors focus:outline-none focus:ring-2",
        // Variant styles
        {
          'bg-blue-500 text-white hover:bg-blue-600': variant === 'primary',
          'bg-green-500 text-white hover:bg-green-600': variant === 'success',
          'bg-red-500 text-white hover:bg-red-600': variant === 'danger',
        },
        // Size styles
        {
          'px-3 py-1.5 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        },
        // Allow overrides
        className
      )}
    >
      Button
    </button>
  )
}
```

---

## Spacing and Sizing

### Spacing Scale

Tailwind's spacing scale (1 unit = 0.25rem = 4px):

```typescript
// Padding
<div className="p-4">        {/* 16px all sides */}
<div className="px-6 py-3">  {/* 24px horizontal, 12px vertical */}
<div className="pt-8">       {/* 32px top */}

// Margin
<div className="m-4">        {/* 16px all sides */}
<div className="mx-auto">    {/* Auto horizontal centering */}
<div className="mt-6 mb-4">  {/* 24px top, 16px bottom */}

// Gap (for flex/grid)
<div className="flex gap-4">      {/* 16px gap */}
<div className="grid gap-x-6 gap-y-4">  {/* Different x/y gaps */}
```

### Common Spacing Patterns

```typescript
// Card with consistent padding
<Card className="p-6">
  <h3 className="mb-4">Title</h3>
  <p className="mb-6">Content</p>
  <Button>Action</Button>
</Card>

// Section spacing
<section className="py-12 md:py-16 lg:py-20">
  <div className="container mx-auto px-4">
    <h2 className="mb-8">Section Title</h2>
  </div>
</section>

// Form field spacing
<div className="space-y-4">
  <FormField />
  <FormField />
  <FormField />
</div>
```

---

## Typography

### Text Sizes (Responsive)

```typescript
// Headings
<h1 className="text-4xl md:text-5xl lg:text-6xl font-bold">
  Main Heading
</h1>

<h2 className="text-3xl md:text-4xl font-semibold">
  Section Heading
</h2>

<h3 className="text-2xl md:text-3xl font-medium">
  Subsection
</h3>

// Body text
<p className="text-base md:text-lg leading-relaxed">
  Body paragraph with comfortable line height
</p>

// Small text
<span className="text-sm text-muted-foreground">
  Helper text or captions
</span>
```

### Font Weights

```typescript
<p className="font-thin">     {/* 100 */}
<p className="font-light">    {/* 300 */}
<p className="font-normal">   {/* 400 */}
<p className="font-medium">   {/* 500 */}
<p className="font-semibold"> {/* 600 */}
<p className="font-bold">     {/* 700 */}
<p className="font-extrabold">{/* 800 */}
```

### Text Colors with Theme

```typescript
// Using CSS variable colors
<h1 className="text-foreground">Primary text</h1>
<p className="text-muted-foreground">Secondary text</p>
<span className="text-destructive">Error text</span>
<a className="text-primary hover:underline">Link</a>

// Custom colors
<p className="text-gray-900 dark:text-gray-100">
<p className="text-blue-600 dark:text-blue-400">
```

---

## Performance Best Practices

### 1. Avoid Arbitrary Values When Possible

```typescript
// ✅ GOOD - use Tailwind's scale
<div className="w-64 h-32 p-4">

// ⚠️ OK but less optimal - arbitrary values
<div className="w-[256px] h-[128px] p-[16px]">
```

### 2. Reuse Common Patterns

```typescript
// Create shared classes for common patterns
const cardStyles = "p-6 border border-border rounded-lg shadow-sm bg-card"

<Card className={cardStyles}>
<Card className={cardStyles}>
```

### 3. Use CSS Variables for Dynamic Values

```typescript
// ❌ Avoid inline styles for dynamic values
<div style={{ width: `${width}px` }}>

// ✅ Better - use CSS variables
<div
  className="w-[var(--dynamic-width)]"
  style={{ '--dynamic-width': `${width}px` } as React.CSSProperties}
>
```

### 4. Minimize className Complexity

```typescript
// ❌ Too complex
<div className="flex items-center justify-between p-4 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg shadow-sm hover:shadow-md transition-shadow">

// ✅ Extract to variable or component
const containerClasses = cn(
  "flex items-center justify-between p-4 rounded-lg transition-shadow",
  "bg-card border border-border shadow-sm hover:shadow-md"
)
<div className={containerClasses}>
```

---

## Common Patterns with shadcn

### Form Layout

```typescript
import { Form, FormField, FormItem, FormLabel, FormControl } from "@/components/ui/form"
import { Input } from "@/components/ui/input"

<Form {...form}>
  <form className="space-y-6">
    <FormField
      name="email"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Email</FormLabel>
          <FormControl>
            <Input
              type="email"
              placeholder="you@example.com"
              className="w-full"
              {...field}
            />
          </FormControl>
        </FormItem>
      )}
    />

    <Button type="submit" className="w-full">
      Submit
    </Button>
  </form>
</Form>
```

### Dialog Styling

```typescript
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"

<Dialog>
  <DialogContent className="sm:max-w-[425px]">
    <DialogHeader>
      <DialogTitle className="text-2xl font-semibold">
        Edit Profile
      </DialogTitle>
    </DialogHeader>
    <div className="grid gap-4 py-4">
      {/* Content with consistent spacing */}
    </div>
  </DialogContent>
</Dialog>
```

### Data Grid / List

```typescript
<div className="rounded-md border">
  <Table>
    <TableHeader>
      <TableRow className="bg-muted/50">
        <TableHead className="font-semibold">Name</TableHead>
        <TableHead className="font-semibold">Status</TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      {items.map((item) => (
        <TableRow
          key={item.id}
          className="hover:bg-muted/50 transition-colors"
        >
          <TableCell className="font-medium">{item.name}</TableCell>
          <TableCell>
            <Badge variant={item.status === 'active' ? 'default' : 'secondary'}>
              {item.status}
            </Badge>
          </TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
</div>
```

---

## Migration from Other Systems

### From MUI to Tailwind + shadcn

| MUI Pattern | Tailwind + shadcn Equivalent |
|-------------|------------------------------|
| `<Box sx={{ display: 'flex' }}>` | `<div className="flex">` |
| `<Box sx={{ p: 2 }}>` | `<div className="p-2">` |
| `<Typography variant="h1">` | `<h1 className="text-4xl font-bold">` |
| `<Button variant="contained">` | `<Button variant="default">` |
| `<TextField />` | `<Input />` |
| `<Grid container spacing={2}>` | `<div className="grid gap-2">` |
| `makeStyles()` | `className with Tailwind` |
| `sx` prop | `className` prop |

---

## Anti-Patterns to Avoid

❌ **Inline styles instead of Tailwind classes**
```typescript
// WRONG
<div style={{ display: 'flex', padding: '16px' }}>
```

❌ **CSS-in-JS libraries (emotion, styled-components)**
```typescript
// WRONG
const StyledDiv = styled.div`
  display: flex;
  padding: 16px;
`
```

❌ **MUI sx prop**
```typescript
// WRONG
<Box sx={{ p: 2, display: 'flex' }}>
```

❌ **Creating custom CSS files for one-off styles**
```typescript
// WRONG - separate CSS file
// styles.css
.my-custom-class { padding: 16px; }

// CORRECT - Tailwind utility
<div className="p-4">
```

---

**Resource Status**: Complete Tailwind v4 styling guide ✅
