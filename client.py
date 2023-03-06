import socket
import threading
import logging

HOST = "127.0.0.1"
PORT = 12345

logging.basicConfig(
    filename="chat.log", filemode="a", format="%(asctime)s - %(message)s", level=logging.INFO
)

username = input("Enter your username: ")


def accept_messages() -> None:
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            print(msg)
            if msg == "Server error":
                raise Exception(msg)

        except Exception as e:
            logging.exception(e)
            client_socket.close()
            break


def send_messages() -> None:
    while True:
        try:
            data = input()

            if data == "boom":
                client_socket.send(data.encode())
                print("Bye bye ...")
                raise Exception

            message = f"{username}/{data}"

            client_socket.send(message.encode())
        except Exception as e:
            client_socket.close()
            logging.exception(e)
            break


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

accept_thread = threading.Thread(target=accept_messages)
accept_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
