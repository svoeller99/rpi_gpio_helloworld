#!/usr/bin/python3

import time
from mfrc522 import SimpleMFRC522
from RPi import GPIO

reader = SimpleMFRC522()

try:
    command = input("Do you want to write or scan? (write/scan): ")
    if command == 'write':
        text = input("Please write the new data: ")
        print("Please place the card to complete writing")
        reader.write(text)
        print("Data writing is complete")
    elif command == 'scan':
        print("Reading... Please place the card...")
        id, text = reader.read()
        print(f"ID: {id}\nText: {text}")
        time.sleep(3)
    else:
        print(f"Unrecognized command '{command}'")
except KeyboardInterrupt:
    print('bye')
GPIO.cleanup()