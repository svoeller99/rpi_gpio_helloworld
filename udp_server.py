import socket

UDP_IP = 'raspberrypi.wlan0'
UDP_PORT = 5000
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, # IPv4
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

cnt = 0

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    message = data.decode('utf-8')
    print("received message from client %s: %s" % addr, message)
    if message == 'INC':
        cnt += 1
    if message == 'DEC':
        cnt -= 1
    sock.sendto(f'hi there, client - counter is {cnt}'.encode('utf-8'), addr)