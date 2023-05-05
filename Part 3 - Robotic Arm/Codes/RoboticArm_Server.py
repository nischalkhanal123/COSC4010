'''
                Raspberry Pi Arm Server Code. This code should before running the client code.
    After the Pi Arm GUI window has been displayed on the client's device, press the Pushbutton to start the PiArm.
                To exit out of program, simply press the red Stop/ Restart Backend button on the top, or do KeyboardInterrupt
                                                  Designed by Nischal Khanal
'''
#Import socket for network communcation with client
import socket
# import thread module
from _thread import *
import threading
#Import the MotorKit for running the PiArm motors
from adafruit_motorkit import MotorKit
#Import GPIO pins from the Pi
import RPi.GPIO as io
#Initialize the MotorKit object for running 4 motors
kit = MotorKit()
#Initialize the MotorKit object at address 0x61 for running the fifth motor
kit2 = MotorKit(address=0x61)
#Initialize the interrupt button for starting the Pi Arm
SwapMotorButton_Pin = 5
#Set the speed of Pi Arm motors
Speed = 0.8
#Function to change the motor from the data received from the slider menu
def ChangeMotor(channel):
    print("You are in change motor")
    #This data has the information obtained from the client
    global data
    global flag
    flag = True
    #Initialize data as a random 4-bit string
    data = "0000"
    #Infinite loop
    while flag:
        #Get the string contents of the data
        data = str(data)
        #The functions to call respective motors depending on the selection
        if str(data[0]) == "0":
            motor0()
            print("You selected:", data[0])
        elif str(data[0]) == "1":
            motor1(data)
            print("You selected:", data[0])
        elif str(data[0]) == "2":
            motor2(data)
            print("You selected:", data[0])
        elif str(data[0]) == "3":
            motor3(data)
            print("You selected:", data[0])
        elif str(data[0]) == "4":
            motor4(data)
            print("You selected:", data[0])
        elif str(data[0]) == "5":
            motor5(data)
            print("You selected:", data[0])
#Motor 0 function makes the Pi Arm go in Idle/ Standby mode
def motor0():
        #Stop all the motors from running
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
        kit.motor3.throttle = 0
        kit.motor4.throttle = 0
        kit2.motor1.throttle = 0
        kit2.motor2.throttle = 0
# Function to run motor1 (Clockwise or anticlockwise) 
def motor1(data):
        print("You are inside motor 1")
        #If index finger sign is recognized
        if (data[1] == "1"):
            print("Moving Motor 1 Forward")
            kit.motor1.throttle = Speed
        #If peace sign is recognized
        elif (data[1] == "2"):
            print("Moving Motor 1 Backward")
            kit.motor1.throttle = -Speed
        #Stop if either of two signs is not recognized
        else:
            kit.motor1.throttle = 0
# Function to run motor2 (Up or Down) 
def motor2(data):
        print("You are inside motor 2")
        print(data)
        if (data[1] == "1"):
            print("Moving Motor 2 Forward")
            kit.motor2.throttle = Speed
        elif (data[1] == "2"):
            print("Moving Motor 2 Backward")
            kit.motor2.throttle = -Speed
        else:
            kit.motor2.throttle = 0
# Function to run motor3 (Up or Down) 
def motor3(data):
        print("You are inside motor 3")
        print(data)
        if (data[1] == "1"):
            print("Moving Motor 2 Forward")
            kit.motor3.throttle = Speed
        elif (data[1] == "2"):
            print("Moving Motor 2 Backward")
            kit.motor3.throttle = -Speed
        else:
            kit.motor3.throttle = 0
# Function to run motor4 (Up or Down) 
def motor4(data):
        print("You are inside motor 4")
        print(data)
        if (data[1] == "1"):
            print("Moving Motor 2 Forward")
            kit.motor4.throttle = Speed
        elif (data[1] == "2"):
            print("Moving Motor 2 Backward")
            kit.motor4.throttle = -Speed
        else:
            kit.motor4.throttle = 0
# Function to run motor5 (Catch or Release) 
def motor5(data):
        print("You are inside motor 5")
        print(data)
        if (data[1] == "1"):
            print("Moving Motor 2 Forward")
            kit2.motor1.throttle = Speed
        elif (data[1] == "2"):
            print("Moving Motor 2 Backward")
            kit2.motor1.throttle = -Speed
        else:
            kit2.motor1.throttle = 0
# Multithread function to obtain the data from the client
def threaded(c):
    global data
    while True:
        # data received from client
        data = c.recv(1024)
        #Decode the data for Raspberry Pi to understand
        data = data.decode()
        if not data:
            print('Data not recognized, closing the device')
            # lock released on exit
            print_lock.release()
            break
    # connection closed
    c.close()
# Main function to control the server-client connection 
def Main():
    host = ""
    # reserve a port on Raspberry Pi (8080)
    # The client needs to have the same port
    port = 8080
    # Make request for the client to connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Socket binded to port", port)
    # put the socket into listening mode
    s.listen(5)
    print("Waiting for the client to connect")
    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        print("Now you can use the Pi Arm by pressing the Pushbutton")
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()
if __name__ == '__main__':
    global flag
    io.setmode(io.BCM)
    io.setup(SwapMotorButton_Pin, io.IN, pull_up_down = io.PUD_DOWN)
    io.add_event_detect(SwapMotorButton_Pin, io.RISING, callback = ChangeMotor, bouncetime = 500)
    print_lock = threading.Lock()
    try:
        #Call the server-client connection function
        Main()
    except KeyboardInterrupt:
        flag = False
        print("Exiting Program")
        #Stop all the motor operation and exit the program
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
        kit.motor3.throttle = 0
        kit.motor4.throttle = 0
        kit2.motor1.throttle = 0
        kit2.motor2.throttle = 0
        io.cleanup()

