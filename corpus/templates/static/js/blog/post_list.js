const cards = document.querySelectorAll('.card');
// console.log(cards) 

const header = document.querySelector('.blogHeader');

gsap.registerPlugin(ScrollTrigger);

gsap.from([cards[0], cards[1], cards[2], header], {
    opacity: 0,
    y:30,
    duration: 1.5,
    ease: 'power1.out',

});

const animateCards = Array.from(cards).slice(3); 

gsap.from(animateCards, {
    scrollTrigger: {
       
        trigger: "animateCards",
        toggle: "restart none none pause",
    },
    opacity: 0,
    y: 50,
    duration: 1,
    stagger: 0.2,
    ease: 'power2.out',
    
});

