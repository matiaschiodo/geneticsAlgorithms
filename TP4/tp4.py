# IFS fractals
from PIL import Image
import random
# import glob
# import cv2
import os

# image size
imgx = 512
imgy = 512

def clearScreen():
	# Limpia la terminal
	os.system('cls' if os.name == 'nt' else 'clear')

# Mostrar menú del programa
opcion = 1
while (opcion != 0):
	clearScreen()
	print("Menú de opciones - Fractales")
	print()
	print("1- Helecho")
	print("2- Arbol")
	# print("3- Dragon")
	# print("4- Curva de Levy")
	# print("5- Dragon de Levy")
	print("0- Salir")
	print()
	opcion = int(input("Ingrese opción: "))
	clearScreen()
	if (opcion == 1):
		# Fractint IFS definition of Fern
		name = 'Helecho'
		mat = [[0.0, 0.0, 0.0, 0.16, 0.0, 0.0, 0.01],
					[0.85, 0.04, -0.04, 0.85, 0.0, 1.6, 0.85],
					[0.2, -0.26, 0.23, 0.22, 0.0, 1.6, 0.07],
					[-0.15, 0.28, 0.26, 0.24, 0.0, 0.44, 0.07]]
		# a = -0.1
		# mat = [[0.0, 0.0, 0.0, 0.16, 0.0, 0.0, 0.01],
		# 			[0.85, -0.1, 0.1, 0.85, 0.0, 1.6, 0.85],
		# 			[0.2, -0.26, 0.23, 0.22, 0.0, 1.6, 0.07],
		# 			[-0.15, 0.28, 0.26, 0.24, 0.0, 0.44, 0.07]]
	elif (opcion == 2):
		# Fractint IFS definition of tree
		name = 'Arbol'
		mat = [[0.195, -0.488, 0.462, 0.414, 0.4431, 0.2452, 0.316],
					[0.462, 0.414, -0.252, 0.361, 0.2511, 0.5692, 0.28],
					[-0.058, -0.07, 0.453, -0.111, 0.5976, 0.0969, 0.039],
					[-0.035, 0.07, -0.469, -0.022, 0.4884, 0.5069, 0.035],
					[-0.637, 0.0, 0.0, 0.501, 0.8562, 0.2513, 0.33]]
	# elif (opcion == 3):
	# 	# Fractint IFS definition of Dragon
	# 	mat = [[0.824074, 0.281482, -0.212346,  0.864198, -1.882290, -0.110607, 0.787473],
	# 				[0.088272, 0.520988, -0.463889, -0.377778,  0.785360,  8.095795, 0.212527]]
	# elif (opcion == 4):
	# 	# Fractint IFS definition of Levy C curve
	# 	mat = [[0.5, -0.5, 0.5, 0.5, 0.0, 0.0, 0.5],
	# 				[0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5]]
	# elif (opcion == 5):
	# 	# Fractint IFS definition of Levy Dragon
	# 	mat = [[0.5, -0.5, 0.5, 0.5, 0.0, 0.0, 0.5],
  #       	[-0.5, -0.5, 0.5, -0.5, 1.0, 0.0, 0.5]]
					 
	if opcion != 0:
	# 	while a <= 0.1:
	# 		mat[1][1] = a
	# 		mat[1][2] = -a
		m = len(mat)
		x = mat[0][4]
		y = mat[0][5]
		xa = x
		xb = x
		ya = y
		yb = y

		for k in range(imgx * imgy):
			p=random.random()
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
		image = Image.new("L", (imgx, imgy))

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
			image.putpixel((jx, jy), 255) 

		image.save("fractales/IFS_{name}.png".format(name = name), "PNG")
		image.show()
			# a += 0.05

		# # Video de transicion
		# img_array = []
		# for filename in glob.glob('../fractales/*.png'):
		# 	img = cv2.imread(filename)
		# 	height, width, layers = img.shape
		# 	size = (width, height)

		# 	img_array.append(img)
		
		# out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
		
		# for i in range(len(img_array)):
		# 	out.write(img_array[i])
		# out.release()