#!/bin/bash
set -e

# This script is a workaround for a Vite build issue where the index.html
# references the final build output (/meraki-panel.js) instead of the
# source entry point (/src/main.tsx). This causes a circular dependency
# for the Vite build process.
#
# To resolve this, we temporarily modify index.html to point to the source
# entry point before running the build, and then restore the original file
# after the build is complete.

# 1. Backup the original index.html
mv index.html index.html.bak

# 2. Create a temporary index.html pointing to the source entry point
sed 's|/meraki-panel.js|/src/main.tsx|' index.html.bak > index.html

# 3. Clean old build artifacts
rm -rf meraki-panel.js meraki-guest-access-card.js assets dist

# 4. Build the Meraki Panel
BUILD_TARGET=panel npx vite build

# 5. Build the Meraki Guest Access Card
BUILD_TARGET=card npx vite build

# 6. Copy build artifacts to root
cp dist/meraki-panel.js .
cp dist/meraki-guest-access-card.js .

# 5. Restore the original index.html
mv index.html.bak index.html

echo "Frontend build completed successfully."
