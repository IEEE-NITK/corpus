/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/*.html",
        "./templates/**/*.html",
        "./templates/**/**/*.html"
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require("@tailwindcss/aspect-ratio"),
        require("@tailwindcss/typography"),
        require("@tailwindcss/container-queries"),
        require("daisyui"),
    ],
    daisyui: {
        themes: ["winter", "night", "synthwave"],
    },
    darkMode: ['class', '[data-theme="night"]'],
}
