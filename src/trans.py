import numpy as np

class Points():

	def __init__(self, coordinates):
		self.__curv = -1
		self.__values = np.copy(coordinates) #a 2d array (dxN)
		self.ref_vec = None #a column vector
		if np.all(self.norm() < 1) == False:
			raise Exception("Vectors should have norm 1")

	def norm(self):
		return np.linalg.norm(self.__values, axis = 1)
	
	def log_map(self, x):

		if x.get_shape()[1] != self.__values.shape[1]:
			raise Exception("Dimensions of inputs not matching: %d and %d"%(x.shape[1], self.__values.shape[1]))
		if x.get_shape()[0] != 1:
			raise Exception("Input should be a single vector")
		
		if self.__curv != -1:
			raise Exception("Vectors already in euclidean space") 	

		lambda_x = 2/(1 - x.norm())
		mob_sum = self.mobius_add(x)
		mob_norm = np.linalg.norm(mob_sum, axis=1)
		print(np.arctanh(mob_norm))
		print((np.arctanh(mob_norm) / mob_norm))
		print((1-x.norm()**2) * (np.arctanh(mob_norm) / mob_norm))
		print(mob_sum)
		print(((1-x.norm()**2) * (np.arctanh(mob_norm) / mob_norm))*mob_sum)
		
		self.ref_vec = np.copy(x)
		self.__curv = 0

	def get_values(self):
		return np.copy(self.__values)

	def get_shape(self):
		return self.__values.shape

	def mobius_add(self, x):
		''' Performs x + y. Performed for each vector y in self array. Returns an array of vectors.'''
		scalar_prod = np.dot(x.get_values(), self.__values.transpose()).ravel()
		norm_self = self.norm()
		norm_x = x.norm()

		return (np.outer(1+2*scalar_prod+norm_self, x.get_values().ravel()) + (1 - norm_x**2)*self.__values) / ((1 + 2*scalar_prod + norm_x**2 + norm_self**2).reshape(-1,1))
		
if __name__ == "__main__":
	t1 = np.array([[-0.04, -0.03, -0.02],[-0.01,  0.00,  0.01],[ 0.02,  0.03,  0.04],[0.02, 0.04, 0.01]])
	a = Points(t1)
	t2 = np.array([[-0.04, -0.03, -0.02]])
	b = Points(t2)
	a.log_map(b)
