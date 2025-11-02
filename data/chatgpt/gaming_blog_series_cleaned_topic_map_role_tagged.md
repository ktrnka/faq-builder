# Goal
Organize potential posts about my time in games, tagging each topic by my role so we don’t over-claim ownership. Also mark exploit/sensitivity risk.

Legend — Role tags:
- **[Built]** I implemented/built core pieces
- **[Led/Co-built]** I drove design/prototype or shared implementation
- **[Observed]** Peers’ systems; I learned from/operated around them

Risk tags:
- (Low) safe to share at principle level
- (Med) avoid operational details that enable bypass
- (High) likely off-limits without heavy redaction

---

## A) Technical implementations **I** did
*(Posts about work I directly built; keep at principles + anecdotes level.)*

1) **Language-aware matchmaking via embeddings (Redis + cosine)** — **[Built]** (Low)
   - Server embeddings = sum of player vectors; probabilistic tie-breaks; time-of-day shifts
   - Lessons: low-latency social routing, safe randomness, incremental rollout

2) **Rule-based profanity filter → CI-driven tuning (multilingual)** — **[Led/Co-built]** (Med)
   - Sampling, per-language FP/FN checks, community examples → tests
   - Lessons: data-first improvements before ML, cultural/linguistic nuance

3) **Friend recommendations / pro-social grouping prototypes** — **[Led/Co-built]** (Low)
   - Cold start pre-launch; path from heuristics → embeddings → social graph ideas
   - Lessons: prototyping under data scarcity, stakeholder feedback loops

4) **Bug fixes in Rust/Unreal to unblock >1.5M players** — **[Built]** (Low)
   - Focus on reliability; breadth-first “fullest-stack” learning
   - Lessons: ownership vs visibility trade-offs, triage habits

5) **Feature-flagging aspirations for engine-backed games** — **[Observed→Advocated]** (Low)
   - What classic SaaS flags miss; feasible patterns: server-side config, content gating, staged rollout via shards

6) **Internal builds & playtests: why edge cases escape** — **[Built/Observed]** (Low)
   - 50–100 person playtests vs 100k+ players; telemetry habits that help

> **Not in this bucket:** scaling architecture, timed-event autoscaling, monetization plumbing — those were mostly peers’ work (see C).

---

## B) Cultural notes & observations for tech folks
*(Best broad-read category; all **[Observed]** with firsthand stories.)*

1) **“Necessary chaos” in creative work vs avoidable chaos** — (Low)
   - Finding the fun; where process helps/hurts; prioritization anti-patterns

2) **Communication hygiene** — (Low)
   - Email vs docs vs Slack vs meetings; public channels > DM silos; habits from 98point6 that transferred well

3) **LiveOps vs SaaS mental models** — (Low)
   - Planned downtime; client/server lockstep; seasonal/event cadences; community temperature

4) **Feedback at firehose scale** — (Low)
   - Passion, bandwagoning, parasocial dynamics; why fixes rarely get applause

5) **Measuring success in F2P** — (Low)
   - Quantity vs quality metrics; retention funnels; seasonal-events as signal; org challenges turning data → change

6) **Generalists vs specialists (and indie vs studio)** — (Low)
   - When generalists shine; specialization at scale; my “fullest-stack” experiment

7) **Iteration speed & why A/B/flags aren’t trivial in games** — (Low)
   - Engine constraints; fairness/consistency expectations for players

8) **Dogfooding spectrum: Swype → healthcare → Palia** — (Low)
   - What you can/can’t learn internally; when to expect surprises post-launch

---

## C) System design observations from peers (respectful, high-level)
*(Frame as principles; do **not** attribute to individuals; keep internal numbers out.)*

1) **Engine-constrained release pipelines (Unreal client+server lockstep)** — **[Observed]** (Low)
   - Why hot-swapping is hard; SDLC that acknowledges lockstep updates

2) **Matchmaking & world sharding trade-offs** — **[Observed]** (Low)
   - Population feel vs cost; friends-first routing; social vs performance

3) **Event-driven capacity planning** — **[Observed]** (Low)
   - Calendar-aware autoscaling; pre-warming for top-of-hour spikes; design–infra sync

4) **Observability for live games** — **[Observed]** (Low)
   - Player-centric SLOs; what to log/alert that differs from SaaS

5) **Monetization & regionalization (principles only)** — **[Observed]** (Low)
   - Storefronts vs bespoke payments; regional sensitivity w/o exact multipliers; fraud vectors exist

---

## D) “Insider Q&A” short-post series (optional)
*(Each answers one classic tech→games question; links to deeper posts.)*
- Why do games have planned downtime?
- Why can’t you just A/B‑test everything?
- Why don’t players praise fixes?
- Why are internal playtests not enough?
- Why does feature flagging look different in games?

---

## Next actions
1) Pick 2–3 items from **A** and **B** to draft first (likely: A1, A2, B1/B3/B4).
2) For each: create a one-page brief (working title, thesis, key anecdotes, do/don’t list, risk notes).
3) Maintain a redline list (what we’ll never publish: thresholds, wordlists, capacity limits, internal IDs, bypass paths, private diagrams).

