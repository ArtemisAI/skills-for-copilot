#!/usr/bin/env node
/**
 * Fill a form field using pure Chrome DevTools Protocol
 * Usage: node fill.js --selector "#email" --value "user@example.com" [--url https://example.com]
 */
import { launchChrome, createPage, closeChrome, outputJSON, outputError } from './lib/cdp.js';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const argv = yargs(hideBin(process.argv))
  .option('selector', {
    type: 'string',
    description: 'CSS selector of input element',
    demandOption: true
  })
  .option('value', {
    type: 'string',
    description: 'Value to fill',
    demandOption: true
  })
  .option('url', {
    type: 'string',
    description: 'URL to navigate to before filling'
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
    description: 'Close browser after filling',
    default: true
  })
  .help()
  .argv;

async function fill() {
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

    // Fill element
    await page.type(argv.selector, argv.value);

    const url = await page.evaluate('window.location.href');

    const result = {
      success: true,
      selector: argv.selector,
      value: argv.value,
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

fill();
