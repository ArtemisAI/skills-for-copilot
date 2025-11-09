#!/usr/bin/env node
/**
 * DOM snapshot with selectors using pure Chrome DevTools Protocol
 * Usage: node snapshot.js [--url https://example.com] [--output snapshot.json]
 */
import { launchChrome, createPage, closeChrome, outputJSON, outputError } from './lib/cdp.js';
import { writeFile } from 'fs/promises';
import { resolve } from 'path';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const argv = yargs(hideBin(process.argv))
  .option('url', {
    type: 'string',
    description: 'URL to snapshot'
  })
  .option('output', {
    type: 'string',
    description: 'Output file for snapshot data'
  })
  .option('headless', {
    type: 'boolean',
    description: 'Run in headless mode',
    default: true
  })
  .option('close', {
    type: 'boolean',
    description: 'Close browser after snapshot',
    default: true
  })
  .help()
  .argv;

async function snapshot() {
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
      await page.navigate(argv.url, { waitUntil: 'load' });
    }

    // Get interactive elements with metadata
    const elements = await page.evaluate(`(() => {
      const interactiveSelectors = [
        'a[href]',
        'button',
        'input',
        'textarea',
        'select',
        '[onclick]',
        '[role="button"]',
        '[role="link"]',
        '[contenteditable]'
      ];

      const elements = [];
      const selector = interactiveSelectors.join(', ');
      const nodes = document.querySelectorAll(selector);

      nodes.forEach((el, index) => {
        const rect = el.getBoundingClientRect();

        // Generate unique selector
        let uniqueSelector = '';
        if (el.id) {
          uniqueSelector = '#' + el.id;
        } else if (el.className) {
          const classes = Array.from(el.classList).join('.');
          uniqueSelector = el.tagName.toLowerCase() + '.' + classes;
        } else {
          uniqueSelector = el.tagName.toLowerCase();
        }

        function getXPath(element) {
          if (element.id) {
            return '//*[@id="' + element.id + '"]';
          }
          if (element === document.body) {
            return '/html/body';
          }
          let ix = 0;
          const siblings = element.parentNode?.childNodes || [];
          for (let i = 0; i < siblings.length; i++) {
            const sibling = siblings[i];
            if (sibling === element) {
              return getXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
            }
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
              ix++;
            }
          }
          return '';
        }

        elements.push({
          index: index,
          tagName: el.tagName.toLowerCase(),
          type: el.type || null,
          id: el.id || null,
          className: el.className || null,
          name: el.name || null,
          value: el.value || null,
          text: el.textContent?.trim().substring(0, 100) || null,
          href: el.href || null,
          selector: uniqueSelector,
          xpath: getXPath(el),
          visible: rect.width > 0 && rect.height > 0,
          position: {
            x: rect.x,
            y: rect.y,
            width: rect.width,
            height: rect.height
          }
        });
      });

      return elements;
    })()`);

    const url = await page.evaluate('window.location.href');
    const title = await page.evaluate('document.title');

    const result = {
      success: true,
      url,
      title,
      elementCount: elements.length,
      elements,
      timestamp: new Date().toISOString()
    };

    if (argv.output) {
      const outputPath = resolve(argv.output);
      await writeFile(outputPath, JSON.stringify(result, null, 2));
      result.outputFile = outputPath;
    }

    outputJSON(result);

    if (argv.close) {
      await closeChrome();
    }
  } catch (error) {
    outputError(error);
  }
}

snapshot();
