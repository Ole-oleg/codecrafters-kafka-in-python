import socket  # noqa: F401


def echo_correlation_id(request):
    corr_id = int.from_bytes(request[8:12], "big")

    return get_response(corr_id)


def get_response(corr_id):
    resonse_body = corr_id.to_bytes(4, "big")
    response_len = len(resonse_body).to_bytes(4, "big")

    return response_len + resonse_body


def main():
    # You can use print statements as follows for debugging,
    # they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    conn, _ = server.accept()  # wait for client

    while True:
        data = conn.recv(64)
        if not data:
            break
        response = echo_correlation_id(data)
        conn.send(response)


if __name__ == "__main__":
    main()
