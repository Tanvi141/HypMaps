import numpy as np

class Points():

	def mobius_add(y, x):
		''' Performs x + y. Performed for each vector y in self array. Returns an array of vectors.'''
		scalar_prod = np.dot(x, y.T).ravel()
		norm_self = np.linalg.norm(y, axis=1)
		norm_x = np.linalg.norm(x, axis=1)
#		print(np.outer(1+2*scalar_prod+norm_self, x.get_values().ravel()) + (1 - norm_x**2)*self.__values)
#		print((1 + 2*scalar_prod + norm_x**2 + norm_self**2).reshape(-1,1))
#		ret =  (np.outer(1+2*scalar_prod+norm_self, x.get_values().ravel()) + (1 - norm_x**2)*self.__values) / ((1 + 2*scalar_prod + norm_x**2 + norm_self**2).reshape(-1,1))
#		print(ret)
		return (np.outer(1+2*scalar_prod+norm_self, x.ravel()) + (1 - norm_x**2)*y) / ((1 + 2*scalar_prod + norm_x**2 + norm_self**2).reshape(-1,1))
	

	def log_map(y, x):
		if x.shape[1] != y.shape[1]:
			raise Exception("Dimensions of inputs not matching: %d and %d"%(x.shape[1], self.__values.shape[1]))
		if x.shape[0] != 1:
			raise Exception("Input should be a single vector")
		
		norm_x = np.linalg.norm(x, axis=1)
		mob_sum = mobius_add(y, x)
		mob_norm = np.linalg.norm(mob_sum, axis=1)
		return mob_sum * ((1-norm_x**2) * (np.arctanh(mob_norm) / mob_norm))[:, np.newaxis]
	

	def exp_map(y, x):
		if x.shape[1] != y.shape[1]:
			raise Exception("Dimensions of inputs not matching: %d and %d"%(x.shape[1], self.__values.shape[1]))
		if x.shape[0] != 1:
			raise Exception("Input should be a single vector")
		
		norm_y = np.linalg.norm(y, axis=1)
		temp_arr = (y/norm_y[:, np.newaxis])*(np.tanh(norm_y()/(1-norm_x()**2)))[:, np.newaxis]
		return mobius_add(temp_arr, x)	
		

	def geodesic(y, x):
		norm_x = np.linalg.norm(x, axis=1)
		norm_y = np.linalg.norm(y, axis=1)
		return np.arccosh( 1+2*(np.linalg.norm(y - x, axis =1)) / ((1-norm_x**2)*(1-norm_y**2))) 

if __name__ == "__main__":
	t1 = np.array([[-0.04, -0.03, -0.02],[-0.01,  0.00,  0.01],[ 0.02,  0.03,  0.04],[0.02, 0.04, 0.01]])
	a = Points(t1)
	t2 = np.array([[-0.04, -0.03, -0.02]])
	b = Points(t2)
	print(t1, t2)
	#print(a.geodesic(b))
	a.log_map(b)
	print(a.get_values())
	a.exp_map()
	print(a.get_values())

