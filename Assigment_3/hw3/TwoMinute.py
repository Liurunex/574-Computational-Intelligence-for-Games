import pickle
import numpy as np
import scipy.optimize
import sys

sys.path.append('c/cs474/hw3/plays.py')
import plays

def main(argv):
	if len(argv) != 5 and len(argv) != 6:
		print("Invalid Input")
		return
	try:
		payoff = False
		i  = 0
		if len(argv) == 6 and argv[1] == "-matrix":
			i = 1
			payoff = True
		remdown   = 4-int(argv[i+1])
		firstdown = int(argv[i+2])
		touchdown = int(argv[i+3])
		time      = int(argv[i+4])/5
	except:
		print("Invalid Input")
		return

	# pickle.load(open("/c/cs474/hw3/two_minute.pickle", "rb"))
	p = pickle.load(open("/c/cs474/hw3/two_minute.pickle", "rb"))
	rows = 3
	cols = 3

	a1 = np.zeros((rows, cols))
	for i in range(rows):
		for j in range(cols):
			for k in range (5):
				val    = 0.0
				curp   = plays.plays[i][j][k]
				nrtime = time - int(curp[1])
				nrdown =  remdown
				
				if curp[2] == False:
					rmtouch = touchdown - int(curp[0])
					rmfirst = firstdown - int(curp[0])

					if rmtouch >= 100 or rmtouch > 0 and nrtime <= 0:
						val = 0.0
					elif rmtouch <= 0:
						val = float(plays.prob[k])
					else:
						if rmfirst <= 0:
							nrdown = 4
							if rmtouch < 10:
								rmfirst = rmtouch
							else:
								rmfirst = 10
						val = float(p[rmtouch, nrdown, rmfirst, nrtime]) * float(plays.prob[k])
				a1[i][j] += val

	if payoff == True:
		for i in range(rows):
			print("[%6f, %6f, %6f]" % (a1[i][0], a1[i][1], a1[i][2]))
		return

	upper_bound = float('inf')
	minval = np.amin(a1)
	if minval != 0:
		upper_bound = 1/minval
	bounds = (0.0, upper_bound)
	b_ub   = [-1.0] * cols
	c      = [1.0] * rows

	a1 = a1*-1
	a1 = a1.T
	result = scipy.optimize.linprog(c, a1.tolist(), b_ub, None, None, bounds)

	value = 1.0 / result.fun
	x = [xi * value for xi in result.x]

	# now solve for P2's strategy
	a1   = a1*-1
	a2   = a1.T
	b_ub = [1.0] * rows
	c    = [-1.0] * cols

	at = a2.tolist()
	result = scipy.optimize.linprog(c, a2.tolist(), b_ub, None, None, bounds)

	y = [yi * value for yi in result.x]

	print("[%6f, %6f, %6f]" % (x[0], x[1], x[2]))
	print("[%6f, %6f, %6f]" % (y[0], y[1], y[2]))
	print("%6f" % value)

if __name__ == "__main__":
    main(sys.argv)
