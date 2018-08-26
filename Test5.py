#
# Draw a rectangle on pyplot image with matplotlib.patches
# https://stackoverflow.com/questions/37435369/matplotlib-how-to-draw-a-rectangle-on-image?rq=1
#

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

im = np.array(Image.open('hubble_friday_12102015.jpg'), dtype=np.uint8)

# Create figure and axes
fig,ax = plt.subplots(1)

# Display the image
ax.imshow(im)

# Create a Rectangle patch
rect = patches.Rectangle((50,100),40,30,linewidth=1,edgecolor='r',facecolor='none')

# Add the patch to the Axes
ax.add_patch(rect)

plt.show()