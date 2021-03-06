import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import colors
# from numba import jlt
import cv2
import numpy as np

MAX_ITERATIONS = 200
HEIGHT = 600
WIDTH = int(HEIGHT * 1.5)

def map(number, l_ini, r_ini, l_final, r_final):
	fraction = (number - l_ini) / (r_ini - l_ini)
	value = fraction * (r_final - l_final) + l_final
	return value

# @jlt
def plot_Mandelbrot_Set(image, min_x, max_x, min_y, max_y):
	for i in range(WIDTH):
		x = map(i, 0, WIDTH, min_x, max_x)
		for j in range(HEIGHT):
			z = 0 + 0j
			y = map(j, 0, HEIGHT, min_y, max_y)
			c = complex(x, y)
			curr_iteration = 0

			while abs(z) < 2 and curr_iteration < MAX_ITERATIONS:
				z = z*z + c
				curr_iteration += 1

			# if curr_iteration == MAX_ITERATIONS:
			# 	image[j][i] = 0
			# else:
			# 	image[j][i] = 255
			image[j][i] = curr_iteration

		if i % 100 == 0:
			print("Calculating Column {}".format(i))	
	return image


def plot_set(image, cmap='jet', gamma=0.3):
	norm = colors.PowerNorm(gamma)
	plt.imshow(image, cmap=cmap, norm=norm)
	plt.show()



mandelbrotSet = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
mandelbrotSet = plot_Mandelbrot_Set(mandelbrotSet, -2.5, 1, -1, 1)

plot_set(mandelbrotSet,cmap='hot')

# cv2.imshow("set", np.array(mandelbrotSet)/255.0)
# plt.imshow(mandelbrotSet)
# plt.show()

