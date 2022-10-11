function create_tags() {
  let user_tags = JSON.parse(
    document.getElementById("script_create_tags").getAttribute("user_tags")
  );
  let td = document.getElementById("tag_item");
  // show user tags
  user_tags.forEach((tag) => {
    let div = document.createElement("div");
    div.classList.add(
      "d-flex",
      "border-primary",
      "border",
      "rounded-circle",
      "pl-2",
      "pr-0",
      "mr-1",
      "ml-1"
    );
    div.style.backgroundColor = "#b5c8ff";
    let p = document.createElement("p");
    p.innerHTML = tag.name;
    p.classList.add(
      "row",
      "justify-content-center",
      "align-self-center",
      "text-center",
      "m-0"
    );
    div.appendChild(p);
    let form = document.createElement("form");
    form.method = "post";
    let hidden = document.createElement("input");
    hidden.type = "hidden";
    hidden.value = tag.name;
    hidden.name = "remove_tag";
    let submit = document.createElement("input");
    submit.type = "submit";
    submit.classList.add(
      "btn-outline-danger",
      "form-control",
      "btn-sm",
      "m-0",
      "ml-1",
      "rounded-circle"
    );
    submit.value = "⌫";
    form.appendChild(hidden);
    form.appendChild(submit);
    div.appendChild(form);
    td.prepend(div);
  });
}

create_tags();
