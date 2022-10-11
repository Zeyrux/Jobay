function create_submit(value) {
  let submit = document.createElement("input");
  submit.type = "submit";
  submit.value = value;
  submit.classList.add("btn", "btn-primary");
  return submit;
}

delete_timeblock = function (parent, day) {
  let form = document.createElement("form");
  form.classList.add("d-none");
  form.method = "POST";
  let submit = create_submit("Löschen");
  form.appendChild(submit);
  form.addEventListener("submit", function () {
    let hidden_hours = document.createElement("input");
    hidden_hours.type = "hidden";
    hidden_hours.name = "delete_timeblock";
    hidden_hours.value =
      parent.children[0].innerHTML + ";" + parent.children[1].innerHTML;
    let hidden_day = document.createElement("input");
    hidden_day.type = "hidden";
    hidden_day.name = "timeblock_delete_day";
    hidden_day.value = day;
    form.appendChild(hidden_hours);
    form.appendChild(hidden_day);
  });
  return form;
};

function create_timeblocks() {
  let tbody = document.getElementById("timeblock_body");
  let timeblocks = JSON.parse(
    document.getElementById("script").getAttribute("timeblocks")
  );
  timeblocks.sort(function (a, b) {
    return a.start - b.end;
  });
  // get max count of rows
  let last_date = new Date();
  let cnt_max_rows = 0;
  let cur_cnt_rows = 0;
  for (let i = 0; i < timeblocks.length; i++) {
    const timeblock = timeblocks[i];
    let start = new Date(timeblock.start * 1000);
    let end = new Date(timeblock.end * 1000);
    timeblocks[i] = [start, end];
    if (last_date.getDay() != start.getDay()) {
      cur_cnt_rows = 1;
    } else {
      cur_cnt_rows++;
    }
    if (cur_cnt_rows > cnt_max_rows) {
      cnt_max_rows = cur_cnt_rows;
    }
    last_date = start;
  }
  // create rows
  let rows = [];
  for (i = 0; i < cnt_max_rows; i++) {
    let tr = document.createElement("tr");
    for (j = 0; j < 7; j++) {
      tr.appendChild(document.createElement("td"));
    }
    tbody.appendChild(tr);
    rows[i] = tr;
  }
  // create timeblocks
  for (let i = 0; i < timeblocks.length; i++) {
    let timeblock = timeblocks[i];
    let p_start = document.createElement("p");
    p_start.innerHTML =
      ("00" + timeblock[0].getHours()).slice(-2) +
      ":" +
      ("00" + timeblock[0].getMinutes()).slice(-2);
    let p_end = document.createElement("p");
    p_end.innerHTML =
      ("00" + timeblock[1].getHours()).slice(-2) +
      ":" +
      ("00" + timeblock[1].getMinutes()).slice(-2);
    let cur_cnt = 0;
    while (true) {
      let td = rows[cur_cnt].children[timeblock[0].getDate() - 1];
      if (td.children.length == 0) {
        td.appendChild(p_start);
        td.appendChild(p_end);
        td.appendChild(delete_timeblock(td, timeblock[0].getDate()));
        break;
      }
      cur_cnt++;
    }
  }
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

function display_edit_timeblock() {
  let tds = document.getElementById("timeblock_foot").children[0].children;
  let button_edit = document.getElementById("timeblock_edit");
  button_edit.addEventListener("click", function () {
    // show add timeblock
    for (let i = 0; i < 7; i++) {
      let td = tds[i];
      if (td.classList.contains("d-none")) {
        td.classList.remove("d-none");
      } else {
        td.classList.add("d-none");
      }
    }
    // show delete timeblock
    let tbody = document.getElementById("timeblock_body");
    for (let tr of tbody.children) {
      for (let td of tr.children) {
        for (let child of td.children) {
          if (child.tagName == "FORM") {
            if (child.classList.contains("d-none")) {
              child.classList.remove("d-none");
            } else {
              child.classList.add("d-none");
            }
          }
        }
      }
    }
  });
}

function create_tag_options() {
  // create options
  let all_tags = JSON.parse(
    document.getElementById("script").getAttribute("all_tags")
  );
  all_tags.forEach((tag) => {
    let button = document.createElement("button");
    button.innerHTML = tag;
    button.classList.add("dropdown-item");
    button.addEventListener("click", function () {
      let hidden = document.createElement("input");
      hidden.type = "hidden";
      hidden.value = button.innerHTML;
      hidden.name = "add_tag";
      document.getElementById("tag_form").appendChild(hidden);
      document.getElementById("tag_form").submit();
    });
    document.getElementById("tag_dropdown").appendChild(button);
  });
}

function init() {
  create_timeblocks();
  display_edit_timeblock();
  create_add_buttons();
  create_submit_for_description();
  create_tag_options();
}

init();
