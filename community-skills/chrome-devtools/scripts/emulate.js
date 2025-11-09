#!/usr/bin/env node
/**
 * Device and network emulation using pure Chrome DevTools Protocol
 * Usage: node emulate.js --url https://example.com --device mobile [--network 3g]
 */
import { launchChrome, createPage, closeChrome, outputJSON, outputError } from './lib/cdp.js';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const DEVICES = {
  mobile: {
    width: 375,
    height: 667,
    deviceScaleFactor: 2,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15'
  },
  tablet: {
    width: 768,
    height: 1024,
    deviceScaleFactor: 2,
    userAgent: 'Mozilla/5.0 (iPad; CPU OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15'
  },
  desktop: {
    width: 1920,
    height: 1080,
    deviceScaleFactor: 1,
    userAgent: null
  }
};

const NETWORKS = {
  '3g': {
    offline: false,
    downloadThroughput: 1.5 * 1024 * 1024 / 8,
    uploadThroughput: 750 * 1024 / 8,
    latency: 100
  },
  '4g': {
    offline: false,
    downloadThroughput: 4 * 1024 * 1024 / 8,
    uploadThroughput: 3 * 1024 * 1024 / 8,
    latency: 20
  },
  slow3g: {
    offline: false,
    downloadThroughput: 500 * 1024 / 8,
    uploadThroughput: 500 * 1024 / 8,
    latency: 400
  },
  offline: {
    offline: true,
    downloadThroughput: 0,
    uploadThroughput: 0,
    latency: 0
  }
};

const argv = yargs(hideBin(process.argv))
  .option('url', {
    type: 'string',
    description: 'URL to test',
    demandOption: true
  })
  .option('device', {
    type: 'string',
    description: 'Device to emulate',
    choices: Object.keys(DEVICES),
    default: 'desktop'
  })
  .option('network', {
    type: 'string',
    description: 'Network condition to emulate',
    choices: Object.keys(NETWORKS)
  })
  .option('cpu-throttle', {
    type: 'number',
    description: 'CPU throttling rate (1 = no throttle, 4 = 4x slowdown)'
  })
  .option('headless', {
    type: 'boolean',
    description: 'Run in headless mode',
    default: false
  })
  .option('close', {
    type: 'boolean',
    description: 'Close browser after emulation',
    default: true
  })
  .help()
  .argv;

async function emulate() {
  try {
    // Launch Chrome
    await launchChrome({
      headless: argv.headless
    });

    // Create page
    const page = await createPage();

    const device = DEVICES[argv.device];

    // Set device metrics
    await page.client.send('Emulation.setDeviceMetricsOverride', {
      width: device.width,
      height: device.height,
      deviceScaleFactor: device.deviceScaleFactor,
      mobile: argv.device !== 'desktop'
    });

    // Set user agent if specified
    if (device.userAgent) {
      await page.client.send('Network.setUserAgentOverride', {
        userAgent: device.userAgent
      });
    }

    // Set network conditions
    if (argv.network) {
      const network = NETWORKS[argv.network];
      await page.client.send('Network.emulateNetworkConditions', network);
    }

    // Set CPU throttling
    if (argv['cpu-throttle']) {
      await page.client.send('Emulation.setCPUThrottlingRate', {
        rate: argv['cpu-throttle']
      });
    }

    // Set geolocation if mobile
    if (argv.device === 'mobile') {
      await page.client.send('Emulation.setGeolocationOverride', {
        latitude: 37.7749,
        longitude: -122.4194,
        accuracy: 100
      });
    }

    // Navigate
    const startTime = Date.now();
    await page.navigate(argv.url, { waitUntil: 'load' });
    const loadTime = Date.now() - startTime;

    const result = {
      success: true,
      url: argv.url,
      emulation: {
        device: argv.device,
        viewport: `${device.width}x${device.height}`,
        network: argv.network || 'none',
        cpuThrottle: argv['cpu-throttle'] || 1
      },
      performance: {
        loadTime,
        loadTimeSeconds: (loadTime / 1000).toFixed(2)
      },
      timestamp: new Date().toISOString()
    };

    outputJSON(result);

    if (argv.close) {
      await closeChrome();
    }
  } catch (error) {
    outputError(error);
  }
}

emulate();
