document.addEventListener("DOMContentLoaded", () => {
  const scrollElements = document.querySelectorAll(".hide-when-scrolling");

  window.addEventListener("scroll", () => {
    const triggerPoint = window.innerHeight / 6;

    scrollElements.forEach((scroll) => {
      if (window.scrollY > triggerPoint) {
        scroll.classList.add("hide-element");
      } else {
        scroll.classList.remove("hide-element");
      }
    });
  });
});
