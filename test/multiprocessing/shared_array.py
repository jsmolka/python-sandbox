import multiprocessing as mp
import time


# Source
# https://stackoverflow.com/a/9743806


class Shared2DArray:
	"""Shared array class."""
	def __init__(self, rows, cols, initial=0):
		"""Constructor."""
		self.__array = mp.Array("i", rows * cols * [initial])
		self.rows = rows
		self.cols = cols

	def __getitem__(self, key):
		"""Numpy-like getter"""
		r, c = key
		if 0 <= r < self.rows and 0 <= c < self.cols:
			return self.__array[r * self.cols + c]
		else:
			raise IndexError("Index out of range")

	def __setitem__(self, key, value):
		"""Numpy-like setter."""
		r, c = key
		if 0 <= r < self.rows and 0 <= c < self.cols:
			self.__array[r * self.cols + c] = value
		else:
			raise IndexError("Index out of range")


def increment(arr):
	"""Increment."""
	while True:
		time.sleep(1)
		for i in range(arr.rows):
			for j in range(arr.cols):
				arr[i, j] += 1
				print(arr[0, 0])


if __name__ == "__main__":
	array = Shared2DArray(3, 3)

	process = mp.Process(target=increment, args=(array,))
	process.start()

	while array[0, 0] != 5:
		pass

	process.terminate()
