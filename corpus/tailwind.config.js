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
                }
            },
            {
                tlm: {
                    "primary":          "#7A4F08",
                    "primary-content":  "#F2E8CE",
                    "secondary":        "#5C3A05",
                    "secondary-content":"#F2E8CE",
                    "accent":           "#C8922A",
                    "accent-content":   "#1C0F02",
                    "neutral":          "#1C0F02",
                    "neutral-content":  "#F2E8CE",
                    "base-100":         "#F2E8CE",
                    "base-200":         "#E6D8A8",
                    "base-300":         "#CCBA80",
                    "base-content":     "#1C0F02",
                    "info":             "#5A7A8A",
                    "success":          "#4A7A3A",
                    "warning":          "#C8922A",
                    "error":            "#8B2500",
                }
            }
        ],
    },
    // TLM is a light theme — do NOT include it in the darkMode array.
    // Including it would cause Tailwind to apply dark: variant styles
    // on the TLM page, which is wrong for a light-themed page.
    darkMode: ['class', '[data-theme="night"]', '[data-theme="codeRed"]'],
}
