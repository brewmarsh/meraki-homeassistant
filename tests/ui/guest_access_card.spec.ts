import { test, expect } from '@playwright/test';

/**
 * Guest Access Card UI Validation
 * This test verifies that the Meraki Guest Access card is correctly rendered in the Home Assistant UI.
 */

test.beforeEach(async ({ page }) => {
  const token = process.env.HA_TOKEN;
  const baseUrl = process.env.BASE_URL || 'http://localhost:8123';

  if (token) {
    // Inject the HA token into local storage to bypass the login page.
    // Home Assistant uses 'hassTokens' key in localStorage for session management.
    await page.addInitScript(
      (data) => {
        const tokens = {
          access_token: data.token,
          token_type: 'Bearer',
          expires_in: 315360000, // 10 years
          refresh_token: 'none',
          hass_url: data.baseUrl,
        };
        window.localStorage.setItem('hassTokens', JSON.stringify(tokens));
        // Also set a flag to skip the onboarding if it appears.
        window.localStorage.setItem('skip_onboarding', 'true');
      },
      { token, baseUrl }
    );
  }
});

test('Guest Access Card UI Validation', async ({ page }) => {
  // Navigate to the dashboard.
  await page.goto('/');

  // Action 2: Implement Login Flow if redirected to the login page
  if (page.url().includes('/auth/authorize')) {
    console.log('Redirected to login page. Attempting authentication...');

    // Fill username
    const username = process.env.HA_USERNAME || 'admin';
    await page.fill('input[name="username"]', username);

    // Some HA versions have a "Next" button, others show password immediately
    const nextButton = page.locator('button:has-text("Next")');
    if (await nextButton.isVisible()) {
      await nextButton.click();
    }

    // Fill password
    const password = process.env.HA_PASSWORD || 'password';
    await page.fill('input[name="password"]', password);

    // Click login button
    await page.click('button:has-text("Log in")');

    // Wait for navigation back to the app
    await page.waitForURL((url) => !url.href.includes('/auth/authorize'), {
      timeout: 30000,
    });
  }

  // Wait for the Home Assistant main interface to load.
  // We look for the main app-drawer-layout or similar top-level element.
  await page.waitForSelector('home-assistant', { timeout: 30000 });

  // Locate the Meraki Guest Access custom card.
  // Playwright's locators pierce Shadow DOM automatically.
  const card = page.locator('meraki-guest-access-card');

  // Assert that the card is visible on the dashboard.
  await expect(card).toBeVisible({ timeout: 30000 });

  // Pierce the Shadow DOM to find the "Generate Access Key" button.
  // We use regex to be case-insensitive and flexible with the exact text.
  const generateButton = card.getByRole('button', {
    name: /Generate Access Key/i,
  });

  // Assert that the "Generate Access Key" button is visible and enabled.
  await expect(generateButton).toBeVisible();
  await expect(generateButton).toBeEnabled();

  // Additional check: Verify the "Network Default" policy is displayed if it's the default.
  const policyLabel = card.locator('text="Network Default"');
  if ((await policyLabel.count()) > 0) {
    await expect(policyLabel).toBeVisible();
  }
});
