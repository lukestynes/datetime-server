import select
import socket
import sys

def port_init():
    """Gets the specified 3 port numbers for each language"""
    print("[Please enter a unique port for each language, it must be between 1024 and 64000]")

    english_port = input("Please enter a port number for English: ")
    maori_port = input("Please enter a port number for Te Reo Maori: ")
    german_port = input("Please enter a port number for German: ")

    #Check for errors, if -1 is returned the program quits out
    if not english_port.isdigit() or not maori_port.isdigit() or not german_port.isdigit():
        print("<ERROR: Port numbers must be integers>")
        return -1
    
    english_port = int(english_port)
    maori_port = int(maori_port)
    german_port = int(german_port)
    
    if english_port == maori_port or english_port == german_port or maori_port == german_port:
        print("<ERROR: Port numbers must be unique")
        return -1
    elif english_port < 1024 or german_port < 1024 or maori_port < 1024:
        print("<ERROR: Port numbers must be between 1024 and 64000>")
        return -1
    elif english_port > 64000 or german_port > 64000 or maori_port > 64000:
        print("<ERROR: Port numbers must be between 1024 and 64000>")
        return -1
    
    return (english_port, maori_port, german_port)

def bind_ports(ports):
    """Attempts to bind the 3 given ports and open 3 sockets"""
    print("Attempting to bind the given ports...")
    sock_english = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_english.bind(('127.0.0.1', ports[0]))

    sock_maori = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_maori.bind(('127.0.0.1', ports[1]))

    sock_german = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_german.bind(('127.0.0.1', ports[2]))

    #TODO: LOOK INTO ERROR CHECKING IF THIS BIND FAILS, BUT I'M NOT SURE HOW IT WOULD
    return (sock_english, sock_maori, sock_german)

def check_request(req_packet):
    """Checks if the recieved packet is a correct DT-Request packet"""
    if req_packet.len() != 6:
        print("<ERROR: Recieved packet is incorrect length. Must be 6 bytes>")
        return False
    elif req_packet[0] != 0x497E:
        print("<ERROR: MagicNumber incorrect value>")
        return False
    elif req_packet[1] != 0x0001:
        print("<ERROR: PacketType incorrect value>")
        return False
    elif req_packet[2] != 0x0001 or req_packet != 0x0002:
        print("<ERROR: RequestType incorrect>")
        return False
    
    return True

def run_loop(socks, ports):
    """Once the sockets are bound this loop runs the server"""
    print("Server is running succesfully")

    while True:
        #TODO: CONVERT THIS TO BE A PROPER THING USING THE SELECT METHOD SO WE DON'T WASTE RESOURCES
        #Look for the DT-Request Packet
        req_packet, addr = socks[0].recvfrom(6) #English
        print(str(req_packet)) #Prints the clients message
        
        port = ports[0]


        
        
        message = bytes("Hello I am UDP Server".encode('utf-8'))
        socks[0].sendto(message, addr) #UDP is connectionless so you have to send it back to where it came from, it can change!

def main():
    print("Date Time Server Started...")
    ports = port_init()

    if ports == -1:
        sys.exit()
    socks = bind_ports(ports)
    run_loop(socks, ports)

if __name__ == "__main__":
    main()