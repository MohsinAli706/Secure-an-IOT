# Description: Simulates the API running on the Raspberry Pi
from flask import Flask, request, jsonify
import threading
import time
import random
import queue

from finger import FingerprintEmulator

app = Flask(__name__)

#############################################
# Global variables

# Global data_queue variable
data_queue = queue.Queue()
# stores json msg, format: {"message": "msg", "status_code": 0, "id": 0}
# status_code: 0 for normal, 1 for error, 2 for stop execution

# Global emulator variable
emulator = FingerprintEmulator()

#############################################
# Helper functions

# Enroll a finger emulated
def enroll_finger(location):
    global data_queue
    location = 1
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            msg = {"message": "Place finger on sensor...", "status_code": 0, "id": 0}
            data_queue.put(msg)
        else:
            msg = {"message": "Place same finger again...", "status_code": 0, "id": 0}
            data_queue.put(msg)
        
        # Simulate capturing an image
        image_success = False
        while not image_success:
            image_prompt = "0" #input("Enter 0 for a successful image capture, 2 for waiting, 3 for an error: ")
            if image_prompt == "0":
                msg = {"message": "Image Taken.", "status_code": 0, "id": 0}
                data_queue.put(msg)
                image_success = True
            elif image_prompt == "2":
                msg = {"message": "Waiting For Finger.", "status_code": 0, "id": 0}
                data_queue.put(msg)
            elif image_prompt == "3":
                msg = {"message": "Imaging Error.", "status_code": 1, "id": 0}
                data_queue.put(msg)
                return False

        msg = {"message": "Templating", "status_code": 0, "id": 0}
        data_queue.put(msg)

        # Simulate converting the image to a template
        template_success = False
        while not template_success:
            template_prompt = "0" #input("Enter 0 for a successful template conversion, 6 for a messy image, 7 for feature fail, 15 for an invalid image: ")
            if template_prompt == "0":
                msg = {"message": "Templated.", "status_code": 0, "id": 0}
                data_queue.put(msg)
                template_success = True
            elif template_prompt == "6":
                msg = {"message": "Image Too Messy.", "status_code": 1, "id": 0}
                data_queue.put(msg)
            elif template_prompt == "7":
                msg = {"message": "Could Not Identify Features.", "status_code": 1, "id": 0}
                data_queue.put(msg)
            elif template_prompt == "15":
                msg = {"message": "Image Invalid.", "status_code": 1, "id": 0}
                data_queue.put(msg)
            else:
                msg = {"message": "Invalid Input.", "status_code": 1, "id": 0}
                data_queue.put( "Invalid input")

        if fingerimg == 1:
            msg = {"message": "Remove Finger.", "status_code": 0, "id": 0}
            data_queue.put(msg)
            while True:
                image_prompt = "0" #input("Enter 2 for waiting, or 0 to continue: ")
                if image_prompt == "2":
                    pass  # Simulate waiting for finger removal)
                elif image_prompt == "0":
                    break

    msg = {"message": "Creating Model.", "status_code": 0, "id": 0}
    data_queue.put(msg)
    
    # Simulate creating a model
    while True:
        model_prompt = "0" #input("Enter 0 for a successful model creation, 10 for prints not matching: ")
        if model_prompt == "0":
            msg = {"message": "Model Created.", "status_code": 0, "id": 0}
            data_queue.put(msg)
            break
        elif model_prompt == "10":
            msg = {"message": "Prints Did Not Match.", "status_code": 1, "id": 0}
            data_queue.put(msg)
        else:
            msg = {"message": "Invalid Input.", "status_code": 1, "id": 0}
            data_queue.put(msg)

    msg = {"message": f"Storing model #{location}", "status_code": 0, "id": location}
    data_queue.put(msg)
    
    # Simulate storing the model
    while True:
        storage_prompt = "0" #input("Enter 0 for successful storage, 11 for bad location, 24 for flash storage error: ")
        if storage_prompt == "0":
            msg = {"message": "Model Stored.", "status_code": 0, "id": 0}
            data_queue.put(msg)
            break
        elif storage_prompt == "11":
            msg = {"message": "Bad Storage Location.", "status_code": 1, "id": 0}
            data_queue.put(msg)
        elif storage_prompt == "24":
            msg = {"message": "Flash Storage Error.", "status_code": 1, "id": 0}
            data_queue.put(msg)
        else:
            msg = {"message": "Invalid Input.", "status_code": 1, "id": 0}
            data_queue.put(msg)

    msg = {"message": "Enrollment Complete.", "status_code": 0, "id": 0}
    data_queue.put(msg)

    msg = {"message": "Function Executed.", "status_code": 2, "id": 0}
    data_queue.put(msg)

#find a finger emulated
def get_fingerprint():
    global emulator
    global data_queue
    
    msg = {"message": "Waiting For Image.", "status_code": 0, "id": 0}
    data_queue.put(msg)
    
    # Simulate capturing an image
    while True:
        image_prompt = "0" #input("Enter 0 for a successful image capture, 1 for an error: ")
        if image_prompt == "0":
            image_result = 0
            msg = {"message": "Image Taken.", "status_code": 0, "id": 0}
            data_queue.put(msg)
            break
        elif image_prompt == "1":
            image_result = random.choice([1, 2, 3])
            msg = {"message": f"Image capture failed with error code {image_result}", "status_code": 1, "id": 0}
            data_queue.put()
            return False

    # Simulate converting the image to a template
    msg = {"message": "Templating.", "status_code": 0, "id": 0}
    data_queue.put(msg)
    while True:
        template_prompt = "0" #input("Enter 0 for a successful template conversion, 3 for an error: ")
        if template_prompt == "0":
            template_result = 0
            msg = {"message": "Templated.", "status_code": 0, "id": 0}
            data_queue.put(msg)
            break
        elif template_prompt == "3":
            template_result = 3
            msg = {"message": f"Image to template conversion failed with error code {template_result}", "status_code": 1, "id": 0}
            data_queue.put(msg)
            return False

    msg = {"message": "Searching.", "status_code": 0, "id": 0}
    data_queue.put(msg)
    
    # Simulate searching for a fingerprint match
    search_result = emulator.finger_search()
    if search_result[0] == 1:
        msg = {"message": f"Fingerprint search successful with finger ID {search_result[0]}", "status_code": 0, "id": search_result[0]}
        data_queue.put(msg)
    else:
        msg = {"message": f"Fingerprint search failed with error code {search_result[0]}", "status_code": 1, "id": search_result[0]}
        data_queue.put(msg)
        return False

    msg = {"message": "Fingerprint Found", "status_code": 0, "id": 0}
    data_queue.put(msg)

    msg = {"message": "Function Executed.", "status_code": 2, "id": search_result[0]}
    data_queue.put(msg)

# Function to update the data_queue based on if-else statements
""" def update_data_queue():
    global data_queue
    if some_condition:
        data_queue.put( "Condition 1 is met."
    elif some_other_condition:
        data_queue.put( "Condition 2 is met."
    else:
        data_queue.put( "No condition is met."
    time.sleep(5)  # Adjust the sleep interval as needed
    thread = threading.current_thread()
    thread._stop()  # Stop the thread when the function is done """


#############################################
# API endpoints

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
    # Generate random sensor data
    sensor_data = {
        'temperature': random.randint(25, 40),
        'humidity': random.randint(0, 100),
    }
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(debug=True)
