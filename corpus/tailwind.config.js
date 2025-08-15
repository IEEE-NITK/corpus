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
                    "base-100": "#330101",  // background
                    "base-200": "#400102",  // cards
                    "base-300": "#0d013b",  // borders
                    "info": "#002357",
                    "success": "#002357",
                    "warning": "#EC0300",
                    "error": "#EC0300",
                }
            }
        ],
    },
    darkMode: ['class', '[data-theme="night"]', '[data-theme="codeRed"]'],
}
