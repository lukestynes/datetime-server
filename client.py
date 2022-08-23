from mimetypes import init
import socket
import select
import sys

def client_init():
    """Get the initial info from the user for the setup"""

    req_type = input("Enter 'date' or 'time' depending what request you want: ")
    if req_type != "date" and req_type != "time":
        print("<ERROR: You must enter 'date' or 'time'>")
        return -1
    
    #TODO: ERROR CHECK ADDRESS
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

def request_packet_builder(data_array):
    """Takes an array of all the packet numbers and converts it to a bytearray packet"""
    composed_packet = bytearray()
    for parameter in data_array:
        composed_packet += parameter.to_bytes(2, byteorder="big")

    return composed_packet

def make_request(req_type, addr, port):
    """Opens the UDP socket and sends the DT-Request packet"""

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if req_type == 'date':
        req = 0x0001
    else:
        req = 0x0002

    request_array = [0x497E, 0x0001, req]
    dt_request = request_packet_builder(request_array)

    sock.sendto(dt_request, (addr, port))

    #Causes the client to timeout and shut if no response in 1 second
    ready = select.select([sock], [], [], 1)
    if ready[0]:
        data, srv_addr = sock.recvfrom(4096)
        sock.close()
        return data
    else:
        print("<ERROR: Server timeout, no response received>")
        sock.close()
        return -1

def check_reponse(resp_packet):
    """Checks if the recieved packet is a correct DT-Reponse packet"""

    if len(resp_packet) < 13:
        print("<ERROR: Packet too small>")
        return -1

    magic_no = (resp_packet[0] << 8) | resp_packet[1]
    packet_type = (resp_packet[2] << 8) | resp_packet[3]
    lang_code = (resp_packet[4] << 8) | resp_packet[5]
    year = (resp_packet[6] << 8) | resp_packet[7]
    month = resp_packet[8]
    day = resp_packet[9]
    hour = resp_packet[10]
    minute = resp_packet[11]
    length = resp_packet[12]
    text = resp_packet[13:]

    if magic_no != 0x497E:
        print("<ERROR: MagicNo wrong>")
        return False
    elif packet_type != 0x0002:
        print("<ERROR: Wrong packet type>")
        return False
    elif lang_code != 0x0001 and lang_code != 0x0002 and lang_code != 0x0003:
        print("<ERROR: Wrong language code>")
        return False
    elif year > 2100:
        print("<ERROR: You're too far in the future>")
        return False
    elif month < 1 or month > 12:
        print("<ERROR: Incorrect month>")
        return False
    elif day < 1 or day > 31:
        print("<ERROR: Incorrect day>")
        return False
    elif hour < 1 or hour > 23:
        print("<ERROR: Incorrect hour>")
        return False
    elif minute < 1 or minute > 59:
        print("<ERROR: Incorrect minute>")
        return False
    elif len(resp_packet) != (13 + length):
        print("<ERROR: Packet recieved wrong size>")
        return False
    return True
    
def print_response(resp_packet):
    """Prints out the received packet nicely to the terminal"""
    magic_no = (resp_packet[0] << 8) | resp_packet[1]
    packet_type = (resp_packet[2] << 8) | resp_packet[3]
    lang_code = (resp_packet[4] << 8) | resp_packet[5]
    year = (resp_packet[6] << 8) | resp_packet[7]
    month = resp_packet[8]
    day = resp_packet[9]
    hour = resp_packet[10]
    minute = resp_packet[11]
    length = resp_packet[12]
    text = resp_packet[13:]
    print("MagicNo: ", magic_no)
    print("PacketType: ", packet_type)
    print("LanguageCode: ", lang_code)
    print("Year: ", year)
    print("Month: ", month)
    print("Day: ", day)
    print("Hour: ", hour)
    print("Minute: ", minute)
    print("Length: ", length)
    print("Text: ", str(text)[2:-1])

def main():
    """Main Function"""
    print("Datetime Client Running...")
    init_values = client_init()
    
    if init_values == -1:
        sys.exit()

    resp_packet = make_request(init_values[0], init_values[1], init_values[2])
    
    if resp_packet == -1:
        sys.exit()

    valid = check_reponse(resp_packet)

    if not valid:
        sys.exit()
    else:
        print_response(resp_packet)


if __name__ == "__main__":
    main()