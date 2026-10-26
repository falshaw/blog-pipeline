# NOTICE — stop-slop fork

This folder is a modified copy of **stop-slop** by Hardik Pandya.

- Upstream: https://github.com/hardikpandya/stop-slop
- Licence: MIT, Copyright (c) 2025 Hardik Pandya — full text in [LICENSE](LICENSE), kept unchanged as the licence requires.

## Changes in this fork

1. **Flag, not ban.** The rhythm, adverb and em-dash absolutes became review flags judged by density; the phrase blacklist, GPT-ism swap and false-agency rule stay hard rules.
2. **Scope & safety section.** Prose-only scope and the comma-stripped `rgba()` verification gate.
3. **"Don't over-correct" section** and extra quick checks (significance inflation, copula avoidance, chatbot register, vague authority, formatting-layer tells, model artifacts in links), several sourced from Wikipedia, "Signs of AI writing".
4. **German section** (`references/phrases.md` → "German AI tells (Deutsch)") and rule 11 — written for this fork.
5. **Patterns from no-ai-slop** (`references/phrases.md` → "Added from no-ai-slop"): weasel attribution, faux-insight setups, importance puffery, superficial analysis tails, fake-profound endings.
   - Source: https://github.com/petergyang/no-ai-slop — MIT License, Copyright (c) 2026 Peter Yang — full text in [LICENSE-no-ai-slop](LICENSE-no-ai-slop).
6. Example 7 ("keep what's load-bearing") in `references/examples.md`.
7. Optional second-opinion pass through a local model instead of a hosted API.

The fork changes are released under the same MIT terms.
