'''
    Autonomous Robot which runs on a square loop with IR sensors and displays using attached camera.
                                         Designed by Nischal Khanal
'''
#Import time.sleep to delay the motors
from time import sleep
#import the DC Motor Module from the MotorModule Library
from MotorModule import DCMotor
#import keyboard module from the pynput library
from pynput import keyboard
#Import thread module from the threading library
import threading
from threading import Thread
#Import Event module from the threading Library Module
from threading import Event
#Import class TrackSensor from InfraredSensor Module
from InfraredSensor import TrackSensor
#Import CV2 for camera operations
import cv2 as cv
# Import Tkinter library to implement GUI
from tkinter import *  
# Class of Autonomous Vehicle
class AutoVehicle:
    #Constructor Vehicle
    def __init__(self,title):
        self.__Title = title
        self.__trackLeftSensor = 0 #Attribute to create Left TrackSensor Object
        self.__trackRightSensor = 0 #Atrribute to create Right TrackSensor Object
        self.__driveForward = 0 #Thread Attribute to create a thread to drive forward
        # Sets the MotorFL to 1 as ID and Front Left as location (from MotorModule)
        self.__MotorFL = DCMotor(1,'Front Left')
        # Sets the MotorFR to 2 as ID and Front Right as location (from MotorModule)
        self.__MotorFR = DCMotor(2,'Front Right')
        # Sets the MotorRL to 3 as ID and Rear Left as location (from MotorModule)
        self.__MotorRL = DCMotor(3,'Rear Left')
        # Sets the MotorRR to 4 as ID and Rear Right as location (from MotorModule)
        self.__MotorRR = DCMotor(4,'Rear Right')
        #Left IR Sensor
        self.__trackLeftSensor = TrackSensor(17)
        #Right IR Sensr
        self.__trackRightSensor = TrackSensor(27)
        #Instantiate thread object
        self.__driveForward = Thread(target = self.OnDrive)
        #Sets to True when the drive thread is started
        self.__FORWARD = False 
    
            
    #Method to drive the vehicle in Forward Direction at set Speed
    def OnDrive(self):
        print('Driving Forward')
        #Set the rotation of the motor
        self.__VehicleSpeed  = -0.60
        self.__MotorFL.rotation = False
        self.__MotorFR.rotation = False
        self.__MotorRL.rotation = False
        self.__MotorRR.rotation = False
        #Set the speed of the motor
        self.__MotorFL.Speed = self.__VehicleSpeed
        self.__MotorFR.Speed = self.__VehicleSpeed
        self.__MotorRL.Speed = self.__VehicleSpeed
        self.__MotorRR.Speed = self.__VehicleSpeed
        while self.__FORWARD:
            # Detect the IR sensor behavior
            flag1 = self.__trackLeftSensor.Detect()
            flag2 = self.__trackRightSensor.Detect()
            # If the left IR sensor detects the tape
            if (flag1 == True and flag2 == False):
                #steers to the right if two flags are true and false
                self.SteerRight()
                #recursively calling the self.OnDrive() function in order to continue moving forward direction
                self.OnDrive()
            # If the right IR sensor detects the tape
            if (flag1 == False and flag2 == True):
                #steers to the left if two flags are false and true
                self.SteerLeft()
                #recursively calling the self.OnDrive() function in order to continue moving forward direction
                self.OnDrive()
            sleep(0.1)
    #Method to Steer Right
    def SteerRight(self):
        #Write code to steer the platform right
            print('Turning Right')
            self.__VehicleSpeed  = -0.85
            self.__MotorFL.rotation = False
            self.__MotorFR.rotation = True
            self.__MotorRL.rotation = False
            self.__MotorRR.rotation = True
            self.__MotorFL.Speed = -self.__VehicleSpeed
            self.__MotorFR.Speed = self.__VehicleSpeed
            self.__MotorRL.Speed = -self.__VehicleSpeed
            self.__MotorRR.Speed = self.__VehicleSpeed
            sleep(0.1)
            
    #Method to Steer Left
    def SteerLeft(self):
        #Write code to steer the platform left
            print('Turning Left')
            self.__VehicleSpeed  = -0.85
            self.__MotorFL.rotation = True
            self.__MotorFR.rotation = False
            self.__MotorRL.rotation = True
            self.__MotorRR.rotation = False
            self.__MotorFL.Speed = self.__VehicleSpeed
            self.__MotorFR.Speed = -self.__VehicleSpeed
            self.__MotorRL.Speed = self.__VehicleSpeed
            self.__MotorRR.Speed = -self.__VehicleSpeed
            sleep(0.1)
            
    #Method to stop the vehicle   
    def StopVehicle(self):
        if self.__FORWARD:
            #Set the flag to False
            self.__FORWARD = not self.__FORWARD
            #Join the event thread
            self.__driveForward.join()
        #Stop the platform
        self.__MotorFL.Stop()
        self.__MotorFR.Stop()
        self.__MotorRL.Stop()
        self.__MotorRR.Stop()
    #Method to create the Drive Forward Thread object with the DriveForward Method
    def DriveForward(self):
        #Set the Attribute self.__FORWARD to True
        self.__FORWARD = True
        #Start the thread using the attribute self.__driveForward
        self.__driveForward.start() 

    #A Method to respond to the keyboard event
    def Control(self,key):
        if key.char == 'd' or key.char == 'D': #Key d or D
            #Method to drive forward
            self.DriveForward()
        if key.char == 's' or key.char == 'S': #Key s or S
            if self.__FORWARD:
                #Method to Stop the vehicle
                self.StopVehicle()
                print('Autonomous Vehicle - Turned Off')
                return False
            else:
                print('Autonomous Vehicle - Not Started')
                return False
# Class to set Camera using Computer Vision
class CVOperations:
    def __init__(self,):
        self.loop = False
        self.CameraInit = False
        self.WindowName = 'Robot'
    # Create a tkinter app
    def app(self):
        self.root = Tk()
        self.root.title("Computer Vision Operations")
        self.SetupGUI()
        self.root.mainloop()
    # Initialize the camera
    def InitCamera(self):
        self.cameraCapture = cv.VideoCapture(0)
        while(self.cameraCapture.isOpened() == False):
            self.cameraCapture = cv.VideoCapture(0)
        self.CameraInit = True
        self.btnInitCamera.config(state = 'disabled')
        self.btnStartVideo.config(state = 'normal')
        cv.startWindowThread()
    # Display the video
    def DisplayVideo(self):
        success,self.frame = self.cameraCapture.read()
        while success and self.CaptureVideo:
            cv.imshow(self.WindowName,self.frame)
            success,self.frame = self.cameraCapture.read()
    # Start the video in thread
    def OnStartVideo(self):
        cv.startWindowThread()
        self.btnTrackCar.config(state = 'normal')
        cv.namedWindow(self.WindowName)
        self.CaptureVideo = True
        self.threadVideo = threading.Thread(None,self.DisplayVideo,None,(),{})
        self.threadVideo.start()
    # Start the tracking operations
    def OnTrackCar(self):
        robot = AutoVehicle('robot')
        print('Press d to Drive and s to Stop')
        listener = keyboard.Listener(on_press = robot.Control)
        listener.start()
        listener.join()
    # Exit the program
    def OnExit(self):
        self.CaptureVideo = False
        sleep(1)
        if self.CameraInit:
            self.cameraCapture.release()
        cv.destroyAllWindows()
        self.root.destroy()
    # Setup the GUI using Tkinter
    def SetupGUI(self):
        bF=LabelFrame(self.root,text="Menu",width=90,height=90)
        bF.grid(column=0,row=0,stick=W)         
        self.btnInitCamera = Button(bF, text='Initialize Camera',command=self.InitCamera)
        self.btnInitCamera.grid(column=0,row=0,sticky=W)    
        self.btnInitCamera.config(font = 'Helvetica 24 bold italic')
        self.btnStartVideo = Button(bF, text="Start Video",
                command=self.OnStartVideo)
        self.btnStartVideo.grid(column=1,row=0,sticky=W)
        self.btnStartVideo.config(state = 'disabled')
        self.btnStartVideo.config(font = 'Helvetica 24 bold')
        self.btnTrackCar = Button(bF, text="Drive Car",
        command=self.OnTrackCar)
        self.btnTrackCar.grid(column=0,row=1,sticky=W)
        self.btnTrackCar.config(state = 'disabled')
        self.btnTrackCar.config(font = 'Helvetica 24 bold')
        
        
        self.btnExit = Button(bF, text="Exit",
                command=self.OnExit)
        self.btnExit.grid(column=1,row=1,sticky=(W))
        self.btnExit.config(font = 'Helvetica 24 bold')
# Main function
if __name__ == '__main__':
    #Instantiate a Vehicle Object
    robot = AutoVehicle('robot') 
    try:
        # Instantiate a CV2 GUI Object
        cvo = CVOperations()
        cvo.app()
    except KeyboardInterrupt:
        robot.StopVehicle()
        OnExit()

