/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/*.html",
        "./templates/**/*.html",
        "./templates/**/**/*.html"
    ],
    theme: {
        extend: {}
    },
    plugins: [
        require("@tailwindcss/forms"),
        require("@tailwindcss/aspect-ratio"),
        require("@tailwindcss/typography"),
        require("@tailwindcss/container-queries"),
        require("daisyui"),
    ],
    daisyui: {
        themes: [
            "winter",
            "night",
            "synthwave",
            {
                codeRed: {
                    "primary": "#C3060A",
                    "secondary": "#002357",
                    "accent": "#011533",
                    "neutral": "#011533",
                    "base-100": "#330101",
                    "base-200": "#400102",
                    "base-300": "#0d013b",
                    "info": "#002357",
                    "success": "#002357",
                    "warning": "#EC0300",
                    "error": "#EC0300",
                },
                tlm: {
                    "primary": "#3a2d10",           // dark brown — matches page text, used for navbar bg
                    "primary-content": "#ffffff",   // white text on dark brown navbar
                    "secondary": "#1f3a5f",
                    "secondary-content": "#ffffff",
                    "accent": "#ff4d2e",
                    "accent-content": "#ffffff",
                    "neutral": "#111111",
                    "neutral-content": "#ffffff",

                    "base-100": "#e6c46b",
                    "base-200": "#d4b35a",
                    "base-300": "#c4a24a",
                    "base-content": "#2a1f08",      // dark text on page background

                    "info": "#1f3a5f",
                    "success": "#1f3a5f",
                    "warning": "#ff4d2e",
                    "error": "#ff4d2e",
                }
            }
        ],
    },
    darkMode: ['class', '[data-theme="night"]', '[data-theme="codeRed"]', '[data-theme="lazarus"]'],
}