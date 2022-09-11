from application.application import socket, application


if __name__ == "__main__":
    socket.run(application, host="localhost", port=5004, debug=True)