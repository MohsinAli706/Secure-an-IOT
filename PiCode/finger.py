import random

class FingerprintEmulator:
    def __init__(self):
        self._finger_id = None
        self._confidence = None
        self._image_taken = True
        self._template_created = True

    def get_image(self) -> int:
        # Simulate taking an image, return random result (OK or an error)
        self._image_taken = random.choice([0, 1]) == 0  # 50% chance of success
        return 0 if self._image_taken else random.choice([1, 2, 3])  # Simulated error code

    def image_2_tz(self, slot: int = 1) -> int:
        # Simulate converting an image to a template
        if self._image_taken:
            # Conversion successful
            self._template_created = True
            return 0
        else:
            # No image taken, return an error
            return 3  # Simulated "IMAGEFAIL" error

    def create_model(self) -> int:
        # Simulate creating a model from the template
        if self._template_created:
            return 0
        else:
            # Template not created, return an error
            return 7  # Simulated "FEATUREFAIL" error

    def store_model(self, location: int, slot: int = 1) -> int:
        # Simulate storing the model in flash memory
        if self._template_created:
            return 0
        else:
            # Template not created, return an error
            return 7  # Simulated "FEATUREFAIL" error

    def finger_search(self) -> tuple[int, int]:
        # Simulate searching for a fingerprint match
        if self._template_created:
            # Return random finger ID and confidence level
            self._finger_id = 1
            self._confidence = 100
        else:
            # No template created, return error values
            self._finger_id = None
            self._confidence = None

        return self._finger_id, self._confidence

""" def user_selectable_conditions():
    emulator = FingerprintEmulator()

    # Let the user select emulator conditions
    image_success = input("Enter '0' to simulate successful image capture, '1' for failure: ")
    if image_success == "0":
        emulator._image_taken = True
    else:
        emulator._image_taken = False

    template_success = input("Enter '0' to simulate successful template conversion, '3' for failure: ")
    if template_success == "0":
        emulator._template_created = True
    else:
        emulator._template_created = False

    return emulator

def get_fingerprint():
    print("Waiting for image...")
    
    # Simulate capturing an image
    while True:
        image_prompt = input("Enter 0 for a successful image capture, 1 for an error: ")
        if image_prompt == "0":
            image_result = 0
            print("Image taken")
            break
        elif image_prompt == "1":
            image_result = random.choice([1, 2, 3])
            print(f"Image capture failed with error code {image_result}")
            return False

    # Simulate converting the image to a template
    print("Templating...")
    while True:
        template_prompt = input("Enter 0 for a successful template conversion, 3 for an error: ")
        if template_prompt == "0":
            template_result = 0
            print("Templated")
            break
        elif template_prompt == "3":
            template_result = 3
            print(f"Image to template conversion failed with error code {template_result}")
            return False


    print("Searching...")
    
    # Simulate searching for a fingerprint match
    search_result = emulator.finger_search()
    if search_result[0] == 0:
        print(f"Fingerprint search successful with finger ID {search_result[0]} and confidence level {search_result[1]}")
    else:
        print(f"Fingerprint search failed with error code {search_result[0]}")
        return False


    return True

def enroll_finger(location):
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="")
        else:
            print("Place same finger again...", end="")
        
        # Simulate capturing an image
        image_success = False
        while not image_success:
            image_prompt = input("Enter 0 for a successful image capture, 2 for waiting, 3 for an error: ")
            if image_prompt == "0":
                image_result = 0
                print("Image taken")
                image_success = True
            elif image_prompt == "2":
                image_result = 2
                print(".", end="")  # Simulate waiting for finger placement
            elif image_prompt == "3":
                image_result = 3
                print("Imaging error")
                return False

        print("Templating...", end="")

        # Simulate converting the image to a template
        template_success = False
        while not template_success:
            template_prompt = input("Enter 0 for a successful template conversion, 6 for a messy image, 7 for feature fail, 15 for an invalid image: ")
            if template_prompt == "0":
                template_result = 0
                print("Templated")
                template_success = True
            elif template_prompt == "6":
                template_result = 6
                print("Image too messy")
            elif template_prompt == "7":
                template_result = 7
                print("Could not identify features")
            elif template_prompt == "15":
                template_result = 15
                print("Image invalid")
            else:
                print("Invalid input")

        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while True:
                image_prompt = input("Enter 2 for waiting, or 0 to continue: ")
                if image_prompt == "2":
                    pass  # Simulate waiting for finger removal
                elif image_prompt == "0":
                    break


    print("Creating model...", end="")
    
    # Simulate creating a model
    while True:
        model_prompt = input("Enter 0 for a successful model creation, 10 for prints not matching: ")
        if model_prompt == "0":
            model_result = 0
            print("Created")
            break
        elif model_prompt == "10":
            model_result = 10
            print("Prints did not match")
        else:
            print("Invalid input")

    print(f"Storing model #{location}...", end="")
    
    # Simulate storing the model
    while True:
        storage_prompt = input("Enter 0 for successful storage, 11 for bad location, 24 for flash storage error: ")
        if storage_prompt == "0":
            storage_result = 0
            print("Stored")
            break
        elif storage_prompt == "11":
            storage_result = 11
            print("Bad storage location")
        elif storage_prompt == "24":
            storage_result = 24
            print("Flash storage error")
        else:
            print("Invalid input")

    return True """