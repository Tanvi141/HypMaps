import numpy as np

class Points():

	def __init__(self, coordinates):
		self.__curv = -1
		self.__values = np.copy(coordinates) #a 2d array (dxN)
		self.ref_vec = None #a column vector

	def norm(self):
		return np.linalg.norm(self.__values, axis = 1)
	
	def transform(self, x):
		lambda_x = 2/(1 - x.norm())
		print(lambda_x.shape)
		self.ref_vec = np.copy(x)

if __name__ == "__main__":
	t1 = np.array([[-4, -3, -2],[-1,  0,  1],[ 2,  3,  4]])
	a = Points(t1)
	t2 = np.array([[-4, -3, -2]])
	b = Points(t2)
	a.transform(b)
