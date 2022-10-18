# IFS fractals
from mayavi import mlab
from PIL import Image
import random
import numpy
import cv2
import os

def clearScreen():
	os.system('cls' if os.name == 'nt' else 'clear')

def ifs(mat, variable = False, ini = 0, step = 1, end = 0):
	a = ini
	while a <= end:
		# image size
		imgx = 512
		imgy = 512
		if variable == True:
			mat[1][1] = round(a, 2)
			mat[1][2] = round(-a, 2)
			print('Procesando: ', round(a, 2))
		m = len(mat)
		x = mat[0][4]
		y = mat[0][5]
		xa = x
		xb = x
		ya = y
		yb = y

		for k in range(imgx * imgy):
			p = random.random()
			psum = 0.0
			for i in range(m):
				psum += mat[i][6]
				if p <= psum:
					break
			x0 = x * mat[i][0] + y * mat[i][1] + mat[i][4]
			y  = x * mat[i][2] + y * mat[i][3] + mat[i][5]
			x = x0
			if x < xa:
					xa = x
			if x > xb:
					xb = x
			if y < ya:
					ya = y
			if y > yb:
					yb = y

		imgy = round(imgy * (yb - ya) / (xb - xa)) 
		image = Image.new("RGB", (imgx, imgy))

		x = 0.0
		y = 0.0
		for k in range(imgx * imgy):
			p = random.random()
			psum = 0.0
			for i in range(m):
				psum += mat[i][6]
				if p <= psum:
					break
			x0 = x * mat[i][0] + y * mat[i][1] + mat[i][4]
			y  = x * mat[i][2] + y * mat[i][3] + mat[i][5]
			x = x0
			jx = int((x - xa) / (xb - xa) * (imgx - 1))
			jy = (imgy - 1) - int((y - ya) / (yb - ya) * (imgy - 1))
			if jx < imgx and jy < imgy: image.putpixel((jx, jy), (0, 255, 0))

		image.resize((512, 512))
		if variable == True:
			image.save("fractales/IFS_{name}_{i}.png".format(name = name, i = round(a, 2)), "PNG")
		else:
			image.save("fractales/IFS_{name}.png".format(name = name), "PNG")
		if variable == False: image.show()
		a += step
	
	# Convertir a video
	if variable:
		a = ini
		images = []
		while a < end:
			images.append("IFS_{name}_{i}.png".format(name = name, i = round(a, 2)))
			a += step
		while a > ini:
			a -= step
			images.append("IFS_{name}_{i}.png".format(name = name, i = round(a, 2)))

		output = "fractales/IFS_{name}_{ini}_{step}_{end}.avi".format(name = name, ini = ini, step = step, end = end)
		shape = 3000, 3000
		fps = 30

		fourcc = cv2.VideoWriter_fourcc(*'DIVX')
		video = cv2.VideoWriter(output, fourcc, fps, shape)

		for image in images:
			image_path = os.path.join('fractales', image)
			image = cv2.imread(image_path)
			resized = cv2.resize(image, shape)
			video.write(resized)

		video.release()

# Montañas 3D
# Variables
levels = 11
size = 2 ** (levels - 1)
height  = numpy.zeros((size + 1, size + 1))

def mountain():
	for level in range(levels):
		step = size // 2 ** level
		for y in range(0, size + 1, step):
			jumpover = 1 - (y // step) % 2 if level > 0 else 0
			for x in range(step * jumpover, size + 1, step * (1 + jumpover)):
				pointer = 1 - (x // step) % 2 + 2 * jumpover if level > 0 else 3
				yref, xref = step * (1 - pointer // 2), step * (1 - pointer % 2)
				corner1 = height[y - yref, x - xref]
				corner2 = height[y + yref, x + xref]
				average = (corner1 + corner2) / 2.0
				variation = step * (random.random() - 0.5)
				height[y,x] = average + variation if level > 0 else 0

	xg, yg = numpy.mgrid[-1:1:1j*size,-1:1:1j*size]

	surf = mlab.surf(xg, yg, height, colormap='gist_earth', warp_scale='auto')
	mlab.show()

# Mostrar menú del programa
opcion = 1
while (opcion != 0):
	clearScreen()
	print("Menú de opciones - Fractales")
	print()
	print("1- Helecho")
	print("2- Arbol")
	print("3- Hoja")
	print("4- Montañas 3D")
	# print("5- Dragon")
	# print("6- Curva de Levy")
	# print("7- Dragon de Levy")
	print("0- Salir")
	print()
	opcion = int(input("Ingrese opción: "))
	clearScreen()
	# mat = [[a, b, c, d, e, f, p], ...]
	# F(x,y) = (ax + by + e, cx + dy + f)
	# Donde p = probabilidad
	if (opcion == 1):
		name = 'Helecho'
		mat = [[0.0, 0.0, 0.0, 0.16, 0.0, 0.0, 0.01],
					[0.85, 0.04, -0.04, 0.85, 0.0, 1.6, 0.85],
					[0.2, -0.26, 0.23, 0.22, 0.0, 1.6, 0.07],
					[-0.15, 0.28, 0.26, 0.24, 0.0, 0.44, 0.07]]
	elif (opcion == 2):
		name = 'Arbol'
		mat = [[0.195, -0.488, 0.462, 0.414, 0.4431, 0.2452, 0.316],
					[0.462, 0.414, -0.252, 0.361, 0.2511, 0.5692, 0.28],
					[-0.058, -0.07, 0.453, -0.111, 0.5976, 0.0969, 0.039],
					[-0.035, 0.07, -0.469, -0.022, 0.4884, 0.5069, 0.035],
					[-0.637, 0.0, 0.0, 0.501, 0.8562, 0.2513, 0.33]]
	elif (opcion == 3):
		name = 'Hoja'
		mat = [[0.456, 0.019, -0.006, 0.683, 2.118, 2.243, 0.281],
		 			[0.327, -0.534, 0.293, 0.591, 2.381, -0.453, 0.315],
					[-0.354, 0.618, 0.351, 0.628, 4.782, -0.748, 0.396],
					[-0.002, 0.006, -0.053, 0.14, 3.49, 0.239, 0.009]]
	elif (opcion == 5):
		name = 'Dragon'
		mat = [[0.824074, 0.281482, -0.212346,  0.864198, -1.882290, -0.110607, 0.787473],
					[0.088272, 0.520988, -0.463889, -0.377778,  0.785360,  8.095795, 0.212527]]
	elif (opcion == 6):
		name = 'Levy_curve'
		mat = [[0.5, -0.5, 0.5, 0.5, 0.0, 0.0, 0.5],
					[0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5]]
	elif (opcion == 7):
		name = 'Levy_dragon'
		mat = [[0.5, -0.5, 0.5, 0.5, 0.0, 0.0, 0.5],
        	[-0.5, -0.5, 0.5, -0.5, 1.0, 0.0, 0.5]]

	if opcion == 4:
		mountain()
	elif opcion != 0:
		variable = ''
		while variable != 1 and variable != 2:
			clearScreen()
			print("Con variable? 2 para Si, 1 para No")
			variable = int(input("Ingrese opción: "))
			if variable == 2:
				clearScreen()
				print('Valor inicial: ')
				ini = float(input("Ingrese opción: "))
				clearScreen()
				print('Valor final: ')
				end = float(input("Ingrese opción: "))
				clearScreen()
				print('Paso de: ')
				step = float(input("Ingrese opción: "))
				clearScreen()
			
			if variable == 1:
				ifs(mat)
			else:
				ifs(mat, True, ini, step, end)