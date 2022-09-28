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
      if (
        rows[cur_cnt].children[timeblock[0].getDate() - 1].children.length == 0
      ) {
        console.log(timeblock[0].getDate(), timeblock);
        rows[cur_cnt].children[timeblock[0].getDate() - 1].appendChild(p_start);
        rows[cur_cnt].children[timeblock[0].getDate() - 1].appendChild(p_end);
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
    for (let i = 0; i < 7; i++) {
      let td = tds[i];
      if (td.classList.contains("d-none")) {
        td.className = "";
      } else {
        td.className = "d-none";
      }
    }
  });
}

function init() {
  create_timeblocks();
  display_edit_timeblock();
  create_add_buttons();
  create_submit_for_description();
}

init();
