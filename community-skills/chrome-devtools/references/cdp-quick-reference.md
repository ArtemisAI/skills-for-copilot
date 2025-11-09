# Chrome DevTools Protocol Quick Reference

## Architecture

```
┌─────────────┐    WebSocket    ┌──────────────┐
│  Your Script │ ←──────────→  │  Chrome       │
│  (Node.js)  │                │  Browser      │
└─────────────┘                └──────────────┘
      ↑                              ↑
      │ Commands & Events            │ 47 Domains
      │                              │ 1000+ Methods
      └──────────────────────────────┘
```

## Core Concepts

### 1. Domains
CDP organizes functionality into domains:
- **Page** - Page navigation and inspection
- **DOM** - Document object model operations
- **Runtime** - JavaScript execution and evaluation
- **Network** - Network monitoring and interception
- **Performance** - Performance metrics
- **Profiler** - CPU profiling
- **HeapProfiler** - Memory profiling
- **Debugger** - JavaScript debugging
- **Emulation** - Device and network emulation

### 2. Commands
Send commands to Chrome:
```javascript
const result = await client.send('Domain.method', { param: value });
```

### 3. Events
Listen to events from Chrome:
```javascript
client.on('Domain.eventName', (params) => {
  console.log('Event received:', params);
});
```

## Common Patterns

### Navigation
```javascript
// Navigate to URL
await client.send('Page.navigate', { url: 'https://example.com' });

// Wait for load event
client.once('Page.loadEventFired', () => {
  console.log('Page loaded');
});

// Get frame tree
const { frameTree } = await client.send('Page.getFrameTree');
```

### DOM Operations
```javascript
// Enable DOM domain
await client.send('DOM.enable');

// Get document
const { root } = await client.send('DOM.getDocument');

// Query selector
const { nodeId } = await client.send('DOM.querySelector', {
  nodeId: root.nodeId,
  selector: 'button'
});

// Get attributes
const { attributes } = await client.send('DOM.getAttributes', { nodeId });
```

### JavaScript Execution
```javascript
// Enable Runtime
await client.send('Runtime.enable');

// Evaluate expression
const { result } = await client.send('Runtime.evaluate', {
  expression: 'document.title',
  returnByValue: true
});

// Call function on object
const { result } = await client.send('Runtime.callFunctionOn', {
  functionDeclaration: 'function() { return this.textContent; }',
  objectId: 'object-id'
});
```

### Network Monitoring
```javascript
// Enable Network
await client.send('Network.enable');

// Listen to requests
client.on('Network.requestWillBeSent', (params) => {
  console.log('Request:', params.request.url);
});

// Listen to responses
client.on('Network.responseReceived', (params) => {
  console.log('Response:', params.response.status);
});

// Get response body
const { body, base64Encoded } = await client.send('Network.getResponseBody', {
  requestId: 'request-id'
});
```

### Screenshots
```javascript
// Capture viewport screenshot
const { data } = await client.send('Page.captureScreenshot', {
  format: 'png',
  quality: 90
});

// Capture full page screenshot
const { contentSize } = await client.send('Page.getLayoutMetrics');
await client.send('Emulation.setDeviceMetricsOverride', {
  width: contentSize.width,
  height: contentSize.height,
  deviceScaleFactor: 1,
  mobile: false
});
const { data } = await client.send('Page.captureScreenshot');
```

### Performance Monitoring
```javascript
// Enable Performance
await client.send('Performance.enable');

// Get metrics
const { metrics } = await client.send('Performance.getMetrics');
// Returns: Timestamp, Documents, Frames, JSEventListeners, Nodes, LayoutCount, etc.

// Start tracing
await client.send('Tracing.start', {
  categories: ['devtools.timeline', 'v8.execute']
});

// Stop tracing
await client.send('Tracing.end');
```

### CPU Profiling
```javascript
// Enable Profiler
await client.send('Profiler.enable');

// Start profiling
await client.send('Profiler.start');

// ... run code to profile ...

// Stop and get profile
const { profile } = await client.send('Profiler.stop');

// Disable
await client.send('Profiler.disable');
```

### Memory Profiling
```javascript
// Enable HeapProfiler
await client.send('HeapProfiler.enable');

// Start sampling
await client.send('HeapProfiler.startSampling', {
  samplingInterval: 32768
});

// ... run code to profile ...

// Stop and get profile
const { profile } = await client.send('HeapProfiler.stopSampling');

// Take heap snapshot
await client.send('HeapProfiler.takeHeapSnapshot');
```

### Code Coverage
```javascript
// JavaScript coverage
await client.send('Profiler.enable');
await client.send('Profiler.startPreciseCoverage', {
  callCount: true,
  detailed: true
});

// ... load page and interact ...

const { result } = await client.send('Profiler.takePreciseCoverage');
await client.send('Profiler.stopPreciseCoverage');

// CSS coverage
await client.send('CSS.enable');
await client.send('CSS.startRuleUsageTracking');

// ... load page ...

const { ruleUsage } = await client.send('CSS.stopRuleUsageTracking');
```

### Device Emulation
```javascript
// Set device metrics
await client.send('Emulation.setDeviceMetricsOverride', {
  width: 375,
  height: 667,
  deviceScaleFactor: 2,
  mobile: true
});

// Set user agent
await client.send('Network.setUserAgentOverride', {
  userAgent: 'Mozilla/5.0 (iPhone; ...'
});

// Set geolocation
await client.send('Emulation.setGeolocationOverride', {
  latitude: 37.7749,
  longitude: -122.4194,
  accuracy: 100
});

// Set timezone
await client.send('Emulation.setTimezoneOverride', {
  timezoneId: 'America/New_York'
});
```

### Network Throttling
```javascript
// Emulate 3G
await client.send('Network.emulateNetworkConditions', {
  offline: false,
  downloadThroughput: 1.5 * 1024 * 1024 / 8,  // 1.5 Mbps
  uploadThroughput: 750 * 1024 / 8,            // 750 Kbps
  latency: 100                                  // 100ms
});

// Go offline
await client.send('Network.emulateNetworkConditions', {
  offline: true,
  downloadThroughput: 0,
  uploadThroughput: 0,
  latency: 0
});
```

### CPU Throttling
```javascript
// Slow down CPU 4x
await client.send('Emulation.setCPUThrottlingRate', {
  rate: 4
});

// Reset to normal
await client.send('Emulation.setCPUThrottlingRate', {
  rate: 1
});
```

### Console Monitoring
```javascript
// Enable Runtime
await client.send('Runtime.enable');

// Listen to console API calls
client.on('Runtime.consoleAPICalled', (params) => {
  console.log('Console:', params.type, params.args);
});

// Listen to exceptions
client.on('Runtime.exceptionThrown', (params) => {
  console.error('Exception:', params.exceptionDetails);
});
```

### Request Interception
```javascript
// Enable fetch domain
await client.send('Fetch.enable', {
  patterns: [{ urlPattern: '*' }]
});

// Intercept requests
client.on('Fetch.requestPaused', async (params) => {
  // Modify or block request
  await client.send('Fetch.continueRequest', {
    requestId: params.requestId,
    headers: modifiedHeaders
  });

  // Or fail the request
  await client.send('Fetch.failRequest', {
    requestId: params.requestId,
    errorReason: 'Blocked'
  });
});
```

### Cookie Management
```javascript
// Get cookies
const { cookies } = await client.send('Network.getCookies');

// Set cookie
await client.send('Network.setCookie', {
  name: 'session',
  value: 'abc123',
  domain: 'example.com',
  path: '/',
  secure: true,
  httpOnly: true
});

// Delete cookies
await client.send('Network.deleteCookies', {
  name: 'session',
  domain: 'example.com'
});
```

## Best Practices

### 1. Enable Domains Before Use
Always enable a domain before using its commands:
```javascript
await client.send('Network.enable');
await client.send('Page.enable');
await client.send('DOM.enable');
```

### 2. Handle Events Asynchronously
Events can arrive at any time:
```javascript
const requests = [];
client.on('Network.requestWillBeSent', (params) => {
  requests.push(params);
});
```

### 3. Clean Up Resources
Disable domains when done:
```javascript
await client.send('Network.disable');
await client.send('Profiler.disable');
```

### 4. Error Handling
Wrap CDP commands in try-catch:
```javascript
try {
  const result = await client.send('Page.navigate', { url });
} catch (error) {
  console.error('Navigation failed:', error);
}
```

### 5. Wait for Events
Use promises to wait for specific events:
```javascript
await new Promise((resolve) => {
  client.once('Page.loadEventFired', resolve);
});
```

## Useful CDP Domains

| Domain | Use Cases |
|--------|-----------|
| Page | Navigation, screenshots, print to PDF |
| DOM | Element queries, attribute manipulation |
| Runtime | JavaScript execution, object inspection |
| Network | Request/response monitoring, interception |
| Performance | Metrics, timeline traces |
| Profiler | CPU profiling |
| HeapProfiler | Memory profiling, heap snapshots |
| Debugger | Breakpoints, step debugging |
| Console | Console API monitoring |
| Emulation | Device/network/sensor emulation |
| Security | Certificate errors, mixed content |
| Storage | localStorage, sessionStorage, IndexedDB |
| Database | WebSQL inspection |
| ApplicationCache | AppCache inspection |
| CSS | Style inspection, coverage |
| Animation | Animation control and inspection |

## Resources

- [Official CDP Documentation](https://chromedevtools.github.io/devtools-protocol/)
- [CDP Viewer (Interactive)](https://chromedevtools.github.io/devtools-protocol/tot/)
- [CDP GitHub](https://github.com/ChromeDevTools/devtools-protocol)
