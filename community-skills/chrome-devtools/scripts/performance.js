#!/usr/bin/env node
/**
 * Performance analysis using pure Chrome DevTools Protocol
 * Usage: node performance.js --url https://example.com [--output perf.json] [--trace]
 */
import { launchChrome, createPage, closeChrome, outputJSON, outputError } from './lib/cdp.js';
import { writeFile } from 'fs/promises';
import { resolve } from 'path';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const argv = yargs(hideBin(process.argv))
  .option('url', {
    type: 'string',
    description: 'URL to analyze',
    demandOption: true
  })
  .option('output', {
    type: 'string',
    description: 'Output file for performance data'
  })
  .option('trace', {
    type: 'boolean',
    description: 'Capture performance trace',
    default: false
  })
  .option('headless', {
    type: 'boolean',
    description: 'Run in headless mode',
    default: true
  })
  .option('close', {
    type: 'boolean',
    description: 'Close browser after analysis',
    default: true
  })
  .help()
  .argv;

async function measurePerformance() {
  try {
    // Launch Chrome
    await launchChrome({
      headless: argv.headless
    });

    // Create page
    const page = await createPage({
      viewport: { width: 1920, height: 1080 }
    });

    // Enable Performance domain
    await page.client.send('Performance.enable');

    // Start trace if requested
    if (argv.trace) {
      await page.client.send('Tracing.start', {
        categories: ['devtools.timeline', 'v8.execute', 'blink.user_timing']
      });
    }

    // Navigate and wait for load
    await page.navigate(argv.url, { waitUntil: 'load' });

    // Wait a bit for metrics to settle
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Get performance metrics
    const { metrics } = await page.client.send('Performance.getMetrics');

    // Get navigation timing
    const navigationTiming = await page.evaluate(() => {
      const perfData = window.performance.timing;
      const perfEntries = performance.getEntriesByType('navigation')[0] || {};

      return {
        domContentLoaded: perfData.domContentLoadedEventEnd - perfData.navigationStart,
        load: perfData.loadEventEnd - perfData.navigationStart,
        domInteractive: perfData.domInteractive - perfData.navigationStart,
        firstByte: perfData.responseStart - perfData.navigationStart,
        dns: perfData.domainLookupEnd - perfData.domainLookupStart,
        tcp: perfData.connectEnd - perfData.connectStart,
        ...perfEntries
      };
    });

    // Get Core Web Vitals
    const webVitals = await page.evaluate(() => {
      return new Promise((resolve) => {
        const vitals = {};

        // LCP
        try {
          new PerformanceObserver((list) => {
            const entries = list.getEntries();
            vitals.LCP = entries[entries.length - 1].renderTime || entries[entries.length - 1].loadTime;
          }).observe({ entryTypes: ['largest-contentful-paint'], buffered: true });
        } catch (e) {}

        // CLS
        try {
          new PerformanceObserver((list) => {
            let cls = 0;
            for (const entry of list.getEntries()) {
              if (!entry.hadRecentInput) {
                cls += entry.value;
              }
            }
            vitals.CLS = cls;
          }).observe({ entryTypes: ['layout-shift'], buffered: true });
        } catch (e) {}

        // FCP
        try {
          const paintEntries = performance.getEntriesByType('paint');
          const fcpEntry = paintEntries.find(entry => entry.name === 'first-contentful-paint');
          if (fcpEntry) {
            vitals.FCP = fcpEntry.startTime;
          }
        } catch (e) {}

        setTimeout(() => resolve(vitals), 1000);
      });
    });

    // Stop trace if started
    if (argv.trace) {
      await page.client.send('Tracing.end');
    }

    // Format metrics
    const metricsMap = {};
    for (const metric of metrics) {
      metricsMap[metric.name] = metric.value;
    }

    const result = {
      success: true,
      url: argv.url,
      timing: navigationTiming,
      vitals: webVitals,
      metrics: metricsMap,
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

measurePerformance();
