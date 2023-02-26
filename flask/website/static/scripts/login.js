function handle_resize() {
  let img = document.getElementById("background_image");
  let ratio_img = img.offsetWidth / img.offsetHeight;
  let ratio_window = window.innerWidth / window.innerHeight;
  if (ratio_img > ratio_window) {
    img.height = window.innerHeight;
    img.style.width = "auto";
    img.style.removeProperty("height");
  } else {
    img.width = window.innerWidth;
    img.style.height = "auto";
    img.style.removeProperty("width");
  }
}

function init() {
  window.addEventListener("resize", handle_resize);
  window.addEventListener("load", handle_resize);
}

init();
