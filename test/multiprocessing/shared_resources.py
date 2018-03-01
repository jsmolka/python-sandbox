from multiprocessing import Process, Queue, Value
from time import sleep
		
# Shared arrays and lists
# https://stackoverflow.com/a/9754423
		
		
def increment(counter):
	"""Increments."""
	while True:
		sleep(1)
		counter.value += 1
		print(counter.value)
		

if __name__ == "__main__":  # Necessary for multiprocessing
	integer = Value("i", 0)
			
	process = Process(target=increment, args=(integer,))
	process.start()

	while integer.value != 5:
		pass

	process.terminate()