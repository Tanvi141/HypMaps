import numpy as np

class Transform():
	
	def __init__(self, EPS):
		self.EPS = EPS

	def th_atanh(self, x):
		#values = np.min(x, [1.0 - EPS])
		return 0.5 * (np.log(1 + x) - np.log(1 - x))

	def lambda_x(self, x):
		return 2. / (1 - np.einsum("ij,ij->i", x, x))
	
	def dot(self, u, v):
		return np.einsum("ij,ij->i", u, v) 
	
	def check_norm(self, u, v):
		if np.argwhere(self.dot(u, u) >= 1):
			raise Exception("Invalid input, norm should be < 1")
		if np.argwhere( self.dot(v, v) >= 1):
			raise Exception("Invalid input, norm should be < 1")
	
	def mobius_add(self, u, v):
		v = v + self.EPS
		dot_u_v = 2. * self.dot(u, v)
		norm_u_sq = self.dot(u, u)
		norm_v_sq = self.dot(v, v)
		denominator = 1. + dot_u_v + norm_v_sq * norm_u_sq
		return ((1. + dot_u_v + norm_v_sq) / (denominator + self.EPS))[:, np.newaxis] * u +  ((1. - norm_u_sq) / (denominator + self.EPS))[:, np.newaxis] * v
	

	def log_map(self, x, y):
		if x.shape[1] != y.shape[1]:
			raise Exception("Dimensions of inputs not matching: %d and %d"%(x.shape[1], self.__values.shape[1]))
		if x.shape[0] != 1:
			raise Exception("Input should be a single vector")
		self.check_norm(x, y)

		diff = self.mobius_add(-x, y) + self.EPS 
		norm_diff = self.dot(diff, diff)
		lam = self.lambda_x(x)
		return (( 2. / lam) * self.th_atanh(norm_diff) / norm_diff)[:, np.newaxis] * diff
	

	def exp_map(self, x, v):
		if x.shape[1] != v.shape[1]:
			raise Exception("Dimensions of inputs not matching: %d and %d"%(x.shape[1], self.__values.shape[1]))
		if x.shape[0] != 1:
			raise Exception("Input should be a single vector")
		
		v = v + self.EPS
		norm_v = self.dot(v, v)
		second_term = (np.tanh(self.lambda_x(x) * norm_v / 2) / norm_v) [:, np.newaxis] * v
		return (self.mobius_add(x, second_term))


	def geodesic(self, y, x):
		self.check_norm(x, y)

		norm_x_sq = self.dot(x, x)
		norm_y_sq = self.dot(y, y)
		return np.arccosh( 1+2*(self.dot(y - x, (y-x))) / ((1-norm_x_sq)*(1-norm_y_sq))) 
