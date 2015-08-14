import sys
sys.path.insert(0,'..')

from mplkit.plot import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase

from mplkit.style import *

cmap = matplotlib.cm.Blues

with SampleStyle() as style:

	plt.figure()

	x,y = np.linspace(-10,10,201), np.linspace(-10,10,201)
	X,Y = np.meshgrid(x,y)
	data = np.log(1./(1+X**2+Y**2))

	contour_image(x,y,data, outline=True, label=True, cguides=[-3.2], cguide_stride=1, contour_smoothing=1)

	style.savefig('contour_image.pdf')
