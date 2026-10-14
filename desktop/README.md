# Shadow System — Windows Desktop

The Windows package uses Change 19 as its starting point and assembles a separate desktop dashboard from the Android WebView source. The Android files and APK workflow remain separate. The dashboard reads and writes the same Change 19 state model; the generated desktop frontend is disposable build output.

## What this build currently provides

- A local-first Windows app with the existing progression systems and a screenshot-inspired Command Center.
- User-set arc name, goal, start and end dates; editable route stages; editable built-in routines; and user-created recurring quests. Removed quests can be restored with their saved history.
- A lifetime day counter. Progression continues after an arc's end date, with the chosen route repeating as a new cycle.
- Local save data and JSON export/import. Each Windows account gets its own WebView profile; there is no account service or cloud sync in this build.
- All 11 system destinations are visible in the desktop navigation.

This is not yet the requested finished public release. Google Calendar synchronization is not implemented: the calendar uses the computer's current local date and does not display Google events. A public release needs a publisher-owned Google OAuth desktop client ID, user consent, token refresh/revocation, and sync conflict handling. Each end user should authorize their own Google account; do not ask users to paste private iCal links. The Android save model also still contains fixed Winter Arc and Day 90 presentation in several legacy screens. Automated checks pass, but a hands-on Windows browser walkthrough and a fresh installer build have not been completed for the current local edits.

## Build on Windows

Prerequisites:

- Windows 10 or Windows 11
- Node.js 22 and pnpm 11.25.0
- Rust 1.90.0 with the MSVC Windows target
- Microsoft C++ Build Tools with the Desktop development with C++ workload

From the repository root:

```powershell
Set-Location desktop
pnpm install --frozen-lockfile
pnpm run desktop:icons
pnpm run desktop:dev
```

Create an installable Windows x64 setup executable:

```powershell
pnpm run desktop:build
```

The NSIS installer is written under `desktop/src-tauri/target/release/bundle/nsis/`. The Windows GitHub Actions workflow runs the static checks and builds the installer as a downloadable artifact. The configured installer embeds Microsoft's WebView2 offline installer so setup can run without a network connection; this adds roughly 127 MB to the installer and the build machine must download that runtime while packaging.

The installed app's core features work offline. Optional Google Calendar synchronization will require an internet connection after it is implemented. The installer is unsigned, so Windows may display a publisher or SmartScreen warning until a signing certificate is configured.

## Save transfer

Android and Windows saves are separate. Use the Data Vault export on Android and import that JSON file on Windows to transfer progress. This is a manual transfer, not synchronization. Back up important records before importing or resetting a profile.
