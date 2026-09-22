# Shadow System // Winter Arc — Change 19

## SYSTEM CORE REFACTOR // STABILIZATION

Change 19 is an architecture and reliability pass, not a new feature mutation. It consolidates the Winter Arc into one coherent real-life progression system.

### Core fixes
- One authoritative 90-day time model with consistent Day 1–90 display indexing.
- Explicit PRE-ARC state before October 1, 2026; progression cannot be earned early.
- Historical day sealing remains immutable; future days never require yesterday to be completed.
- One authoritative screen router, including a working WORLD destination.
- Rank visual evolution is connected to the real XP/rank engine.
- One authoritative Build Forge equipment source.
- Legacy artifact-equipment slots migrate into Build Forge and no longer compete with it.
- Build Forge stats now feed Character Power, Aura Power and Dungeon Combat Power.
- Equipment progression has real Day gates rather than immediate acquisition.
- Dungeon and combat use the same build/power state.
- Mutation 15–18 systems read the same state model and time model.
- Obsolete Moonlit/V6 simplicity runtime removed; useful legacy telemetry remains as a single telemetry surface.
- Runtime System Integrity audit added to the SYSTEM screen.
- Build-time static self-test added before Gradle runs.

### System Integrity checks
The app checks state schema, time model, navigation, rank pipeline, Build Forge, combat/aura links, Day 90 environment/event mapping, dungeon state, proof state, ascension state and legacy-equipment migration.

### Android
- Version: **5.0.0**
- versionCode: **19**
- application label: **Shadow System // Winter Arc**
- compile/target SDK: 35
- Java: 17 in GitHub Actions
- Gradle: 8.7 in GitHub Actions

### Build on GitHub
1. Push the project contents to `main`.
2. Open **Actions → Build Shadow System APK**.
3. The workflow runs the Change 19 self-test before Gradle.
4. A failed self-test stops the Android build.
5. On success, open the run → **Artifacts** → `ShadowSystem-final-apk`.
6. Download `app-debug.apk` to Android and install it.
