# Engagement pass with `last30days` (optional, third-party)

[`last30days`](https://github.com/mvanhorn/last30days-skill) is a separate skill that pulls the last 30 days of discussion on a topic from Reddit, X, YouTube, Hacker News and the web. In blog-pipeline it is the **engagement pass on a story you already picked** — never a topic-discovery tool (it needs a topic as input).

## What it is for

The community *reaction*: the contrarian read, the real pain point, the quotable practitioner line with a named handle. Fed a real story it surfaces things like the user question nobody in the press asked ("can I set a maximum drawdown per agent?") — exactly the material that makes a take feel first-hand.

## Preflight

- Run its diagnose / preflight mode first and read which sources are available. Missing tools (e.g. `yt-dlp` for YouTube transcripts, an authenticated `gh` for GitHub, X cookies) silently drop sources.
- **Always pass a plan with real sub-queries** (`--plan`); a bare invocation is the degraded path.
- **Always pass target subreddits** (`--subreddits`) from your beat's source table: the public Reddit endpoint intermittently refuses requests and falls back to a thinner feed, which is the usual cause of all-single-source clusters.
- Prediction-market blocks return noise on non-market topics; pass explicit keywords or ignore the block.
- Check the flag names against the version you have installed; they change between releases.

## Reading the output

Clusters tagged single-source are noise, not reaction. If the whole result is single-source, the story has not landed or sources are down — say so in your notes and don't present a two-like post as a groundswell.
