const fs = require('fs');
const path = require('path');

const packageJsonPath = path.join(__dirname, '..', 'package.json');
const manifestJsonPath = path.join(__dirname, '..', 'custom_components', 'meraki_ha', 'manifest.json');

try {
  const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
  const manifestJson = JSON.parse(fs.readFileSync(manifestJsonPath, 'utf8'));

  if (manifestJson.version !== packageJson.version) {
    console.log(`Updating manifest.json version from ${manifestJson.version} to ${packageJson.version}`);
    manifestJson.version = packageJson.version;
    fs.writeFileSync(manifestJsonPath, JSON.stringify(manifestJson, null, 2) + '\n');
    console.log('Successfully updated manifest.json version.');
  } else {
    console.log('Version in manifest.json is already up to date.');
  }
} catch (error) {
  console.error('Error syncing version:', error.message);
  process.exit(1);
}
