# Shadow System — Windows Desktop Audit

## Baseline and scope

- The desktop package is based on local Change 19 (`6ecd7a1`, Android versionCode 19 / versionName 5.0.0) on `codex/windows-desktop`.
- Android remains a single-page HTML/CSS/JavaScript WebView app. Tauri packages a generated copy of its local assets and adds the Windows dashboard without replacing the Android source or APK workflow. The Windows installer embeds the WebView2 offline runtime; Android keeps its existing Gradle/APK workflow.
- The local archive does not contain every Change 1–19 file. A sampled comparison of 19 markers across the available archives found the sampled earlier markers in Change 19; it is not a full mutation-by-mutation audit.
- Changes are committed locally and will be published with a normal fast-forward push; no force-push is used.

## Verification status

`PASS` means the named automated check completed. `PARTIAL` or `UNVERIFIED` means the feature has not passed a full interactive Windows release check. Static source checks are not proof that every button or game rule works.

| Area | Status | Evidence and remaining work |
|---|---|---|
| Desktop frontend preparation | PASS | `node desktop/prepare-frontend.cjs` assembled 173 bundled assets. Its separate generated copy leaves the Android HTML source intact. |
| Change 19 integrity | PASS | `node tools/self_test.js` passed 38 checks, including syntax, route destinations, assets, version and save-recovery guards. |
| Save recovery | PASS | `node tools/test_storage_recovery.js` passed three corrupt-save and storage-failure scenarios. |
| Desktop navigation and wiring | PARTIAL | Static frontend checks pass and all 11 destination links are now visible, including Living World, Personal Arc and Lifetime Record. A live click-through has not been completed. The browser tool rejected local app-file access and explicitly disallowed alternate browser routes, so no workaround was attempted. |
| User customization | PARTIAL | Name, arc name and goal, start/end dates, up to 12 route stages, existing routine names/descriptions/rewards/active state, and custom quest definitions are editable. Routine count and per-stage date boundaries are not user-defined. One arc is limited to 100 years. |
| Lifetime calendar and progression | PARTIAL | Start dates use the current machine-local date by default; historical dates remain selectable and missed days are not sealed. The lifetime day counter continues after an arc ends and the route repeats in cycles. Some inherited Arc/Ascension screens and metrics still use fixed Day 90 language and need a wider redesign. Calendar entries currently use the system clock; Google events are not synced. |
| Custom quest library | PASS / PARTIAL | `node tools/test_custom_quest_rewards.js` checks zero-XP rewards, edited rewards, recurring quest completion and undo accounting. Removal now archives a quest and its period history, with a restore action. Real WebView click and save-reload behavior still need a Windows test. |
| Google Calendar | NOT IMPLEMENTED | No OAuth client, Google sign-in, event import, token handling or sync conflict handling exists in this source. A public release needs the publisher's desktop OAuth client ID and a complete consent/sync flow. User-pasted private iCal links are not a safe shortcut. |
| Other progression modules | UNVERIFIED | Character, skills, equipment, bosses, dungeons, evidence, journal and analytics code is present. Their reward boundaries, migrations and save round trips have not been exercised end to end. |
| Local data and profiles | PARTIAL | JSON export/import and local recovery are present. This build has no service account or cloud sync; each Windows account has a local WebView profile. |
| Offline installer | PARTIAL | Tauri is configured to embed Microsoft's WebView2 offline installer. The app's bundled core does not need internet after setup; this configuration increases the installer by about 127 MB. Installer creation and a no-network installation have not been run for the current changes. |
| Current Windows executable | NOT BUILT HERE | A prior Actions run produced an installer for an earlier state, documented in the previous audit. It does not include today's uncommitted changes. Rust/Cargo are not installed in this local environment, so the native Tauri build could not run. The checked-in Actions workflow can build after changes are committed and pushed, but no upload was made. |
| Android workflow | UNVERIFIED | Android source and workflow remain in place. The available PC has no Android SDK/JDK and the local Gradle wrapper is a stub, so an APK regression build was not possible. |

## Release configuration

Tauri 2 uses Windows WebView2 and an NSIS per-user installer. The workflow pins Node 22, pnpm 11.25.0, Rust 1.90.0, Tauri CLI 2.12.2 and Tauri 2.12.3. The Cargo dependency graph is not yet locked with a committed `Cargo.lock`. The installer is unsigned, so SmartScreen may show an unknown-publisher warning.

## Remaining release work

1. Make the inherited fixed 90-day screens and metrics reflect the user's chosen route and remain editable for life.
2. Finish add/remove/custom schedule behavior for routines and route stages, and preserve records when dates or definitions change.
3. Implement publisher-configured Google OAuth and Calendar sync, including offline changes and conflict recovery.
4. Run a real Windows installer build, installation, first launch, navigation, persistence, export/import, upgrade/uninstall and offline checks.
5. Run Android CI after the latest source changes and review a complete Change 1–19 archive if one becomes available.
6. Commit `Cargo.lock` and configure code signing before public distribution.
