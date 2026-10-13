# Shadow System // Winter Arc - Windows Desktop

This is the Windows desktop package for the Change 19 baseline. It loads the existing bundled HTML, JavaScript, CSS and assets from the Android app, so desktop and Android keep the same progression system and content. The Android Gradle project and APK workflow remain separate.

## Build and run on Windows

Development prerequisites:

- Windows 10 (April 2018 or newer) or Windows 11
- Node.js 22
- pnpm 11.25.0
- Rust 1.90.0 with the MSVC Windows target
- Microsoft C++ Build Tools with the Desktop development with C++ workload

From the repository root:

```powershell
Set-Location desktop
pnpm install --frozen-lockfile
pnpm run desktop:icons
pnpm run desktop:dev
```

To make the installable Windows x64 setup executable:

```powershell
pnpm run desktop:build
```

The installer is written under `desktop/src-tauri/target/release/bundle/nsis/`. The separate GitHub Actions workflow builds the same NSIS installer on a Windows runner and uploads it as the `ShadowSystem-Windows-Installer` artifact.

## Progress and backups

Windows and Android keep separate local saves. The Windows app uses the WebView2 profile for its local browser storage; it does not silently copy Android WebView data or sync across devices. Use the app's Data Vault export on Android and import that JSON backup on Windows if you want to transfer progress.

The interface and game systems are bundled locally. The existing Google Fonts import is optional for appearance; system font fallbacks remain available when offline.

The installer is not code-signed. Windows may show a publisher or SmartScreen warning until a signing certificate is configured.
