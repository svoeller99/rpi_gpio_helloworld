import socket

UDP_IP = 'raspberrypi4wifi'
UDP_PORT = 5000

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

while True:
    message = input('enter a message: ')
    message = message.encode('utf-8')

    sock = socket.socket(socket.AF_INET, # IPv4
                        socket.SOCK_DGRAM) # UDP
    sock.sendto(message, (UDP_IP, UDP_PORT))
    data, addr = sock.recvfrom(1024)
    print("received message from server %s: %s" % addr, data)