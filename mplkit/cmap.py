import matplotlib
import numpy as np
def cmap_map(function,cmap):
    """ Applies function (which should operate on vectors of shape 3:
    [r, g, b], on colormap cmap. This routine will break any discontinuous     points in a colormap.
    """
    cdict = cmap._segmentdata
    step_dict = {}
    # First get the list of points where the segments start or end
    for key in ('red','green','blue'):         step_dict[key] = map(lambda x: x[0], cdict[key])
    step_list = sum(step_dict.values(), [])
    step_list = np.array(list(set(step_list)))
    # Then compute the LUT, and apply the function to the LUT
    reduced_cmap = lambda step : np.array(cmap(step)[0:3])
    old_LUT = np.array(map( reduced_cmap, step_list))
    new_LUT = np.array(map( function, old_LUT))
    # Now try to make a minimal segment definition of the new LUT
    cdict = {}
    for i,key in enumerate(('red','green','blue')):
        this_cdict = {}
        for j,step in enumerate(step_list):
            if step in step_dict[key]:
                this_cdict[step] = new_LUT[j,i]
            elif new_LUT[j,i]!=old_LUT[j,i]:
                this_cdict[step] = new_LUT[j,i]
        colorvector=  map(lambda x: x + (x[1], ), this_cdict.items())
        colorvector.sort()
        cdict[key] = colorvector

    return matplotlib.colors.LinearSegmentedColormap('colormap',cdict,cmap.N)

def reverse(cmap):
	if getattr(cmap,'_segmentdata',None) is not None:
		data = cmap._segmentdata

		cdict = {}
		for key in ['green','red','blue']:
			newline = []
			for line in data[key]:
				x = line[0]
				y = line[1]
				y2 = line[2]
				newline.append(  (1-x,y,y2)  )
			newline = sorted(newline,cmp=lambda x1,x2: cmp(x1[0],x2[0])	)

			cdict[key] = tuple(newline)
		return matplotlib.colors.LinearSegmentedColormap('colormap',cdict,cmap.N)
	print "Cannot reverse cmap"
	return cmap

from matplotlib.colors import Colormap
class InverseColormap(Colormap):
    """
    A class that wraps around another object and returns its complement.
    """
    def __init__(self, cmap):
        self.cmap = cmap

    def __call__(self, X, alpha=None, bytes=False):
        color = self.cmap(X, alpha=alpha, bytes=bytes)

        def invert(c):
            c = map(lambda x: 1-x, c)
            c[-1] = 1
            return tuple(c)

        if isinstance(X, (np.ndarray,) ):
            color = 1 - color
            color[:,-1] = 1
            return color
        else:
            return invert(color)

    def set_bad(self, color='k', alpha=None):
        self.cmap.set_bad(color=color, alpha=alpha)

    def set_under(self, color='k', alpha=None):
        self.cmap.set_under(color=color, alpha=alpha)

    def set_over(self, color='k', alpha=None):
        self.cmap.set_over(color=color, alpha=alpha)

    def _set_extremes(self):
        self.cmap._set_extremes()

    def _init(self):
        """Generate the lookup table, self._lut"""
        return self.cmap._init()

    def is_gray(self):
        return self.cmap.is_gray()

    def __getattr__(self, key):
        return getattr(self.cmap,key)
