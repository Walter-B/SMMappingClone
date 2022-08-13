
# How to display multiple images in one figure correctly?
# https://stackoverflow.com/questions/46615554/how-to-display-multiple-images-in-one-figure-correctly

import matplotlib.pyplot as plt
import numpy as np

# settings
h, w = 10, 10        # for raster image
nrows, ncols = 5, 4  # array of sub-plots
figsize = [6, 8]     # figure size, inches

# prep (x,y) for extra plotting on selected sub-plots
xs = np.linspace(0, 2*np.pi, 60)  # from 0 to 2pi
ys = np.abs(np.sin(xs))           # absolute of sine

# create figure (fig), and array of axes (ax)
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

# plot simple raster image on each sub-plot
for i, axi in enumerate(ax.flat):
    # i runs from 0 to (nrows*ncols-1)
    # axi is equivalent with ax[rowid][colid]
    img = np.random.randint(10, size=(h, w))
    axi.imshow(img, alpha=0.25)
    # get indices of row/column
    rowid = i // ncols
    colid = i % ncols
    # write row/col indices as axes' title for identification
    axi.set_title("Row:"+str(rowid)+", Col:"+str(colid))

# one can access the axes by ax[row_id][col_id]
# do additional plotting on ax[row_id][col_id] of your choice
ax[0][2].plot(xs, 3*ys, color='red', linewidth=3)
ax[4][3].plot(ys**2, xs, color='green', linewidth=3)

# plt.tight_layout(True)
plt.tight_layout()
plt.show()
