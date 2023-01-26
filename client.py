import client_IPv4
import client_IPv6

# Nhut Cao 906939
# ELEC-C7420 Basic principles in networking

def main():
    version = int(input("Which version of IP would you like to connect, IPv4 or IPv6? Please type 4 or 6\n>>> "))
    while version != 4 and version != 6:
        version = input("Unknown IP version. Please type 4 or 6\n>>> ")
    if version == 4:
        client_IPv4.main()
    else:
        client_IPv6.main()


if __name__ == "__main__":
    main()
