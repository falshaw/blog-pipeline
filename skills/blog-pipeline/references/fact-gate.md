# Fact gate — nothing ships on an unverified claim

Checklist step 6b, before the deploy ask. A "verify against two sources" instruction alone does not stop errors: posts written from model memory produce wrong model sizes, wrong price ratios and cost tables off by 2–4×; posts written from coverage copy numbers from the coverage instead of the source (a network-wide total credited to one member, two papers merged into one). A gate with a table and a second agent does.

## The gate

1. **Every number, date, named study, named incident and quote** in both languages carries an inline link to its **primary** source: the paper, filing, official doc, or vendor/lab post — not a roundup.
2. **Claim table** — one row per claim, for the primary AND the secondary language:

   | # | Claim (as written) | Lang | Source URL | Primary? | Verified (quote from source) |
   |---|--------------------|------|------------|----------|------------------------------|

   **0 unlinked rows.** Put the totals (N claims · N linked · N verified) in the deploy ask.
3. **A separate verification agent** that did not write the draft opens every link and confirms each claim word for word against the fetched page. Claims it cannot confirm are **cut, not softened**.
4. **Time-sensitive claims** (regulatory deadlines, ban or export status, "currently") carry their date in the sentence.
5. Local-model output is never a source. If a local draft introduced a fact, it goes through the same table.

## The six traps (the writer checks these while writing)

Verifiers find these on almost every post — usually several per post:

1. **Headline/meta stronger than the source.** "Not yet fully using" became "Nobody uses it". The title and meta carry the source's own hedge.
2. **Venue / channel misattributed.** "Told \<outlet\>" when the person spoke at a press conference that the outlet reported; "reported at the time" when it was a social-media post. Say where it was said.
3. **Syndication ≠ original outlet.** A page on an aggregator is labelled with the outlet that actually wrote it, never the aggregator or the outlet it cites.
4. **Quotes cut mid-phrase, or paraphrase in quote marks.** Copy verbatim from the fetched page; paraphrase goes without quote marks. In the secondary language, see writing.md § Quotes.
5. **Relative time.** "This month", "this year", "until this year" go stale or were never true; use the month or date.
6. **Thesis written as finding.** The post's own argument is marked as opinion ("In our view", „Unserer Einschätzung nach“); a scout's framing ("all three leaders including X") is re-checked, not inherited.

## Verifier prompt (template)

```
You are verifying a blog draft you did not write. For each row of the claim table:
open the URL, find the passage that supports the claim, and quote it verbatim.
Mark each row CONFIRMED (quote matches the claim, including its hedge), WEAKER
(source says less than the draft), WRONG, or NOT FOUND. Do not use your own
knowledge. Report a table plus the list of rows that must be cut or rewritten.
```
