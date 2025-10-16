<!-- FIX: Carousel, tab not working without this component -->
document.addEventListener("DOMContentLoaded", function () {
  const carousels = document.querySelectorAll(".carousel");
  const tabLinks = document.querySelectorAll("[data-mdb-tab-init]");
  const collapse = document.querySelectorAll("[data-mdb-collapse-init]");
  const tooltips = document.querySelectorAll("[data-mdb-tooltip-init]");
  const inputs = document.querySelectorAll("[data-mdb-input-init]");
  const scrollspys = document.querySelectorAll("[data-mdb-scrollspy-init]");

  document
    .getElementById("contactForm")
    .addEventListener("submit", function () {
      const btn = document.getElementById("submitBtn");
      const spinner = document.getElementById("spinnerSubmit");

      btn.disabled = true;
      spinner.style.display = "inline-block";
    });

  collapse.forEach((collapse) => {
    new mdb.Collapse(collapse);
  });

  tabLinks.forEach((tabLink) => {
    new mdb.Tab(tabLink);
  });

  carousels.forEach((carousel) => {
    new mdb.Carousel(carousel);
  });

  tooltips.forEach((tooltip) => {
    new mdb.Tooltip(tooltip);
  });

  inputs.forEach((formOutline) => {
    const input = formOutline.querySelector("input");
    const mdbInput = new mdb.Input(formOutline);
    mdbInput.update(input);
  });

 scrollspys.forEach((scrollspy) => {
    new mdb.ScrollSpy(scrollspy, {
      target: "#scroll-table-contents",
       offset: 140
    });
  });

});
