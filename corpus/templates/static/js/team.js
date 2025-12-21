document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".team-btn");
    const sections = document.querySelectorAll(".team-content");

    function activate(id) {
        sections.forEach(s => s.classList.remove("active-content"));
        buttons.forEach(b => {
            b.classList.remove("active-btn");
            b.setAttribute("aria-selected", "false");
        });

        document.getElementById(id).classList.add("active-content");
        const btn = document.getElementById(id + "-btn");
        btn.classList.add("active-btn");
        btn.setAttribute("aria-selected", "true");
    }

    buttons.forEach(btn =>
        btn.addEventListener("click", () => activate(btn.dataset.target))
    );

    activate("IEEE");
});
