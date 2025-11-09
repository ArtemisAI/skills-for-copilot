#!/usr/bin/env node
/**
 * Navigate to a URL using pure Chrome DevTools Protocol
 * Usage: node navigate.js --url https://example.com [--wait-until load|domcontentloaded|networkidle] [--timeout 30000]
 */
import { launchChrome, createPage, closeChrome, outputJSON, outputError } from './lib/cdp.js';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const argv = yargs(hideBin(process.argv))
  .option('url', {
    type: 'string',
    description: 'URL to navigate to',
    demandOption: true
  })
  .option('headless', {
    type: 'boolean',
    description: 'Run in headless mode',
    default: true
  })
  .option('wait-until', {
    type: 'string',
    description: 'Wait until event (load, domcontentloaded, networkidle)',
    default: 'load'
  })
  .option('timeout', {
    type: 'number',
    description: 'Timeout in milliseconds',
    default: 30000
  })
  .option('close', {
    type: 'boolean',
    description: 'Close browser after navigation',
    default: true
  })
  .help()
  .argv;

async function navigate() {
  try {
    // Launch Chrome
    await launchChrome({
      headless: argv.headless
    });

    // Create page
    const page = await createPage({
      viewport: { width: 1920, height: 1080 }
    });

    // Navigate
    await page.navigate(argv.url, {
      waitUntil: argv['wait-until']
    });

    // Get page info
    const title = await page.evaluate('document.title');
    const url = await page.evaluate('window.location.href');

    const result = {
      success: true,
      url,
      title
    };

    outputJSON(result);

    if (argv.close) {
      await closeChrome();
    }
  } catch (error) {
    outputError(error);
  }
}

navigate();
