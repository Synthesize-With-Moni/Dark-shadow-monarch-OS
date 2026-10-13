# Change 19 — Stabilization Audit

## Confirmed fixed

1. **World routing** — `world` is now registered in the authoritative router.
2. **Rank visual** — `rankFromXP()` is defined and tied to `rankForLevel(levelFromXP())`.
3. **Day 1–90 indexing** — user-facing systems use `currentDayNumber()`; internal grid storage remains zero-based.
4. **Day 90** — Ascension environment and World Ascension event are reachable on actual Day 90.
5. **Pre-Arc** — before 2026-10-01 the app is `PRE-ARC`; progression rewards are gated.
6. **Equipment** — old artifact-equipment state migrates into Build Forge and is no longer an active parallel equipment source.
7. **Build integration** — Build Forge feeds character power, aura and combat power.
8. **Equipment gating** — gear has real Arc-day requirements.
9. **Dungeon threat** — the missing `dungeonThreat()` adapter is now defined and backed by the authoritative threat engine.
10. **Mutation 17/18** — both remain intact and use the stabilized day model.
11. **V6 simplicity runtime** — obsolete Soft Ascension/simple-mode runtime was removed; useful telemetry remains under one renderer.
12. **Router** — Ascension rendering is integrated into the main router rather than a second router override.
13. **Import migration** — imported old saves are passed through the same Change 19 migration path.
14. **Runtime integrity** — the app has a System Integrity panel with checks and a manual re-run action.
15. **Build gate** — GitHub Actions runs `tools/self_test.js` before Gradle.

## Static verification

The Change 19 self-test currently passes **36 checks**, including:
- JavaScript syntax
- state schema
- PRE-ARC model
- Day-number model
- World route
- rank engine
- Build Forge
- dungeon threat engine
- combat/aura links
- Day 90 mappings
- runtime audit presence
- duplicate function declarations
- obsolete V6 simplicity removal
- asset references and dynamic asset families
- Android version metadata
- workflow self-test integration
- Mutation 17/18 retention
- Corrupt-save recovery and save-failure guard

## Design rule

**No more mutation stacking until the stabilized core survives the APK test.**
