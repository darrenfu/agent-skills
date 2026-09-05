import test from 'node:test';
import assert from 'node:assert/strict';
import { win32 } from 'node:path';
import { resolveVercelCommand } from '../../../skills/vercel-optimize/lib/vercel.mjs';

test('POSIX keeps the executable on PATH without probing Windows files', () => {
  assert.deepEqual(resolveVercelCommand({
    platform: 'darwin',
    exists: () => { throw new Error('Unexpected filesystem probe'); },
  }), { file: 'vercel', prefix: [] });
});

test('Windows runs the npm JavaScript entry directly when paths contain spaces', () => {
  const directory = 'C:\\Program Files\\nodejs';
  const entry = win32.join(directory, 'node_modules', 'vercel', 'dist', 'vc.js');
  for (const key of ['PATH', 'Path', 'path']) {
    assert.deepEqual(resolveVercelCommand({
      platform: 'win32',
      env: { [key]: directory },
      execPath: 'C:\\Program Files\\nodejs\\node.exe',
      exists: (file) => file === entry,
    }), { file: 'C:\\Program Files\\nodejs\\node.exe', prefix: [entry] });
  }
});

test('Windows finds a project-local package adjacent to node_modules/.bin', () => {
  const directory = 'C:\\project with spaces\\node_modules\\.bin';
  const entry = 'C:\\project with spaces\\node_modules\\vercel\\dist\\index.js';
  assert.deepEqual(resolveVercelCommand({
    platform: 'win32', env: { PATH: directory }, execPath: 'node.exe',
    exists: (file) => file === entry,
  }), { file: 'node.exe', prefix: [entry] });
});

test('Windows expands a relative command shim without invoking a shell', () => {
  const directory = 'C:\\package manager\\bin';
  const shim = win32.join(directory, 'vc.cmd');
  const entry = 'C:\\package manager\\packages\\vercel\\dist\\vc.js';
  assert.deepEqual(resolveVercelCommand({
    platform: 'win32', env: { PATH: directory }, execPath: 'node.exe',
    exists: (file) => file === shim || file === entry,
    readText: (file) => {
      assert.equal(file, shim);
      return '@"%~dp0..\\packages\\vercel\\dist\\vc.js" %*';
    },
  }), { file: 'node.exe', prefix: [entry] });
});

test('Windows skips unreadable shims and searches later PATH entries', () => {
  const entry = 'D:\\tools\\node_modules\\vercel\\dist\\vc.js';
  assert.deepEqual(resolveVercelCommand({
    platform: 'win32', env: { PATH: 'C:\\broken;D:\\tools' }, execPath: 'node.exe',
    exists: (file) => file === 'C:\\broken\\vercel.cmd' || file === entry,
    readText: () => { throw new Error('Access denied'); },
  }), { file: 'node.exe', prefix: [entry] });
});

test('Windows reports a missing installation without falling back to a shell', () => {
  assert.deepEqual(resolveVercelCommand({
    platform: 'win32', env: { PATH: 'C:\\empty' }, execPath: 'node.exe',
    exists: () => false,
  }), { file: 'node.exe', prefix: [], missing: true });
});
