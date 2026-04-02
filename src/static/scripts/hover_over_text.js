document.addEventListener("DOMContentLoaded", () => {
  const voiceBtn = document.createElement("button");

  voiceBtn.innerHTML = "<i class='fas fa-microphone'></i>";
  voiceBtn.className = "btn btn-lg btn-rounded btn-primary shadow-sm";
  voiceBtn.style.display = "none";
  voiceBtn.style.padding = "2px 8px";

  const targets = document.querySelectorAll(".hover-target");

  targets.forEach((target) => {
    target.style.display = "flex";
    target.style.alignItems = "center";
    target.style.width = "fit-content";

    target.addEventListener("mouseenter", () => {
      target.appendChild(voiceBtn);
      voiceBtn.style.display = "inline-block";
    });
    target.addEventListener("mouseleave", () => {
      voiceBtn.style.display = "none";
    });
  });
});
