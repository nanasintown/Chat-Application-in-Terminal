import socket
from threading import Thread

# Nhut Cao 906939
# ELEC-C7420 Basic principles in networking

# localIPv4 = "192.168.10.2"
localIPv4 = '10.100.11.182'  # aalto network
globalIPv4 = '10.100.0.1'  # aalto network


# Disable firewall for clients ?

PORTIPV4 = 34000
FORMAT = 'utf-8'
BUFFER = 4096
BACKLOG = 5


def receive(socket_v4):
    while True:
        message = socket_v4.recv(BUFFER).decode(FORMAT)
        if message.startswith("/downloaded"):
            file_data = message.split("\n")[1]
            file_name = message.split("\n")[2]
            new_file = open(file_name, "a")
            new_file.write(file_data)
            new_file.close()
        else:
            print(message)


def send(socket_v4):
    message = input(">>> ")
    while message != "/Q":
        socket_v4.send(bytes(message, FORMAT))
        message = input(">>> ")
    print("You log out from the server. See ya later!")
    socket_v4.send(bytes(message, FORMAT))


def main():
    socket_v4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr_v4 = (localIPv4, PORTIPV4)
    socket_v4.connect(addr_v4)

    receive_thread = Thread(target=receive, args=(socket_v4,))
    send_thread = Thread(target=send, args=(socket_v4,))
    receive_thread.start()
    send_thread.start()


if __name__ == "__main__":
    main()