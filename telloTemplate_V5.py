# Started from Tello Template
# This Python app is in the Public domain
# Some parts from Tello3.py

import threading, socket, sys, time, subprocess

host = ''
port = 9000
locaddr = (host,port)
rad = 100
tello_address = ('192.168.10.1', 8889) # Get the Tello drone's address

# Create a UDP socketd
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(locaddr)

def recv():
    # Message receiver
    count = 0
    global wait
    global breakr
    while True:
        try:
            data, server = sock.recvfrom(1518) # Get data from UDP port 1518?
            print(data.decode(encoding="utf-8")) # Encode data so drone can read it
            if data.decode(encoding="utf-8") == "ok": # Ok is good
                wait = False
            if breakr == True: # Stop the function
                break
        except Exception:
            print ('\nError recv\n')
            break

def sendmsg(msg, sleep = 5):
    # Message sender

    print("Sending: " + msg)
    msg = msg.encode(encoding="utf-8")
    sock.sendto(msg, tello_address)
    time.sleep(sleep)

# recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()
print("\nFirst & Last Names")
print("Program Name: ")
print("Date: ")
print("\n****CHECK YOUR TELLO WIFI ADDRESS")
print("\n****CHECK SURROUNDING AREA BEFORE FLIGHT****")
print(input("\nAre you ready to take flight? "))
print("\nStarting Drone!\n")

time.sleep(1)
try:
    sendmsg('command', 0)
    sendmsg('takeoff')

    # Commands go here, read the SDK for commands.

    sendmsg('land')
    print('Great Flight!!!')
except KeyboardInterrupt: # Ctrl+C (Use if drone is going crazy and to exit the application)
    sendmsg('emergency')
breakr = True
sock.close()
