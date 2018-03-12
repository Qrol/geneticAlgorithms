import numpy as np
#import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random
import time
import os

width = 10
height = 10

def searchedLine(x):
	return -3*x + 3

def f(a, x, b):
	return a * x + b


class Point:
	def __init__(self):
		self.coords = [random() * width - width/2, random() * height - height/2, 1]

		self.label = 1 if self.coords[1] >= searchedLine(self.coords[0]) else -1

class NeuralNetwork:
	def __init__(self, inp_number, learning_rate = 0.01):
		self.num = inp_number
		self.lrt = learning_rate
		self.weights = [random()*2 - 1 for i in range(inp_number + 1)]

	def guess(self, point):
		sum = 0
		for i in range(len(self.weights)):
			sum += self.weights[i] * point.coords[i]

		if sum >= 0:
			return 1
		else:
			return -1

	def calcError(self, point):
		return point.label - self.guess(point)

	def train(self, point):
		for i in range(len(self.weights)):
			self.weights[i] += self.lrt * self.calcError(point) * point.coords[i]

	def checkAll(self, points):
		for i in range(len(points)):
			if not self.guess(points[i]) == points[i].label:
				return False
		return True




#===ANIMATION SECTION ================
fig = plt.figure()
ax = plt.axes(xlim=(-width/2, width/2), ylim=(-height/2, height/2))
lines = [plt.plot([],[],"b-")[0], plt.plot([],[], color='black', linestyle='--')[0]]
scatters = [plt.scatter([],[], c='red'), plt.scatter([],[], c='green'), plt.scatter([],[], c='blue')]
plt.title("y=")
XAxis = np.array([0, width]) - width/2
allPos = False
index = 0
#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)


def init():
    for line in lines:
        line.set_data([], [])
    return lines

def count():
	return 0
def animate(i):
	global points, network, lines, XAxis, searchedLine, pointsXs, pointsYs, index, allPos


	x = XAxis
	y = f(-network.weights[0]/network.weights[1], XAxis, -network.weights[2]/network.weights[1])
	lines[0].set_data(x, y)
	lines[1].set_data(XAxis, searchedLine(XAxis))

	#plt.figtext(0.025, 0.95, "text test")

	#points
	green = [[],[]]
	red = [[],[]]

	if allPos:
		print "y = {0:.2f}x + {1:.2f}".format(-network.weights[0]/network.weights[1], -network.weights[2]/network.weights[1])
		plt.pause(2000)
		#os.system("pause")
		#os.system("exit")
	allPos = True

	for j in range(len(points)):
		if points[index].label == network.guess(points[index]):
			index = (index + 1) % len(points)
		else:
			break
	for e, el in enumerate(points):
		if e == index:
			scatters[2].set_offsets(np.c_[[el.coords[0]], [el.coords[1]]])
		elif el.label == network.guess(el):
			green[0].append(el.coords[0])
			green[1].append(el.coords[1])
		else:
			allPos = False
			red[0].append(el.coords[0])
			red[1].append(el.coords[1])
	scatters[0].set_offsets(np.c_[red[0], red[1]])
	scatters[1].set_offsets(np.c_[green[0], green[1]])
	plt.title("y = {0:.2f}x + {1:.2f}".format(-network.weights[0]/network.weights[1], -network.weights[2]/network.weights[1]))

	network.train(points[index])
	index = (index + 1) % len(points)
	return lines
#=====================================
points = []
#Creating training points
for i in range(1000):
	points.append(Point())
#Some points used in training
pointsXs = [points[i].coords[0] for i in range(min(len(points), 200))]
pointsYs = [points[i].coords[1] for i in range(min(len(points), 200))]
network = NeuralNetwork(2, 0.1)


'''
print "Points coordinates: "
for pt in points:
	print "({0[0]:.2f}, {0[1]:.2f})".format(pt.coords)
'''
'''
rep = 0
# and rep <10000

try:
	while(not network.checkAll(points)):
		for pt in points:
			network.train(pt)
		rep+=1
except KeyboardInterrupt:
	print "Interrupted with keyboard. The line is: "
finally:
	print "y = {0:.2f}x + {1:.2f}".format(-network.weights[0]/network.weights[1], -network.weights[2]/network.weights[1])
'''
#for i in range(len(pointsXs)):
#	print pointsXs[i], pointsYs[i]


#plt.scatter(pointsYs, pointsXs)
#plt.axis([-width/2, width/2, -height/2, height/2])




ani = animation.FuncAnimation(fig, animate, init_func=init, interval=500)
#ani.save("animationPerceptron.html")
plt.show()
#raw_input()
