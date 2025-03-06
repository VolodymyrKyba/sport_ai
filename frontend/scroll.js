gsap.registerPlugin(ScrollTrigger);

const container = document.querySelector(".next-section");
const answer = document.querySelector(".answer");
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
// .to(answer, {
//   height: "auto",
// });
