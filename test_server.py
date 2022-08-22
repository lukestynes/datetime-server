import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 12345))

while True:
    data, addr = sock.recvfrom(4096) #Something about it being equal to packet size, this is 4096 bytes
    
    print(str(data)) #Prints the clients message
    
    message = bytes("Hello I am UDP Server".encode('utf-8'))
    sock.sendto(message, addr) #UDP is connectionless so you have to send it back to where it came from, it can change!