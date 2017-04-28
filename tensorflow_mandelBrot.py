import numpy as np
import tensorflow as tf
import cv2


X, Y = 0,0
Z = 0

# Starting the sesssion right from the start
sess = tf.InteractiveSession()


def Calculate_Colors(a):
	"""Display an array of iteration counts as a
	colorful picture of a fractal."""
	a_cyclic = (6.28*a/20.0).reshape(list(a.shape)+[1])
	# img = np.concatenate([155-80*np.cos(a_cyclic),
	# 					30+50*np.sin(a_cyclic),
	# 					10+20*np.cos(a_cyclic)], 2)

	# print((10+20*np.cos(a_cyclic)).shape)
	img = np.concatenate([10+20*np.cos(a_cyclic),
						30+50*np.sin(a_cyclic),
						155-80*np.cos(a_cyclic)], 2)
	img[a==a.max()] = 0
	a = img
	a = np.uint8(np.clip(a, 0, 255))

	return a/255.0

def Calculate_New_Colors(a):

	mapping = [() for _ in range(16)]
	mapping[0] = (66, 30, 15)
	mapping[1] = (25, 7, 26)
	mapping[2] = (9, 1, 47)
	mapping[3] = (4, 4, 73)
	mapping[4] = (0, 7, 100)
	mapping[5] = (12, 44, 138)
	mapping[6] = (24, 82, 177)
	mapping[7] = (57, 125, 209)
	mapping[8] = (134, 181, 229)
	mapping[9] = (211, 236, 248)
	mapping[10] = (241, 233, 191)
	mapping[11] = (248, 201, 95)
	mapping[12] = (255, 170, 0)
	mapping[13] = (204, 128, 0)
	mapping[14] = (153, 87, 0)
	mapping[15] = (106, 52, 3)

	a_reshaped = a.reshape(list(a.shape)+[1])

	blue_matrix = np.array([[mapping[int(ele)%16][2] for ele in row] for row in a_reshaped])
	blue_matrix = blue_matrix.reshape(list(blue_matrix.shape)+[1])

	green_matrix = np.array([[mapping[int(ele)%16][1] for ele in row] for row in a_reshaped])
	green_matrix = green_matrix.reshape(list(green_matrix.shape)+[1])

	red_matrix = np.array([[mapping[int(ele)%16][0] for ele in row] for row in a_reshaped])
	red_matrix = red_matrix.reshape(list(red_matrix.shape)+[1])

	img = np.concatenate([ blue_matrix,
							green_matrix,
							red_matrix], 2)
	
	img[a==a.max()] = 0

	return img/255.0



def Plot_Set(image):
	
	global start_x, start_y, end_x, end_y, draw_started, clone
	clone = image.copy()
	height, width, channels = image.shape
	# height, width = image.shape
	start_x, start_y = 0, 0
	end_x, end_y = width, height
	draw_started = False

	# print(image[0].shape)

	def On_Mouse(event, x, y, flags, params):
		global start_x, start_y, end_x, end_y, draw_started, clone

		if event == cv2.EVENT_LBUTTONDOWN:
			print('Start Mouse Position: '+str(x)+', '+str(y))
			start_x = x
			start_y = y
			draw_started = True
		if draw_started == True:
			clone = image.copy()
			cv2.rectangle(clone, (start_x, start_y), (x, y), (255,255,255), 2)
			cv2.imshow("set", clone)
		if event == cv2.EVENT_LBUTTONUP:
	 		print('End Mouse Position: '+str(x)+', '+str(y))
	 		end_x = x
	 		end_y = y
	 		cv2.rectangle(clone, (start_x, start_y), (end_x, end_y), (255,255,255), 2)
	 		cv2.imshow("set", clone)
	 		draw_started = False


	cv2.namedWindow("set")
	cv2.setMouseCallback("set", On_Mouse)

	while True:
		cv2.imshow("set", clone)

		
		k = cv2.waitKey(1)

		if k & 0xFF == ord(' '):
			return (start_x, end_x, start_y, end_y, width, height)

		if k & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			return False


def Create_Iteration_Matrix(min_x=-2.5, max_x=1, min_y=-1.3, max_y=1.3):

	x_diff = max_x - min_x
	step = x_diff/700
	# print(step, max_x, min_x)

	Y, X = np.mgrid[min_y: max_y: step,  min_x: max_x: step]
	Z = X+1j*Y

	# Y, X = np.mgrid[0: 1,  0: 1]
	# Z = X+1j*Y

	# creating the matrices required
	cs = tf.constant(Z.astype(np.complex64))
	zs = tf.Variable(cs)
	ns = tf.Variable(tf.zeros_like(cs, tf.float32))

	# initializing tensorflow variables
	tf.global_variables_initializer().run()

	# mandelbrot function
	zs_new = zs*zs + cs

	# boolean matrix for checking if it has diverged
	not_diverged = tf.abs(zs_new) < 4

	# diverged = tf.abs(zs_new) >= 4
	# flag = tf.abs(zs_new) >= 4

	# escape_z = tf.mul(tf.abs(zs_new), tf.mul(tf.cast(diverged, tf.float32), tf.cast(flag, tf.float32)))

	update_zs = zs.assign(zs_new)
	update_count = ns.assign_add(tf.cast(not_diverged, tf.float32))

	for _ in range(200):
		update_zs.eval()
		update_count.eval()

	return ns.eval()

def calculate_Set_Coordinates(temp, dim, max_val, min_val):
	return  min_val + (temp/dim) * (max_val - min_val)


def main():

	min_x, max_x, min_y, max_y = -2.5, 1, -1.3, 1.3

	while True:
		print("Creating Plot")
		ns = Create_Iteration_Matrix(min_x, max_x, min_y, max_y)
		a = Calculate_Colors(ns)
		# a = Calculate_New_Colors(ns)
		returned_packet = Plot_Set(a)


		if not returned_packet:
			break
		else:
			temp_min_x, temp_max_x, temp_min_y, temp_max_y, width, height = returned_packet
			new_min_x = calculate_Set_Coordinates(temp_min_x, width, max_x, min_x)
			new_max_x = calculate_Set_Coordinates(temp_max_x, width, max_x, min_x)
			new_min_y = calculate_Set_Coordinates(temp_min_y, height, max_y, min_y)
			new_max_y = calculate_Set_Coordinates(temp_max_y, height, max_y, min_y)
			min_x, max_x, min_y, max_y = new_min_x, new_max_x, new_min_y, new_max_y


main()
cv2.destroyAllWindows()