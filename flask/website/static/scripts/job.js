function init() {
  let td_duration = document.getElementsByClassName("duration")[0];
  let td_payment = document.getElementsByClassName("payment")[0];
  let td_time_start = document.getElementsByClassName("time_start")[0];
  td_duration.innerHTML = duration_to_str(parseInt(td_duration.innerHTML));
  td_payment.innerHTML = payment_to_str(parseInt(td_payment.innerHTML));
  td_time_start.innerHTML = unix_to_str(parseInt(td_time_start.innerHTML));

  let manager = new Manager();
  manager.add_resizable_bg_img();
}

init();
