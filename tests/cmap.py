import sys
sys.path.insert(0,'..')

from mplkit.cmap import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase

cmap = matplotlib.cm.Blues
id_cmap = WrappedColormap(cmap)
inv_cmap = InverseColormap(cmap)
mono_cmap = MonochromeColormap(cmap)
rev_cmap = ReverseColormap(cmap)
cat_cmap = ConcatenatedColormap(cmap,0.2,inv_cmap,0.8,mono_cmap)
norm = Normalize(vmin=0, vmax=1)

plt.subplot(6,1,1)
plt.title("Normal")
cb1 = ColorbarBase(plt.gca(), cmap=cmap,
								   norm=norm,
								   orientation='horizontal')

plt.subplot(6,1,2)
plt.title("Wrapped")
cb1 = ColorbarBase(plt.gca(), cmap=id_cmap,
								   norm=norm,
								   orientation='horizontal')

plt.subplot(6,1,3)
plt.title("Inverted")
cb1 = ColorbarBase(plt.gca(), cmap=inv_cmap,
								   norm=norm,
								   orientation='horizontal')

plt.subplot(6,1,4)
plt.title("Monochromed")
cb1 = ColorbarBase(plt.gca(), cmap=mono_cmap,
								   norm=norm,
								   orientation='horizontal')

plt.subplot(6,1,5)
plt.title("Reversed")
cb1 = ColorbarBase(plt.gca(), cmap=rev_cmap,
								   norm=norm,
								   orientation='horizontal')

plt.subplot(6,1,6)
plt.title("Concatenated")
cb1 = ColorbarBase(plt.gca(), cmap=cat_cmap,
								   norm=norm,
								   orientation='horizontal')

plt.tight_layout()
plt.savefig('cmap.pdf')
