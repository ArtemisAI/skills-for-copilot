#!/usr/bin/env node
/**
 * CPU and memory profiling using pure Chrome DevTools Protocol
 * Usage: node profile.js --url https://example.com --type cpu|memory [--output profile.json]
 */
import { launchChrome, createPage, closeChrome, outputJSON, outputError } from './lib/cdp.js';
import { writeFile } from 'fs/promises';
import { resolve } from 'path';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const argv = yargs(hideBin(process.argv))
  .option('url', {
    type: 'string',
    description: 'URL to profile',
    demandOption: true
  })
  .option('type', {
    type: 'string',
    description: 'Profile type (cpu or memory)',
    choices: ['cpu', 'memory'],
    default: 'cpu'
  })
  .option('duration', {
    type: 'number',
    description: 'Profiling duration in milliseconds',
    default: 5000
  })
  .option('output', {
    type: 'string',
    description: 'Output file for profile data'
  })
  .option('headless', {
    type: 'boolean',
    description: 'Run in headless mode',
    default: true
  })
  .option('close', {
    type: 'boolean',
    description: 'Close browser after profiling',
    default: true
  })
  .help()
  .argv;

async function profile() {
  try {
    // Launch Chrome
    await launchChrome({
      headless: argv.headless
    });

    // Create page
    const page = await createPage({
      viewport: { width: 1920, height: 1080 }
    });

    let profileData;

    if (argv.type === 'cpu') {
      // CPU Profiling
      await page.client.send('Profiler.enable');
      await page.client.send('Profiler.start');

      // Navigate and wait
      await page.navigate(argv.url, { waitUntil: 'load' });
      await new Promise(resolve => setTimeout(resolve, argv.duration));

      // Stop profiling and get data
      const { profile } = await page.client.send('Profiler.stop');
      profileData = profile;

      await page.client.send('Profiler.disable');
    } else {
      // Memory Profiling
      await page.client.send('HeapProfiler.enable');
      await page.client.send('HeapProfiler.startSampling', {
        samplingInterval: 32768
      });

      // Navigate and wait
      await page.navigate(argv.url, { waitUntil: 'load' });
      await new Promise(resolve => setTimeout(resolve, argv.duration));

      // Stop profiling and get data
      const { profile } = await page.client.send('HeapProfiler.stopSampling');
      profileData = profile;

      // Also get heap snapshot
      await page.client.send('HeapProfiler.collectGarbage');

      await page.client.send('HeapProfiler.disable');
    }

    const result = {
      success: true,
      url: argv.url,
      type: argv.type,
      duration: argv.duration,
      profile: profileData,
      timestamp: new Date().toISOString()
    };

    // Save to file if requested
    if (argv.output) {
      const outputPath = resolve(argv.output);
      await writeFile(outputPath, JSON.stringify(result, null, 2));
      result.outputFile = outputPath;
      // Remove large profile data from console output
      delete result.profile;
    }

    outputJSON(result);

    if (argv.close) {
      await closeChrome();
    }
  } catch (error) {
    outputError(error);
  }
}

profile();
