'''
        Pi Arm client code from external device. This code shall be run after running the server code on Raspberry Pi.
                                                Designed by Nischal Khanal
'''
#Import the cv2 module for computer vision operations
import cv2
#Import the mediapipe library for live Machine Learning
import mediapipe as mp
#Import tkinter and time for GUI based operations
from tkinter import *
import time
#Import socket for network communcation with client
import socket
# Make sure the IP address is the same as the IP address of Raspberry Pi
ip = "10.121.138.149"
# Initialize mediapipe modules for drawing co-ordinates in hands
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
# For webcam input:
mp_hands = mp.solutions.hands
#Empty function for bypassing errors
def nothing(x):
    pass
#Open the connected camera
cap = cv2.VideoCapture(0)
#Send request to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, 8080))
#Pi Arm GUI window
cv2.namedWindow('PiARM Control')
#Pi Arm motor selection slider
cv2.createTrackbar('MOTOR:','PiARM Control',1,5,nothing)
with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_height, image_width, _ = image.shape
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                fin=''
                if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y:
                    val1 = 0
                else:
                    val1 = 1
                    fin ='Index '
                if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y:
                    val2 = 0
                else:
                    val2 = 1
                    fin += 'Middle '
                if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y:
                    val3 = 0
                else:
                    val3 = 1
                    fin += 'Ring '
                if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y:
                    val4 = 0
                else:
                    val4 = 1
                    fin += 'PINKY '
                #Return the total amount of fingers detected
                val=val1 +val2+val3+val4
                #Get the value obtained from the slider
                r = cv2.getTrackbarPos('MOTOR:', 'PiARM Control')
                #Combine the finger value and slider value
                tempVal=str(r) + str(val)
                # Send the combined value to Raspberry Pi
                client.send(tempVal.encode())
                # Display the finger detected on the window
                fps= str(val)+' fingers'
                cv2.putText(image, (fps), (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
                cv2.putText(image, (fin), (0, 60), cv2.FONT_HERSHEY_PLAIN, 2, (10, 10, 0), 2)
        # Display the Window
        cv2.imshow('PiARM Control', image)
        #Hit Esc for closing the program
        if cv2.waitKey(5) & 0xFF == 27:
            break
# Close the program and connection
cap.release()
