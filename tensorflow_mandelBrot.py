import numpy as np
import tensorflow as tf
import cv2


def DisplayFractal(a):
	"""Display an array of iteration counts as a
	 colorful picture of a fractal."""
	a_cyclic = (6.28*a/20.0).reshape(list(a.shape)+[1])
	img = np.concatenate([10+20*np.cos(a_cyclic),
	                    30+50*np.sin(a_cyclic),
	                    155-80*np.cos(a_cyclic)], 2)
	img[a==a.max()] = 0
	a = img
	a = np.uint8(np.clip(a, 0, 255))
	cv2.imshow("set", a/255.0)
	cv2.waitKey(0)





# Starting the sesssion right from the start
sess = tf.InteractiveSession()


# defining the grid for operations
Y, X = np.mgrid[-1.3:1.3:0.005, -2.5:1:0.005]
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


for _ in range(200):
	update_zs.eval()
	update_count.eval()

DisplayFractal(ns.eval())


