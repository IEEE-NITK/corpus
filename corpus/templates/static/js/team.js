document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".team-btn");
    const sections = document.querySelectorAll(".team-content");

    function activate(id) {
        // Hide all sections
        sections.forEach(s => s.classList.remove("active-content"));

        // Reset all buttons
        buttons.forEach(b => {
            b.classList.remove("active-btn");
            b.setAttribute("aria-selected", "false");
        });

        // Activate selected section
        const section = document.getElementById(id);
        if (!section) return;
        section.classList.add("active-content");

        // Activate corresponding button
        const btn = document.getElementById(id + "-btn");
        if (!btn) return;
        btn.classList.add("active-btn");
        btn.setAttribute("aria-selected", "true");
    }

    // Button click handlers
    buttons.forEach(btn =>
        btn.addEventListener("click", () =>
            activate(btn.dataset.target)
        )
    );

    // Default section
    activate("IEEE");
});

var slider = tns({
    container: '#slider-div',
    items: 3,
    nav: true,
    controls: false,
    speed: 300,
    autoplay: true,
    autoplayText: [" ", " "],
    autoplayHoverPause: false,
    autoplayTimeout: 4000,
    swipeAngle: false,
    mouseDrag: true,
});
