# Shadow System // Winter Arc — Change 19 Architecture

## Source of truth

- `state` is the single persisted runtime state.
- `currentDay()` remains the zero-based internal day index for compatibility; `currentDayNumber()` is the authoritative user-facing Day 1–90 number.
- `arcHasStarted()` gates all progression before 2026-10-01.
- `switchSystemScreen()` is the authoritative screen router.
- `GEAR14` + `loadouts` + `gearStats14()` are the single active equipment system. Legacy artifacts are acquisition/history only.
- `buildStats()` feeds Character Power, Aura Power and Dungeon Combat Power.
- Mutation 15–18 consume the same state/time/proof records.

## Day model

The calendar is time-driven, not completion-driven. A day can close as PERFECT, COMPLETE, PARTIAL or SURVIVED/FAILED without blocking the next day. Historical day state is immutable.

## Pre-Arc model

Before October 1, 2026 the app is explicitly in `PRE-ARC`. The UI may preview the system, but quests, focus rewards, combat, proofs, projects, mastery and progression rewards cannot be earned early.

## Build gate

`tools/self_test.js` runs before Gradle in GitHub Actions. It validates JavaScript syntax, duplicate function declarations, asset references, version metadata, Day 1–90 indexing, World/Ascension mappings, mutation retention and the stabilized architecture anchors.
