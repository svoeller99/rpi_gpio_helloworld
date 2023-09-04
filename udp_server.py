import socket

UDP_IP = 'raspberrypi.wlan0'
UDP_PORT = 5000
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, # IPv4
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    print("received message from %s: %s" % addr, data)
