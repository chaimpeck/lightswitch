import time
import RPi.GPIO as GPIO


from config import (
	GPIO_NUMBER_MODE,
	SENSOR_INPUT_PIN,
	SERVO_OUTPUT_PIN,
)

def setup():
	# Set GPIO number mode
	GPIO.setmode(GPIO_NUMBER_MODE)

	# Set pin 11 as the sensor input
	GPIO.setup(SENSOR_INPUT_PIN, GPIO.IN)

	# Set pin 13 as output
	GPIO.setup(SERVO_OUTPUT_PIN, GPIO.OUT)

def get_servo_pwm(freq=50):
	return GPIO.PWM(SERVO_OUTPUT_PIN, freq)

def get_sensor_input():
	return GPIO.input(SENSOR_INPUT_PIN)

class Servo:
	def __init__(self, pwm_freq=50):
		self.pwm_freq = pwm_freq

	def move(self, angle):
		servo_pwm = get_servo_pwm(self.pwm_freq)
		duty = angle / 18 + 2
		print(duty)
		servo_pwm.start(duty)
		# servo_pwm.ChangeDutyCycle(duty)
		time.sleep(.3)
		servo_pwm.stop()

	def reset_position(self):
		self.move(90)

	def turn_on(self):
		self.move(25)
		self.reset_position()

	def turn_off(self):
		self.move(155)
		self.reset_position()



def main():
	print("Starting lightswitch controller")

	# Call the setup function, to initialize the GPIO pins
	setup()

	# Create a new instance of the Servo object
	servo = Servo()

	# Start by reseting the position
	servo.reset_position()

	# Testing the servo motor on the light switch
	# servo.turn_on()
	# servo.turn_off()
	# servo.turn_on()

	print("Initialized lightswitch controller")

	# Start a loop that will continously check the input from the sensor
	while True:
		# As long as the sensor is false, stay in this loop
		while get_sensor_input() == False:
			time.sleep(.1)

		print("Sensed motion! Going dark")
		servo.turn_off()

		# Now, wait for motion to end before going back to top of loop
		while get_sensor_input() == True:
			time.sleep(.1)

		print("Sensing is over")

	print("Cleaning up")
	GPIO.cleanup()
	print("Exiting")


if __name__ == '__main__':
	main()
