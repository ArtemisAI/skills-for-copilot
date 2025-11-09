# Web App Testing

## Overview

Test local web applications using Playwright for UI verification and debugging. Use when you need to automate browser testing, verify UI behavior, test user interactions, or debug web applications systematically.

## When to Use

- Testing local web applications and development servers
- Verifying UI behavior and user interactions
- Debugging web application issues systematically
- Automating browser-based testing workflows
- Validating responsive design and cross-browser compatibility
- Capturing screenshots and test artifacts

## Core Capabilities

Playwright provides:
- **Browser Automation** - Control Chrome, Firefox, Safari programmatically
- **UI Interaction** - Click, type, navigate, fill forms
- **Assertions** - Verify element presence, text content, visibility
- **Screenshots** - Capture page state for debugging
- **Network Monitoring** - Track requests and responses
- **Mobile Emulation** - Test responsive designs

## Workflows

### Workflow 1: Basic Web App Testing Setup

**Step 1: Install Playwright**

```bash
# For Python
pip install playwright
playwright install

# For Node/TypeScript
npm install -D @playwright/test
npx playwright install
```

**Step 2: Start Your Application**

```bash
# Start your dev server (example)
npm run dev
# or
python -m http.server 8000
# or
python app.py
```

**Step 3: Write Basic Test**

**Python:**
```python
from playwright.sync_api import sync_playwright

def test_homepage():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Navigate to local app
        page.goto("http://localhost:3000")
        
        # Verify page loaded
        assert page.title() == "My App"
        
        # Verify element exists
        heading = page.locator("h1")
        assert heading.inner_text() == "Welcome"
        
        browser.close()

if __name__ == "__main__":
    test_homepage()
```

**TypeScript:**
```typescript
import { test, expect } from '@playwright/test';

test('homepage loads correctly', async ({ page }) => {
  await page.goto('http://localhost:3000');
  
  await expect(page).toHaveTitle('My App');
  
  const heading = page.locator('h1');
  await expect(heading).toHaveText('Welcome');
});
```

### Workflow 2: Interactive Testing

**Clicking and Navigation:**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # See browser
    page = browser.new_page()
    
    page.goto("http://localhost:3000")
    
    # Click a button
    page.click("button#submit")
    
    # Click a link
    page.click("a[href='/about']")
    
    # Wait for navigation
    page.wait_for_url("**/about")
    
    browser.close()
```

**Form Filling:**
```python
# Fill form fields
page.fill("input#name", "John Doe")
page.fill("input#email", "john@example.com")
page.select_option("select#country", "USA")
page.check("input#terms")  # Checkbox

# Submit form
page.click("button[type='submit']")

# Wait for response
page.wait_for_selector("div.success-message")
```

**Keyboard and Mouse:**
```python
# Keyboard input
page.keyboard.type("Hello World")
page.keyboard.press("Enter")
page.keyboard.press("Control+A")

# Mouse actions
page.mouse.move(100, 200)
page.mouse.click(100, 200)
page.hover("div.tooltip-trigger")
```

### Workflow 3: Assertions and Verification

```python
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:3000")
    
    # Verify element exists
    expect(page.locator("h1")).to_be_visible()
    
    # Verify text content
    expect(page.locator("h1")).to_have_text("Welcome")
    
    # Verify attribute
    expect(page.locator("a")).to_have_attribute("href", "/about")
    
    # Verify CSS class
    expect(page.locator("button")).to_have_class("btn-primary")
    
    # Verify count
    expect(page.locator("li")).to_have_count(5)
    
    browser.close()
```

### Workflow 4: Screenshots and Debugging

```python
# Take full page screenshot
page.screenshot(path="screenshot.png", full_page=True)

# Screenshot specific element
element = page.locator("div.header")
element.screenshot(path="header.png")

# Record video
browser = p.chromium.launch()
context = browser.new_context(
    record_video_dir="videos/"
)
page = context.new_page()
# ... perform actions ...
context.close()  # Video saved

# Pause for debugging
page.pause()  # Opens Playwright Inspector
```

### Workflow 5: Network Monitoring

```python
# Monitor network requests
def handle_request(request):
    print(f"Request: {request.method} {request.url}")

def handle_response(response):
    print(f"Response: {response.status} {response.url}")

page.on("request", handle_request)
page.on("response", handle_response)

page.goto("http://localhost:3000")

# Wait for specific request
with page.expect_response("**/api/data") as response_info:
    page.click("button#load-data")
response = response_info.value
print(f"API Response: {response.json()}")
```

### Workflow 6: Mobile and Responsive Testing

```python
# Emulate mobile device
iphone = p.devices["iPhone 12"]
browser = p.chromium.launch()
context = browser.new_context(**iphone)
page = context.new_page()

page.goto("http://localhost:3000")
page.screenshot(path="mobile.png")

# Custom viewport
page.set_viewport_size({"width": 1280, "height": 720})
page.screenshot(path="desktop.png")
```

## Examples

### Example 1: Complete E2E Test

```python
from playwright.sync_api import sync_playwright

def test_login_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to app
        page.goto("http://localhost:3000")
        
        # Click login button
        page.click("a[href='/login']")
        page.wait_for_url("**/login")
        
        # Fill login form
        page.fill("input#username", "testuser")
        page.fill("input#password", "testpass123")
        page.click("button[type='submit']")
        
        # Verify redirected to dashboard
        page.wait_for_url("**/dashboard")
        
        # Verify user name displayed
        user_name = page.locator("span.user-name")
        assert user_name.inner_text() == "testuser"
        
        # Take success screenshot
        page.screenshot(path="login-success.png")
        
        browser.close()

if __name__ == "__main__":
    test_login_flow()
```

### Example 2: Multi-Page Testing

```python
def test_navigation():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        pages_to_test = [
            ("http://localhost:3000/", "Home Page"),
            ("http://localhost:3000/about", "About Us"),
            ("http://localhost:3000/contact", "Contact"),
        ]
        
        for url, expected_title in pages_to_test:
            page.goto(url)
            assert expected_title in page.title()
            print(f"✓ {url} - {expected_title}")
        
        browser.close()
```

### Example 3: Form Validation Testing

```python
def test_form_validation():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        page.goto("http://localhost:3000/signup")
        
        # Submit empty form
        page.click("button[type='submit']")
        
        # Verify error messages
        errors = page.locator("span.error")
        assert errors.count() > 0
        
        # Fill invalid email
        page.fill("input#email", "invalid-email")
        page.click("button[type='submit']")
        
        # Verify email error
        email_error = page.locator("span.error-email")
        assert "valid email" in email_error.inner_text().lower()
        
        browser.close()
```

## Resources

### Workspace References

**Core Documentation:**
- `webapp-testing/SKILL.md` - Complete web app testing skill

**Scripts:**
- `webapp-testing/scripts/` - Testing utilities (if available)

### External Documentation

**Official Resources:**
- Playwright Docs: https://playwright.dev/
- Python API: https://playwright.dev/python/
- TypeScript API: https://playwright.dev/docs/api/class-playwright

**Installation:**
```bash
pip install playwright pytest-playwright
playwright install

# Or for Node
npm install -D @playwright/test
```

## Guidelines

### Best Practices

1. **Start Server First** - Ensure dev server is running before tests
2. **Use Explicit Waits** - Wait for elements/navigation rather than sleep()
3. **Descriptive Selectors** - Use meaningful IDs and data attributes
4. **Clean Up** - Close browsers after tests
5. **Screenshots on Failure** - Capture state when tests fail

### Selector Strategies

**Priority order:**
```python
# 1. User-facing attributes (best)
page.click("button:has-text('Submit')")
page.click("a[role='button']")

# 2. Test IDs (good)
page.click("data-testid=submit-button")

# 3. CSS selectors (okay)
page.click("button.btn-primary")

# 4. XPath (last resort)
page.click("xpath=//button[@class='btn']")
```

### Common Patterns

**Wait for Element:**
```python
# Wait for element to be visible
page.wait_for_selector("div.content", state="visible")

# Wait with timeout
page.wait_for_selector("div.loading", state="hidden", timeout=5000)

# Wait for function
page.wait_for_function("document.readyState === 'complete'")
```

**Handle Popups:**
```python
# Handle alert
page.on("dialog", lambda dialog: dialog.accept())
page.click("button#show-alert")

# Handle popup window
with page.expect_popup() as popup_info:
    page.click("a[target='_blank']")
popup = popup_info.value
```

**Multiple Contexts:**
```python
# Test with multiple users
browser = p.chromium.launch()
context1 = browser.new_context()
context2 = browser.new_context()

page1 = context1.new_page()
page2 = context2.new_page()

# Each context has separate cookies/storage
```

## Troubleshooting

### Problem: Elements not found
**Solution:** Add explicit waits, check selector, verify page loaded

### Problem: Tests flaky/intermittent
**Solution:** Use proper waits instead of sleep(), wait for network idle

### Problem: Browser doesn't close
**Solution:** Use context managers or ensure browser.close() in finally block

### Problem: Can't interact with element
**Solution:** Check if element is visible, not covered, and interactive

## Next Steps

After basic testing:

1. **Organize Tests** - Structure into test suites
2. **Add CI/CD** - Integrate with GitHub Actions
3. **Parallel Testing** - Run tests concurrently
4. **Visual Regression** - Compare screenshots over time
5. **Performance Testing** - Measure load times and metrics

## Additional Context

This instruction set covers Playwright-based testing. For complete skill documentation and advanced patterns, see `webapp-testing/SKILL.md`.

Use @workspace to query the original skill for specific testing scenarios or edge cases.
