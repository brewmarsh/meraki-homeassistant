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

# 3. Clean old build artifacts and run the Vite build
rm -rf meraki-panel.js assets
vite build

# 4. Restore the original index.html
mv index.html.bak index.html

echo "Frontend build completed successfully."
