function add_tags_logic() {
  let children = document.getElementsByClassName("tags_div")[0].children;
  for (let i = 0; i < children.length; i++) {
    let button = children[i];
    let hidden = children[i + 1];
    button.addEventListener("click", function () {
      if (button.classList.contains("tag_pressed")) {
        button.classList.remove("tag_pressed");
        hidden.name = "";
      } else {
        button.classList.add("tag_pressed");
        hidden.name = "tag_" + button.value;
      }
    });
  }
}

function init() {
  add_tags_logic();

  let manager = new Manager();
  manager.add_resizable_bg_img();
}

init();
