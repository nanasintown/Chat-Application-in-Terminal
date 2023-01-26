from datetime import datetime
# Nhut Cao 906939
# ELEC-C7420 Basic principles in networking
FORMAT = 'utf-8'


def broadcast(message, online_users):
    for name in online_users:
        online_users[name].send(bytes(message, FORMAT))


def public_message(sender_name, message, online_users, registered_users, buffered_messages):
    time_stamp = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
    sent_message = f'[{time_stamp}] Public message from {sender_name}: {message[9:]}'
    for member in registered_users:
        if member not in online_users:
            buffered_messages[member].append(sent_message)
    broadcast(sent_message, online_users)


def private_message(sender_name, message, online_user, registered_users, last_online, buffered_messages):
    receiver_name = message.split()[0]
    if receiver_name not in registered_users:
        online_user[sender_name].send(bytes("User not found. Please check again", FORMAT))
    elif receiver_name not in online_user:
        online_user[sender_name].send(bytes(f"The user is currently offline. Last online \
{last_online[receiver_name]}. \nThe user will see the message later.", FORMAT))
        time_stamp = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
        message_body = message.split(' ', 1)[1]
        buffered_messages[receiver_name].append("[" + time_stamp + "] " + sender_name + ": " + message_body)
    else: 
        time_stamp = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
        message_body = message.split(' ', 1)[1]
        online_user[receiver_name].send(bytes(f"[{time_stamp}] {sender_name}: {message_body}", FORMAT))
        online_user[sender_name].send(bytes(f"{receiver_name} has seen.", FORMAT))


def send_file(sender_name, message, online_users, file_database, buffered_messages):
    receiver_name = message.split()[0]
    file_path = message.split()[1]
    openfile = open(file_path)
    file_data = openfile.read()
    file_database[file_path] = file_data
    if receiver_name in online_users:
        online_users[sender_name].send(bytes(f"{receiver_name} has seen your file transfer", FORMAT))
        online_users[receiver_name].send(bytes(f"{sender_name} sent a file. \
        Do you want to save the file?\nType '/accept {file_path} as <file name>' \
        to save the file\n>>>", FORMAT))
    else: 
        time_stamp = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
        online_users[sender_name].send(bytes(f"{receiver_name} is currently offline. \
        They will see your file transfer later.", FORMAT))
        buffered_messages[receiver_name].append(f"[{time_stamp}] {sender_name} sent a file. Do you \
        want to save the file?\nType '/accept {file_path} as <file name>' to save the file\n>>>")


def accept_file(sender_name, message, online_user, file_database):
    file_path = message.split()[0]
    file_name = message.split()[2]
    if file_path not in file_database:
        online_user[sender_name].send(bytes(f"There is no file {file_path} in the server. Please check again.", FORMAT))
    else:
        file_data = file_database[file_path]
        online_user[sender_name].send(bytes(f"The file has been successfully saved\n", FORMAT))
        online_user[sender_name].send(bytes(f"/downloaded\n{file_data}\n{file_name}", FORMAT))


def see_users(sender_name, online_users, registered_users, group_owner):
    registered_users_info = "Registered users: "
    for name in registered_users:
        registered_users_info += name + ", "
    registered_users_info = registered_users_info[:-2]

    online_users_info = "Online users: "
    for name in online_users:
        online_users_info += name + ", "
    online_users_info = online_users_info[:-2]

    # groups_infor = ""
    if len(group_owner) == 0:
        groups_info = "No available groups  "
    else:
        groups_info = "Available groups: "
        for groupName in group_owner:
            groups_info += groupName + ", "
    groups_info = groups_info[:-2]
    
    online_users[sender_name].send(bytes(f"{registered_users_info}\n{online_users_info}\n{groups_info}\n", FORMAT))


def user_status(sender_name, message, online_users, registered_users, last_online):
    receiver_user = message
    if receiver_user not in registered_users:
        online_users[sender_name].send(bytes(f"There is no such user {receiver_user} in the server", FORMAT))
    elif receiver_user in online_users:
        online_users[sender_name].send(bytes(f"The user {receiver_user} is currently online", FORMAT))
    else: 
        online_users[sender_name].send(bytes(f"The user {receiver_user} is currently offline. Last online \
{last_online[receiver_user]}", FORMAT))

    
def instructions(sender_name, online_users):
    # ------- Universal broadcast message -------
    # Command @everyone <message>
    online_users[sender_name].send(bytes("\nSend '@everyone <message>' command to send a message to all users.", FORMAT))
    # Private message
    # Command /to <user name> <message>
    online_users[sender_name].send(bytes("\nSend '/to <user name> <message>' command to send a private message to a\
     user", FORMAT))

    # ------- Server stats -------
    # Command ?who
    online_users[sender_name].send(bytes("\nSend '?who' to see all registered users, online users, available \
    groups", FORMAT))
    # Command ?status <user name>
    online_users[sender_name].send(bytes("\nSend '?status <client name>' to check current status of a user", FORMAT))
    # Command ?command
    online_users[sender_name].send(bytes("\nSend '?how' to see instructions on how to use the chat application",
                                         FORMAT))

    # ------- Group chat -------
    # Command /create <group name>
    online_users[sender_name].send(bytes("\nSend '/create <group name>' to create a new group. Group name should \
    be one word", FORMAT))
    # Command /add <group name> <member> <member>...<member>. Only for group creator
    online_users[sender_name].send(bytes("\nSend '/add <member> <member>...<member>' to add members to a group. \
    Only for group owner", FORMAT))
    # Command /remove <group name> <member> <member>...<member>. Only for group owner
    online_users[sender_name].send(bytes("\nSend '/remove <member> <member>...<member>' to remove members from a group.\
     Only for group owner", FORMAT))
    # Command ?members <group name>
    online_users[sender_name].send(bytes("\nSend '?members <group name>' to see members of the group", FORMAT))
    # Command /join <group name>. For any users
    online_users[sender_name].send(bytes("\nSend '/join <group name>' to join an existing group", FORMAT))
    # Command /send <group name> <message>. For any users
    online_users[sender_name].send(bytes("\nSend '/send <group name> <message>' to send a message to joined \
    group", FORMAT))

    # ------- File transfer -------
    # Command /file <client name> <file path>
    online_users[sender_name].send(bytes("\nSend '/file <client name> <file path>' command to send a file to a user",
                                         FORMAT))
    # Command /accept <file path> as <file name>
    online_users[sender_name].send(bytes("\nSend '/accept <file path> as <file name>' command to receive the file \
    from the server", FORMAT))

    # ------- End chat -------
    # Command /quit
    online_users[sender_name].send(bytes("\nType '/quit' to left the chat", FORMAT))


def create_group(sender_name, message, group_owner, group_members, online_users):
    group_name = message
    if group_name in group_owner:
        online_users[sender_name].send(bytes("The group " + group_name + " already exists. Please choose different name",
                                             FORMAT))
    else: 
        group_owner[group_name] = sender_name
        group_members[group_name] = [sender_name]
        time_stamp = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
        message = f"[{time_stamp}] {sender_name} created the group {group_name}"
        broadcast(message, online_users)


def add_users(sender_name, message, group_owner, group_members, online_users, registered_users):
    group_name = message.split()[0]
    added_users = message.split(' ', 1)[1].split()
    if group_name not in group_owner:
        online_users[sender_name].send(bytes("The group does not exist. Check name again!", FORMAT))
    elif sender_name != group_owner[group_name]:
        online_users[sender_name].send(bytes("Only admin/group owner can add user to the group.", FORMAT))
    else:
        for member in added_users:
            if member in registered_users:
                group_members[group_name].append(member)
                online_users[sender_name].send(bytes(f"User {member} has been added to {group_name}\n", FORMAT))
            else:
                online_users[sender_name].send(bytes(f"User {member} does not exist and can't be\
                 added to {group_name}\n", FORMAT))


def see_members(sender_name, message, group_owner, group_members, online_users):
    group_name = message
    if group_name not in group_owner:
        online_users[sender_name].send(bytes("This group does not exist. Please check again", FORMAT))
    else:
        admin = group_owner[group_name]
        members_info = f"The member(s) in the group {group_name} are: "
        for member in group_members[group_name]:
            if member == admin: 
                members_info += f"{member} (admin), "
            else: 
                members_info += f"{member}, "
        members_info = members_info[:-2]
        online_users[sender_name].send(bytes(members_info, FORMAT))


def join_group(sender_name, message, group_owner, group_members, online_users):
    group_name = message
    if group_name not in group_owner:
        online_users[sender_name].send(bytes("This group does not exist. Please check again!", FORMAT))
    elif sender_name in group_members[group_name]:
        online_users[sender_name].send(bytes(f"You have already joined the group {group_name}", FORMAT))
    else:
        group_members[group_name].append(sender_name)
        time_stamp = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
        message = f"[{time_stamp}] {sender_name} has joined the group {group_name}"
        broadcast(message, online_users)


def send_group_message(sender_name, message, group_owner, group_members, online_users, buffered_msg):
    group_name = message.split()[0]
    group_msg = message.split(' ', 1)[1]
    if group_name not in group_owner:
        online_users[sender_name].send(bytes("This group does not exist. Please check again", FORMAT))
    elif sender_name not in group_members[group_name]:
        online_users[sender_name].send(bytes(f"You are not a member in the group {group_name} to send \
        message. Type '/join {group_name}' to join the group", FORMAT))
    else:
        curr_onl_not_sender = []
        offline_users = []
        for member in group_members[group_name]:
            if member in online_users and member != sender_name:
                curr_onl_not_sender.append(member)
            else:
                offline_users.append(member)

        if len(group_members[group_name]) == 1:
            online_users[sender_name].send(bytes(f"No available members. Add more members with '/add \
{group_name} <member> <member>...'", FORMAT))
        else:
            time_stamp = datetime.now().strftime("%d/%m/%y-%H:%M:%S")

            if len(curr_onl_not_sender) == 0:
                online_users[sender_name].send(bytes(f"Users are offline.", FORMAT))
            else:
                seen_users = "Members "
                for member in curr_onl_not_sender:
                    seen_users += f"{member}, "
                    online_users[member].send(bytes(f"[{time_stamp}] Message from {group_name}, {sender_name}: {group_msg}", FORMAT))
                seen_users = seen_users[:-2] + " have seen."
                online_users[sender_name].send(bytes(seen_users, FORMAT))
            for member in offline_users:
                buffered_msg[member].append(f"[{time_stamp}] Group {group_name}, {sender_name}: {group_msg}")


def go_offline(sender_name, online_users, last_seen):
    del online_users[sender_name]
    last_seen[sender_name] = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
    message = f"\nUser {sender_name} has left the chat"
    for name in online_users:
        online_users[name].send(bytes(message, FORMAT))
