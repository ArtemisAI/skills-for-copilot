#!/usr/bin/env node
/**
 * Evaluate JavaScript in page context using pure Chrome DevTools Protocol
 * Usage: node evaluate.js --script "document.title" [--url https://example.com]
 */
import { launchChrome, createPage, closeChrome, outputJSON, outputError } from './lib/cdp.js';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const argv = yargs(hideBin(process.argv))
  .option('script', {
    type: 'string',
    description: 'JavaScript code to evaluate',
    demandOption: true
  })
  .option('url', {
    type: 'string',
    description: 'URL to navigate to before evaluation'
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
    description: 'Close browser after evaluation',
    default: true
  })
  .help()
  .argv;

async function evaluate() {
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

    // Evaluate script
    const scriptResult = await page.evaluate(argv.script);

    const url = await page.evaluate('window.location.href');

    const result = {
      success: true,
      result: scriptResult,
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

evaluate();
