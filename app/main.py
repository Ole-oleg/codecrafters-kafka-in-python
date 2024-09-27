import socket  # noqa: F401
from dataclasses import dataclass


THROTTLE_TIME_MS = 0


@dataclass
class Request:
    request_len: int
    request_api_key: int
    request_api_version: int
    correlation_id: int
    client_id: str | None


@dataclass
class Response:
    correlation_id: int
    error_code: int
    api_key: int


def parse_request(request) -> Request | None:
    request_len = int.from_bytes(request[0:4], "big")
    if request_len > 7:
        return Request(
            request_len=request_len,
            request_api_key=int.from_bytes(request[4:6], "big"),
            request_api_version=int.from_bytes(request[6:8], "big"),
            correlation_id=int.from_bytes(request[8:12], "big"),
            client_id=request[12:].decode("utf-8") if len(request) >= 12 else None,
        )


def respond(request_bytes) -> Response | None:
    request = parse_request(request_bytes)
    print(request)
    acceptable_apis = list(range(5))
    if request:
        if request.request_api_version not in acceptable_apis:
            return Response(
                correlation_id=request.correlation_id,
                api_key=request.request_api_key,
                error_code=35,
            )

        return Response(
            correlation_id=request.correlation_id,
            api_key=request.request_api_key,
            error_code=0,
        )


def convert_response_to_bytes(response):
    min_version = max_verion = 4
    tag_buffer = int(0).to_bytes(1)

    response_body = response.correlation_id.to_bytes(4, "big")
    response_body += response.error_code.to_bytes(2, "big")

    response_body += int(2).to_bytes(1)
    response_body += response.api_key.to_bytes(2, "big")
    response_body += int(min_version).to_bytes(2, "big")
    response_body += int(max_verion).to_bytes(2, "big")

    response_body += tag_buffer
    response_body += THROTTLE_TIME_MS.to_bytes(4, "big")
    response_body += tag_buffer

    return len(response_body).to_bytes(4, "big") + response_body


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
        response = respond(data)
        response_bytes = convert_response_to_bytes(response)
        conn.send(response_bytes)


if __name__ == "__main__":
    main()
