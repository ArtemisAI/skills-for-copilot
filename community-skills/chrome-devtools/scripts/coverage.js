#!/usr/bin/env node
/**
 * Code coverage analysis using pure Chrome DevTools Protocol
 * Usage: node coverage.js --url https://example.com [--output coverage.json]
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
    description: 'Output file for coverage data'
  })
  .option('css', {
    type: 'boolean',
    description: 'Include CSS coverage',
    default: true
  })
  .option('js', {
    type: 'boolean',
    description: 'Include JavaScript coverage',
    default: true
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

async function coverage() {
  try {
    // Launch Chrome
    await launchChrome({
      headless: argv.headless
    });

    // Create page
    const page = await createPage({
      viewport: { width: 1920, height: 1080 }
    });

    // Start coverage
    if (argv.js) {
      await page.client.send('Profiler.enable');
      await page.client.send('Profiler.startPreciseCoverage', {
        callCount: true,
        detailed: true
      });
    }

    if (argv.css) {
      await page.client.send('CSS.enable');
      await page.client.send('CSS.startRuleUsageTracking');
    }

    // Navigate
    await page.navigate(argv.url, { waitUntil: 'networkidle' });

    // Wait a bit for interactions
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Collect coverage
    let jsCoverage = null;
    let cssCoverage = null;

    if (argv.js) {
      const { result } = await page.client.send('Profiler.takePreciseCoverage');
      jsCoverage = result;
      await page.client.send('Profiler.stopPreciseCoverage');
      await page.client.send('Profiler.disable');
    }

    if (argv.css) {
      const { ruleUsage } = await page.client.send('CSS.stopRuleUsageTracking');
      cssCoverage = ruleUsage;
      await page.client.send('CSS.disable');
    }

    // Calculate statistics
    const jsStats = jsCoverage ? calculateJSCoverage(jsCoverage) : null;
    const cssStats = cssCoverage ? calculateCSSCoverage(cssCoverage) : null;

    const result = {
      success: true,
      url: argv.url,
      javascript: jsStats,
      css: cssStats,
      timestamp: new Date().toISOString()
    };

    // Save to file if requested
    if (argv.output) {
      const outputPath = resolve(argv.output);
      const detailedResult = {
        ...result,
        jsCoverageDetails: jsCoverage,
        cssCoverageDetails: cssCoverage
      };
      await writeFile(outputPath, JSON.stringify(detailedResult, null, 2));
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

function calculateJSCoverage(coverage) {
  let totalBytes = 0;
  let usedBytes = 0;

  for (const entry of coverage) {
    for (const range of entry.functions) {
      totalBytes += range.ranges.reduce((sum, r) => sum + (r.endOffset - r.startOffset), 0);
      usedBytes += range.ranges.filter(r => r.count > 0).reduce((sum, r) => sum + (r.endOffset - r.startOffset), 0);
    }
  }

  return {
    totalBytes,
    usedBytes,
    unusedBytes: totalBytes - usedBytes,
    percentageUsed: totalBytes > 0 ? ((usedBytes / totalBytes) * 100).toFixed(2) : 0,
    scriptCount: coverage.length
  };
}

function calculateCSSCoverage(coverage) {
  const totalRules = coverage.length;
  const usedRules = coverage.filter(rule => rule.used).length;

  return {
    totalRules,
    usedRules,
    unusedRules: totalRules - usedRules,
    percentageUsed: totalRules > 0 ? ((usedRules / totalRules) * 100).toFixed(2) : 0
  };
}

coverage();
