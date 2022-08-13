
# https://stackoverflow.com/questions/31452451/importing-an-svg-file-into-a-matplotlib-figure
import svgutils.transform as sg
import svgutils.compose as sc
# from IPython.display import SVG  # /!\ note the 'SVG' function also in svgutils.compose

# Figure("30cm", "30cm", SVG('FIGURES/grid.svg'), SVG('FIGURES/colorbar_ver.svg')).save('FIGURES/compose.svg')
# SVG('FIGURES/compose.svg')

# https://stackoverflow.com/questions/60792318/how-to-create-a-high-resolution-combined-figure

def new_tile(self, ncols, nrows):
    dx = self.width.to('px').value/ncols
    dy = self.height.to('px').value/nrows
    ix, iy = 0, 0
    for el in self:
        el.move(dx*ix, dy*iy)
        ix += 1
        if ix >= ncols:
            ix = 0
            iy += 1
        if iy > nrows:
            break
    return self


# https://stackoverflow.com/questions/45850144/is-there-a-bug-in-svgutils-compose-module-regarding-the-arrangement-of-figures
sc.Figure.tile = new_tile

scale_factor = 2.

fig = sc.Figure("40cm", "25cm",
       sc.Panel(
          sc.Text("A", 25, 20),
          sc.SVG('FIGURES/grid.svg').scale(scale_factor)
          ),
       sc.Panel(
          sc.Text("B", 25, 20),
          sc.SVG('FIGURES/colorbar_ver.svg').scale(scale_factor)
          )
       ).tile(1, 2)\

fig.save('FIGURES/bis3.svg')