import socket
from socket import AF_INET6, SOCK_STREAM
from threading import Thread

# Nhut Cao 906939
# ELEC-C7420 Basic principles in networking

# localIPv6 = "fe80::4aa:40ad:ff4c:43b9"
localIPv6 = "fe80::724c:a5ff:fe00:800"  # aalto open
globalIPv6 = "2001:708:150:10::8b55"  # Aalto open

# Disable firewall for clients ?

PORTIPV6 = 36000
FORMAT = 'utf-8'
BUFFER = 1024
WAIT = 5


def receive(socket_v6):
    while True:
        message = socket_v6.recv(BUFFER).decode(FORMAT)
        if message.startswith("/downloaded"):
            file_data = message.split("\n")[1]
            file_name = message.split("\n")[2]
            new_file = open(file_name, "a")
            new_file.write(file_data)
            new_file.close()
        else:
            print(message)


def send(socket_v6):
    message = input(">>> ")
    while message != "/Q":
        socket_v6.send(bytes(message, FORMAT))
        message = input(">>> ")
    print("You log out the server. See ya later!")
    socket_v6.send(bytes(message, FORMAT))


def main():
    socket_v6 = socket.socket(AF_INET6, SOCK_STREAM)
    addr_v6 = (globalIPv6, PORTIPV6)
    socket_v6.connect(addr_v6)
        
    receive_thread = Thread(target=receive, args=(socket_v6,))
    send_thread = Thread(target=send, args=(socket_v6,))
    receive_thread.start()
    send_thread.start()


if __name__ == "__main__":
    main()