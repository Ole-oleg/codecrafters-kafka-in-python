import socket  # noqa: F401

CORR_ID = 7


def get_response():
    resonse_body = CORR_ID.to_bytes(4, "big")
    response_len = len(resonse_body).to_bytes(4, "big")

    return response_len + resonse_body


def main():
    # You can use print statements as follows for debugging,
    # they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    conn, addr = server.accept()  # wait for client

    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.send(get_response())


if __name__ == "__main__":
    main()
