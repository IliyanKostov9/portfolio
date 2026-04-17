import { getCookie } from "./cookie.js";

document.addEventListener("DOMContentLoaded", () => {
  const createdVoiceBtn = document.createElement("button");

  createdVoiceBtn.innerHTML = "<i class='fas fa-microphone'></i>";
  createdVoiceBtn.className = "btn btn-lg btn-rounded btn-primary shadow-sm";
  createdVoiceBtn.style.display = "none";
  createdVoiceBtn.style.padding = "2px 8px";

  const voiceBtns = document.querySelectorAll(".hover-target");
  const csrfToken = getCookie("csrftoken");

  voiceBtns.forEach((voiceBtn) => {
    voiceBtn.addEventListener("click", () => {
      const text = voiceBtn.textContent;
      fetch("/home/voice/", {
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
      voiceBtn.appendChild(createdVoiceBtn);
      createdVoiceBtn.style.display = "inline-block";
    });
    voiceBtn.addEventListener("mouseleave", () => {
      createdVoiceBtn.style.display = "none";
    });
  });
});
