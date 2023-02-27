function get_height(element) {
  let computedStyle = getComputedStyle(element);
  return (
    element.clientHeight -
    (parseFloat(computedStyle.paddingTop) +
      parseFloat(computedStyle.paddingBottom))
  );
}

function double_digits(number) {
  if (number < 10) {
    number = "0" + number;
  }
  return number;
}

function unix_to_str(unix) {
  let date = new Date(unix * 1000);
  console.log(date);
  return (
    double_digits(date.getDate()) +
    "." +
    double_digits(date.getMonth() + 1) +
    "." +
    date.getFullYear() +
    " - " +
    double_digits(date.getHours()) +
    ":" +
    double_digits(date.getMinutes())
  );
}

function payment_to_str(payment) {
  return Math.ceil(payment / 100) + ",00€";
}

function duration_to_str(duration) {
  return Math.ceil(duration / 60) + ":" + double_digits(duration % 60);
}

class Manager {
  constructor() {
    window.addEventListener("load", this.init);
    window.addEventListener("resize", this.init);
  }

  init() {
    // input line
    for (let line of document.getElementsByClassName("input_line")) {
      line.height = get_height(line.parentNode);
      line.style.display = "inline";
    }
    // input icon
    for (let icon of this.document.getElementsByClassName("input_icon")) {
      icon.height = get_height(icon.parentNode);
      icon.style.display = "inline";
    }
  }

  get_margin_top_bottom(element) {
    return (
      parseFloat(
        window.getComputedStyle(element, null).getPropertyValue("padding-top")
      ) *
        -1 -
      parseFloat(
        window
          .getComputedStyle(element, null)
          .getPropertyValue("padding-bottom")
      )
    );
  }

  add_resizable_bg_img() {
    window.addEventListener("resize", this.resizable_bg_img);
    window.addEventListener("load", this.resizable_bg_img);
  }

  resizable_bg_img() {
    let imgs = document.getElementsByClassName("background_img");
    for (let img of imgs) {
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
  }
}
