---
name: chrome-devtools
description: Browser automation, debugging, and performance analysis using pure Chrome DevTools Protocol (CDP). Use for automating browsers, taking screenshots, analyzing performance, monitoring network traffic, web scraping, form automation, and JavaScript debugging without high-level libraries.
license: Apache-2.0
---

# Chrome DevTools Protocol (CDP) Skill

Browser automation via pure Chrome DevTools Protocol - direct WebSocket communication with Chrome. No Puppeteer, no Playwright - just raw CDP for maximum control and performance. All scripts output JSON for easy parsing.

## Quick Start

### Installation

#### Step 1: Install System Dependencies (Linux/WSL only)

On Linux/WSL, Chrome requires system libraries. Install them first:

```bash
cd .claude/skills/chrome-devtools/scripts
./install-deps.sh  # Auto-detects OS and installs required libs
```

Supports: Ubuntu, Debian, Fedora, RHEL, CentOS, Arch, Manjaro

**macOS/Windows**: Skip this step (dependencies bundled with Chrome)

#### Step 2: Install Node Dependencies

```bash
cd .claude/skills/chrome-devtools/scripts
npm install  # Installs chrome-launcher, ws (WebSocket), debug, yargs
```

### Test
```bash
node navigate.js --url https://example.com
# Output: {"success": true, "url": "https://example.com", "title": "Example Domain"}
```

## Available Scripts

All scripts are in `.claude/skills/chrome-devtools/scripts/`

### Script Usage
- `./scripts/README.md`

### Core Automation
- `navigate.js` - Navigate to URLs
- `screenshot.js` - Capture screenshots (full page or element)
- `click.js` - Click elements
- `fill.js` - Fill form fields
- `evaluate.js` - Execute JavaScript in page context

### Analysis & Monitoring
- `snapshot.js` - Extract interactive elements with metadata
- `console.js` - Monitor console messages/errors
- `network.js` - Track HTTP requests/responses
- `performance.js` - Measure Core Web Vitals + record traces

### Advanced CDP Features
- `profile.js` - CPU and memory profiling
- `coverage.js` - JavaScript and CSS code coverage analysis
- `emulate.js` - Device and network emulation (mobile, tablet, 3G, 4G)

## Usage Patterns

### Single Command
```bash
cd .claude/skills/chrome-devtools/scripts
node screenshot.js --url https://example.com --output ./docs/screenshots/page.png
```
**Important**: Always save screenshots to `./docs/screenshots` directory.

### Chain Commands (reuse browser)
```bash
# Keep browser open with --close false
node navigate.js --url https://example.com/login --close false
node fill.js --selector "#email" --value "user@example.com" --close false
node fill.js --selector "#password" --value "secret" --close false
node click.js --selector "button[type=submit]"
```

### Parse JSON Output
```bash
# Extract specific fields with jq
node performance.js --url https://example.com | jq '.vitals.LCP'

# Save to file
node network.js --url https://example.com --output /tmp/requests.json
```

## Common Workflows

### Web Scraping
```bash
node evaluate.js --url https://example.com --script "
  Array.from(document.querySelectorAll('.item')).map(el => ({
    title: el.querySelector('h2')?.textContent,
    link: el.querySelector('a')?.href
  }))
" | jq '.result'
```

### Performance Testing
```bash
PERF=$(node performance.js --url https://example.com)
LCP=$(echo $PERF | jq '.vitals.LCP')
if (( $(echo "$LCP < 2500" | bc -l) )); then
  echo "✓ LCP passed: ${LCP}ms"
else
  echo "✗ LCP failed: ${LCP}ms"
fi
```

### Form Automation
```bash
node fill.js --url https://example.com --selector "#search" --value "query" --close false
node click.js --selector "button[type=submit]"
```

### Error Monitoring
```bash
node console.js --url https://example.com --types error,warn --duration 5000 | jq '.messageCount'
```

## Script Options

All scripts support:
- `--headless false` - Show browser window
- `--close false` - Keep browser open for chaining
- `--timeout 30000` - Set timeout (milliseconds)
- `--wait-until networkidle2` - Wait strategy

See `./scripts/README.md` for complete options.

## Output Format

All scripts output JSON to stdout:
```json
{
  "success": true,
  "url": "https://example.com",
  ... // script-specific data
}
```

Errors go to stderr:
```json
{
  "success": false,
  "error": "Error message"
}
```

## Finding Elements

Use `snapshot.js` to discover selectors:
```bash
node snapshot.js --url https://example.com | jq '.elements[] | {tagName, text, selector}'
```

## Troubleshooting

### Common Errors

**"Cannot find package 'chrome-launcher'"**
- Run: `npm install` in the scripts directory

**"error while loading shared libraries: libnss3.so"** (Linux/WSL)
- Missing system dependencies
- Fix: Run `./install-deps.sh` in scripts directory
- Manual install: `sudo apt-get install -y libnss3 libnspr4 libasound2t64 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1`

**"Failed to launch the browser process"**
- Check system dependencies installed (Linux/WSL)
- Verify Chrome downloaded: `ls ~/.cache/puppeteer`
- Try: `npm rebuild` then `npm install`

**Chrome not found**
- chrome-launcher will use system Chrome if available
- Install Chrome manually: https://www.google.com/chrome/
- On Linux: `sudo apt-get install chromium-browser` or `google-chrome-stable`

### Script Issues

**Element not found**
- Get snapshot first to find correct selector: `node snapshot.js --url <url>`

**Script hangs**
- Increase timeout: `--timeout 60000`
- Change wait strategy: `--wait-until load` or `--wait-until domcontentloaded`

**Blank screenshot**
- Wait for page load: `--wait-until networkidle2`
- Increase timeout: `--timeout 30000`

**Permission denied on scripts**
- Make executable: `chmod +x *.sh`

## Reference Documentation

Detailed guides available in `./references/`:
- [CDP Quick Reference](./references/cdp-quick-reference.md) - Common CDP patterns and examples
- [CDP Domains Reference](./references/cdp-domains.md) - All 47 Chrome DevTools Protocol domains
- [Performance Analysis Guide](./references/performance-guide.md) - Core Web Vitals optimization

## Advanced Usage

### Custom Scripts
Create custom scripts using the CDP library:
```javascript
import { launchChrome, createPage, closeChrome, outputJSON } from './lib/cdp.js';

async function myScript() {
  await launchChrome({ headless: true });
  const page = await createPage();

  // Use page methods or direct CDP
  await page.navigate('https://example.com');

  // Direct CDP access via page.client
  await page.client.send('Emulation.setCPUThrottlingRate', { rate: 4 });

  await closeChrome();
}
```

### Pure CDP Access
All scripts use pure Chrome DevTools Protocol via WebSocket:
```javascript
import { launchChrome, createCDPClient } from './lib/cdp.js';

const chrome = await launchChrome();
const { client, target } = await createCDPClient();

// Send CDP commands directly
await client.send('Page.navigate', { url: 'https://example.com' });
await client.send('Page.captureScreenshot', { format: 'png' });

// Listen to CDP events
client.on('Network.responseReceived', (params) => {
  console.log('Response:', params.response.url);
});
```

See reference documentation for advanced patterns and complete API coverage.

## Why Pure CDP?

**Advantages over Puppeteer/Playwright:**
- **Zero abstraction overhead** - Direct WebSocket communication with Chrome
- **Smaller footprint** - No large libraries, just chrome-launcher and ws
- **Maximum control** - Access to all 47 CDP domains and 1000+ commands
- **Better debugging** - See exactly what's being sent to Chrome
- **Future-proof** - CDP is the official protocol, won't be deprecated
- **Flexibility** - Easily customize and extend for specific needs

**Use cases:**
- Performance-critical automation
- Advanced debugging scenarios
- Custom browser instrumentation
- Learning CDP fundamentals
- Building your own automation framework

## External Resources

- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) - Official CDP documentation
- [CDP Viewer](https://chromedevtools.github.io/devtools-protocol/tot/) - Interactive protocol reference
- [chrome-launcher](https://github.com/GoogleChrome/chrome-launcher) - Launch Chrome from Node.js
- [Scripts README](./scripts/README.md)
