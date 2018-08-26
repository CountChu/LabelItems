#
# https://stackoverflow.com/questions/34768717/matplotlib-unable-to-save-image-in-same-resolution-as-original-image
#

import matplotlib.pyplot as plt

# On-screen, things will be displayed at 80dpi regardless of what we set here
# This is effectively the dpi for the saved figure. We need to specify it,
# otherwise `savefig` will pick a default dpi based on your local configuration
dpi = 80

im_data = plt.imread('hubble_friday_12102015.jpg')
height, width, nbands = im_data.shape

# What size does the figure need to be in inches to fit the image?
figsize = width / float(dpi), height / float(dpi)

# Create a figure of the right size with one axes that takes up the full figure
fig = plt.figure(figsize=figsize)
ax = fig.add_axes([0, 0, 1, 1])

# Hide spines, ticks, etc.
ax.axis('off')

# Display the image.
ax.imshow(im_data, interpolation='nearest')

# Add something...
ax.annotate('Look at This!', xy=(590, 650), xytext=(500, 500),
            color='cyan', size=24, ha='right',
            arrowprops=dict(arrowstyle='fancy', fc='cyan', ec='none'))

# Ensure we're displaying with square pixels and the right extent.
# This is optional if you haven't called `plot` or anything else that might
# change the limits/aspect.  We don't need this step in this case.
ax.set(xlim=[0, width], ylim=[height, 0], aspect=1)

fig.savefig('test.jpg', dpi=dpi, transparent=True)
plt.show()