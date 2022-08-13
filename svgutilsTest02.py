

# Programmatically Merging SVG files
# https://jetholt.com/micro/programmatically-merging-svg-files/

import svgutils.transform as sg
import sys
import re

background = sg.fromfile('FIGURES/grid2.svg')
logo = sg.fromfile('FIGURES/colorbar_ver.svg')


def convert_to_pixels(measurement):
    value = float(re.search(r'[0-9\.]+', measurement).group())
    if measurement.endswith("px"):
        return value
    elif measurement.endswith("mm"):
        return value * 3.7795275591
    else:
        # unit not supported
        return value


width = convert_to_pixels(background.get_size()[0])
height = convert_to_pixels(background.get_size()[1])
logo_width = convert_to_pixels(logo.get_size()[0])
logo_height = convert_to_pixels(logo.get_size()[1])

plot2 = logo.getroot()

# Top Left
# root.moveto(1, 1)

# Top Right
#root.moveto(width - logo_width - 1, 1)

# Bottom Left
#root.moveto(1, height - logo_height - 1)

# Bottom Right
# plot2.moveto(width - logo_width - 1, height - logo_height - 1)

# plot2.moveto(490, 350)  # x, y
plot2.moveto(450, 100)  # x, y
# plot2.moveto(490, -150)  # x, y

# root.moveto(width, height)~~

# background.append([root])
#
# background.save('output.svg')

# https://python.hotexamples.com/examples/svgutils.transform/-/fromfile/python-fromfile-function-examples.html

# get the plot objects
plot1 = background.getroot()

plot1.moveto(0, 5)

# create new SVG figure
width, height = "18cm", "18cm"
fig = sg.SVGFigure(width, height)

fig.append([plot1, plot2])
# fig.save('composition_with_legend_in_tight_layout.svg')
fig.save('composition2.svg')

# Python fromfile Examples
# https://python.hotexamples.com/examples/svgutils.transform/-/fromfile/python-fromfile-function-examples.html

# def mergeSvgFiles(self):
#     files = (self.circosFile, self.colorbarFile, self.legendFile)
#     fOutSVG = self.fantomCircosSVG
#     fOutPNG = self.fantomCircosPNG
#     # create new SVG figure
#     width, height = "18cm", "18cm"
#     fig = sg.SVGFigure(width, height)
#
#     # load matpotlib-generated figures
#     fig1 = sg.fromfile(files[0])
#     fig2 = sg.fromfile(files[1])
#     fig3 = sg.fromfile(files[2])
#
#     # get the plot objects
#     plot1 = fig1.getroot()
#     plot2 = fig2.getroot()
#     plot3 = fig3.getroot()
#
#     plot1.moveto(0, 5, scale=0.21)
#     plot2.moveto(490, 550, scale=0.25)
#     plot3.moveto(180, 280, scale=0.6)
#
#     # add text labels
#     # txt1 = sg.TextElement(25,20, "A", size=12, weight="bold")
#     # txt2 = sg.TextElement(305,20, "B", size=12, weight="bold")
#
#     # append plots and labels to figure
#     fig.append([plot1, plot2, plot3])
#     # fig.append([txt1, txt2])
#
#     # save generated SVG files
#     fig.save(fOutSVG)