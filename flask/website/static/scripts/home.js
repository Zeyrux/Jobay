function init() {
  let img = document.getElementById("background_image");
  let ratio_img = img.offsetWidth / img.offsetHeight;
  let ratio_window = window.innerWidth / window.innerHeight;
  if (ratio_img > ratio_window) {
    img.height = window.innerHeight;
  } else {
    img.width = window.innerWidth;
  }
}

// init();
