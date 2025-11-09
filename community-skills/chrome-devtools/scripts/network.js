#!/usr/bin/env node
/**
 * Network monitoring using pure Chrome DevTools Protocol
 * Usage: node network.js --url https://example.com [--output network.json] [--filter script]
 */
import { launchChrome, createPage, closeChrome, outputJSON, outputError } from './lib/cdp.js';
import { writeFile } from 'fs/promises';
import { resolve } from 'path';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const argv = yargs(hideBin(process.argv))
  .option('url', {
    type: 'string',
    description: 'URL to monitor',
    demandOption: true
  })
  .option('output', {
    type: 'string',
    description: 'Output file for network data'
  })
  .option('filter', {
    type: 'string',
    description: 'Filter by resource type (document, stylesheet, script, xhr, fetch, image)'
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

async function monitorNetwork() {
  try {
    // Launch Chrome
    await launchChrome({
      headless: argv.headless
    });

    // Create page
    const page = await createPage({
      viewport: { width: 1920, height: 1080 }
    });

    const requests = [];
    const responses = [];
    const failures = [];

    // Track network requests
    page.client.on('Network.requestWillBeSent', (params) => {
      requests.push({
        requestId: params.requestId,
        url: params.request.url,
        method: params.request.method,
        headers: params.request.headers,
        timestamp: params.timestamp,
        type: params.type
      });
    });

    // Track network responses
    page.client.on('Network.responseReceived', (params) => {
      responses.push({
        requestId: params.requestId,
        url: params.response.url,
        status: params.response.status,
        statusText: params.response.statusText,
        headers: params.response.headers,
        mimeType: params.response.mimeType,
        timestamp: params.timestamp,
        type: params.type
      });
    });

    // Track failures
    page.client.on('Network.loadingFailed', (params) => {
      failures.push({
        requestId: params.requestId,
        errorText: params.errorText,
        timestamp: params.timestamp,
        type: params.type
      });
    });

    // Navigate
    await page.navigate(argv.url, { waitUntil: 'networkidle' });

    // Wait a bit for all network activity to complete
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Merge request and response data
    const networkData = requests.map(req => {
      const resp = responses.find(r => r.requestId === req.requestId);
      const failure = failures.find(f => f.requestId === req.requestId);

      return {
        url: req.url,
        method: req.method,
        type: req.type,
        status: resp?.status,
        statusText: resp?.statusText,
        mimeType: resp?.mimeType,
        failed: !!failure,
        errorText: failure?.errorText,
        timestamp: req.timestamp
      };
    });

    // Filter if requested
    let filteredData = networkData;
    if (argv.filter) {
      filteredData = networkData.filter(item =>
        item.type?.toLowerCase() === argv.filter.toLowerCase()
      );
    }

    const result = {
      success: true,
      url: argv.url,
      requestCount: filteredData.length,
      requests: filteredData,
      summary: {
        total: networkData.length,
        failed: failures.length,
        byType: networkData.reduce((acc, item) => {
          acc[item.type || 'other'] = (acc[item.type || 'other'] || 0) + 1;
          return acc;
        }, {})
      },
      timestamp: new Date().toISOString()
    };

    // Save to file if requested
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

monitorNetwork();
