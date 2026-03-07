import { test, expect } from '@playwright/test';

test('Dashboard cards render without errors', async ({ page }) => {
  // Debug log to confirm which variables are reaching the process
  console.log('Environment HA_ keys:', Object.keys(process.env).filter(k => k.startsWith('HA_')));

  const username = process.env.HA_USERNAME;
  const password = process.env.HA_PASSWORD;

  if (!username) {
    throw new Error('HA_USERNAME environment variable must be set');
  }
  if (!password) {
    throw new Error('HA_PASSWORD environment variable must be set');
  }

  // Go to Home Assistant login page
  await page.goto('/');

  // Check if we are already logged in or if we need to log in
  if (page.url().includes('/auth/login')) {
    // Fill out the login form
    await page.fill('input[name="username"]', username);
    await page.fill('input[name="password"]', password);
    await page.click('button[type="submit"]');
  }

  // Navigate to the dashboard
  await page.goto('/lovelace/0');

  // Wait for the dashboard to settle
  await page.waitForLoadState('networkidle');

  // Assert no error cards are present
  // Home Assistant uses <hui-error-card> for cards that fail to load
  const errorCards = page.locator('hui-error-card');
  await expect(errorCards).toHaveCount(0, { message: 'Found an error card on the dashboard!' });

  // Also check for the text "Entity not found" which is common when entities are missing
  await expect(page.getByText('Entity not found')).toHaveCount(0, { message: 'Found "Entity not found" text on the dashboard!' });

  // Optional: check for "Custom element doesn't exist" which happens if the card isn't registered
  await expect(page.getByText("Custom element doesn't exist")).toHaveCount(0, { message: 'A custom card element was not found/registered!' });
});
