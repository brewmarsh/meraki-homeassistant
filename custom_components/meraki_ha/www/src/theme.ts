import { createTheme, ThemeOptions } from '@mui/material/styles';

const getHATheme = (darkMode: boolean): ThemeOptions => {
    const haTheme = {
        '--primary-color': darkMode ? '#4fd1c5' : '#3277a8',
        '--primary-background-color': darkMode ? '#1a202c' : '#f5f5f5',
        '--card-background-color': darkMode ? '#2d3748' : '#ffffff',
        '--primary-text-color': darkMode ? '#edf2f7' : '#212121',
        '--secondary-text-color': darkMode ? '#a0aec0' : '#727272',
        '--divider-color': darkMode ? 'rgba(255, 255, 255, 0.12)' : 'rgba(0, 0, 0, 0.12)',
    };

    return {
        palette: {
            mode: darkMode ? 'dark' : 'light',
            primary: {
                main: haTheme['--primary-color'],
            },
            background: {
                default: haTheme['--primary-background-color'],
                paper: haTheme['--card-background-color'],
            },
            text: {
                primary: haTheme['--primary-text-color'],
                secondary: haTheme['--secondary-text-color'],
            },
            divider: haTheme['--divider-color'],
        },
        typography: {
            fontFamily: 'Roboto, sans-serif',
            h4: {
                fontWeight: 700,
                color: haTheme['--primary-text-color'],
            },
            h5: {
                fontWeight: 600,
                color: haTheme['--primary-text-color'],
            },
            h6: {
                fontWeight: 600,
                color: haTheme['--secondary-text-color'],
            },
            body1: {
                color: haTheme['--primary-text-color'],
            },
            body2: {
                color: haTheme['--secondary-text-color'],
            },
        },
        components: {
            MuiCard: {
                styleOverrides: {
                    root: {
                        borderRadius: 8,
                        boxShadow: 'none',
                        border: `1px solid ${haTheme['--divider-color']}`,
                    },
                },
            },
            MuiDivider: {
                styleOverrides: {
                    root: {
                        borderColor: haTheme['--divider-color'],
                    }
                }
            }
        }
    };
};

export const createDynamicTheme = (darkMode: boolean) => {
    return createTheme(getHATheme(darkMode));
};