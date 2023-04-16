from gpiozero import Servo
from time import sleep

servo1 = Servo(18)
servo2 = Servo(19)
config_array = []
current_door = []
config_filename = "servoconfig.txt"

try:
    while True:
        with open(config_filename) as config_file:
            config_array = config_file.readlines()
            
        for line in config_array:
            current_door = line.split(":")
            # print(current_door)
            
            if current_door[0].strip() == "Door1" and current_door[1].strip() == "closed":
                servo1.value = -1
                servo2.value = 1
            elif current_door[0].strip() == "Door1" and current_door[1].strip() == "open":
                servo1.value = 1
                servo2.value = -1
        
        sleep(1)
        
except KeyboardInterrupt:
    print("Program stopped")
