document.addEventListener("DOMContentLoaded", () => {
  const lazyElements = document.querySelectorAll(".lazy");

  const observer = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const el = entry.target;
          if (el.tagName === "IMG" && el.dataset.src) {
            el.src = el.dataset.src;
          }

          el.classList.add("loaded");
          observer.unobserve(el);
        }
      });
    },
    {
      threshold: 0.1,
    },
  );

  lazyElements.forEach((el) => {
    observer.observe(el);
  });
});
