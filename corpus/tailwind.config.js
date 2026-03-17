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
                },

            },
            {
                tlm: {
                    "primary": "#C8922A",
                    "primary-content": "#1A1208",
                    "secondary": "#7A5214",
                    "secondary-content": "#F0DCA0",
                    "accent": "#E8C170",
                    "accent-content": "#1A1208",
                    "neutral": "#1A1208",
                    "neutral-content": "#F0DCA0",
                    "base-100": "#1A1208",
                    "base-200": "#241A0C",
                    "base-300": "#2E2210",
                    "base-content": "#F0DCA0",
                    "info": "#6B8CAE",
                    "success": "#5A7A3A",
                    "warning": "#C8922A",
                    "error": "#8B2500",
                }
            }
        ],
    },
    darkMode: ['class', '[data-theme="night"]', '[data-theme="codeRed"]', '[data-theme="tlm"]'],
}
