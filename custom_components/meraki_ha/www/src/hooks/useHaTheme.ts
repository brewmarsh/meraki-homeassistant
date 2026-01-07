/**
 * Hook to integrate with Home Assistant theming.
 * 
 * This reads theme information from the hass object and computes
 * CSS variables to apply to the panel. It also attempts to read
 * CSS variables from the parent document where HA sets them.
 */

import { useEffect, useMemo } from 'react';
import type { HomeAssistant } from '../types/hass';

// Default dark theme colors
const DARK_THEME = {
  '--primary-color': '#03a9f4',
  '--accent-color': '#ff9800',
  '--primary-text-color': '#f1f5f9',
  '--secondary-text-color': '#94a3b8',
  '--disabled-text-color': '#64748b',
  '--primary-background-color': '#0f172a',
  '--secondary-background-color': '#1e293b',
  '--card-background-color': '#1e293b',
  '--divider-color': '#334155',
  '--success-color': '#10b981',
  '--warning-color': '#f59e0b',
  '--error-color': '#ef4444',
};

// Default light theme colors
const LIGHT_THEME = {
  '--primary-color': '#03a9f4',
  '--accent-color': '#ff9800',
  '--primary-text-color': '#1f2937',
  '--secondary-text-color': '#6b7280',
  '--disabled-text-color': '#9ca3af',
  '--primary-background-color': '#f8fafc',
  '--secondary-background-color': '#ffffff',
  '--card-background-color': '#ffffff',
  '--divider-color': '#e2e8f0',
  '--success-color': '#10b981',
  '--warning-color': '#f59e0b',
  '--error-color': '#ef4444',
};

/**
 * Try to read a CSS variable from the document root or parent frames.
 */
function getCssVariable(name: string): string | null {
  // Try document root
  const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  if (value) return value;
  
  // Try parent document (in case we're in an iframe)
  try {
    if (window.parent && window.parent !== window) {
      const parentValue = getComputedStyle(window.parent.document.documentElement).getPropertyValue(name).trim();
      if (parentValue) return parentValue;
    }
  } catch {
    // Cross-origin access denied - ignore
  }
  
  return null;
}

/**
 * Get theme variables from HA's CSS or use defaults.
 */
function getThemeVariables(isDarkMode: boolean): Record<string, string> {
  const defaults = isDarkMode ? DARK_THEME : LIGHT_THEME;
  const result: Record<string, string> = {};
  
  for (const [key, fallback] of Object.entries(defaults)) {
    result[key] = getCssVariable(key) || fallback;
  }
  
  return result;
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
  const isDarkMode = hass?.themes?.darkMode ?? true; // Default to dark mode
  
  const themeVars = useMemo(() => {
    return getThemeVariables(isDarkMode);
  }, [isDarkMode]);
  
  // Convert theme vars to React CSSProperties style object
  const style = useMemo(() => {
    const cssProps: Record<string, string> = {};
    for (const [key, value] of Object.entries(themeVars)) {
      cssProps[key] = value;
    }
    // Also set our custom vars that map to HA vars
    cssProps['--text-primary'] = themeVars['--primary-text-color'];
    cssProps['--text-secondary'] = themeVars['--secondary-text-color'];
    cssProps['--text-muted'] = themeVars['--disabled-text-color'];
    cssProps['--bg-primary'] = themeVars['--primary-background-color'];
    cssProps['--bg-secondary'] = themeVars['--secondary-background-color'];
    cssProps['--card-bg'] = themeVars['--card-background-color'];
    cssProps['--card-border'] = themeVars['--divider-color'];
    cssProps['--primary'] = themeVars['--primary-color'];
    cssProps['--success'] = themeVars['--success-color'];
    cssProps['--warning'] = themeVars['--warning-color'];
    cssProps['--error'] = themeVars['--error-color'];
    return cssProps as React.CSSProperties;
  }, [themeVars]);
  
  // Also update document root with theme vars for global CSS
  useEffect(() => {
    const root = document.documentElement;
    for (const [key, value] of Object.entries(themeVars)) {
      root.style.setProperty(key, value);
    }
    // Set our custom vars
    root.style.setProperty('--text-primary', themeVars['--primary-text-color']);
    root.style.setProperty('--text-secondary', themeVars['--secondary-text-color']);
    root.style.setProperty('--text-muted', themeVars['--disabled-text-color']);
    root.style.setProperty('--bg-primary', themeVars['--primary-background-color']);
    root.style.setProperty('--bg-secondary', themeVars['--secondary-background-color']);
    root.style.setProperty('--card-bg', themeVars['--card-background-color']);
    root.style.setProperty('--card-border', themeVars['--divider-color']);
    root.style.setProperty('--primary', themeVars['--primary-color']);
    root.style.setProperty('--success', themeVars['--success-color']);
    root.style.setProperty('--warning', themeVars['--warning-color']);
    root.style.setProperty('--error', themeVars['--error-color']);
  }, [themeVars]);
  
  return { isDarkMode, themeVars, style };
}

export default useHaTheme;

