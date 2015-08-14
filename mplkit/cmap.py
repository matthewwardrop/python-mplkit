import matplotlib
from matplotlib.colors import Colormap, LinearSegmentedColormap, ListedColormap

import numpy as np

class WrappedColormap(Colormap):
	"""
	`WrappedColormap` wraps around an instance of `matplotlib.colors.Colormap`,
	provides the `luma` method, but otherwise does nothing to the colormap.
	"""
	def __init__(self, cmap, *args, **kwargs):
		assert(isinstance(cmap, Colormap))
		self.cmap = cmap
		self.init(*args,**kwargs)

	def init(*args,**kwargs):
		pass

	def __call__(self, X, alpha=None, bytes=False):
		return self.cmap(X, alpha=alpha, bytes=bytes)

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

	def luma(self, X, alpha=None, bytes=False):
		color = self(X, alpha=alpha, bytes=bytes)

		def get_luma(c):
			return np.average(c,axis=-1,weights=[0.299,0.587,0.114,0])

		return get_luma(color)

class ReversedColormap(WrappedColormap):
	'Reverses the color map.'

	def __call__(self, X, alpha=None, bytes=False):
		return self.cmap(1-X, alpha=alpha, bytes=bytes)

class InvertedColormap(WrappedColormap):
	'Inverts the color map according to (R,G,B,A) - > (1-R,1-G,1-B,A).'

	def __call__(self, X, alpha=None, bytes=False):
		color = self.cmap(X, alpha=alpha, bytes=bytes)

		def invert(c):
			c = map(lambda x: 1-x, c)
			c[-1] = 1
			return tuple(c)

		if isinstance(X, (np.ndarray,) ):
			color = 1 - color
			color[...,-1] = 1
			return color
		else:
			return invert(color)

class DesaturatedColormap(WrappedColormap):
	'Constructs a new colormap that preserves only the luma; or "brightess".'

	def __call__(self, X, alpha=None, bytes=False):
		color = self.cmap(X, alpha=alpha, bytes=bytes)

		def get_luma(c):
			return np.average(c,axis=-1,weights=[0.299,0.587,0.114,0])

		r = np.kron(get_luma(color),[1,1,1,1]).reshape(np.shape(X)+(4,))
		r[...,-1] = 1
		return r

class ConcatenatedColormap(WrappedColormap):
	"""
	`ConcatenatedColormap` wraps around an instances of `matplotlib.colors.Colormap`,
	and when used as a colour map returns the result of concatenating linearly the
	maps. Should be initialised as:
	ConcatenatedColormap(<cmap1>,0.2,<cmap2>,...)
	Where the numbers indicate where the cmaps are joined. The 0 at the beginning and the 1
	at the end are inferred.
	"""

	def init(self,*args):
		self.cmaps = [self.cmap]
		self.cmap_joins = []
		assert(len(args) % 2 == 0)
		for i in xrange(0,len(args),2):
			self.cmap_joins.append(float(args[i]))
			assert(args[i] < 1 and args[i] > 0 and (i==0 or args[i] > self.cmap_joins[-2]))
			assert(isinstance(args[i+1],Colormap))
			self.cmaps.append(args[i+1])

	def __call__(self, X, alpha=None, bytes=False):
		def get_color(v):
			min = 0
			max = 1
			cmap_index = np.sum(np.array(self.cmap_joins) < v)
			assert (cmap_index <= len(self.cmaps))
			if (cmap_index > 0):
				min = self.cmap_joins[cmap_index-1]
			if (cmap_index < len(self.cmaps)-1):
				max = self.cmap_joins[cmap_index]

			scaled_v = (v-min)/(max-min)
			return tuple(self.cmaps[cmap_index](scaled_v,alpha=alpha,bytes=bytes))

		if isinstance(X,np.ndarray):
			vfunc = np.vectorize(get_color,otypes=["float","float","float", "float"])
			return np.rollaxis(np.array(vfunc(X)),0,len(X.shape)+1)
		else:
			return get_color(X)

	def set_bad(self, color='k', alpha=None):
		pass#self.cmap.set_bad(color=color, alpha=alpha)

	def set_under(self, color='k', alpha=None):
		pass#self.cmap.set_under(color=color, alpha=alpha)

	def set_over(self, color='k', alpha=None):
		pass#self.cmap.set_over(color=color, alpha=alpha)

	def _set_extremes(self):
		pass#self.cmap._set_extremes()

	def _init(self):
		"""Generate the lookup table, self._lut"""
		for cm in self.cmaps:
			cm._init()

	def is_gray(self):
		return np.all([cm.is_gray() for cm in self.cmaps])

	def __getattr__(self, key):
		return getattr(self.cmap,key)

	def luma(self, X, alpha=None, bytes=False):
		color = self(X, alpha=alpha, bytes=bytes)

		def get_luma(c):
			return np.average(c,axis=-1,weights=[0.299,0.587,0.114,0])

		return get_luma(color)
