gsap.registerPlugin(ScrollTrigger);

const container = document.querySelector(".next-section");

gsap
  .timeline({
    scrollTrigger: {
      trigger: container,
      start: "top 80%",
      end: "top 30%",
      toggleActions: "restart none none reverse",
      scrub: 2,
      markers: true,
    },
  })
  .to(container, {
    width: "100%",
    scale: 1.9,
    backgroundColor: "white",
    duration: 2.0,
    height: "400vh",
  });
// .from(container, {
//   opacity: 0, // Fade in content as it appears.
//   duration: 1,
//   ease: "power1.out",
// });
