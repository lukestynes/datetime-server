import socket

def client_init():
    """Get the initial info from the user for the setup"""

    req_type = input("Enter 'date' or 'time' depending what request you want: ")
    if req_type != "date" and req_type != "time":
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

    return req_type, addr, port

def packet_builder(data_array):
    """Takes an array of all the packet numbers and converts it to a bytearray packet"""

    composed_packet = bytearray()

    #Goes through each inputted parameter and adjusts the numbers into bytes correctly
    for parameter in data_array:
        if parameter < 256:
            composed_packet += parameter.to_bytes(1, byteorder="big")
        elif parameter < 655356:
            composed_packet += parameter.to_bytes(2, byteorder="big")
        elif parameter < 16777216:
            composed_packet += parameter.to_bytes(3, byteorder="big")
        elif parameter < 4294967296:
            composed_packet += parameter.to_bytes(4, byteorder="big")

    return composed_packet

def make_request(req_type, addr, port):
    """Opens the UDP socket and sends the DT-Request packet"""

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if req_type == 'date':
        req = 0x0001
    else:
        req = 0x0002

    request_array = [0x497E, 0x0001, req]
    dt_request = packet_builder(request_array)

    sock.sendto(dt_request, (addr, port))

    #TODO: TIMEOUT AFTER 1 SECOND OF NO REQUEST
    data, srv_addr = sock.recvfrom(4096)
    print("Server response")
    print(str(data))

    sock.close()


def main():
    """Main Function"""
    print("Datetime Client Running...")
    req_type, addr, port = client_init()
    make_request(req_type, addr, port)

if __name__ == "__main__":
    main()