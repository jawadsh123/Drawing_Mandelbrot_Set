import numpy as np
import tensorflow as tf
import cv2


X, Y = 0,0
Z = 0

# Starting the sesssion right from the start
sess = tf.InteractiveSession()


def Claculate_Colors(a):
	"""Display an array of iteration counts as a
	colorful picture of a fractal."""
	a_cyclic = (6.28*a/20.0).reshape(list(a.shape)+[1])
	img = np.concatenate([10+20*np.cos(a_cyclic),
		30+50*np.sin(a_cyclic),
		155-80*np.cos(a_cyclic)], 2)
	img[a==a.max()] = 0
	a = img
	a = np.uint8(np.clip(a, 0, 255))

	return a/255.0



def Plot_Set(image):
	
	global start_x, start_y, end_x, end_y, draw_started, clone
	clone = image.copy()
	start_x, start_y = 0, 0
	end_x, end_y = 0, 0
	draw_started = False

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


		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break


Create_Iteration_Matrix(min_x=-2.5, max_x=1, min_y=1.3, max_y=1):

	x_diff = max_x - min_x
	step = x_diff/700

	Y, X = np.mgrid[min_y:max_y:step, min_x:max_x:step]
	Z = X+1j*Y

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

update_zs = zs.assign(zs_new)
update_count = ns.assign_add(tf.cast(not_diverged, tf.float32))



def main():
	for _ in range(200):
		update_zs.eval()
		update_count.eval()

	a = Claculate_Colors(ns.eval())

	Plot_Set(a)

main()
cv2.destroyAllWindows()