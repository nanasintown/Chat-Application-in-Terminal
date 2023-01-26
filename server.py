import socket
from threading import Thread
from functions import private_message, send_file, accept_file, broadcast, public_message, instructions,\
    create_group, see_users, see_members, add_users, join_group,\
    user_status, go_offline, send_group_message

# Nhut Cao 906939
# ELEC-C7420 Basic principles in networking

# ---------- Define parameters ----------

BUFFER = 4096
FORMAT = 'utf-8'
BACKLOG = 5

# localIPv4 = "192.168.10.2"
# globalIPv4 = "82.130.45.97"
# localIPv6 = "fe80::4aa:40ad:ff4c:43b9"

# as my local IPv6 from my home router is not usable, I used the address from Aalto network, which works fine
localIPv4 = '10.100.11.182'  # aalto
globalIPv4 = '10.100.0.1'  # aalto
localIPv6 = "fe80::724c:a5ff:fe00:800"  # aalto open
globalIPv6 = "2001:708:150:10::8b55"  # Aalto open
portIPv4 = 34000
portIPv6 = 36000
address_v4 = (localIPv4, portIPv4)
address_IPv6 = (globalIPv6, portIPv6)
server_v4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_v6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
server_v4.bind(address_v4)
server_v6.bind(address_IPv6)
server_v4.listen(BACKLOG)
server_v6.listen(BACKLOG)

# ---------- DEFINE DATABASE ----------

registered_users = {}  # registered clients sockets
registered_addr = {}  # client addresses
online_users = {}  # online client sockets
last_online = {}  # last online time
group_owner = {}  # group owner/creator
group_members = {}  # group members
buffer_msg = {}  # buffered messages list
file_database = {}  # file data


def clients_v4():
    while True:
        client_IPv4, client_address_v4 = server_v4.accept()
        print("[NEW CONNECTION] %s:%s connected." % client_address_v4)
        client_IPv4.send(bytes("Welcome to the chat!\n", FORMAT))
        client_IPv4.send(bytes("Enter your name to register/login", FORMAT))
        name = client_IPv4.recv(BUFFER).decode(FORMAT)
        registered_addr[name] = client_address_v4
        registered_users[name] = client_IPv4
        online_users[name] = client_IPv4
        client_IPv4.send(bytes("\nSend '?how' for instruction of the chat application\n", FORMAT))
        message = f"{name} has joined the chat"
        broadcast(message, online_users)

        if name not in buffer_msg:
            buffer_msg[name] = []
        elif len(buffer_msg[name]) != 0:
            client_IPv4.send(bytes("\nUnseen messages\n", FORMAT))
            for unseen_message in buffer_msg[name]:
                client_IPv4.send(bytes(f"{unseen_message}\n", FORMAT))
        Thread(target=handle_client, args=(name, client_IPv4)).start()


def clients_v6():
    while True:
        clientIPv6, client_addressIPv6 = server_v6.accept()
        print("[NEW CONNECTION] %s:%s:%s:%s connected." % client_addressIPv6)
        clientIPv6.send(bytes("Welcome to the chat!\n", FORMAT))
        clientIPv6.send(bytes("Enter your name to register/login", FORMAT))
        name = clientIPv6.recv(BUFFER).decode(FORMAT)
        registered_addr[name] = client_addressIPv6
        registered_users[name] = clientIPv6  # socket
        online_users[name] = clientIPv6  # socket
        clientIPv6.send(bytes("\nSend '?how' for instruction of the chat application\n", FORMAT))
        message = f"{name} has joined the chat"
        broadcast(message, online_users)

        if name not in buffer_msg:
            buffer_msg[name] = []
        elif len(buffer_msg[name]) != 0:
            clientIPv6.send(bytes("\nUnseen messages\n", FORMAT))
            for unseen_message in buffer_msg[name]:
                clientIPv6.send(bytes(f"{unseen_message}\n", FORMAT))
        Thread(target=handle_client, args=(name, clientIPv6)).start()


def handle_client(sender_name, client):
    while True:
        if sender_name not in online_users:
            break
        message = client.recv(BUFFER).decode(FORMAT)  # String
        if message.startswith("@everyone "):  # message to everyone in the chat server
            public_message(sender_name, message, online_users, registered_users, buffer_msg)
        elif message.startswith("/to "):  # direct message to a user
            private_message(sender_name, message[4:], online_users, registered_users, last_online, buffer_msg)
        elif message.startswith("/file "):  # send file
            send_file(sender_name, message[6:], online_users, file_database, buffer_msg)
        elif message.startswith("/accept "):  # accept the file
            accept_file(sender_name, message[8:], online_users, file_database)
        elif message.startswith("?who"):  # see registered users, group available
            see_users(sender_name, online_users, registered_users, group_owner)
        elif message.startswith("?status "):  # see status of registered users
            user_status(sender_name, message[8:], online_users, registered_users, last_online)
        elif message.startswith("?how"):  # see instruction
            instructions(sender_name, online_users)
        elif message.startswith("/create "):  # create group chat
            create_group(sender_name, message[8:], group_owner, group_members, online_users)
        elif message.startswith("/add "):  # add member to group
            add_users(sender_name, message[5:], group_owner, group_members, online_users, registered_users)
        elif message.startswith("?members "):  # see members of group
            see_members(sender_name, message[9:], group_owner, group_members, online_users)
        elif message.startswith("/join "):  # join group
            join_group(sender_name, message[6:], group_owner, group_members, online_users)
        elif message.startswith("/send "):  # send message to group
            send_group_message(sender_name, message[6:], group_owner, group_members, online_users, buffer_msg)
        elif message.startswith("/quit"):  # go offline
            go_offline(sender_name, online_users, last_online)
        else: 
            client.send(bytes("Unknown command. Try again!", FORMAT))


if __name__ == "__main__":
    server_v4.listen(5)
    print("Server is starting. Waiting for the clients to connect...")
    serverIPv4 = Thread(target=clients_v4)
    serverIPv6 = Thread(target=clients_v6)
    serverIPv4.start()
    serverIPv6.start()
    serverIPv4.join()
    serverIPv6.join()
    server_v4.close()
    server_v6.close()
