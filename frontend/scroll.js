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
    // height: "auto",
  });
// gsap.to(".tt", {
//   fontSize: "45px",
//   scale: 0.8,
//   duration: 1,
//   transformOrigin: "center center",
// });
