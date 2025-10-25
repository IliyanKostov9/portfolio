function getCookie(name) {
  const cookies = document.cookie.split("; ");
  for (const c of cookies) {
    const [key, val] = c.split("=");
    if (key == name) return val;
  }
  return null;
}

function setCookie(name, value, days) {
  const date = new Date();
  date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = `${name}=${value};expires=${date.toUTCString()};path=/`;
}
