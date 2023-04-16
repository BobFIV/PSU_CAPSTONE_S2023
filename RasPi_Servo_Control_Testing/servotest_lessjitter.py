import RPi.GPIO as GPIO
import pigpio
import time

servo1 = 18
servo2 = 19
config_array = []
current_door = []
config_filename = "servoconfig.txt"

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servo1, GPIO.OUT)
# GPIO.setup(servo2, GPIO.OUT)

pwm = pigpio.pi()
pwm.set_mode(servo1, pigpio.OUTPUT)
pwm.set_mode(servo2, pigpio.OUTPUT)

pwm.set_PWM_frequency(servo1, 50)
pwm.set_PWM_frequency(servo2, 50)

try:
    while True:
        with open(config_filename) as config_file:
            config_array = config_file.readlines()
            
        for line in config_array:
            current_door = line.split(":")
            # print(current_door)
            
            if current_door[0].strip() == "Door1" and current_door[1].strip() == "closed":
                pwm.set_servo_pulsewidth(servo1, 500)    
                pwm.set_servo_pulsewidth(servo2, 1500)    
            elif current_door[0].strip() == "Door1" and current_door[1].strip() == "open":
                pwm.set_servo_pulsewidth(servo1, 1500)    
                pwm.set_servo_pulsewidth(servo2, 500)    
        
        time.sleep(1)
        
except KeyboardInterrupt:
    print("Program stopped")
    
    pwm.set_PWM_dutycycle(servo1, 0)
    pwm.set_PWM_dutycycle(servo2, 0)
    pwm.set_PWM_frequency(servo1, 0)
    pwm.set_PWM_frequency(servo2, 0)
    # GPIO.cleanup()
