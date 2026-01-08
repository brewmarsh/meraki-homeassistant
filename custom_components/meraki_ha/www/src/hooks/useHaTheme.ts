/**
 * Hook to integrate with Home Assistant theming.
 *
 * This reads theme information from HA's CSS variables and applies them
 * to the panel. HA sets variables like --primary-color, --card-background-color,
 * etc. on the document root.
 */

import { useEffect, useMemo, useRef, useState } from 'react';
import type { HomeAssistant } from '../types/hass';

type ThemeMode = 'auto' | 'dark' | 'light';
const THEME_STORAGE_KEY = 'meraki_ha_theme_mode';

/**
 * Read a CSS variable from the document, resolving any var() references.
 */
function getCssVariable(name: string): string | null {
  try {
    const value = getComputedStyle(document.documentElement)
      .getPropertyValue(name)
      .trim();
    if (value) return value;
  } catch {
    // Ignore errors
  }
  return null;
}

/**
 * Calculate luminance of a color to determine if it's dark or light.
 * Returns a value between 0 (black) and 1 (white).
 */
function getColorLuminance(color: string): number {
  if (!color) return 0.5;

  // Handle hex colors
  if (color.startsWith('#')) {
    const hex = color.slice(1);
    let r: number, g: number, b: number;
    if (hex.length === 3) {
      r = parseInt(hex[0] + hex[0], 16);
      g = parseInt(hex[1] + hex[1], 16);
      b = parseInt(hex[2] + hex[2], 16);
    } else {
      r = parseInt(hex.slice(0, 2), 16);
      g = parseInt(hex.slice(2, 4), 16);
      b = parseInt(hex.slice(4, 6), 16);
    }
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  }

  // Handle rgb/rgba colors
  const rgbMatch = color.match(/rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/);
  if (rgbMatch) {
    const [, r, g, b] = rgbMatch.map(Number);
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  }

  // Handle common color names
  if (
    color.includes('fff') ||
    color.includes('fafafa') ||
    color.includes('f5f5f5')
  ) {
    return 0.95;
  }
  if (
    color.includes('000') ||
    color.includes('1c1c') ||
    color.includes('111')
  ) {
    return 0.05;
  }

  return 0.5;
}

/**
 * Detect if we're in dark mode using multiple signals for reliability.
 */
function detectDarkMode(textColor: string, bgColor: string): boolean {
  // Primary signal: Check if text color is light (luminance > 0.5 = light text = dark mode)
  const textLuminance = getColorLuminance(textColor);
  if (textLuminance > 0.6) {
    return true; // Light text = dark mode
  }
  if (textLuminance < 0.4) {
    return false; // Dark text = light mode
  }

  // Fallback: Check background color (luminance < 0.5 = dark background = dark mode)
  const bgLuminance = getColorLuminance(bgColor);
  return bgLuminance < 0.5;
}

/**
 * Get all theme variables from HA's CSS.
 */
function getHaThemeVariables(): Record<string, string> {
  return {
    // Read HA's variables directly
    '--primary-color': getCssVariable('--primary-color') || '#03a9f4',
    '--accent-color': getCssVariable('--accent-color') || '#ff9800',
    '--primary-text-color':
      getCssVariable('--primary-text-color') || '#212121',
    '--secondary-text-color':
      getCssVariable('--secondary-text-color') || '#727272',
    '--disabled-text-color':
      getCssVariable('--disabled-text-color') || '#bdbdbd',
    '--primary-background-color':
      getCssVariable('--primary-background-color') || '#fafafa',
    '--secondary-background-color':
      getCssVariable('--secondary-background-color') || '#e5e5e5',
    '--card-background-color':
      getCssVariable('--card-background-color') || '#ffffff',
    '--divider-color':
      getCssVariable('--divider-color') || 'rgba(0, 0, 0, 0.12)',
    '--success-color': getCssVariable('--success-color') || '#43a047',
    '--warning-color': getCssVariable('--warning-color') || '#ffa600',
    '--error-color': getCssVariable('--error-color') || '#db4437',
  };
}

export interface UseHaThemeResult {
  isDarkMode: boolean;
  themeVars: Record<string, string>;
  style: React.CSSProperties;
  themeMode: ThemeMode;
}

/**
 * Get the user's theme preference from localStorage.
 */
function getStoredThemeMode(): ThemeMode {
  try {
    const stored = localStorage.getItem(THEME_STORAGE_KEY) as ThemeMode;
    if (stored && ['auto', 'dark', 'light'].includes(stored)) {
      return stored;
    }
  } catch {
    // localStorage might not be available
  }
  return 'auto';
}

/**
 * Hook to get HA theme information and CSS variables.
 */
export function useHaTheme(hass: HomeAssistant | null): UseHaThemeResult {
  const panelRef = useRef<HTMLElement | null>(null);
  const [themeMode, setThemeMode] = useState<ThemeMode>(getStoredThemeMode);

  // Listen for theme mode changes from Settings
  useEffect(() => {
    const handleThemeChange = (event: CustomEvent<ThemeMode>) => {
      setThemeMode(event.detail);
    };

    window.addEventListener(
      'meraki-theme-change',
      handleThemeChange as EventListener
    );
    return () => {
      window.removeEventListener(
        'meraki-theme-change',
        handleThemeChange as EventListener
      );
    };
  }, []);

  // Get theme variables from HA
  const themeVars = useMemo(() => {
    return getHaThemeVariables();
    // Re-read when hass changes (theme might have changed)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hass?.themes]);

  // Detect dark mode based on user preference or auto-detection
  const isDarkMode = useMemo(() => {
    // If user has explicitly chosen a mode, use that
    if (themeMode === 'dark') return true;
    if (themeMode === 'light') return false;

    // Auto mode: detect from actual color values (most reliable)
    // Note: hass.themes.darkMode can be incorrect for custom themes,
    // so we always verify against actual colors
    const textColor = themeVars['--primary-text-color'];
    const bgColor = themeVars['--primary-background-color'];

    return detectDarkMode(textColor, bgColor);
  }, [themeVars, themeMode]);

  // Compute tertiary background (HA doesn't provide this, so we derive it)
  const tertiaryBg = useMemo(() => {
    // Use a color between secondary-background and card-background
    // For iOS theme: dark = #2c2c2e, light = #f2f2f7
    return isDarkMode ? '#2c2c2e' : '#f2f2f7';
  }, [isDarkMode]);

  // Convert theme vars to React CSSProperties style object
  // Uses native HA theme values directly without overrides
  const style = useMemo(() => {
    const cssProps: Record<string, string> = {};

    // Map HA variables directly to our custom variables (no overrides)
    cssProps['--text-primary'] = themeVars['--primary-text-color'];
    cssProps['--text-secondary'] = themeVars['--secondary-text-color'];
    cssProps['--text-muted'] = themeVars['--disabled-text-color'];
    cssProps['--bg-primary'] = themeVars['--primary-background-color'];
    cssProps['--bg-secondary'] = themeVars['--secondary-background-color'];
    cssProps['--bg-tertiary'] = tertiaryBg; // HA doesn't have this, so we derive it
    cssProps['--card-bg'] = themeVars['--card-background-color'];
    cssProps['--card-border'] = themeVars['--divider-color'];
    cssProps['--primary'] = themeVars['--primary-color'];
    cssProps['--primary-light'] = isDarkMode
      ? 'rgba(10, 132, 255, 0.15)' // iOS blue alpha
      : 'rgba(0, 122, 255, 0.1)';
    cssProps['--success'] = themeVars['--success-color'];
    cssProps['--success-light'] = isDarkMode
      ? 'rgba(48, 209, 88, 0.2)' // iOS green alpha
      : 'rgba(52, 199, 89, 0.15)';
    cssProps['--warning'] = themeVars['--warning-color'];
    cssProps['--warning-light'] = isDarkMode
      ? 'rgba(255, 159, 10, 0.2)' // iOS orange alpha
      : 'rgba(255, 149, 0, 0.15)';
    cssProps['--error'] = themeVars['--error-color'];
    cssProps['--error-light'] = isDarkMode
      ? 'rgba(255, 69, 58, 0.2)' // iOS red alpha
      : 'rgba(255, 59, 48, 0.15)';

    return cssProps as React.CSSProperties;
  }, [themeVars, tertiaryBg, isDarkMode]);

  // Update document root with theme mode and our custom vars
  useEffect(() => {
    const root = document.documentElement;

    // Set theme mode attribute for CSS selectors
    root.setAttribute('data-theme', isDarkMode ? 'dark' : 'light');

    // Set our custom variables on the root
    for (const [key, value] of Object.entries(style)) {
      root.style.setProperty(key, value as string);
    }

    // Also set on the panel element for scoped styles
    const panel = document.querySelector('.meraki-panel');
    if (panel && panel instanceof HTMLElement) {
      panelRef.current = panel;
      for (const [key, value] of Object.entries(style)) {
        panel.style.setProperty(key, value as string);
      }
    }
  }, [style, isDarkMode]);

  return { isDarkMode, themeVars, style, themeMode };
}

export default useHaTheme;
