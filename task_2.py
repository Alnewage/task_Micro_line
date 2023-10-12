import socket
import threading


def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response = data.upper()
        client_socket.send(response)
    client_socket.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("0.0.0.0", 8080))

server.listen(5)
print("Сервер слушает на порту 8080...")

while True:
    client_socket, addr = server.accept()
    print(f"Принято соединение с {addr[0]}:{addr[1]}")

    client_handler = threading.Thread(target=handle_client,
                                      args=(client_socket,))
    client_handler.start()
