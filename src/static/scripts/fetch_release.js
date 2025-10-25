try {
  const response = await fetch(
    "https://api.github.com/repos/IliyanKostov9/portfolio/releases/latest",
  );
  const data = await response.json();
  const version = data.tag_name;
  document.getElementById("github-version").textContent = version;
} catch (error) {
  console.error(`Cannot fetch latest release! ${error}`);
}
