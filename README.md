# COSC4010: nUWTech Laboratory Development

As a part of the independent study, three projects were done by combining the hardware and software components. A detailed explanation of the projects are given below.


# Project 1: Simple IoT

**Description:** This project deals with creating a simple IoT using Raspberry Pi. The purpose of this project is to create a webpage through HTML, CSS and JavaScript, and connect the webpage to Python (using Flask web framework) and power the webpage on the Raspberry Pi. The webpage contains the status of the Blue LED connected to the Raspberry Pi, a slider to increase or decrease the brightness/ intensity of the LED and a window that displays the blue LED through the camera connected to the Raspberry Pi. 

Raspberry Pi basically acts as a web server, and the clients will be one of the computers connected to the same network as Raspberry Pi. The clients will be able to access the webpage through the IP address of Raspberry Pi and control the LEDs using the slider from the webpage remotely. 

**Components Used:**<br>
*Hardware:* 
1) Raspberry Pi
2) Camera
3) Blue LED

*Programming and Markup Languages:*<br>
1) Python <br>
*libraries:* Flask, OpenCV, GPIOZero, atexit
2) HTML<br>
*components*: CSS, JavaScript

![Simple IoT](https://i.ibb.co/D8JjLjh/Simple-Io-T-1.gif)

# Project 2: Track Following Autonomous Vehicle with Camera Display

This project deals with creating an autonomous vehicle or robot, using Raspberry Pi. It uses components such as the robot platform, 4 motors, an Adafruit HAT to control the motor and infrared (IR) sensors to follow the track or line taped with an electric tape. The vehicle runs in a loop of a square of with round edges. The attached camera will display the car. 

The two IR sensors is faced down on the floor, lying on either sides to detect the tape. If both IR sensors does not detect the electric tape, the vehicle moves forward. Likewise, if the left IR sensor detects the black tape on the rounded edges, the vehicle will steer left. Similarly, if the right IR sensor detects the black tape on the rounded edges, the vehicle will steer right. 

**Components Used:**<br>

*Hardware:* <br>
1) Raspberry Pi
2) Camera
3) Adafruit MotorHAT
4) IR sensors (x2)
5) Vehicle Platform
6) Battery Pack for Motors
7) Portable Power Supply for Raspberry Pi'

*Programming and Markup Languages:*<br>
1) Python <br>
*libraries:* Time, OpenCV, Adafruit Motor Module, Pynput, Threading, Tkinter

![Autonomous vehicle](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTkxNDJhZTUxYTQxNGFkZTFhNjEzNDZmOTI0NTg3YzEyYTBkNjZkMSZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/Q2a5nsBT2j2ej0XE83/giphy.gif)

# Project 3: Controlling a Robotic Arm with Hand Gestures

This project deals with controlling the a 6-motored Arm-like Robot using application of computer vision on Raspberry Pi. For this, a 6-motored Arm-like Robot is be controlled using the MediaPipe ML Solutions Hand Gestures Algorithm (link: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker).

Each of the six motors need to be selected, one at a time for their operations. The input pins of the motor that controls the robots is connected to the IO pins of the Raspberry Pi through the Adafruit MotorHAT and is controlled through the supplied hand gestures in real time. 

For instance, if the first motor is selected and if an input of the index finger is provided through the camera, the robot moves in clockwise direction. Likewise, the index+middle fingers (2 fingers) will make the robot move anticlockwise, and so on. 

Hand gesture operation is run through desktop and the robot movement operation is run through Raspberry Pi. The inter-process communication between desktop and Raspberry pi is done through socket programming in the same network. 

- The camera takes inputs such as *Index Finger*, *Peace Sign*, and *Palm sign*.
- The slider is used to change the motor’s position, motor 0 being standby mode.
- The index finger makes it go either clockwise, right, or catch depending on the orientation.
- The Peace sign makes it go either anti-clockwise, left, or release depending on the orientation.
- The Palm sign pauses or halts the Arm.

**Components Used:**<br>
*Hardware:* <br>
1) Raspberry Pi
2) Camera
3) Adafruit MotorHATs (x2)
5) Vehicle Platform
6) Battery Pack for Motors (x2)
7) Portable Power Supply for Raspberry Pi'

*Programming Languages:*<br>
1) Python <br>
*libraries:* Mediapipe, Time, OpenCV, Adafruit Motor Module, Pynput, Threading, Tkinter, Socket

![Robot Arm](https://s12.gifyu.com/images/RoboticArm.md.gif)
