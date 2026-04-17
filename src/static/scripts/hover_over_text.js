import { getCookie } from "./cookie.js";

document.addEventListener("DOMContentLoaded", () => {
  const createdBtn = document.createElement("button");

  createdBtn.innerHTML = "<i class='fas fa-microphone'></i>";
  createdBtn.className = "btn btn-lg btn-rounded btn-primary shadow-sm";
  createdBtn.style.display = "none";
  createdBtn.style.padding = "2px 8px";

  const voiceBtns = document.querySelectorAll(".hover-target");
  const csrfToken = getCookie("csrftoken");

  voiceBtns.forEach((voiceBtn) => {
    voiceBtn.style.display = "flex";
    voiceBtn.style.alignItems = "center";
    voiceBtn.style.width = "fit-content";

    voiceBtn.addEventListener("click", () => {
      const text = voiceBtn.textContent;
      fetch("home/voice/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
          text: text,
        }),
      })
        .then((response) => response.blob())
        .then((blob) => {
          new Audio(URL.createObjectURL(blob)).play();
        });
    });

    voiceBtn.addEventListener("mouseenter", () => {
      voiceBtn.appendChild(createdBtn);
      createdBtn.style.display = "inline-block";
    });
    voiceBtn.addEventListener("mouseleave", () => {
      createdBtn.style.display = "none";
    });
  });
});
