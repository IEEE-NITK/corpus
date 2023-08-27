$(document).ready(() => {
    new TypeIt("#typewriter", {
        loop: true,
        deleteSpeed: 100
    })
        .type("Solving Problems", { delay: 1000 })
        .delete()
        .type("NITK", { delay: 1500 })
        .delete()
        .type("Humanity", { delay: 1500 })
        .delete()
        .go();
});
