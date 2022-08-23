import select
import socket
import sys
import datetime

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
    if len(req_packet) != 6:
        print("<ERROR: Recieved packet is incorrect length. Must be 6 bytes>")
        print(len(req_packet))
        return False
    
    magic_no = (req_packet[0] << 8) | req_packet[1]
    packet_type = (req_packet[2] << 8) | req_packet[3]
    request_type = (req_packet[4] << 8) | req_packet[5]
    
    if magic_no != 0x497E:
        print("<ERROR: MagicNumber incorrect value. Packet discarded>")
        return False
    elif packet_type != 0x0001:
        print("<ERROR: PacketType incorrect value. Packet discarded>")
        return False
    elif request_type != 0x0001 and req_packet != 0x0002:
        print("<ERROR: RequestType incorrect. Packet discarded>")
        return False
    
    return True, request_type

def text_representation(req_type, lang, date_info):
    if lang == "eng":
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        
        if req_type == "date":
            return "Today's date is {} {}, {}".format(months[date_info[1] - 1], date_info[2], date_info[0])
        else:
            return "The current time is {}:{}".format(date_info[3], date_info[4])
    elif lang == "mao":
        months = ["Kohitatea", "Hui-tanguru", "Poutu-te-rangi", "Paenga-whawha", "Haratua", "Pipiri", "Hongongoi", "Here-turi-koka", "Mahuru", "Whiringa-a-nuku", "Whiringa-a-rangi", "Hakihea"]

        if req_type == "date":
            return "Ko te ra o tenei ra ko {} {}, {}".format(months[date_info[1] - 1], date_info[2], date_info[0])
        else:
            return "Ko te wa o tenei wa {}:{}".format(date_info[3], date_info[4])
    else:
        months = ["Januar", "Februar", "Marz", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

        if req_type == "date":
            return "Heute ist der {} {}, {}".format(months[date_info[1] - 1], date_info[2], date_info[0])
        else:
            return "Die Uhrzeit ist {}:{}".format(date_info[3], date_info[4])


def response_packet_builder(req_type, port):
    """Creates a DT-Response packet to be sent to the client"""
    lang = None
    
    match port:
        case "eng":
            lang = 0x0001
        case "mao":
            lang = 0x0002
        case "ger":
            lang = 0x0003
    
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    hour = datetime.datetime.now().time().hour
    minute = datetime.datetime.now().time().hour
    text = "hello"
    length = len(text) #TODO LENGTH OF TEXT FIELD

    data_array = [0x497E, 0x0002, lang, year, month, day, hour, minute, length]
    composed_packet = bytearray()
    for i in range(len(data_array)):
        if i < 4: #First 4 bytes
            for parameter in data_array[0:3]:
                composed_packet += parameter.to_bytes(2, byteorder="big")
        elif i < 9:
            for parameter in data_array[4:]:
                composed_packet += parameter.to_bytes(1, byteorder="big")
    composed_packet += text.encode('utf-8')

    return composed_packet

def run_loop(socks, ports):
    """Once the sockets are bound this loop runs the server"""
    print("Server is running succesfully")

    while True:
        #TODO: CONVERT THIS TO BE A PROPER THING USING THE SELECT METHOD SO WE DON'T WASTE RESOURCES
        #Look for the DT-Request Packet
        req_packet, addr = socks[0].recvfrom(6) #English
        #port = ports[0] #TODO NEEDS TO UPDATE PORT DEPENDING ON WHICH SOCKET WE READ
        print(str(req_packet)) #Prints the clients message
        
        valid, req_type = check_request(req_packet)
        if valid:
            #Packet is correct, move on to next step
            dt_response = response_packet_builder(req_type, "eng")

            socks[0].sendto(dt_response, addr) #UDP is connectionless so you have to send it back to where it came from, it can change!

        

def main():
    print("Date Time Server Started...")
    ports = port_init()

    if ports == -1:
        sys.exit()
    socks = bind_ports(ports)
    run_loop(socks, ports)

if __name__ == "__main__":
    main()