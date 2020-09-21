import numpy as np

class Points():

	def __init__(self, coordinates):
		self.__curv = -1
		self.__values = np.copy(coordinates) #a 2d array (dxN)
		self.__ref_vec = None #a column vector
		if np.all(self.norm() < 1) == False:
			raise Exception("Vectors should have norm 1")

	def get_values(self):
		return np.copy(self.__values)

	def get_shape(self):
		return self.__values.shape
	
	def norm(self):
		return np.linalg.norm(self.__values, axis = 1)
	
	def mobius_add(self, x):
		''' Performs x + y. Performed for each vector y in self array. Returns an array of vectors.'''
		scalar_prod = np.dot(x.get_values(), self.__values.transpose()).ravel()
		norm_self = self.norm()
		norm_x = x.norm()
#		print(np.outer(1+2*scalar_prod+norm_self, x.get_values().ravel()) + (1 - norm_x**2)*self.__values)
#		print((1 + 2*scalar_prod + norm_x**2 + norm_self**2).reshape(-1,1))
#		ret =  (np.outer(1+2*scalar_prod+norm_self, x.get_values().ravel()) + (1 - norm_x**2)*self.__values) / ((1 + 2*scalar_prod + norm_x**2 + norm_self**2).reshape(-1,1))
#		print(ret)
		return (np.outer(1+2*scalar_prod+norm_self, x.get_values().ravel()) + (1 - norm_x**2)*self.__values) / ((1 + 2*scalar_prod + norm_x**2 + norm_self**2).reshape(-1,1))
		#query: <x,y> means scalar prod
	

	def log_map(self, x):
		if x.get_shape()[1] != self.__values.shape[1]:
			raise Exception("Dimensions of inputs not matching: %d and %d"%(x.shape[1], self.__values.shape[1]))
		if x.get_shape()[0] != 1:
			raise Exception("Input should be a single vector")
		
		if self.__curv != -1:
			raise Exception("Vectors already in euclidean space") 	
	
		self.__ref_vec = Points(x.get_values())
		self.__curv = 0

		mob_sum = self.mobius_add(x)
		mob_norm = np.linalg.norm(mob_sum, axis=1)
		self.__values = mob_sum * ((1-x.norm()**2) * (np.arctanh(mob_norm) / mob_norm))[:, np.newaxis]
	
	def exp_map(self):
	#query: not taking x as input, instead using the vec stored in private vars
		if self.__curv != 0:
			raise Exception("Vectors already in hyp space") 	
	
		#self.__ref_vec.log_map(self.__ref_vec)
		x= self.__ref_vec
#		print(np.tanh(self.norm()/(1-x.norm()**2)))
#		print(self.__values/self.norm()[:, np.newaxis])
#		print((self.__values/self.norm()[:, np.newaxis])*(np.tanh(self.norm()/(1-x.norm()**2)))[:, np.newaxis])
		temp_arr = Points((self.__values/self.norm()[:, np.newaxis])*(np.tanh(self.norm()/(1-x.norm()**2)))[:, np.newaxis])
		self.__values = temp_arr.mobius_add(x)	
		
		self.__ref__vec = None
		self.__curv = 0


	def geodesic(self, x):
		print(self.__values)
		print(x.get_values())
		if self.__curv == 0:
			return np.linalg.norm(self.__values - x.get_values(), axis=1)
		
		elif self.__curv == -1:
			print(np.linalg.norm(self.__values - x.get_values(), axis =1))
			print((1-x.norm()**2)*(1-self.norm()**2))
			print( np.arccosh( 1+2*(np.linalg.norm(self.__values - x.get_values(), axis =1)) / ((1-x.norm()**2)*(1-self.norm()**2))) )
if __name__ == "__main__":
	t1 = np.array([[-0.04, -0.03, -0.02],[-0.01,  0.00,  0.01],[ 0.02,  0.03,  0.04],[0.02, 0.04, 0.01]])
	a = Points(t1)
	t2 = np.array([[-0.04, -0.03, -0.02]])
	b = Points(t2)
	print(a.geodesic(b))
	a.log_map(b)
	print(a.get_values())
	a.exp_map()
	print(a.get_values())

