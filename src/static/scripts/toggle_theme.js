const cookies = document.cookie.split("; ");
const themeCookie = cookies.find((c) => c.startsWith("theme="));
if (themeCookie && themeCookie.split("=")[1] == "dark") {
  document.documentElement.classList.add("dark-mode");
}
