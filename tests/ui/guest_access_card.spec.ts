import { test, expect } from '@playwright/test';

test.describe('Meraki Guest Access Card UI Validation', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the dashboard. Adjust the path if necessary for your local setup.
    await page.goto('/');

    // In a real scenario, you might need to handle Home Assistant authentication here.
    // Assuming for this test suite that the user is already logged in or the dashboard is accessible.
  });

  test('should render the guest access card and its components', async ({ page }) => {
    // Locate the custom card.
    // Note: Playwright locators pierce the Shadow DOM by default.
    const card = page.locator('meraki-guest-access-card');
    await expect(card).toBeVisible();

    // Verify the "Group Policy" dropdown contains the "Network Default" fallback option.
    // The dropdown is likely within an ha-form, which contains an ha-select or similar.
    // We look for the text "Network Default" which should be visible when the dropdown is interacted with or as a label.
    // Based on the code: policyOptions.push({ value: 'NONE', label: 'Network Default' });
    const policyDropdown = card.locator('ha-form').locator('text=Group Policy');
    await expect(policyDropdown).toBeVisible();

    // Check for the "Network Default" label.
    // It might be inside a list or a select option.
    const networkDefaultOption = card.locator('text="Network Default"');
    await expect(networkDefaultOption).toBeVisible();

    // Verify the "Generate Access Key" button is present and visible.
    const generateButton = card.locator('ha-button:has-text("Generate Access Key")');
    await expect(generateButton).toBeVisible();
    await expect(generateButton).toBeEnabled();
  });
});
