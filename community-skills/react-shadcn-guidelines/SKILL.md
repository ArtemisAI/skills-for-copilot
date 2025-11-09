---
name: react-shadcn-guidelines
description: React + shadcn/ui + Tailwind CSS v4 development patterns. Modern React with Suspense, lazy loading, shadcn components, Tailwind v4 styling, TanStack Query/Router, file organization, performance optimization, and TypeScript best practices. Use when creating components, pages, styling with Tailwind, using shadcn/ui, or working with frontend code.
---

# React + shadcn/ui + Tailwind v4 Guidelines

## Purpose

Modern React development emphasizing shadcn/ui components, Tailwind CSS v4 styling, Suspense-based patterns, and best practices for building maintainable frontend applications.

## When to Use This Skill

Automatically activates when working on:
- Creating React components or pages
- Using shadcn/ui components
- Styling with Tailwind CSS v4
- Fetching data with TanStack Query
- Setting up routing with TanStack Router
- Organizing frontend code
- Performance optimization
- TypeScript in React projects

---

## Quick Start

### New Component Checklist

- [ ] Use `React.FC<Props>` pattern with TypeScript
- [ ] Import shadcn components from `@/components/ui/`
- [ ] Style with Tailwind v4 classes via `className`
- [ ] Use `cn()` utility for conditional classes
- [ ] Lazy load if heavy: `React.lazy(() => import())`
- [ ] Wrap in `<Suspense>` for loading states
- [ ] Use `useSuspenseQuery` for data fetching
- [ ] Import aliases: `@/`, `~types`, `~components`
- [ ] Use `useCallback` for event handlers passed to children
- [ ] Default export at bottom
- [ ] NO MUI, NO inline styles, NO CSS-in-JS

### New Feature Checklist

- [ ] Create `features/{feature-name}/` directory
- [ ] Subdirectories: `api/`, `components/`, `hooks/`, `helpers/`, `types/`
- [ ] API service: `api/{feature}Api.ts`
- [ ] TypeScript types in `types/`
- [ ] Route: `routes/{feature-name}/index.tsx`
- [ ] Lazy load feature components
- [ ] Use Suspense boundaries
- [ ] Export public API from `index.ts`

---

## Core Principles (7 Key Rules)

### 1. shadcn Components ONLY for UI

```typescript
// ✅ ALWAYS: shadcn components
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent } from "@/components/ui/dialog"

// ❌ NEVER: MUI or other libraries
import { Button } from '@mui/material' // BLOCKED!
```

### 2. Tailwind v4 for ALL Styling

```typescript
// ✅ ALWAYS: className with Tailwind
<div className="flex items-center gap-4 p-4 bg-background">

// ❌ NEVER: Inline styles or CSS-in-JS
<div style={{ display: 'flex' }}>  // BLOCKED!
<div sx={{ p: 2 }}>               // BLOCKED!
```

### 3. Use cn() Utility for Conditional Classes

```typescript
import { cn } from "@/lib/utils"

<Button className={cn(
  "bg-primary text-white",
  isActive && "ring-2 ring-offset-2",
  disabled && "opacity-50 cursor-not-allowed"
)}>
```

### 4. Lazy Load Heavy Components

```typescript
const DataGrid = React.lazy(() => import('./DataGrid'));

<Suspense fallback={<LoadingSpinner />}>
  <DataGrid />
</Suspense>
```

### 5. useSuspenseQuery for Data Fetching

```typescript
const { data } = useSuspenseQuery({
  queryKey: ['users'],
  queryFn: () => api.getUsers()
});
```

### 6. No Early Returns with Loading Spinners

```typescript
// ❌ NEVER - causes layout shift
if (isLoading) return <Spinner />;

// ✅ ALWAYS - consistent layout
<Suspense fallback={<Spinner />}>
  <Content />
</Suspense>
```

### 7. Organize by Features, Not Types

```
features/
  users/
    api/, components/, hooks/, types/
```

---

## Common Imports Cheatsheet

```typescript
// React & Lazy Loading
import React, { useState, useCallback, useMemo } from 'react';
const Heavy = React.lazy(() => import('./Heavy'));

// shadcn/ui Components
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardContent } from "@/components/ui/card"
import { Dialog, DialogTrigger, DialogContent } from "@/components/ui/dialog"
import { Form, FormField, FormItem, FormLabel } from "@/components/ui/form"

// Utilities
import { cn } from "@/lib/utils"

// TanStack Query (Suspense)
import { useSuspenseQuery, useQueryClient } from '@tanstack/react-query';

// TanStack Router
import { createFileRoute } from '@tanstack/react-router';

// Types
import type { User } from '~types/user';
```

---

## Quick Reference

### shadcn Component Installation

```bash
# Install individual components (copy-paste model)
npx shadcn@latest add button
npx shadcn@latest add dialog
npx shadcn@latest add form
npx shadcn@latest add card
```

### Tailwind v4 Common Patterns

| Pattern | Tailwind Classes |
|---------|-----------------|
| Flex container | `flex items-center justify-between gap-4` |
| Grid layout | `grid grid-cols-1 md:grid-cols-3 gap-4` |
| Responsive text | `text-sm md:text-base lg:text-lg` |
| Card padding | `p-4 md:p-6` |
| Button | `px-4 py-2 rounded-md bg-primary text-white` |
| Dark mode | `bg-background text-foreground` (uses CSS vars) |

### Import Aliases

| Alias | Resolves To | Example |
|-------|-------------|---------|
| `@/` | `src/` | `import { Button } from '@/components/ui/button'` |
| `~types` | `src/types` | `import type { User } from '~types/user'` |
| `~components` | `src/components` | `import { Header } from '~components/Header'` |

---

## Topic Guides

### 🎨 Component Patterns
**Modern React components with shadcn**
- `React.FC<Props>` for type safety
- `React.lazy()` for code splitting
- Suspense for loading states
- Component structure best practices

**[📖 Complete Guide: resources/component-patterns.md](resources/component-patterns.md)**

---

### 🎭 shadcn/ui Components
**Component catalog and usage patterns**
- Installation and setup
- Button, Dialog, Form, Card, etc.
- Composition patterns
- Customization with Tailwind
- Accessibility features

**[📖 Complete Guide: resources/shadcn-components.md](resources/shadcn-components.md)**

---

### 🎨 Tailwind v4 Styling
**Modern utility-first CSS with v4 features**
- CSS variables for theming
- Responsive design patterns
- Dark mode implementation
- Component styling strategies
- Performance best practices

**[📖 Complete Guide: resources/tailwind-v4-styling.md](resources/tailwind-v4-styling.md)**

---

### 📊 Data Fetching
**TanStack Query with Suspense**
- useSuspenseQuery pattern
- Cache-first strategy
- API service layer
- Mutation patterns

**[📖 Complete Guide: resources/data-fetching.md](resources/data-fetching.md)**

---

### 📁 File Organization
**Features-based structure**
- features/ vs components/
- Feature subdirectories (api/, components/, hooks/)
- Import organization
- Barrel exports

**[📖 Complete Guide: resources/file-organization.md](resources/file-organization.md)**

---

### ⏳ Loading & Error States
**Suspense and error boundaries**
- No early returns rule
- SuspenseLoader pattern
- Error handling
- User feedback with toast

**[📖 Complete Guide: resources/loading-and-error-states.md](resources/loading-and-error-states.md)**

---

### 🛣️ Routing
**TanStack Router patterns**
- File-based routing
- Lazy loaded routes
- Route loaders
- Breadcrumb data

**[📖 Complete Guide: resources/routing-guide.md](resources/routing-guide.md)**

---

### ⚡ Performance
**Optimization patterns**
- useMemo for expensive computations
- useCallback for event handlers
- React.memo for expensive components
- Debounced search
- Memory leak prevention

**[📖 Complete Guide: resources/performance.md](resources/performance.md)**

---

### 📘 TypeScript
**TypeScript standards**
- Strict mode, no `any`
- Explicit return types
- Type imports
- Component prop interfaces

**[📖 Complete Guide: resources/typescript-standards.md](resources/typescript-standards.md)**

---

### 🔧 Common Patterns
**React Hook Form, dialogs, and more**
- Forms with shadcn Form components
- Dialog patterns
- Authentication hooks
- Data grid integration

**[📖 Complete Guide: resources/common-patterns.md](resources/common-patterns.md)**

---

### 📚 Complete Examples
**Full working examples**
- Modern component with all patterns
- shadcn form example
- Data fetching with Suspense
- Feature structure
- Route with lazy loading

**[📖 Complete Guide: resources/complete-examples.md](resources/complete-examples.md)**

---

## Navigation Guide

| Need to... | Read this resource |
|------------|-------------------|
| Create a component | [component-patterns.md](resources/component-patterns.md) |
| Use shadcn components | [shadcn-components.md](resources/shadcn-components.md) |
| Style with Tailwind v4 | [tailwind-v4-styling.md](resources/tailwind-v4-styling.md) |
| Fetch data | [data-fetching.md](resources/data-fetching.md) |
| Organize files/folders | [file-organization.md](resources/file-organization.md) |
| Handle loading/errors | [loading-and-error-states.md](resources/loading-and-error-states.md) |
| Set up routing | [routing-guide.md](resources/routing-guide.md) |
| Optimize performance | [performance.md](resources/performance.md) |
| TypeScript types | [typescript-standards.md](resources/typescript-standards.md) |
| Forms/Dialogs/Auth | [common-patterns.md](resources/common-patterns.md) |
| See full examples | [complete-examples.md](resources/complete-examples.md) |

---

## Quick Reference: File Structure

```
src/
  features/
    users/
      api/
        userApi.ts            # API service
      components/
        UserProfile.tsx       # Main component
        UserList.tsx          # Related components
        UserCard.tsx          # Sub-components
      hooks/
        useUser.ts            # Custom hooks
        useSuspenseUser.ts    # Suspense hooks
      helpers/
        userHelpers.ts        # Utilities
      types/
        index.ts              # TypeScript types
      index.ts                # Public exports

  components/
    ui/
      button.tsx              # shadcn button
      card.tsx                # shadcn card
      dialog.tsx              # shadcn dialog
      form.tsx                # shadcn form
    LoadingSpinner/
      LoadingSpinner.tsx      # Reusable loader
    Header/
      Header.tsx              # Reusable header

  routes/
    users/
      index.tsx               # Route component
      $userId/
        index.tsx             # Dynamic route
```

---

## Anti-Patterns to Avoid

❌ MUI or other component libraries (use shadcn only)
❌ Inline styles with `style={{}}` (use Tailwind classes)
❌ CSS-in-JS (makeStyles, styled-components, emotion)
❌ Early returns with loading spinners (use Suspense)
❌ `sx` prop (MUI pattern - use className)
❌ CSS modules (use Tailwind)
❌ Global CSS (except for Tailwind base/utilities)

---

## Modern Component Template (Quick Copy)

```typescript
import React, { useState, useCallback } from 'react';
import { useSuspenseQuery } from '@tanstack/react-query';
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardContent } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import { featureApi } from '../api/featureApi';
import type { FeatureData } from '~types/feature';

interface MyComponentProps {
  id: number;
  className?: string;
  onAction?: () => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({
  id,
  className,
  onAction
}) => {
  const [isActive, setIsActive] = useState(false);

  const { data } = useSuspenseQuery({
    queryKey: ['feature', id],
    queryFn: () => featureApi.getFeature(id),
  });

  const handleAction = useCallback(() => {
    setIsActive(prev => !prev);
    onAction?.();
  }, [onAction]);

  return (
    <Card className={cn("p-4", className)}>
      <CardHeader>
        <h2 className="text-lg font-semibold">{data.title}</h2>
      </CardHeader>
      <CardContent>
        <Button
          onClick={handleAction}
          className={cn(
            "bg-primary text-white",
            isActive && "ring-2 ring-offset-2"
          )}
        >
          {isActive ? 'Active' : 'Inactive'}
        </Button>
      </CardContent>
    </Card>
  );
};

export default MyComponent;
```

---

## Related Skills

- **error-tracking**: Sentry error tracking (applies to frontend)
- **skill-developer**: Meta-skill for creating skills

---

**Skill Status**: Modular structure following showcase pattern ✅
**Line Count**: < 400 (following 500-line rule) ✅
**Progressive Disclosure**: 10 resource files for deep dives ✅
