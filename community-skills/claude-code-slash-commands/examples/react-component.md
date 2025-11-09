# React Component Generator Example

Complete command for generating React components with TypeScript and tests.

## File: `.claude/commands/component.md`

```markdown
---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [component-name] [directory]
description: Generate React component with TypeScript and tests
model: claude-3-5-sonnet-20241022
---

## Component Generation Task

Generate a complete React component with the following specifications:

**Component Name**: $ARGUMENTS (first argument)
**Directory**: $ARGUMENTS (second argument, default: src/components)

## Requirements

### 1. Component Structure
- TypeScript functional component with proper typing
- Props interface with JSDoc comments
- Default export with named export for testing
- Proper file naming convention

### 2. Styling
- CSS Modules or styled-components (detect existing pattern: @src/components/)
- Responsive design considerations
- Accessibility attributes

### 3. Testing
- Jest + React Testing Library test file
- Test component rendering
- Test props handling
- Test user interactions
- Accessibility testing

### 4. Documentation
- JSDoc comments for component and props
- Usage examples in comments
- Prop descriptions

### 5. Best Practices
- Use React hooks appropriately
- Implement proper error boundaries if needed
- Add PropTypes for runtime validation (optional)
- Follow team's coding standards: @.eslintrc.json

## File Structure

Create the following files:
```
[directory]/
├── [ComponentName].tsx
├── [ComponentName].module.css (or .styled.ts)
├── [ComponentName].test.tsx
└── index.ts (barrel export)
```

## Example Component Template

```typescript
import React from 'react';
import styles from './ComponentName.module.css';

/**
 * ComponentName - Brief description
 * @param {Props} props - Component props
 */
interface Props {
  /** Description of prop */
  propName: string;
  /** Optional prop */
  optionalProp?: number;
}

export const ComponentName: React.FC<Props> = ({ 
  propName, 
  optionalProp = 0 
}) => {
  return (
    <div className={styles.container}>
      {/* Component implementation */}
    </div>
  );
};

export default ComponentName;
```

## Testing Template

```typescript
import { render, screen } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('renders without crashing', () => {
    render(<ComponentName propName="test" />);
  });

  it('displays the correct content', () => {
    render(<ComponentName propName="Hello" />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
});
```

After creating files, run:
- !`npm run lint` (if available)
- !`npm test ComponentName` (run tests)
```

## Usage Examples

```bash
# Generate component in default location
/component Button

# Generate in specific directory
/component UserProfile src/features/user

# With nested path
/component Modal src/components/common
```

## Key Features

1. **Complete Setup**: Creates component, styles, tests, and exports
2. **Type Safety**: Full TypeScript support with proper interfaces
3. **Testing Ready**: Includes comprehensive test suite
4. **Documented**: JSDoc comments for better IDE support
5. **Consistent**: Follows team's existing patterns

## Customization Options

Modify the command to support:
- Different styling solutions (Tailwind, Emotion, etc.)
- Storybook story generation
- Additional test cases
- Different component patterns (HOC, render props)

## Best Practices

- Review generated files before committing
- Customize the component to your specific needs
- Update tests to cover edge cases
- Add Storybook stories if using Storybook
- Follow your team's component architecture
