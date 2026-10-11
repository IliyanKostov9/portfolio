document.addEventListener("DOMContentLoaded", () => {
  const progressbar = document.querySelector("#progressBar");

  window.addEventListener("scroll", (event) => {
    const position = Math.round(
      (window.scrollY /
        (document.documentElement.scrollHeight - window.innerHeight)) *
        100,
    );

    progressbar.style.width = `${position}%`;
    progressbar.setAttribute("aria-valuenow", position);
  });
});
