# Shadow System // Winter Arc - Windows Desktop Audit

## Baseline and scope

- Desktop work is based on Change 19 at 6ecd7a1 (versionName 5.0.0, Android versionCode 19) on the local codex/windows-desktop branch.
- The app is an existing single-page HTML/CSS/JavaScript application inside the Android WebView project. The current screens and systems are retained and loaded as local Tauri frontend assets.
- The available local history includes the Change 18 archive and earlier archives, but no separate Change 19 ZIP or full Change 1-19 archive. The public Change 19 repository snapshot is the source used here; this audit does not claim a byte-for-byte comparison against unavailable earlier files.
- Windows packaging uses Tauri 2 with the system WebView2 runtime and an NSIS setup executable. Android Gradle files and the APK workflow remain present.

## Feature inventory

WORKING means the named automated check passed. PARTIAL means there is a concrete implementation but important behavior or packaging checks remain. UNVERIFIED means the code is present, but this work has not exercised it end to end. These labels describe evidence, not a claim that every game rule is correct.

| Area | Status | Evidence and remaining check |
|---|---|---|
| Change 19 source and 11 routed screens | PARTIAL | The original HTML app and router remain. Routes cover Core, Quests, Dungeon, Skills, Character, World, Inventory, Arc, Vault, Ascension and System. Static checks confirm the World route and no duplicate function declarations; live navigation still needs a Windows run. |
| 90-day calendar and day-state history | UNVERIFIED | The state includes 90-day mission, outcome, lock-time and penalty arrays; expired days are processed by closeExpiredDays(). Day-number and Day 90 mappings pass static checks. A controlled date-based progression run is still needed. |
| Chapters, Arc milestones and Ascension | UNVERIFIED | The Arc intelligence and Monarch Ascension modules are present, and Mutation 17/18 markers remain. Chapter-by-chapter unlock and Day 90 evidence/report behavior have not been exercised. |
| Character XP, level, rank, titles and achievements | UNVERIFIED | The XP/level/rank pipeline and achievement renderer are present. Reward, rank-boundary and persistence scenarios need behavioral tests. |
| Daily/custom quests, bosses and dungeon challenges | UNVERIFIED | Quest, custom-quest, boss and dungeon state/handlers are present. Duplicate reward prevention and failure/recovery outcomes have not been simulated. |
| Skill tree, mastery and specializations | UNVERIFIED | Skill unlock, capability mastery, practice and specialization data/renderers are present. Unlock costs and progression edges have not been exercised. |
| Inventory, equipment and Build Forge | PARTIAL | Change 19 migration maps legacy artifact equipment into the Build Forge loadout and static checks confirm the build/combat/aura links. Save migration and equipment progression need scenario tests. |
| Training, focus, learning, projects and proof of work | UNVERIFIED | Focus sessions, capability practice, project/evidence and proof-entry data are present. No end-to-end session or export/import scenario has been run. |
| Journal, habits, analytics and end-of-Arc report | UNVERIFIED | Journal, habit, analytics and Ascension screens exist. The end report has not been checked against a completed 90-day history. |
| Save persistence and portable backup/restore | PARTIAL | The app uses localStorage and JSON import/export. A data-loss path on corrupt JSON was repaired: corrupt content is copied to a recovery key before defaults are used; if writes fail, editing pauses and the current recovery copy can be exported. The new Node behavior test passes corrupt-save and quota-failure cases. A full app restart and backup/restore round trip remains unverified. |
| Offline use | PARTIAL | Main HTML, JavaScript and image assets are bundled locally. Google Fonts is an optional external import with system fallbacks; the no-network launch has not been run. |
| Desktop title, sizing, icon, navigation and installer | PARTIAL | Tauri config defines a resizable 1360x900 window, a 1024x680 minimum, app identity, icon generation and a current-user NSIS setup. The Windows workflow is configured, but no installer is verified until the branch workflow succeeds. |
| Android APK workflow | UNVERIFIED | Android source and the existing build workflow are retained; the only workflow addition runs the new save-recovery behavior test. This PC has no Android SDK/JDK and its Gradle wrapper is a stub, so no local APK regression build was possible. The prior Change 19 Actions run passed before these edits. |
| Integrity checks and duplicate definitions | WORKING | node tools/self_test.js passes 36 checks, including JavaScript syntax, state schema, day mappings, route presence, asset references, Change 19 systems, and duplicate-function detection. node tools/test_storage_recovery.js passes all three recovery scenarios. |

## Desktop choice and security

Tauri fits this source because it is a local static WebView application with no Android JavaScript bridge, no network-backed core feature, and existing browser storage and JSON transfer. The desktop package uses WebView2, keeps Android storage separate, and grants only Tauri's default core window capability; it does not add broad filesystem or shell permissions.

The Windows workflow pins Node 22, pnpm 11.25.0, Rust 1.90.0, Tauri CLI 2.12.2 and Tauri 2.12.3. The pnpm lockfile is committed. The Rust lockfile and actual Windows build are still pending verification on the Windows runner.

## Remaining release checks

1. Run the branch workflow and resolve any packaging failures.
2. Verify the uploaded NSIS .exe exists and test its first launch, save persistence, import/export, upgrade and uninstall behavior.
3. Run a controlled 90-day progression/save migration suite and compare the Change 18 archive for any unique behavior absent from Change 19.
4. Run the Android APK workflow after the save-recovery addition.
5. Sign the installer only if a signing certificate is later configured. The current installer is unsigned.