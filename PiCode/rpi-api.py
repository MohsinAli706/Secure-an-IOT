# Description: Data API running on the Raspberry Pi
from flask import Flask, request, jsonify
import threading
import time
import random
import queue

import adafruit_fingerprint
import adafruit_dht
import pulseio
import serial
import board

app = Flask(__name__)
data_queue = queue.Queue()

# Fingerprint Functions
##################################################
# import board
# uart = busio.UART(board.TX, board.RX, baudrate=57600)

# If using with a computer such as Linux/RaspberryPi, Mac, Windows with USB/serial converter:
#uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

#If using with Linux/Raspberry Pi and hardware UART:
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi 3 with pi3-disable-bt
# uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def get_fingerprint():

    if finger.read_templates() != adafruit_fingerprint.OK:
        msg = {"message": "Failed to read templates", "status_code": 1, "id": 0}
        data_queue.put(msg)

    if finger.count_templates() != adafruit_fingerprint.OK:
        msg = {"message": "Failed to read templates", "status_code": 1, "id": 0}
        data_queue.put(msg)

    if finger.read_sysparam() != adafruit_fingerprint.OK:
        msg = {"message": "Failed to get system parameters", "status_code": 1, "id": 0}
        data_queue.put(msg)
    
    """Get a finger print image, template it, and see if it matches!"""
    
    msg = {"message": "Place Finger On Sensor.", "status_code": 0, "id": 0}
    data_queue.put(msg)

    msg = {"message": "", "status_code": 0, "id": 0}
    while finger.get_image() != adafruit_fingerprint.OK:
        pass

    msg = {"message": "Finger Detected! Remove Finger.", "status_code": 0, "id": 0}
    data_queue.put(msg)

    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        msg = {"message": "Imaging Error.", "status_code": 1, "id": 0}
        data_queue.put(msg)
        return False

    msg = {"message": "Searching...", "status_code": 0, "id": 0}
    data_queue.put(msg)

    if finger.finger_search() != adafruit_fingerprint.OK:
        msg = {"message": "Finger Not Found.", "status_code": 1, "id": 0}
        data_queue.put(msg)
        return False
    
    msg = {"message": "Finger Found!", "status_code": 2, "id": finger.finger_id}
    data_queue.put(msg)
    return True

def enroll_finger(location):
    
    if finger.read_templates() != adafruit_fingerprint.OK:
        msg = {"message": "Failed to read templates", "status_code": 1, "id": 0}
        data_queue.put(msg)

    if finger.count_templates() != adafruit_fingerprint.OK:
        msg = {"message": "Failed to read templates", "status_code": 1, "id": 0}
        data_queue.put(msg)

    if finger.read_sysparam() != adafruit_fingerprint.OK:
        msg = {"message": "Failed to get system parameters", "status_code": 1, "id": 0}
        data_queue.put(msg)
    
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            msg = {"message": "Place finger on sensor...", "status_code": 0, "id": 0}
            data_queue.put(msg)
        else:
            msg = {"message": "Place same finger again...", "status_code": 0, "id": 0}
            data_queue.put(msg)

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                msg = {"message": "Image Taken.", "status_code": 0, "id": 0}
                data_queue.put(msg)
                break
            if i == adafruit_fingerprint.NOFINGER:
                msg = {"message": "Waiting For Finger.", "status_code": 0, "id": 0}
                data_queue.put(msg)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                msg = {"message": "Imaging Error.", "status_code": 1, "id": 0}
                data_queue.put(msg)
                return False
            else:
                msg = {"message": "Other Error.", "status_code": 1, "id": 0}
                data_queue.put(msg)
                return False

        msg = {"message": "Templating", "status_code": 0, "id": 0}
        data_queue.put(msg)

        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            msg = {"message": "Templated.", "status_code": 0, "id": 0}
            data_queue.put(msg)

        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                msg = {"message": "Image Too Messy.", "status_code": 1, "id": 0}
                data_queue.put(msg)
            elif i == adafruit_fingerprint.FEATUREFAIL:
                msg = {"message": "Could Not Identify Features.", "status_code": 1, "id": 0}
                data_queue.put(msg)
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                msg = {"message": "Image Invalid.", "status_code": 1, "id": 0}
                data_queue.put(msg)

            else:
                msg = {"message": "Other Error.", "status_code": 1, "id": 0}
                data_queue.put(msg)
            
            return False

        if fingerimg == 1:
            msg = {"message": "Remove Finger.", "status_code": 0, "id": 0}
            data_queue.put(msg)

            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    msg = {"message": "Creating Model...", "status_code": 0, "id": 0}
    data_queue.put(msg)

    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        msg = {"message": "Created.", "status_code": 0, "id": 0}
        data_queue.put(msg)

    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            msg = {"message": "Prints Did Not Match.", "status_code": 1, "id": 0}
            data_queue.put(msg)

        else:
            msg = {"message": "Other Error.", "status_code": 1, "id": 0}
            data_queue.put(msg)

        return False

    msg = {"message": "Storing Model...", "status_code": 0, "id": 0}
    data_queue.put(msg)

    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        msg = {"message": "Stored.", "status_code": 0, "id": 0}
        data_queue.put(msg)

    else:
        if i == adafruit_fingerprint.BADLOCATION:
            msg = {"message": "Bad Storage Location.", "status_code": 1, "id": 0}
            data_queue.put(msg)

        elif i == adafruit_fingerprint.FLASHERR:
            msg = {"message": "Flash Storage Error.", "status_code": 1, "id": 0}
            data_queue.put(msg)

        else:
            msg = {"message": "Other Error.", "status_code": 1, "id": 0}
            data_queue.put(msg)

        return False

    return True

##################################################

global data

# Sensor Functions
##################################################
def dhtData():
    # Initial the dht device, with data pin connected to:
    dhtDevice = adafruit_dht.DHT22(board.D4)

    while True:
        try:
            data = {
                'temperature': dhtDevice.temperature,
                'humidity': dhtDevice.humidity,
            }
            return data
            
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        
        except Exception as error:
            dhtDevice.exit()
            raise error
        
def buzzer(data):
    OFF = 0
    ON = 2**15
    
    # Initialize the PWM buzzer
    buzzer = pulseio.PWMOut(board.D18, variable_frequency=True)

    # Set the initial frequency to 440 Hz
    buzzer.frequency = 440

    # Set the initial duty cycle to 0 (off)
    buzzer.duty_cycle = OFF

    # If the temperature is above 40 degrees or if the humidity is above 70, turn on the buzzer 5 times
    if data['temperature'] > 40 or data['humidity'] > 70:
        for i in range(5):
            buzzer.duty_cycle = ON
            time.sleep(0.5)
            buzzer.duty_cycle = OFF
            time.sleep(0.5)

    buzzer.duty_cycle = OFF


##################################################

# Flask Initialization
##################################################
app = Flask(__name__)

# Global data_queue variable
data_queue = queue.Queue()
# stores json msg, format: {"message": "msg", "status_code": 0, "id": 0}
# status_code: 0 for normal, 1 for error, 2 for stop execution

#############################################

# API endpoints
##################################################

@app.route('/enrollFinger', methods=['POST'])
def start_enroll_finger():
    fingerid = request.form.get('signupUserID')  # Get the 'fingerid' value from the POST request

    if not fingerid:
        return f"Missing {fingerid} parameter in the request.", 400

    # Start a new thread for enrolling a finger with the received 'fingerid'
    global enroll_thread

    enroll_thread = threading.Thread(target=enroll_finger, args=(fingerid,))
    enroll_thread.daemon = True
    enroll_thread.start()

    return jsonify({'message' : "Enroll Function Started."})

# Find a finger
@app.route('/getFingerprint', methods=['POST'])
def start_get_fingerprint():
    # Start a new thread for getting a fingerprint
    global find_thread

    if 'find_thread' in globals() and find_thread.is_alive():
        return jsonify({'message': "Find Function Is Already Running."})
    find_thread = threading.Thread(target=get_fingerprint)
    find_thread.daemon = True
    find_thread.start()
    
    return jsonify({'message' : "Find Function Started."})

# Get the current message
@app.route('/get-message', methods=['GET'])
def get_message():
    if not data_queue.empty():  # Check if the queue is not empty
        data = data_queue.get()
        return jsonify(data)
    
    # If the queue is empty, return the "Previous." message with status code 0 and id 0
    return jsonify({"message": "Previous.", "status_code": 0, "id": 0})
    

# Get sensor data
@app.route('/sensor-data', methods=['GET'])
def get_sensor_data():    
    sensor_data = dhtData()
    buzzer(sensor_data)

    return jsonify(sensor_data)

#############################################

# Main
##################################################
if __name__ == '__main__':
    app.run(debug=True)
