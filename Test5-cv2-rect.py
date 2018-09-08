#
# Draw a rectangle on image with cv2.
# https://stackoverflow.com/questions/37435369/matplotlib-how-to-draw-a-rectangle-on-image?rq=1
#

import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2

im = np.array(Image.open('hubble_friday_12102015.jpg'), dtype=np.uint8)

# Create figure and axes
fig,ax = plt.subplots(1)

cv2.rectangle(
	im,
	(100,100),
	(500,500),
	(0,255,0),
	3)

cv2.imwrite('output.jpg', im)

# Display the image
ax.imshow(im)


plt.show()