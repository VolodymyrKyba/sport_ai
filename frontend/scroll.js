gsap.registerPlugin(ScrollTrigger);

const container = document.querySelector(".next-section");

gsap
  .timeline({
    scrollTrigger: {
      trigger: container,
      start: "top 100%",
      end: "bottom 50%",
      toggleActions: "restart none none reverse",
      scrub: true,
      markers: true,
    },
  })
  .to(container, {
    scale: 2.0,
  });
