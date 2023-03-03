import socket
import sys
import threading
import logging
import signal

HOST = "127.0.0.1"
PORT = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients: set[socket.socket] = set()

logging.basicConfig(
    filename="chat.log", filemode="a", format="%(asctime)s - %(message)s", level=logging.INFO
)


def send_messages(msg: str, client_sock: socket.socket) -> None:
    for client in clients:
        if client != client_sock:
            client.sendall(msg.encode())


def new_client(client_sock: socket.socket, addr: tuple) -> None:
    with client_sock:
        while True:
            try:
                data = client_sock.recv(1024).decode()
                if data == "boom":
                    raise Exception("Connection stopped by user")
                msg = data.replace("/", ":// ")
                send_messages(msg, client_sock)
                logging.info(f"{addr}:{msg}") if msg else None
            except Exception as e:
                logging.exception(e)
                clients.remove(client_sock)
                print(f"[*]{addr} is disconnected")
                break


def receive() -> None:
    while True:
        client_socket, address = server_socket.accept()
        print(f"[*]Accepted connection from {address}")
        clients.add(client_socket)
        t = threading.Thread(target=new_client, args=(client_socket, address))
        t.daemon = True
        t.start()


def close_connections(signum, frame) -> None:
    for client in clients:
        client.send("Server error".encode())
    sys.exit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, close_connections)
    receive()
