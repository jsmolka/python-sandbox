from multiprocessing import Process, Queue, Value
# from threading import Thread
from time import sleep
		
# Shared arrays and lists
# https://stackoverflow.com/a/9754423
		
		
def increment(counter):
	while True:
		sleep(1)
		counter.value += 1
		print(counter.value)
		

if __name__ == "__main__":  # Necessary for multiprocessing
	integer = Value("i", 0)
			
	process = Process(target=increment, args=(integer,))
	# thread = Thread(target=increment, args=(integer,))
	# thread.daemon = True  # Script exists properly even if the thread is still running
	process.start()
	# thread.start()

	while integer.value != 5:
		pass

	process.terminate()