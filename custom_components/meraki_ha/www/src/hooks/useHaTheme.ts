/**
 * Hook to integrate with Home Assistant theming.
 *
 * This reads theme information from HA's CSS variables and applies them
 * to the panel. HA sets variables like --primary-color, --card-background-color,
 * etc. on the document root.
 */

import { useEffect, useMemo, useRef } from 'react';
import type { HomeAssistant } from '../types/hass';

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
 * Detect if we're in dark mode by checking background color luminance.
 */
function detectDarkMode(): boolean {
  const bgColor = getCssVariable('--primary-background-color');
  if (!bgColor) return true; // Default to dark

  // Parse the color and check luminance
  // Light backgrounds have high luminance, dark have low
  if (bgColor.startsWith('#')) {
    const hex = bgColor.slice(1);
    const r = parseInt(hex.slice(0, 2), 16);
    const g = parseInt(hex.slice(2, 4), 16);
    const b = parseInt(hex.slice(4, 6), 16);
    // Relative luminance formula
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
    return luminance < 0.5;
  }

  // Check for common light theme indicators
  if (
    bgColor.includes('fafafa') ||
    bgColor.includes('ffffff') ||
    bgColor.includes('f5f5f5')
  ) {
    return false;
  }

  return true; // Default to dark
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
}

/**
 * Hook to get HA theme information and CSS variables.
 */
export function useHaTheme(hass: HomeAssistant | null): UseHaThemeResult {
  // Detect dark mode from HA's themes object or by inspecting CSS
  const isDarkMode = useMemo(() => {
    // First try HA's theme setting
    if (hass?.themes?.darkMode !== undefined) {
      return hass.themes.darkMode;
    }
    // Fall back to detecting from CSS
    return detectDarkMode();
  }, [hass?.themes?.darkMode]);

  const panelRef = useRef<HTMLElement | null>(null);

  // Get theme variables from HA
  const themeVars = useMemo(() => {
    return getHaThemeVariables();
    // Re-read when hass changes (theme might have changed)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hass?.themes]);

  // Compute tertiary background based on primary/secondary
  const tertiaryBg = useMemo(() => {
    if (isDarkMode) {
      return '#334155'; // Slate 700
    }
    // For light mode, use a slightly darker shade than secondary
    const secondary = themeVars['--secondary-background-color'];
    if (secondary === '#ffffff' || secondary?.includes('fff')) {
      return '#f1f5f9'; // Slate 100
    }
    return '#e2e8f0'; // Slate 200
  }, [isDarkMode, themeVars]);

  // Convert theme vars to React CSSProperties style object
  const style = useMemo(() => {
    const cssProps: Record<string, string> = {};

    // Map HA variables to our custom variables
    cssProps['--text-primary'] = themeVars['--primary-text-color'];
    cssProps['--text-secondary'] = themeVars['--secondary-text-color'];
    cssProps['--text-muted'] = themeVars['--disabled-text-color'];
    cssProps['--bg-primary'] = themeVars['--primary-background-color'];
    cssProps['--bg-secondary'] = themeVars['--secondary-background-color'];
    cssProps['--bg-tertiary'] = tertiaryBg;
    cssProps['--card-bg'] = themeVars['--card-background-color'];
    cssProps['--card-border'] = themeVars['--divider-color'];
    cssProps['--primary'] = themeVars['--primary-color'];
    cssProps['--primary-light'] = isDarkMode
      ? 'rgba(3, 169, 244, 0.15)'
      : 'rgba(3, 169, 244, 0.1)';
    cssProps['--success'] = themeVars['--success-color'];
    cssProps['--success-light'] = isDarkMode
      ? 'rgba(67, 160, 71, 0.2)'
      : 'rgba(67, 160, 71, 0.15)';
    cssProps['--warning'] = themeVars['--warning-color'];
    cssProps['--warning-light'] = isDarkMode
      ? 'rgba(255, 166, 0, 0.2)'
      : 'rgba(255, 166, 0, 0.15)';
    cssProps['--error'] = themeVars['--error-color'];
    cssProps['--error-light'] = isDarkMode
      ? 'rgba(219, 68, 55, 0.2)'
      : 'rgba(219, 68, 55, 0.15)';

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

  return { isDarkMode, themeVars, style };
}

export default useHaTheme;
