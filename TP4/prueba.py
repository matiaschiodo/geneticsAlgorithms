import glob
import cv2

# Video de transicion
img_array = []
for filename in glob.glob('../fractales/*.png'):
  img = cv2.imread(filename)
  height, width, layers = img.shape
  size = (width, height)
  print(size)
  img_array.append(img)

out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

for i in range(len(img_array)):
  out.write(img_array[i])
out.release()