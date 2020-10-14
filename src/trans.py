import numpy as np

class Points():
	
	def __init__(self, EPS):
		self.EPS = EPS
		print(self.EPS)

	def th_atanh(self, x):
		#values = np.min(x, [1.0 - EPS])
		return 0.5 * (np.log(1 + x) - np.log(1 - x))

	def lambda_x(self, x):
		return 2. / (1 - np.einsum("ij,ij->i", x, x))
	
	def dot(self, u, v):
		return np.einsum("ij,ij->i", u, v) 

	def mobius_add(self, u, v):
		v = v + self.EPS
		dot_u_v = 2. * self.dot(u, v)
		norm_u_sq = self.dot(u, u)
		norm_v_sq = self.dot(v, v)
		denominator = 1. + dot_u_v + norm_v_sq * norm_u_sq
		return ((1. + dot_u_v + norm_v_sq) / (denominator + self.EPS))[:, np.newaxis] * u +  ((1. - norm_u_sq) / (denominator + self.EPS))[:, np.newaxis] * v
		#return (1. + dot_u_v + norm_v_sq) / (denominator + self.EPS) * u +  (1. - norm_u_sq) / (denominator + self.EPS) * v
	

	def log_map(self, x, y):
		if x.shape[1] != y.shape[1]:
			raise Exception("Dimensions of inputs not matching: %d and %d"%(x.shape[1], self.__values.shape[1]))
		if x.shape[0] != 1:
			raise Exception("Input should be a single vector")
		
		diff = self.mobius_add(-x, y) + self.EPS 
		norm_diff = self.dot(diff, diff)
		lam = self.lambda_x(x)
		return (( 2. / lam) * self.th_atanh(norm_diff) / norm_diff)[:, np.newaxis] * diff
	

	def exp_map(self, x, v):
		if x.shape[1] != y.shape[1]:
			raise Exception("Dimensions of inputs not matching: %d and %d"%(x.shape[1], self.__values.shape[1]))
		if x.shape[0] != 1:
			raise Exception("Input should be a single vector")
		
		v = v + self.EPS
		norm_v = self.dot(v, v)
		second_term = (np.tanh(self.lambda_x(x) * norm_v / 2) / norm_v) [:, np.newaxis] * v
		return (self.mobius_add(x, second_term))


	def geodesic(self, y, x):
		norm_x_sq = self.dot(x, x)
		norm_y_sq = self.dot(y, y)
		print( 1+2*(self.dot(y - x, (y-x))) / ((1-norm_x_sq)*(1-norm_y_sq))) 
		return np.arccosh( 1+2*(self.dot(y - x, (y-x))) / ((1-norm_x_sq)*(1-norm_y_sq))) 

if __name__ == "__main__":
	a = Points(0)
	y = np.array([[0.02, 0.04, 0.01]])
	x = np.array([[-0.04, -0.03, -0.02]])
	print("x and y", x, y)
	#print("mob_add", a.mobius_add(y, x))
	log_x = a.log_map(x, y)
	print("log map", log_x)
	print("exp map", a.exp_map(x, log_x))
	print("\n\non array")	
	y2 = np.array([[-0.032, -0.04, 0.05], [0.02, 0.04, 0.01]])
	#print("mob_add", a.mobius_add(y2, x))
	log_x = a.log_map(x, y2)
	print("log map", log_x)
	print("exp map", a.exp_map(x, log_x))
	x = np.array([[0.10757873243866733,0.6093478669582405]])
	y = np.array([[0.46352923985723493,0.10584204760372007]])
	print(a.geodesic(x, y), 1.6061649971520338)
	y2 = np.array([[0.46352923985723493,0.10584204760372007], [0.29977866446656565,0.05307632917590743], [0.029805528569373907,0.6437093307617852]])
	print(a.geodesic(x, y2), 1.444218397542425,0.2821437387738971)
