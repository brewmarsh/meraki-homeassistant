import React from 'react';

interface ThemeSelectorProps {
  theme: string;
  setTheme: (theme: string) => void;
}

const ThemeSelector: React.FC<ThemeSelectorProps> = ({ theme, setTheme }) => {
  return (
    <div className="relative">
      <select
        value={theme}
        onChange={(e) => setTheme(e.target.value)}
        className="p-2 border rounded-lg bg-light-card dark:bg-dark-card dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-cisco-blue"
        aria-label="Theme selector"
      >
        <option value="system">System</option>
        <option value="light">Light</option>
        <option value="dark">Dark</option>
      </select>
    </div>
  );
};

export default ThemeSelector;
