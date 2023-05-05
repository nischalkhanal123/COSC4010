'''
                Simple IoT device to increase/ decrease the brightness of the connected blue LED from a client
                                                     Designed by Nischal Khanal
                Note: Be sure to run this program on Raspberry Pi through sudo privileges
'''

# Import Flask, render_template,request and Response modules
from flask import Flask, render_template,request, Response
# Import PWMLED to control the brightness
from gpiozero import PWMLED
# Import CV2 for camera operations
import cv2
# Import atexit to safely close camera operations each time the page is reloaded
import atexit
#Instantiate a Flask object
app = Flask(__name__)
# Instantiate a PWMLED object connected to GPIO 21 and having 5000 frequency
led = PWMLED(21, frequency = 5000)
# FUnction to display the Blue LED from Camera
def gen_frames():
    # Capture the video in real-time
    cap = cv2.VideoCapture(0)
    # Infinte loop
    while True:
        #Read each frames from the camera
        success, frame = cap.read()
        #If the camera is not detected, break from the loop
        if not success:
            break
        else:
            # Return the frames as .jpg to send to HTML
            ret, buffer = cv2.imencode('.jpg', frame)
            # conver the jpg to bytes
            frame = buffer.tobytes()
            # Send the byte values to the HTML caller
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    #Release the camera after breaking loop
    cap.release()
# Function to release the camera everytime during webpage reload
def cleanup():
    cap.release()

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/set_brightness', methods=['POST'])
def slider():
    brightness = float(request.form['brightness'])
    print('Brightness:', brightness)
    led.value = int(brightness)/100
    return 'Got it'

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
atexit.register(cleanup)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
