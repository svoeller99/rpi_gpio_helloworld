import dht11
import socket
import time
from RPi import GPIO

def celcius_to_fahrenheit(celcius):
    return (celcius * 9/5) + 32

UDP_IP = 'raspberrypi.wlan0'
UDP_PORT = 5000
BUFFER_SIZE = 1024
DHT_PIN = 17

sock = socket.socket(socket.AF_INET, # IPv4
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

GPIO.setmode(GPIO.BCM)
dht = dht11.DHT11(pin = DHT_PIN)

last_good_reading = ""

while True:
    dht_reading = dht.read()
    if dht_reading.is_valid():
        data, addr = sock.recvfrom(BUFFER_SIZE)
        celcius = dht_reading.temperature
        fahrenheit = celcius_to_fahrenheit(celcius)
        last_good_reading = f"Temp: {fahrenheit: .1f} F. Hum: {dht_reading.humidity: .1f} %"
        sock.sendto(last_good_reading.encode('utf-8'), addr)
    else:
        time.sleep(.2)