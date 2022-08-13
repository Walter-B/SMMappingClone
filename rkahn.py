# https://github.com/rkahnGitHub/memoire/blob/master/PYTHON/SM%20mapping.ipynb

import glob, os

import numpy as np  # requires numpy

# 1) download 'GDAL' from https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
# install in Terminal, with pip install <download location>,
#   e.g. pip install C:\Users\<user>\Downloads\GDAL-3.4.1-cp38-cp38-win_amd64.whl
#
# 2) download 'Fiona' from https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona
# install in Terminal, with pip install <download location>
#   e.g. pin install C:\Users\<user>\Downloads\Fiona-1.8.21-cp38-cp38-win_amd64.whl
#
# 3) do a an install of 'geopandas' directly from PyCharm settings

import geopandas as gpd  # requires geopandas
import rasterio  # requires rasterio
import rasterio.mask
import rasterio.plot
from rasterio.enums import Resampling
import matplotlib.pyplot as plt  # requires matplotlib
from pathlib import Path
import rasterstats  # requires rasterstats
from rasterstats import zonal_stats
import datetime
from IPython.display import display  # requires ipython
import plotly.express as px  # requires plotly
import plotly.graph_objects as go
import plotly.offline
import pandas as pd

plotly.offline.init_notebook_mode()

print('All libraries successfully imported!')
print(f'Rasterstats : {rasterstats.__version__}')

import glob, os, time
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
import rasterio.plot
from rasterio import features

# Set directory
# work_path = f'/export/homes/students/rkahn/memoire/EXPORT/'
work_path = f'EXPORT/'
print(work_path)
cartes = f'{work_path}CARTES_CSV/'
# cartes_display = '/export/homes/students/rkahn/memoire/FIGURES/SM/cartes_display.csv'
cartes_display = 'FIGURES/SM/cartes_display.csv'
print(cartes_display)
vector_file = f'{work_path}COMPOSITE_SEGMENTED/NDVI_2019_2021_SEGMENTED.shp'

# Jonction segments-estimations
sm = pd.read_csv(f'{cartes}SM_201901.csv')
print(sm)

loca = gpd.read_file(vector_file)
display(loca)

carte_merged = loca.merge(sm, left_on="label", right_on="label")
carte_merged.head()
# carte_merged.to_file(cartes_display)

# Create nomalized legend
import matplotlib.pyplot as plt
import matplotlib as mpl

fig = plt.figure()
# ax = fig.add_axes([0.02, 0.9, 0.9, 0.02])
ax = fig.add_axes([0.5, 0.01, 0.01, 0.5])

cb = mpl.colorbar.ColorbarBase(ax, orientation='vertical',
                               cmap='Blues',
                               norm=mpl.colors.Normalize(3.12, 28.72),  # vmax and vmin
                               # extend='both',
                               label='Humidité du sol (vol %)',
                               ticks=[4, 7, 10, 13, 16, 19, 22, 25, 28])

# plt.savefig('/export/homes/students/rkahn/memoire/FIGURES/SM/colorbar_ver.svg')
# plt.tight_layout()
plt.savefig('FIGURES/colorbar_ver.svg', transparent=True)

# Display all SM maps
# function for cartes's titles
date1 = "2019-01-01"
date2 = "2022-03-01"
y0 = int(date1.split('-')[0])  # 2014
y1 = int(date2.split('-')[0])  # 2016
m0 = int(date1.split('-')[1]) - 1  # 10-1 --> 9 because will be used for indexing
m1 = int(date2.split('-')[1]) - 1  # 01-1 --> 0 because will be used for indexing
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
date = []
start = m0
for y in range(y0, y1 + 1):
    for m in range(start, 12):
        date.append(str(months[m % 12]) + '-' + str(y))
        if y == y1 and (m % 12) == m1:
            break
    start = 0
print(date)

loca = gpd.read_file(vector_file)
# display(loca)

# im_file = sorted(glob.glob(f'{cartes}*.csv'))
im_file = sorted(glob.glob(f'H_RASTER_MEANS_8_STATIONS/*.tif'))
# display(im_file)

h, w = 10, 10  # for raster image
nrows, ncols = 6, 12  # array of sub-plots
figsize = [8, 10]  # figure size, inches

# fig, axs = plt.subplots(nrows=7, ncols=6, sharex=True, sharey=True) #attempt to display the cards on a grid
# create figure (fig), and array of axes (ax)
fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

# # ======================================================================================================================
# for index, i  in enumerate(im_file):
#     sm = pd.read_csv(i)
#     carte_merged = loca.merge(sm, left_on="label", right_on="label")
#     # # display(carte_merged)
#     # fig, ax = plt.subplots(1, 1, figsize=(8,8))
#     # plt.title(date, loc='center', fontsize=15)
#     # cax = fig.add_axes([ax.get_position().x1+0.01, ax.get_position().y0, 0.02, ax.get_position().height])
#     # color_map = plt.cm.get_cmap("RdYlBu_r")
#     color_map = plt.cm.get_cmap("Blues")
#     reversed_color_map = color_map.reversed()
#     # carte_merged.plot(column='Estimation', linewidth=2, cmap=color_map, min=3.12, max=28.72)
#     carte_merged.plot(column='Estimation', linewidth=2, cmap=color_map)
#     plt.axis('off')
#     plt.title(date[index], size=14)
#     fig_date = os.path.basename(i)[:-4]
#
#     # plt.savefig(f'/export/homes/students/rkahn/memoire/FIGURES/SM/{fig_date}.pdf', format='pdf')
#     # plt.savefig(f'FIGURES/SM/{fig_date}.pdf', format='pdf')
#     plt.show()
# # ======================================================================================================================
# quit()

import rasterio

norm = mpl.colors.Normalize(vmin=0, vmax=0.5)

# plot simple raster image on each sub-plot
for i, axi in enumerate(axs.flat):
    # i runs from 0 to (nrows*ncols-1)
    # axi is equivalent with ax[rowid][colid]
    # img = np.random.randint(10, size=(h, w))

    try:
        # sm = pd.read_csv(im_file[i])
        # carte_merged = loca.merge(sm, left_on="label", right_on="label")
        # color_map = plt.cm.get_cmap("Blues")
        # reversed_color_map = color_map.reversed()
        # # carte_merged.plot(column='Estimation', linewidth=2, cmap=color_map, min=3.12, max=28.72)
        # carte_merged.plot(column='Estimation', linewidth=2, cmap=color_map)
        #
        # # turn axes off on each subplot (saved as image)
        # plt.axis('off')
        #
        # # plt.title(date[i], size=14)
        fig_date = os.path.basename(im_file[i])[:-4]
        #
        # plt.savefig(f'FIGURES/SM/{fig_date}.png', format='png')
        # # https://stackoverflow.com/questions/9622163/save-plot-to-image-file-instead-of-displaying-it-using-matplotlib
        # plt.close()
        #
        # image = plt.imread(f'FIGURES/SM/{fig_date}.png')

        # image = plt.imread(f'H_RASTER_MEANS_8_STATIONS/2015-04.tif')
        b1 = rasterio.open(im_file[i])
        ba1 = b1.read()
        image = np.reshape(ba1, (ba1.shape[0] * ba1.shape[1], ba1.shape[2]))

        axi.imshow(image, norm=norm)
        # get indices of row/column
        # rowid = i // ncols
        # colid = i % ncols
        # write row/col indices as axes' title for identification
        axi.set_title(fig_date, size=8)

        # https://stackoverflow.com/questions/25862026/turn-off-axes-in-subplots
        # turn axes off on resulting grid plot
        axi.axis('off')

    except IndexError:
        axi.axis('off')

# plt.tight_layout(True)
plt.tight_layout()
plt.savefig(f'FIGURES/grid2.svg')
# plt.show()
# ======================================================================================================================

# # https://stackoverflow.com/questions/31452451/importing-an-svg-file-into-a-matplotlib-figure
# from svgutils.compose import *
# # from IPython.display import SVG  # /!\ note the 'SVG' function also in svgutils.compose
#
# Figure("30cm", "30cm", SVG('FIGURES/grid.svg'), SVG('FIGURES/colorbar_ver.svg')).save('FIGURES/compose.svg')
# # SVG('FIGURES/compose.svg')
#
# Figure("16cm", "6.5cm",
#        Panel(
#           Text("A", 25, 20),
#           SVG('FIGURES/colorbar_ver.svg')
#           ),
#        Panel(
#           Text("B", 25, 20),
#           SVG('FIGURES/grid.svg')
#           )
#        ).save('FIGURES/out.svg')
#
# # https://svgutils.readthedocs.io/en/latest/tutorials/composing_multipanel_figures.html