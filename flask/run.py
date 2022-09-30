from website import create_app

app, socket = create_app()

if __name__ == "__main__":
    socket.run(app, host="localhost", port=5004, debug=True)
