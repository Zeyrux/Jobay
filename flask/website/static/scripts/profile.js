function create_submit(value) {
  let submit = document.createElement("input");
  submit.type = "submit";
  submit.value = value;
  submit.classList.add("btn", "btn-primary");
  return submit;
}

function create_timeblocks() {
  let tbody = document.getElementById("timeblock_body");
  let timeblocks = JSON.parse(
    document.getElementById("timeblock_creater").getAttribute("timeblocks")
  );
  timeblocks.forEach((timeblock) => {
    start = new Date(timeblock.start);
    end = new Date(timeblock.end);
    console.log(end);
  });
}

function display_edit_timeblock() {
  let tfoot = document.getElementById("timeblock_foot");
  let timeblock_edit = document.getElementById("timeblock_edit");
  timeblock_edit.addEventListener("click", function () {
    for (let td of tfoot.children[0].children) {
      if (td.className == "d-none") {
        td.className = "";
      } else {
        td.className = "d-none";
      }
    }
  });
}

function create_add_buttons() {
  let inputs = document.getElementsByClassName("form-control-plaintext");
  for (let input of inputs) {
    input.addEventListener(
      "input",
      function add_submit() {
        input.parentElement.appendChild(create_submit("Speichern"));
      },
      { once: true }
    );
  }
}

function create_submit_for_description() {
  let description_textarea = document.getElementById("description");
  description_textarea.addEventListener(
    "input",
    function () {
      let hidden = document.createElement("input");
      hidden.type = "hidden";
      hidden.name = "description";
      let submit = create_submit("Speichern");
      description_textarea.parentElement.appendChild(hidden);
      description_textarea.parentElement.appendChild(submit);
    },
    { once: true }
  );
}

function init() {
  create_timeblocks();
  display_edit_timeblock();
  create_add_buttons();
  create_submit_for_description();
}

init();
