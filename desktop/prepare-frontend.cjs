'use strict';
const fs = require('node:fs');
const path = require('node:path');

function prepareFrontend(root = path.resolve(__dirname, '..')) {
  const source = path.join(root, 'app', 'src', 'main', 'assets');
  const desktop = path.join(root, 'desktop');
  const output = path.join(desktop, 'frontend');
  const sourceHtml = path.join(source, 'index.html');
  if (!fs.existsSync(sourceHtml)) throw new Error('Change 19 Android WebView source is missing: ' + sourceHtml);

  fs.rmSync(output, { recursive: true, force: true });
  fs.cpSync(source, output, { recursive: true });
  let html = fs.readFileSync(sourceHtml, 'utf8');
  if (html.includes('desktop-dashboard.js')) throw new Error('The source already contains a generated desktop dashboard include.');
  const cssTag = '<link rel="stylesheet" href="./desktop-dashboard.css">';
  const jsTag = '<script src="./desktop-dashboard.js"></script>';
  const shellTag = '<script>document.documentElement.classList.add("desktop-shell");</script>';
  if (!html.includes('</head>') || !html.includes('</body>')) throw new Error('Could not locate the HTML insertion points.');
  html = html.replace('</head>', shellTag + '\n' + cssTag + '\n</head>');
  html = html.replace('</body>', jsTag + '\n</body>');
  html = html.replace(/@import\s+url\(['"]https:\/\/fonts\.googleapis\.com\/[^)]*\);?\s*/gi, '');
  fs.writeFileSync(path.join(output, 'index.html'), html, 'utf8');
  fs.copyFileSync(path.join(desktop, 'desktop-dashboard.css'), path.join(output, 'desktop-dashboard.css'));
  fs.copyFileSync(path.join(desktop, 'desktop-dashboard.js'), path.join(output, 'desktop-dashboard.js'));
  const desktopAssets = path.join(desktop, 'assets');
  if (fs.existsSync(desktopAssets)) fs.cpSync(desktopAssets, path.join(output, 'assets'), { recursive: true });
  return { output, assets: fs.readdirSync(path.join(output, 'assets')).length };
}

if (require.main === module) {
  const result = prepareFrontend();
  console.log('Prepared Windows frontend from Change 19: ' + result.assets + ' bundled assets.');
}

module.exports = { prepareFrontend };
