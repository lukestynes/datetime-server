import socket

def client_init():
    """Get the initial info from the user for the setup"""

    req_type = input("Enter 'date' or 'time' depending what request you want: ")
    if req_type != 'data' or req_type != 'time':
        print("<ERROR: You must enter 'date' or 'time'>")
        return -1
    
    addr = input("Enter the address of the server: ")
    port = input("Enter the port of the server: ")

    if not port.isdigit():
        print("<ERROR: Port number must be an integer>")
        return -1
    
    port = int(port)
    if port < 1024 or port > 64000:
        print("<ERROR: Port number must be between 1024 and 64000>")
        return -1

    return (req_type, addr, port)


def main():
    """Main Function"""
    print("Datetime Client Running...")
    init_values = client_init()

if __name__ == "__main__":
    main()