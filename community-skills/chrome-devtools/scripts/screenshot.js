#!/usr/bin/env node
/**
 * Take a screenshot using pure Chrome DevTools Protocol
 * Usage: node screenshot.js --output screenshot.png [--url https://example.com] [--full-page] [--selector .element]
 */
import { launchChrome, createPage, closeChrome, outputJSON, outputError } from './lib/cdp.js';
import { writeFile } from 'fs/promises';
import { resolve } from 'path';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const argv = yargs(hideBin(process.argv))
  .option('output', {
    type: 'string',
    description: 'Output file path',
    demandOption: true
  })
  .option('url', {
    type: 'string',
    description: 'URL to navigate to before screenshot'
  })
  .option('headless', {
    type: 'boolean',
    description: 'Run in headless mode',
    default: true
  })
  .option('full-page', {
    type: 'boolean',
    description: 'Capture full page screenshot',
    default: false
  })
  .option('selector', {
    type: 'string',
    description: 'CSS selector of element to screenshot'
  })
  .option('format', {
    type: 'string',
    description: 'Image format (png or jpeg)',
    default: 'png',
    choices: ['png', 'jpeg']
  })
  .option('quality', {
    type: 'number',
    description: 'Image quality (0-100, jpeg only)',
    default: 90
  })
  .option('wait-until', {
    type: 'string',
    description: 'Wait until event',
    default: 'load'
  })
  .option('close', {
    type: 'boolean',
    description: 'Close browser after screenshot',
    default: true
  })
  .help()
  .argv;

async function screenshot() {
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

    let buffer;
    let url = '';

    if (argv.selector) {
      // Screenshot specific element
      const nodeId = await page.querySelector(argv.selector);
      if (!nodeId) {
        throw new Error(`Element not found: ${argv.selector}`);
      }

      // Get element bounds
      const { model } = await page.client.send('DOM.getBoxModel', { nodeId });
      const [x, y, , , , , width, height] = model.border;

      buffer = await page.screenshot({
        format: argv.format,
        quality: argv.quality,
        clip: {
          x,
          y,
          width: width - x,
          height: height - y,
          scale: 1
        }
      });
    } else if (argv['full-page']) {
      // Full page screenshot
      const { contentSize } = await page.client.send('Page.getLayoutMetrics');

      await page.setViewport(contentSize.width, contentSize.height);

      buffer = await page.screenshot({
        format: argv.format,
        quality: argv.quality
      });
    } else {
      // Viewport screenshot
      buffer = await page.screenshot({
        format: argv.format,
        quality: argv.quality
      });
    }

    // Get current URL
    url = await page.evaluate('window.location.href');

    // Save screenshot
    const outputPath = resolve(argv.output);
    await writeFile(outputPath, buffer);

    const result = {
      success: true,
      output: outputPath,
      size: buffer.length,
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

screenshot();
