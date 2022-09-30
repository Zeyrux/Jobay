function show_tags() {
  let div_tags = document.getElementById("div_tags");
  let tags = JSON.parse(document.getElementById("script").getAttribute("tags"));
  tags.forEach((tag) => {
    let hidden = document.createElement("input");
    hidden.type = "hidden";
    hidden.value = tag.name;
    let button = document.createElement("input");
    button.type = "button";
    button.value = tag.name;
    button.classList.add("btn-secondary");
    button.classList.add("form-control");
    button.addEventListener("click", function () {
      if (button.classList.contains("btn-secondary")) {
        button.classList.remove("btn-secondary");
        button.classList.add("btn-primary");
        hidden.name = "tag_" + tag.name;
      } else {
        button.classList.remove("btn-primary");
        button.classList.add("btn-secondary");
        hidden.name = "";
      }
    });
    div_tags.appendChild(button);
    div_tags.appendChild(hidden);
  });
}

function init() {
  show_tags();
}

init();
