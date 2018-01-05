from multiprocessing import Process, Queue, Array
from time import sleep
		
# Source
# https://stackoverflow.com/a/9743806
		
		
class Shared2DArray:
	def __init__(self, rows, cols, initial=0):
		self.__array = Array("i", rows * cols * [initial])
		self.rows = rows
		self.cols = cols
		
	def __getitem__(self, key):
		r, c = key
		if 0 <= r < self.rows and 0 <= c < self.cols:
			return self.__array[r * self.cols + c]
		else:
			raise IndexError("Index out of range")

	def __setitem__(self, key, value):
		r, c = key
		if 0 <= r < self.rows and 0 <= c < self.cols:
			self.__array[r * self.cols + c] = value
		else:
			raise IndexError("Index out of range")
	
		
		
def increment(arr):
	while True:
		sleep(1)
		for i in range(0, arr.rows):
			for j in range(0, arr.cols):
				arr[i, j] += 1
		print(arr[0, 0])
		

if __name__ == "__main__":  # Necessary for multiprocessing
	array = Shared2DArray(3, 3)
			
	process = Process(target=increment, args=(array,))
	process.start()
	
	while array[0, 0] != 5:
		pass

	process.terminate()