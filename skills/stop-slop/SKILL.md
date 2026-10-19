---
name: stop-slop
description: Removes AI writing patterns from prose (GPT-ism vocabulary, significance inflation, contrast formulas, em-dash density, chatbot register), in English and German, and scores the result on five axes. Use when drafting, editing or reviewing text, for "stop-slop", "de-slop this", "remove the AI tells", "does this sound like AI", "humanise this", and as the mandatory pre-deploy pass on every blog-pipeline post. Edits prose only, never code, CSS or a built site tree.
metadata:
  trigger: Writing prose, editing drafts, reviewing content for AI patterns
  author: Hardik Pandya (https://hvpandya.com) — upstream; fork changes listed in NOTICE.md
  upstream: https://github.com/hardikpandya/stop-slop
---

# Stop Slop

Eliminate predictable AI writing patterns from prose.

## About this fork

Fork of the upstream [`stop-slop`](https://github.com/hardikpandya/stop-slop) skill by Hardik Pandya (MIT, see [LICENSE](LICENSE)). This fork turns the rhythm, adverb, and em-dash absolutes into review flags rather than hard bans: judge each case, cut what is empty, keep what is load-bearing. The phrase blacklist, the GPT-ism vocabulary swap, and the false-agency rule (name the human) are the high-value core and stay as hard rules. It adds a German section and a few patterns from `no-ai-slop`. Every fork change is listed in [NOTICE.md](NOTICE.md). Pairs with `blog-pipeline` (mandatory pass before every deploy, score ≥35/50).

**Why flag, not ban.** The tell is density, not the device. A human reaches for an em-dash or a three-item list now and then; AI reaches for them on every line. Cutting *every* em-dash or *every* adverb on sight just swaps one robotic tic for another — what the machine actually lacks is the taste to know when one earns its place. So flag the pattern, count how often it recurs, and cut for taste. The judgment is the point.

## Scope & safety (HARD RULE — read first)

stop-slop edits **prose only** — the words in a draft. It is NOT a global find/replace and NEVER runs over code, CSS, HTML attributes, inline styles, JSON, or a built/deployed file tree.

- **The em-dash rule targets the `—` / `–` glyph itself — it must NEVER touch the punctuation around it.** In particular, NEVER delete a comma. A regex that collapses `,.`→`.` turns every CSS `rgba(r,g,b,.5)` into invalid `rgba(r,g,b.5)` and silently destroys a site's colours. A site-wide punctuation sweep of exactly this kind can corrupt thousands of colour values in one pass.
- **There is no "site-wide em-dash sweep."** Apply edits to a manuscript, never to a whole site or a tree of HTML/CSS. A bulk character replace over built files is the classic way to break production.
- **Verification gate:** after ANY bulk text edit that could reach markup, run `grep -rnE 'rgba\([0-9]+,[0-9]+,[0-9]+\.[0-9]+\)' <edited files>` (a comma-stripped colour). It MUST return zero. Non-zero = you corrupted CSS → revert. Render one page before declaring done. (Use `[0-9]`, not `\d`: `grep -E` has no `\d`, so a `\d` pattern matches nothing and passes on broken CSS.)

## Core Rules

1. **Cut filler phrases and AI vocabulary.** Remove throat-clearing openers and emphasis crutches. Swap GPT-ism words (delve, leverage, robust, seamless, tapestry, underscore, testament, realm, foster) for the plain word you'd actually say out loud. Flag every adverb: cut the empty ones, keep the load-bearing ones that change the meaning. See [references/phrases.md](references/phrases.md).

2. **Break formulaic structures.** Avoid binary contrasts, negative listings, dramatic fragmentation, rhetorical setups, false agency. See [references/structures.md](references/structures.md).

3. **Prefer active voice.** Default to a human subject doing something, and never let inanimate objects perform human actions ("the complaint becomes a fix" — someone fixed it). Passive is a *flag*, not a ban: in technical and security prose the actor is sometimes unknown or irrelevant ("the port was left open", "the key was rotated") and forcing an actor there reads worse. Flag each passive; rewrite the ones that hide a knowable actor.

4. **Be specific.** No vague declaratives ("The reasons are structural"). Name the specific thing. No lazy extremes ("every," "always," "never") doing vague work.

5. **Put the reader in the room.** No narrator-from-a-distance voice. "You" beats "People." Specifics beat abstractions.

6. **Vary rhythm.** Mix sentence lengths. Vary list length — sometimes two items, sometimes three or more; do not mechanically forbid three. End paragraphs differently. Flag em dashes by **frequency**, not one at a time: two or three across a piece reads human, a dozen is the tell — thin them out and keep only the one or two that genuinely beat a comma or period. (`blog-pipeline` makes this concrete per site: a site may set `em_dash_policy: none`, otherwise under ~3 per 1,000 words.)

7. **Trust readers.** State facts directly. Skip softening, justification, hand-holding.

8. **Cut quotables.** If it sounds like a pull-quote, rewrite it.

9. **Deflate significance.** AI inflates ordinary facts into milestones: "a testament to", "underscores the importance of", "marks a key turning point", "leaves an indelible mark", "setting the stage for", "evolving landscape", "enduring legacy". State the fact; let the reader decide if it matters. Same family: copula avoidance — "stands as / serves as / boasts / features" where "is" or "has" would do.

10. **Strip chatbot register.** Assistant-voice leaking into prose: "Great question", "You're absolutely right", "Honestly?", "Here's the kicker", "Let's dive in", "But that's only half the story". These are conversation moves, not writing — delete them.

11. **German drafts get the German list.** The same logic applies in German: openers („In der heutigen schnelllebigen Welt“), puffery („spielt eine entscheidende Rolle“), buzzwords („nahtlos“, „ganzheitlich“), the „Es geht nicht um X, sondern um Y“ formula, and Denglisch overload. See the German section of [references/phrases.md](references/phrases.md).

## Don't over-correct

The failure mode of anti-slop editing is now itself a tell. Three rules:

- **Rewrite, don't thesaurus-swap.** Replacing a flagged word with a rare synonym produces "syntax salad" — improbable word choices that read worse than the original and are detectable in their own right. Cut the clause or restate the fact plainly instead.
- **Density is the signal, never a single hit.** One em-dash, one "not X but Y", one "robust" proves nothing — humans use all of these. Flag on repetition and co-occurrence across the piece.
- **Stale tells have flipped.** "Delve/tapestry/realm/beacon" largely vanished from model output in 2025; treat them as low-weight legacy checks. The current generation's fingerprint is structural: significance inflation, dangling "-ing" analysis tails, copula avoidance, uniform paragraph geometry, contrastive-construction density. Weight those. And never "de-polish" clean human prose just to look less like AI — em-dashes and good rhythm are allowed to survive the edit.

## Quick Checks

Before delivering prose:

- Any adverbs? Flag each one — cut the empty ones, keep the load-bearing ones.
- Any GPT-ism vocabulary (delve, leverage, robust, seamless, tapestry, underscore, testament, realm, foster, myriad)? Swap for the plain word.
- Any passive voice? Find the actor, make them the subject.
- Inanimate thing doing a human verb ("the decision emerges")? Name the person.
- Sentence starts with a Wh- word? Flag it as a possible crutch — restructure when it is one, leave it when it reads naturally.
- Any "here's what/this/that" throat-clearing? Cut to the point.
- Any "not X, it's Y" contrasts? State Y directly.
- Three consecutive sentences match length? Break one.
- Paragraph ends with punchy one-liner? Vary it.
- Em dash anywhere? Flag it — prefer a comma or period, but keep it where it genuinely reads best.
- List always landing on three items? Flag the pattern and vary the length; do not forbid three.
- Vague declarative ("The implications are significant")? Name the specific implication.
- Narrator-from-a-distance ("Nobody designed this")? Put the reader in the scene.
- Meta-joiners ("The rest of this essay...")? Delete. Let the essay move.
- Signposted conclusion ("In conclusion," "To sum up," "Ultimately,")? Cut the signpost; just say the thing.
- An "-ing" tail bolting shallow analysis onto a fact ("highlighting the need for," "reflecting a broader shift")? Cut it or make it a real clause.
- "Serves as / stands as / represents / boasts" where "is"/"has" would do? Use "is"/"has."
- Significance inflation ("a testament to," "underscores the importance," "turning point," "evolving landscape")? State the plain fact.
- Chatbot register ("Great question," "You're absolutely right," "Let's dive in")? Delete.
- "Whether you're a X or a Y" dual-audience opener? Pick the actual reader and speak to them.
- Vague authority ("experts note," "observers say," "widely regarded")? Name the source or cut the claim.
- Every paragraph the same 3-sentence rectangle? Merge, split, vary — burstiness reads human.
- Formatting tells: bold-inline-header bullets everywhere, emoji bullets, "X: A Comprehensive Guide" colon-subtitle headings, `---` breaks before every heading? Strip them.
- Vague connection ("associated with," "in connection with," "linked to") where a direct verb exists? Say what the relationship is.
- Promotional travel-guide register ("vibrant," "nestled," "rich heritage," "diverse array," "groundbreaking")? State the plain fact.
- "Y rather than X" / "not just X but also Y" parallelism stacking up? Same density rule as "not X, but Y."
- Chatbot residue in links or markup (`utm_source=chatgpt.com`, `oaicite`, `contentReference`, `[cite: 1]`)? Strip the parameter or artifact; on a blog post, re-check that the link is the primary source.
- Headings that skip a level (H2 → H4) or "X and Y" section titles ("Challenges and Legacy," "Awards and Recognition")? Fix the hierarchy, retitle with what the section argues.
- German text: any „Zusammenfassend lässt sich sagen“, „von entscheidender Bedeutung“, „Mehrwert schaffen“, or English where a common German word exists? Fix per the German list.

Source for the Wikipedia-derived checks: Wikipedia, "Signs of AI writing" (https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Detail in the two reference files.

## Scoring

Rate 1-10 on each dimension:

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds human? |
| Density | Anything cuttable? |

Below 35/50: revise.

**Loop until it passes:** score → list the concrete hits (quote each) → revise → re-score. Stop only at ≥35/50, and report the final score with the axis breakdown (blog-pipeline puts it in the deploy ask). Score each language separately. After the last pass on anything that will reach HTML, run the rgba verification gate above.

## Optional second opinion (independent model)

The writer is a poor judge of its own tells, so a cheap pass by a *different* model helps. If you run Ollama locally, the `blog-pipeline` helper does it without spending your main model's tokens:

```bash
node .claude/skills/blog-pipeline/scripts/local-llm.mjs \
  -s "You detect AI writing tells. List ONLY concrete instances found in the text, each quoted verbatim: 'not X, it's Y' antithesis, delve/leverage/robust/seamless, em-dash overuse, tricolon padding, hedging stacks, empty transitions (Moreover, Furthermore), summary sentences restating the paragraph. German too: 'Zusammenfassend', 'nahtlos', 'ganzheitlich', 'Es geht nicht um X, sondern um Y'. If the text is clean, say CLEAN." \
  "Find the AI tells in this text." -f draft.md
```

**This does NOT replace the rules above.** Small local models miss things a careful read catches. Treat a `CLEAN` verdict as weak evidence, never as a pass.

## Examples

See [references/examples.md](references/examples.md) for before/after transformations.

## License

MIT — upstream copyright and permission notice in [LICENSE](LICENSE); fork changes and third-party credits in [NOTICE.md](NOTICE.md).
