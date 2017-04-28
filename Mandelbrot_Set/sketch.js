
function plot_Mandelbrot_Set(){

	for (var i = 0; i < width; i++) {
		for (var j = 0; j < height; j++) {
			x = map(i, 0, width, -2.5, 1);
			y = map(j, 0, height, -1, 1);
			c = math.complex(x, y);
			z = math.complex(0, 0);

			max_iterations = 1000;
			curr_iterations = 0;


			while (z.re*z.re + z.im*z.im < 2*2 && curr_iterations < max_iterations) {
				z = math.add(math.multiply(z, z), c);
				curr_iterations += 1;
			}


			colorMode(HSL, 360, 100, 100, 1);
			c = map(curr_iterations, 0, 1000, 45, 0);
			new_color = color(234, 100, c);
			stroke(new_color);
			point(i, j);
		}
	}
}

function plot_Mandelbrot_point(curr_x, curr_y) {
	x = map(this.curr_x, 0, width, -2.5, 1);
	y = map(this.curr_y, 0, height, -1, 1);
	c = math.complex(x, y);
	z = math.complex(0, 0);

	max_iterations = 100;
	curr_iterations = 0;


	while (z.re*z.re + z.im*z.im < 2*2 && curr_iterations < max_iterations) {
		z = math.add(math.multiply(z, z), c);
		curr_iterations += 1;
	}

	colorMode(HSL, 360, 100, 100, 1);
	c = map(curr_iterations, 0, 1000, 0, 50);
	new_color = color(234, 100, c);
	stroke(new_color);
	point(this.curr_x, this.curr_y);
}

var curr_x = 0;
var curr_y = 0;

function setup() {
	createCanvas(875,500);
	// colorMode(HSL, 360, 100, 100, 1);
	// c = 25;
	// background(color(234, 100, c));

	plot_Mandelbrot_Set();
}

function draw() {

	// plot_Mandelbrot_point(curr_x, curr_y);
	// if (curr_x == width) {
	// 	curr_x = 0;
	// 	curr_y += 1;
	// } else {
	// 	curr_x += 1;
	// }

	// if (curr_x == width && curr_y == height) {
	// 	remove();
	// }
  
}