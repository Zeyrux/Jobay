class JobCreator {
  constructor() {
    this.super_div = document.getElementsByClassName("job_super_div")[0];
    let self = this;
    socket.on("answer_request_jobs", function (jobs) {
      JSON.parse(jobs).forEach((job) => {
        self.add_job(new Job(job));
      });
    });

    this.request_jobs();
  }

  request_jobs() {
    socket.emit("request_jobs");
  }

  add_job(job) {
    let div = document.createElement("div");
    div.classList.add("job_div");
    let heading = document.createElement("h1");
    heading.innerHTML = job.name;
    heading.classList.add("h2");
    let job_image = document.createElement("img");
    let table = document.createElement("table");
    let row = document.createElement("tr");
    let td = document.createElement("td");
    let img = document.createElement("img")
    [
      ["Dauer", duration_to_str(job.duration)],
      ["Bezahlung", payment_to_str(job.payment)],
      ["Zeit", unix_to_str(job.time_start)],
    ].forEach((data) => {
      let row = document.createElement("tr");
      row.classList.add("job_row");
      let td_title = document.createElement("td");
      td_title.innerHTML = data[0];
      let td_data = document.createElement("td");
      td_data.innerHTML = data[1];
      row.appendChild(td_title);
      row.appendChild(td_data);
      table.appendChild(row);
    });
    div.appendChild(heading);
    div.appendChild(job_image);
    div.appendChild(table);
    this.super_div.appendChild(div);
  }
}

function init() {
  let manager = new Manager();
  manager.add_resizable_bg_img();

  let job_creator = new JobCreator();
}

init();
