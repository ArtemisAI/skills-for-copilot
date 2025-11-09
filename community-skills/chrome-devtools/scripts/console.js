#!/usr/bin/env node
/**
 * Console monitoring using pure Chrome DevTools Protocol
 * Usage: node console.js --url https://example.com [--types error,warn] [--duration 5000]
 */
import { launchChrome, createPage, closeChrome, outputJSON, outputError } from './lib/cdp.js';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const argv = yargs(hideBin(process.argv))
  .option('url', {
    type: 'string',
    description: 'URL to monitor',
    demandOption: true
  })
  .option('types', {
    type: 'string',
    description: 'Comma-separated console message types to capture (log,info,warn,error)'
  })
  .option('duration', {
    type: 'number',
    description: 'Duration to monitor in milliseconds',
    default: 5000
  })
  .option('headless', {
    type: 'boolean',
    description: 'Run in headless mode',
    default: true
  })
  .option('close', {
    type: 'boolean',
    description: 'Close browser after monitoring',
    default: true
  })
  .help()
  .argv;

async function monitorConsole() {
  try {
    // Launch Chrome
    await launchChrome({
      headless: argv.headless
    });

    // Create page
    const page = await createPage({
      viewport: { width: 1920, height: 1080 }
    });

    const messages = [];
    const filterTypes = argv.types ? argv.types.split(',') : null;

    // Listen for console API calls
    page.client.on('Runtime.consoleAPICalled', (params) => {
      if (!filterTypes || filterTypes.includes(params.type)) {
        messages.push({
          type: params.type,
          args: params.args.map(arg => arg.value || arg.description),
          stackTrace: params.stackTrace,
          timestamp: params.timestamp
        });
      }
    });

    // Listen for exceptions
    page.client.on('Runtime.exceptionThrown', (params) => {
      messages.push({
        type: 'exception',
        text: params.exceptionDetails.text,
        exception: params.exceptionDetails.exception,
        stackTrace: params.exceptionDetails.stackTrace,
        timestamp: params.timestamp
      });
    });

    // Navigate
    await page.navigate(argv.url, { waitUntil: 'load' });

    // Wait for additional time
    await new Promise(resolve => setTimeout(resolve, argv.duration));

    const url = await page.evaluate('window.location.href');

    const result = {
      success: true,
      url,
      messageCount: messages.length,
      messages,
      summary: messages.reduce((acc, msg) => {
        acc[msg.type] = (acc[msg.type] || 0) + 1;
        return acc;
      }, {}),
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

monitorConsole();
