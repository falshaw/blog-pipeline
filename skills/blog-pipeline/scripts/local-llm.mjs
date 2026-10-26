#!/usr/bin/env node
/**
 * local-llm.mjs — hand heavy text work to a local Ollama model so the main agent doesn't spend tokens on it.
 *
 * The agent orchestrates; the local model reads the big inputs and writes the long drafts.
 * Inputs go file → Ollama directly (never through the agent's context); with -o the result
 * lands on disk and the agent only reads what it needs.
 *
 * Usage:
 *   node local-llm.mjs "prompt" -f a.md -f b.log              # files appended as context
 *   node local-llm.mjs "write the German version" -f post.md -o post.de.md
 *   node local-llm.mjs -s "system prompt" "prompt"
 *   cat x.txt | node local-llm.mjs "summarise this" -f -      # piped input only with -f -
 *   node local-llm.mjs -m qwen2.5:14b "..."                   # pin a model
 *
 * Model:  -m, else LOCAL_LLM_MODEL, else the first installed model from LOCAL_LLM_PREFERRED
 *         (comma-separated, biggest first), else the first model Ollama lists.
 * Env:    OLLAMA_URL (default http://127.0.0.1:11434)
 *         LOCAL_LLM_THINK=1   let reasoning models think first (slower, fewer slips)
 *         LOCAL_LLM_LOG=1     append every call to $LOCAL_LLM_DATA_DIR/calls.jsonl (opt-in; may hold
 *                             private input — keep it local, never commit it)
 *         LOCAL_LLM_DATA_DIR  where the lock file and optional log live (default ./.local-llm)
 *         LOCAL_LLM_MAX_CTX   context cap in tokens (default 65536)
 * Exit:   0 ok · 1 error · 2 Ollama not running
 */

import { readFileSync, writeFileSync, renameSync, appendFileSync, mkdirSync, openSync, closeSync, statSync, unlinkSync } from 'node:fs';
import { request } from 'node:http';
import { request as requestHttps } from 'node:https';
import { basename, join, resolve } from 'node:path';

const OLLAMA = (process.env.OLLAMA_URL ?? 'http://127.0.0.1:11434').replace(/\/$/, '');
const DATA_DIR = resolve(process.env.LOCAL_LLM_DATA_DIR ?? '.local-llm');
const PREFERRED = (process.env.LOCAL_LLM_PREFERRED ?? '').split(',').map((s) => s.trim()).filter(Boolean);
const MAX_CTX = Number(process.env.LOCAL_LLM_MAX_CTX ?? 65536);

const args = process.argv.slice(2);
const USAGE = 'usage: local-llm.mjs "prompt" [-f file]... [-s system] [-m model] [-o out]   (env: OLLAMA_URL, LOCAL_LLM_MODEL, LOCAL_LLM_THINK=1, LOCAL_LLM_LOG=1)';
if (args.length === 1 && ['-h', '--help'].includes(args[0])) {
  console.log(USAGE);
  process.exit(0);
}
const files = [];
let system, model, out, prompt = '';
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (['-f', '-s', '-m', '-o'].includes(a) && i + 1 >= args.length) {
    console.error(`${a} needs a value`);
    process.exit(1);
  }
  if (a === '-f') files.push(args[++i]);
  else if (a === '-s') system = args[++i];
  else if (a === '-m') model = args[++i];
  else if (a === '-o') out = args[++i];
  else prompt += (prompt ? ' ' : '') + a;
}
if (!prompt) {
  console.error(USAGE);
  process.exit(1);
}
// Without this the model assumes its training-time clock and flags current dates as "in the future".
const today = new Date().toISOString().slice(0, 10);
system = `Today's date is ${today}.` + (system ? `\n\n${system}` : '');

let tags;
try {
  tags = await (await fetch(`${OLLAMA}/api/tags`, { signal: AbortSignal.timeout(5000) })).json();
} catch {
  console.error(`Ollama not reachable at ${OLLAMA} — start Ollama first.`);
  process.exit(2);
}
const installed = (tags.models ?? []).map((m) => m.name);
const withTag = (m) => (m && !m.includes(':') ? `${m}:latest` : m); // Ollama lists untagged pulls as name:latest
model = withTag(model ?? process.env.LOCAL_LLM_MODEL ?? PREFERRED.map(withTag).find((m) => installed.includes(m)) ?? installed[0]);
if (!model || !installed.includes(model)) {
  console.error(`Model ${model ?? '(none)'} not pulled. Installed: ${installed.join(', ') || '(none)'} — run "ollama pull <model>".`);
  process.exit(1);
}

// Piped input only on explicit `-f -`: auto-reading stdin whenever it is not a TTY can hang forever
// in shells that hand the process an open pipe that never closes.
const context = files
  .map((f) => (f === '-' ? `<stdin>\n${readFileSync(0, 'utf8')}\n</stdin>` : `<file name="${basename(f)}">\n${readFileSync(f, 'utf8')}\n</file>`))
  .join('\n\n');
const content = context ? `${context}\n\n${prompt}` : prompt;

// Ollama defaults to a small window and silently truncates — size it to the input (~3.5 chars/token)
// plus room for the answer.
const numCtx = Math.min(MAX_CTX, Math.max(8192, Math.ceil(content.length / 3.5) + 8192));

// One local job at a time: parallel agents would otherwise load several large contexts at once and
// exhaust RAM/VRAM. A lock older than 40 min is treated as stale.
mkdirSync(DATA_DIR, { recursive: true });
const LOCK = join(DATA_DIR, '.lock');
for (let waited = 0; ; waited += 5) {
  try {
    closeSync(openSync(LOCK, 'wx'));
    break;
  } catch {
    try {
      if (Date.now() - statSync(LOCK).mtimeMs > 40 * 60 * 1000) unlinkSync(LOCK);
    } catch {}
    if (waited % 60 === 0) console.error(`[local-llm] waiting for another local job (${waited} s)`);
    await new Promise((r) => setTimeout(r, 5000));
  }
}
process.on('exit', () => {
  try {
    unlinkSync(LOCK);
  } catch {}
});
// process.exit() runs the 'exit' handler above, so an interrupted or killed run never leaves a stale lock.
process.on('SIGINT', () => process.exit(130));
process.on('SIGTERM', () => process.exit(143));

// Streamed over node:http(s), not fetch: fetch (undici) drops a request after 300 s without response
// headers, and Ollama sends none before the first token, so long or queued answers would die at 5 min.
const t0 = Date.now();
const body = JSON.stringify({
  model,
  stream: true,
  think: !!process.env.LOCAL_LLM_THINK,
  options: { num_ctx: numCtx },
  messages: [{ role: 'system', content: system }, { role: 'user', content }],
});
const doRequest = OLLAMA.startsWith('https:') ? requestHttps : request;
const data = await new Promise((resolveP) => {
  const acc = { status: 0, content: '', error: undefined, prompt_eval_count: undefined, eval_count: undefined };
  const req = doRequest(
    `${OLLAMA}/api/chat`,
    { method: 'POST', headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) } },
    (res) => {
      acc.status = res.statusCode;
      res.setEncoding('utf8');
      let buffer = '';
      const take = (line) => {
        if (!line.trim()) return;
        let chunk;
        try {
          chunk = JSON.parse(line);
        } catch {
          acc.error ??= 'non-JSON response';
          return;
        }
        if (chunk.error) acc.error = chunk.error;
        acc.content += chunk.message?.content ?? '';
        if (chunk.done) Object.assign(acc, { prompt_eval_count: chunk.prompt_eval_count, eval_count: chunk.eval_count });
      };
      res.on('data', (d) => {
        buffer += d;
        let nl;
        while ((nl = buffer.indexOf('\n')) >= 0) {
          take(buffer.slice(0, nl));
          buffer = buffer.slice(nl + 1);
        }
      });
      res.on('end', () => {
        take(buffer);
        resolveP(acc);
      });
    },
  );
  req.setTimeout(30 * 60 * 1000, () => req.destroy(new Error('no data for 30 min')));
  req.on('error', (e) => resolveP({ ...acc, error: e.message }));
  req.end(body);
});
if (data.status !== 200 || data.error || !data.content.trim()) {
  console.error(`Ollama ${data.status}: ${data.error ?? 'empty response'}`);
  process.exit(1);
}

const text = data.content.trim() + '\n';

// Opt-in call log, e.g. as raw material for a later fine-tune. May contain private input: keep it local.
if (process.env.LOCAL_LLM_LOG === '1') {
  appendFileSync(
    join(DATA_DIR, 'calls.jsonl'),
    JSON.stringify({ ts: new Date().toISOString(), model, system, prompt, files: files.map((f) => basename(f)), input: content, output: text }) + '\n',
  );
}
const stats = `[local-llm] ${model} · ctx ${numCtx} · in ${data.prompt_eval_count} tok · out ${data.eval_count} tok · ${((Date.now() - t0) / 1000).toFixed(0)} s`;
if (out) {
  // Write to a temp file and rename, so a crash never leaves a truncated output.
  writeFileSync(out + '.tmp', text, 'utf8');
  renameSync(out + '.tmp', out);
  console.log(`${stats} → ${out} (${Buffer.byteLength(text)} bytes)`);
} else {
  process.stdout.write(text);
  console.error(stats);
}
