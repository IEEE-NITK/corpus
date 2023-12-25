/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/*.html",
        "./templates/**/*.html",
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require("@tailwindcss/typography"),
        require("@tailwindcss/container-queries"),
        require("@tailwindcss/forms"),
        require("@tailwindcss/aspect-ratio"),
        require("daisyui"),
    ],
    daisyui: {
        themes: ["winter", "night", "synthwave"]
    },
    darkMode: ['class', '[data-theme="night"]']
}
