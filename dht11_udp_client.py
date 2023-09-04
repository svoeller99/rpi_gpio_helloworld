import socket
from time import sleep

UDP_IP = 'raspberrypi4wifi'
UDP_PORT = 5000

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

while True:
    sock = socket.socket(socket.AF_INET, # IPv4
                        socket.SOCK_DGRAM) # UDP
    sock.sendto(b'', (UDP_IP, UDP_PORT))
    data, addr = sock.recvfrom(1024)
    print(data.decode('utf-8'))
    sleep(1)