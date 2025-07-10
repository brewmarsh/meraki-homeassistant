const fs = require('fs');

try {
  const manifest = JSON.parse(
    fs.readFileSync('custom_components/meraki_ha/manifest.json', 'utf8')
  );
  console.log(manifest.version);
} catch (error) {
  console.error('Error reading manifest.json:', error);
  process.exit(1);
}
