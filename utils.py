import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

def stack_bands(r, g, b):
    """Empilha três volumes 3D em um volume 4D RGB ao longo do último eixo."""
    slice_ = np.s_[..., None]
    return np.concatenate([r[slice_], g[slice_], b[slice_]], axis=r.ndim)

class Explorer(object):
    """Um slicer interativo simples que "panoramiza" uma série de fatias 2D ao longo de um
     dado eixo de volume 3D. Kwargs adicionais são passados para "imshow"."""
    def __init__(self, data, axis=2, **kwargs):
        self.data = data
        self.axis = axis
        self.start, self.stop = 0, data.shape[self.axis] - 1

        kwargs['cmap'] = kwargs.get('cmap', 'gray_r')
        
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(self[self.start], **kwargs)
        self.ax.axis('off')

        self.sliderax = self.fig.add_axes([0.2, 0.02, 0.6, 0.03])
        self.slider = Slider(self.sliderax, 'Z-slice', self.start, self.stop,
                             valinit=self.start, valfmt='%i')
        self.slider.on_changed(self.update)

    def __getitem__(self, i):
        slices = self.data.ndim * [slice(None)]
        slices[self.axis] = i
        return self.data[slices].swapaxes(0, 1)

    def update(self, val):
        dat = self[int(val)]
        self.im.set(data=dat, clim=[dat.min(), dat.max()])
        self.fig.canvas.draw()

    def show(self):
        plt.show()

def grid(x, y, z, dx=1, dy=1, extent=None, nodata=0):
    """Transforme pontos não ordenados, mas regularmente espaçados (ou seja, já em grade)
    em uma grade 2D regular. "z" pode ser uma matriz 1d de números ou uma matriz 2d de cores r, g, b."""
    if extent is None:
        extent = [x.min(), y.min(), x.max(), y.max()]
    xmin, ymin, xmax, ymax = extent

    nrows = (ymax - ymin) // dy + 1
    ncols = (xmax - xmin) // dx + 1
    i = ((y - ymin) / dy).astype(int)
    j = ((x - xmin) / dx).astype(int)

    if z.ndim > 1:
        output = nodata * np.ones((nrows, ncols, z.shape[1]), z.dtype)
        output[i, j, :] = z
    else:
        output = nodata * np.ones((nrows, ncols), z.dtype)
        output[i, j] = z

    return output
