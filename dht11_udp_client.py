import socket
from time import sleep

UDP_IP = 'raspberrypi4wifi'
UDP_PORT = 5000

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

def request_reading(command = ''):
    sock = socket.socket(socket.AF_INET, # IPv4
                        socket.SOCK_DGRAM) # UDP
    sock.sendto(command.encode('utf-8'), (UDP_IP, UDP_PORT))
    data, addr = sock.recvfrom(1024)
    print(data.decode('utf-8'))

while True:
    request_reading()
    sleep(1)
    request_reading('TEMP')
    sleep(1)
    request_reading('HUM')
    sleep(1)