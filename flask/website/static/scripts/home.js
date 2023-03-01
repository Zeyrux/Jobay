class JobCreator {
  constructor() {
    this.super_div = document.getElementsByClassName("job_super_div")[0];
    this.job_img_url = this.super_div.getAttribute("job_img");
    this.job_url = this.super_div.getAttribute("job_url");
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
    let self = this;
    let div = document.createElement("div");
    div.classList.add("job_div");
    div.addEventListener("click", function () {
      console.log(self.job_url + "?id=" + job.id);
      // TODO: REWORK (remove localhost:5004)
      let url = new URL("http://localhost:5004" + self.job_url);
      url.searchParams.append("id", job.id);
      window.location.href = url;
    });
    let heading = document.createElement("h1");
    heading.innerHTML = job.name;
    heading.classList.add("h2");
    let table = document.createElement("table");
    let row = document.createElement("tr");
    let td_tags = document.createElement("td");
    td_tags.classList.add(["td_tags", "td"]);
    let td_img = document.createElement("td");
    td_img.classList.add("td");
    job.tags.forEach((tag) => {
      let p = document.createElement("p");
      p.innerHTML = tag;
      td_tags.appendChild(p);
    });
    let img = document.createElement("img");
    img.src = this.job_img_url;
    img.classList.add("input_icon");
    td_img.appendChild(img);
    row.appendChild(td_img);
    row.appendChild(td_tags);
    table.appendChild(row);
    [
      ["Dauer", duration_to_str(job.duration)],
      ["Bezahlung", payment_to_str(job.payment)],
      ["Zeit", unix_to_str(job.time_start)],
    ].forEach((data) => {
      let row = document.createElement("tr");
      row.classList.add("job_row");
      let td_title = document.createElement("td");
      td_title.innerHTML = data[0];
      td_title.classList.add("td");
      let td_data = document.createElement("td");
      td_data.innerHTML = data[1];
      td_data.classList.add("td");
      row.appendChild(td_title);
      row.appendChild(td_data);
      table.appendChild(row);
    });
    div.appendChild(heading);
    div.appendChild(table);
    this.super_div.appendChild(div);
  }
}

function init() {
  let manager = new Manager();
  manager.add_resizable_bg_img();

  let job_creator = new JobCreator();
  setInterval(manager.init, 20);
}

init();
