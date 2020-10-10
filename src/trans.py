import numpy as np

class Points():
	
	def __init__(self, EPS):
		self.EPS = EPS

	def th_atanh(self, x):
		#values = np.min(x, [1.0 - EPS])
		return 0.5 * (np.log(1 + x) - np.log(1 - x))

	def lambda_x(self, x):
		return 2. / (1 - np.dot(x, x.T))
	
	def mobius_add(self, y, x):
		''' Performs x + y. Performed for each vector y in self array. Returns an array of vectors.'''
		scalar_prod = np.dot(x, y.T).ravel()
		print(scalar_prod)
		norm_self = np.dot(y, y.T) 
		norm_x = np.dot(x, x.T)
		print(norm_self, norm_x)
		return (np.outer(1+2*scalar_prod+norm_self, x.ravel()) + (1 - norm_x**2)*y) / ((1 + 2*scalar_prod + norm_x**2 + norm_self**2).reshape(-1,1))
	

	def log_map(self, x, y):
		if x.shape[1] != y.shape[1]:
			raise Exception("Dimensions of inputs not matching: %d and %d"%(x.shape[1], self.__values.shape[1]))
		if x.shape[0] != 1:
			raise Exception("Input should be a single vector")
		
		diff = self.mobius_add(-x, y) 
		norm_diff = np.dot(diff, diff.T)
		lam = self.lambda_x(x)
		return (( 2. / lam) * self.th_atanh(norm_diff) / norm_diff) * diff
	

	def exp_map(self, x, v):
		if x.shape[1] != y.shape[1]:
			raise Exception("Dimensions of inputs not matching: %d and %d"%(x.shape[1], self.__values.shape[1]))
		if x.shape[0] != 1:
			raise Exception("Input should be a single vector")
		
		norm_v = np.dot(v, v.T)
		second_term = (np.tanh(self.lambda_x(x) * norm_v / 2) / norm_v) * v
		return (self.mobius_add(x, second_term))


	def geodesic(self, y, x):
		norm_x = np.linalg.norm(x, axis=1)
		norm_y = np.linalg.norm(y, axis=1)
		return np.arccosh( 1+2*(np.linalg.norm(y - x, axis =1)) / ((1-norm_x**2)*(1-norm_y**2))) 

if __name__ == "__main__":
	a = Points(0.03)
	x = np.array([[0.02, 0.04, 0.01]])
	y = np.array([[-0.04, -0.03, -0.02]])
	log_x = a.log_map(x, y)
	print(log_x)
	print(a.exp_map(x, log_x))
	#print(geodesic())	

