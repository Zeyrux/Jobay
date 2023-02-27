class Job {
  constructor(job) {
    this.id = job["id"];
    this.name = job["name"];
    this.duration = job["duration"];
    this.payment = job["payment"];
    this.time_start = job["time_start"];
    this.tags = job["tags"];
  }
}
