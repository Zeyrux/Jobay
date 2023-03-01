class Messager {
  constructor() {
    this.div = document.getElementsByClassName("chat_div")[0];
    this.submit = document.getElementsByClassName("submit")[0];
    this.input = document.getElementsByClassName("input")[0];
    this.init();
  }

  init() {
    let self = this;
    let msgs_send = JSON.parse(self.div.getAttribute("msgs_send"));
    let msgs_received = JSON.parse(self.div.getAttribute("msgs_received"));
    let msg_send = msgs_send[0];
    let msg_received = msgs_received[0];
    let pointer_send = 0;
    let pointer_received = 0;
    let finished_send = false;
    if (msgs_send.length == 0) {
      finished_send = true;
    }
    let finished_received = false;
    if (msgs_received.length == 0) {
      finished_received = true;
    }
    console.log(msgs_send);
    console.log(msgs_received);
    console.log(finished_send);
    console.log(finished_received);
    while (!(finished_send && finished_received)) {
      let added = false;
      console.log("Send");
      console.log(msg_send);
      console.log(msg_received);
      if (!finished_send) {
        // same start
        if (msg_received == undefined) {
          self.create_msg(msg_send["content"], true);
          if (pointer_send == msgs_send.length - 1) {
            finished_send = true;
          } else {
            pointer_send += 1;
            msg_send = msgs_send[pointer_send];
          }
          added = true;
        } // same start
        else if (msg_send["time"] <= msg_received["time"]) {
          self.create_msg(msg_send["content"], true);
          if (pointer_send == msgs_send.length - 1) {
            finished_send = true;
          } else {
            pointer_send += 1;
            msg_send = msgs_send[pointer_send];
          }
          added = true;
        }
      }
      if (!added) {
        self.create_msg(msg_received["content"], false);
        if (pointer_received == msgs_received.length - 1) {
          finished_received = true;
        } else {
          pointer_received += 1;
          msg_received = msgs_received[pointer_received];
        }
      }
    }
    self.div.scrollTop = self.div.scrollHeight;
    self.submit.addEventListener("click", function () {
      if (self.input.value.length != 0) {
        self.create_msg(self.input.value, true);
        socket.emit(
          "msg_send",
          self.input.value,
          self.div.getAttribute("chat_partner")
        );
        self.input.value = "";
      }
    });
    socket.on("receive_msg", function (msg) {
      console.log(msg);
      self.create_msg(msg["content"], false);
    });
  }

  create_msg(msg, send) {
    let p = document.createElement("p");
    p.innerHTML = msg;
    p.classList.add("msg");
    if (send) {
    } else {
      p.classList.add("received");
    }
    this.div.appendChild(p);
  }
}

function init() {
  let manager = new Manager();
  manager.add_resizable_bg_img();

  let messager = new Messager();
}

init();
