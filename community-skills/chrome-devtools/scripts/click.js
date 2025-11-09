#!/usr/bin/env node
/**
 * Click an element using pure Chrome DevTools Protocol
 * Usage: node click.js --selector button.submit [--url https://example.com]
 */
import { launchChrome, createPage, closeChrome, outputJSON, outputError } from './lib/cdp.js';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const argv = yargs(hideBin(process.argv))
  .option('selector', {
    type: 'string',
    description: 'CSS selector of element to click',
    demandOption: true
  })
  .option('url', {
    type: 'string',
    description: 'URL to navigate to before clicking'
  })
  .option('headless', {
    type: 'boolean',
    description: 'Run in headless mode',
    default: true
  })
  .option('wait-until', {
    type: 'string',
    description: 'Wait until event',
    default: 'load'
  })
  .option('close', {
    type: 'boolean',
    description: 'Close browser after click',
    default: true
  })
  .help()
  .argv;

async function click() {
  try {
    // Launch Chrome
    await launchChrome({
      headless: argv.headless
    });

    // Create page
    const page = await createPage({
      viewport: { width: 1920, height: 1080 }
    });

    // Navigate if URL provided
    if (argv.url) {
      await page.navigate(argv.url, {
        waitUntil: argv['wait-until']
      });
    }

    // Click element
    await page.click(argv.selector);

    const url = await page.evaluate('window.location.href');

    const result = {
      success: true,
      selector: argv.selector,
      url
    };

    outputJSON(result);

    if (argv.close) {
      await closeChrome();
    }
  } catch (error) {
    outputError(error);
  }
}

click();
