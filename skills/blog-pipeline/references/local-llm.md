# Local model lane — drafts on Ollama, judgement stays with the agent

Optional. Enable with `defaults.local_llm.enabled: true`. Goal: spend as few main-model tokens as possible on bulk reading and first drafts.

## Setup

1. Install [Ollama](https://ollama.com) and pull a capable instruct model. For bilingual drafting a 27B–32B dense model is a good floor; smaller models write noticeably weaker German and invent facts more often.
2. Pick the model: `-m <model>` per call, or `LOCAL_LLM_MODEL`, or `LOCAL_LLM_PREFERRED=modelA,modelB` (first installed wins); with none set, the first installed model is used. Ollama on another host or port: `OLLAMA_URL` (default `http://127.0.0.1:11434`). The script reads only these flags and variables, not the config.
3. Test: `node .claude/skills/blog-pipeline/scripts/local-llm.mjs "Say OK."` — exit 2 means Ollama is not running.

Script: [../scripts/local-llm.mjs](../scripts/local-llm.mjs). System prompt: [../scripts/prompts/no-slop-writer.md](../scripts/prompts/no-slop-writer.md).

## Split of work

| Local model | Agent |
|-------------|-------|
| Digest long sources into the facts and quotes the post needs | Topic choice (the user picks), the outline and the take |
| First primary-language draft from the agent's outline + sourced fact notes | Edits to the drafts — fix, don't rewrite |
| First secondary-language draft written natively from the edited primary | stop-slop, every gate, every fact check |
| Bulk categorising, reformatting | Everything that is deployed or sent |

## Commands

```bash
LLM=.claude/skills/blog-pipeline/scripts/local-llm.mjs
SYS="$(cat .claude/skills/blog-pipeline/scripts/prompts/no-slop-writer.md)"
export LOCAL_LLM_MODEL=qwen2.5:32b              # or pass -m <model> per call
# export OLLAMA_URL=http://127.0.0.1:11434      # only if Ollama is not on the default address

# digest a long source into fact notes (input never enters the agent's context)
node $LLM -s "$SYS" "Extract every number, date, named source and verbatim quote relevant to <topic>, each with where it appears." -f source.txt -o notes.md

# primary draft from outline + notes
node $LLM -s "$SYS" "Write the blog post from this outline and these notes. Use only facts from the notes." -f outline.md -f notes.md -o post.en.md

# native secondary-language draft
node $LLM -s "$SYS" "Write the German version of this post for German readers, natively, not as a translation. Keep every fact, number, quote and link." -f post.en.md -o post.de.md
```

Read outputs in parts (`head`, `grep`), never whole when you only need a check.

## Rules

- **Local output is a draft.** Every fact in it goes through the fact gate; small models invent banks, deadlines and statistics with full confidence.
- **One local job at a time** — the script holds a lock file so parallel agents queue instead of loading several large contexts.
- **Don't fork per-site agents on a token-saving run** — a forked agent carries the whole conversation. Run the sites one after another.
- **Call log is opt-in** (`LOCAL_LLM_LOG=1` → `.local-llm/calls.jsonl`). It may contain private input: keep it local, never commit or upload it.

## Corrections as training data (optional)

If you plan to fine-tune the local model later, keep each corrected draft as a pair: system = the no-slop prompt, user = the exact task + input, assistant = your corrected text, plus `meta: {type: "correction", source, fixed: "<what was wrong>", date}` — one JSONL line per pair, primary and secondary separately. A few pairs cannot move a large model; wait until you have dozens before training. Only publishable text belongs in a training set that leaves your machine.
