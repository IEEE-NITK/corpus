/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				ieeeblue: '#00629B'
			},
			fontFamily: {
				roboto: ["Roboto"]
			}
		}
	},
	plugins: [
		require('@tailwindcss/typography'),
		require('@tailwindcss/forms'),
		require('@tailwindcss/aspect-ratio'),
		require('@tailwindcss/container-queries'),
		require('daisyui')
	],
	daisyui: {
		themes: ['winter', 'night'],
		darkTheme: 'night'
	}
};
