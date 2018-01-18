import threading
from time import sleep

# Source
# https://stackoverflow.com/a/3393759


def output():
	t = threading.Timer(1.0, output)
	t.daemon = True
	t.start()
	print("output")
	sleep(5)  # Timer calls the function ever n seconds, even if it's not finished yet

def control():
	t = threading.Timer(1.0, control)
	t.daemon = True
	t.start()
	print("control")

	
output()
control()

while True:
	pass  # Necessary because daemons end with main loop
