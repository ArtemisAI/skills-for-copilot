/**
 * Pure Chrome DevTools Protocol (CDP) client
 * Direct WebSocket-based communication with Chrome without high-level libraries
 */
import chromeLauncher from 'chrome-launcher';
import WebSocket from 'ws';
import debug from 'debug';
import { EventEmitter } from 'events';

const log = debug('chrome-devtools:cdp');

let chromeInstance = null;
let cdpClients = new Map();
let messageId = 0;

/**
 * CDP Client - manages WebSocket connection and command execution
 */
class CDPClient extends EventEmitter {
  constructor(wsUrl) {
    super();
    this.wsUrl = wsUrl;
    this.ws = null;
    this.pendingMessages = new Map();
    this.messageId = 0;
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);

      this.ws.on('open', () => {
        log('WebSocket connected');
        resolve();
      });

      this.ws.on('message', (data) => {
        const message = JSON.parse(data.toString());

        if (message.id !== undefined) {
          // Response to a command
          const pending = this.pendingMessages.get(message.id);
          if (pending) {
            this.pendingMessages.delete(message.id);
            if (message.error) {
              pending.reject(new Error(message.error.message));
            } else {
              pending.resolve(message.result);
            }
          }
        } else if (message.method) {
          // Event from Chrome
          this.emit(message.method, message.params);
        }
      });

      this.ws.on('error', (error) => {
        log('WebSocket error:', error);
        reject(error);
      });

      this.ws.on('close', () => {
        log('WebSocket closed');
        this.emit('disconnect');
      });
    });
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = ++this.messageId;
      const message = { id, method, params };

      this.pendingMessages.set(id, { resolve, reject });
      this.ws.send(JSON.stringify(message));

      // Timeout after 30 seconds
      setTimeout(() => {
        if (this.pendingMessages.has(id)) {
          this.pendingMessages.delete(id);
          reject(new Error(`Command timeout: ${method}`));
        }
      }, 30000);
    });
  }

  close() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

/**
 * Launch Chrome or connect to existing instance
 */
export async function launchChrome(options = {}) {
  if (chromeInstance && chromeInstance.pid) {
    log('Reusing existing Chrome instance');
    return chromeInstance;
  }

  const chromeFlags = [
    '--disable-gpu',
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    ...(options.headless !== false ? ['--headless=new'] : []),
    ...(options.flags || [])
  ];

  log('Launching Chrome with flags:', chromeFlags);

  chromeInstance = await chromeLauncher.launch({
    chromeFlags,
    port: options.port || 0, // Random port
    handleSIGINT: true,
    ...options
  });

  log(`Chrome launched on port ${chromeInstance.port}`);
  return chromeInstance;
}

/**
 * Create CDP client for a specific target (page/tab)
 */
export async function createCDPClient(targetId = null) {
  if (!chromeInstance) {
    await launchChrome();
  }

  const debuggerUrl = `http://localhost:${chromeInstance.port}`;

  // Get list of targets
  const response = await fetch(`${debuggerUrl}/json/list`);
  const targets = await response.json();

  let target;
  if (targetId) {
    target = targets.find(t => t.id === targetId);
  } else {
    // Get first page target or create new one
    target = targets.find(t => t.type === 'page');

    if (!target) {
      // Create new target
      const newTargetResponse = await fetch(`${debuggerUrl}/json/new`);
      target = await newTargetResponse.json();
    }
  }

  if (!target || !target.webSocketDebuggerUrl) {
    throw new Error('No target available');
  }

  log('Connecting to target:', target.id);

  const client = new CDPClient(target.webSocketDebuggerUrl);
  await client.connect();

  cdpClients.set(target.id, { client, target });

  return { client, target };
}

/**
 * Close specific CDP client
 */
export async function closeCDPClient(targetId) {
  const item = cdpClients.get(targetId);
  if (item) {
    item.client.close();
    cdpClients.delete(targetId);
  }
}

/**
 * Close all CDP clients and Chrome
 */
export async function closeChrome() {
  // Close all CDP clients
  for (const [targetId, item] of cdpClients.entries()) {
    item.client.close();
  }
  cdpClients.clear();

  // Close Chrome
  if (chromeInstance) {
    await chromeInstance.kill();
    chromeInstance = null;
  }
}

/**
 * Page helpers - high-level abstractions over CDP
 */
export class Page {
  constructor(client, target) {
    this.client = client;
    this.target = target;
    this.frameId = null;
  }

  async enable() {
    // Enable necessary domains
    await this.client.send('Page.enable');
    await this.client.send('DOM.enable');
    await this.client.send('Runtime.enable');
    await this.client.send('Network.enable');

    // Get frame tree
    const { frameTree } = await this.client.send('Page.getFrameTree');
    this.frameId = frameTree.frame.id;
  }

  async navigate(url, options = {}) {
    const { frameId } = await this.client.send('Page.navigate', { url });

    // Wait for load event
    if (options.waitUntil !== 'none') {
      await this.waitForLoad(options.waitUntil || 'load');
    }

    return frameId;
  }

  async waitForLoad(event = 'load') {
    return new Promise((resolve) => {
      const handler = () => {
        this.client.removeListener('Page.loadEventFired', handler);
        this.client.removeListener('Page.domContentEventFired', handler);
        resolve();
      };

      if (event === 'load') {
        this.client.once('Page.loadEventFired', handler);
      } else if (event === 'domcontentloaded') {
        this.client.once('Page.domContentEventFired', handler);
      } else {
        // networkidle - wait for no network activity for 500ms
        let timeout;
        const networkHandler = () => {
          clearTimeout(timeout);
          timeout = setTimeout(() => {
            this.client.removeListener('Network.requestWillBeSent', networkHandler);
            this.client.removeListener('Network.responseReceived', networkHandler);
            resolve();
          }, 500);
        };
        this.client.on('Network.requestWillBeSent', networkHandler);
        this.client.on('Network.responseReceived', networkHandler);
      }
    });
  }

  async screenshot(options = {}) {
    const params = {
      format: options.format || 'png',
      quality: options.quality || 90,
      ...options
    };

    const { data } = await this.client.send('Page.captureScreenshot', params);
    return Buffer.from(data, 'base64');
  }

  async evaluate(script) {
    const { result, exceptionDetails } = await this.client.send('Runtime.evaluate', {
      expression: script,
      returnByValue: true,
      awaitPromise: true
    });

    if (exceptionDetails) {
      throw new Error(exceptionDetails.text || 'Evaluation failed');
    }

    return result.value;
  }

  async querySelector(selector) {
    const { root } = await this.client.send('DOM.getDocument');
    const { nodeId } = await this.client.send('DOM.querySelector', {
      nodeId: root.nodeId,
      selector
    });
    return nodeId;
  }

  async click(selector) {
    const nodeId = await this.querySelector(selector);

    if (!nodeId) {
      throw new Error(`Element not found: ${selector}`);
    }

    // Get box model to find click coordinates
    const { model } = await this.client.send('DOM.getBoxModel', { nodeId });
    const [x1, y1, x2, y2] = model.border;
    const x = (x1 + x2) / 2;
    const y = (y1 + y2) / 2;

    // Simulate mouse click
    await this.client.send('Input.dispatchMouseEvent', {
      type: 'mousePressed',
      x,
      y,
      button: 'left',
      clickCount: 1
    });

    await this.client.send('Input.dispatchMouseEvent', {
      type: 'mouseReleased',
      x,
      y,
      button: 'left',
      clickCount: 1
    });
  }

  async type(selector, text) {
    const nodeId = await this.querySelector(selector);

    if (!nodeId) {
      throw new Error(`Element not found: ${selector}`);
    }

    // Focus element
    await this.client.send('DOM.focus', { nodeId });

    // Type each character
    for (const char of text) {
      await this.client.send('Input.dispatchKeyEvent', {
        type: 'keyDown',
        text: char
      });

      await this.client.send('Input.dispatchKeyEvent', {
        type: 'keyUp',
        text: char
      });
    }
  }

  async getContent() {
    const { root } = await this.client.send('DOM.getDocument');
    const { outerHTML } = await this.client.send('DOM.getOuterHTML', {
      nodeId: root.nodeId
    });
    return outerHTML;
  }

  async setViewport(width, height, deviceScaleFactor = 1) {
    await this.client.send('Emulation.setDeviceMetricsOverride', {
      width,
      height,
      deviceScaleFactor,
      mobile: false
    });
  }
}

/**
 * Helper to create and initialize a page
 */
export async function createPage(options = {}) {
  const { client, target } = await createCDPClient();
  const page = new Page(client, target);
  await page.enable();

  if (options.viewport) {
    await page.setViewport(
      options.viewport.width || 1920,
      options.viewport.height || 1080,
      options.viewport.deviceScaleFactor || 1
    );
  }

  return page;
}

/**
 * Output JSON result
 */
export function outputJSON(data) {
  console.log(JSON.stringify(data, null, 2));
}

/**
 * Output error
 */
export function outputError(error) {
  console.error(JSON.stringify({
    success: false,
    error: error.message,
    stack: error.stack
  }, null, 2));
  process.exit(1);
}
