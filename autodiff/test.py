
from reverse_autodiff import *


if __name__ == '__main__':
	#
	x1 = ADVar(10)
	x2 = ADVar(15)
	z1 = x1 * x1
	z2 = x2 * x2
	y = x2*z1 + z2
	print DerProp.top is y.data.left
	
	# CalcGrad()
	
	y.propagate()
	
	print y.val
	print y.adj
	print z1.adj
	print z2.adj
	print x1.adj
	print x2.adj

