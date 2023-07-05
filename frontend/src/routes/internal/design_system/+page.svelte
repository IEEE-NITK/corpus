<script>
	import '../../../app.postcss';
</script>

<div class="container prose mx-auto">
	<h1>Design System</h1>
	<p>
		Corpus uses Svelte as the frontend, and Django REST Framework as its backend. On this page,
		there are specifications about the frontend aspect, especially about the UI/UX of Corpus.
	</p>
	<p>For details about development, please refer to the Frontend and Backend development guides.</p>

	<h2>Overview</h2>
	<p>
		Corpus is a <a href="https://kit.svelte.dev/">SvelteKit</a> application. The UI is made using
		<a href="https://daisyui.com/">DaisyUI</a>, which is a library based on
		<a href="https://tailwindcss.com/">Tailwind CSS</a>. For maximum use cases, prioritise the
		DaisyUI classes, before moving towards Tailwind CSS classes. Only in the rarest of cases should
		you have to write custom CSS.
	</p>

	<h2>Colors</h2>
	<p>
		Corpus uses the <code>winter</code> theme for light mode, and <code>night</code> theme for dark
		mode. These are configured in <code>tailwind.config.cjs</code>. Any edits to the same can be
		made there.
	</p>
	<p>
		Along with this, the official color of IEEE is provided as <code>ieeeblue</code>. It has been
		added to Tailwind, so you can use it as a utility in any class that uses colors for components.
	</p>
	<h2>Typography</h2>
</div>
