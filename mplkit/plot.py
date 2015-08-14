from matplotlib import cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects

import types
import numpy as np
import scipy.ndimage

from .cmap import ReversedColormap, WrappedColormap, InvertedColormap

__all__ = ['contour_image']

def contour_image(x,y,Z,
					vmin=None,
					vmax=None,
					label=False,
					contour_smoothing=1,
					outline=None,

					contour_opts={},
					clabel_opts={},
					imshow_opts={},

					cguides=False,
					cguide_tomax=True,
					cguide_stride=1,
					cguide_opts={}):
	'''
	This function wraps around matplotlib.pyplot.[imshow, contour, clabel, quiver] to
	produce scientific plots with (potentially) labelled contours. All arguments
	sported by these underlying methods can be passed using `<method>_opts`
	respectively. In addition, this function adds the following options:
	 - vmax and vmin : None (default) or a numerical value. These replace the option
	 	in the appropriate argument dictionary; for consistency across plotting calls.
	 - label : False (default) or True. Whether contour labels should be shown.
	 - contour_smoothing : 1 (default) or positive float; indicating scale of
	 	contour resolution (<1 means fewer points, >1 means more interpolated points).
	 - outline : None (default), True, a colour (or colours), or a function mapping a RGBA colour to the
	 	desired outline colour.
	 - cguides : False (default), True or list of contour values. If True, guides
	  	are shown on every contour. Guides are arrows which point to regions of
		greater value.
	 - cguide_tomax : True (default) or False : Whether guides point to regions of
	 	greater (or lesser) value.
	 - cguide_stride : 1 (default), or positive integer : Specifies how often (i.e.
	 	every `cguide_stride`) points the guides should be drawn.
	 - cguide_opts : dictionary of kwargs. Supports all kwargs of `quiver`.

	This function returns the values of plt.imshow, plt.contour, and plt.clabel
	in that order. If the function was not called, `None` is returned instead.
	'''
	ax = plt.gca()

	x_delta = float((x[-1]-x[0]))/(len(x)-1)/2.
	y_delta = float((y[-1]-y[0]))/(len(y)-1)/2.

	extent=(x[0],x[-1],y[0],y[-1])

	extent_delta = (x[0]-x_delta,x[-1]+x_delta,y[0]-y_delta,y[-1]+y_delta)

	ax.set_xlim(x[0],x[-1])
	ax.set_ylim(y[0],y[-1])

	aspect=(x[-1]-x[0])/(y[-1]-y[0])

	Z = Z.transpose()

	if vmin is None:
		vmin = np.min(Z)
	if vmax is None:
		vmax = np.max(Z)

	# imshow plotting
	imshow_cs = ax.imshow(Z,origin='lower',aspect='auto',extent=extent_delta,vmax=vmax,vmin=vmin, **imshow_opts)

	# contour plotting
	if contour_smoothing != 1:
		Z = scipy.ndimage.zoom(Z, contour_smoothing)
	if 'cmap' not in contour_opts:
		contour_opts['cmap'] = InvertedColormap(imshow_cs.cmap)
	elif 'cmap' in contour_opts and not isinstance(contour_opts['cmap'], WrappedColormap):
		contour_opts['cmap'] = WrappedColormap(contour_opts['cmap'])

	contour_cs = ax.contour(Z, extent=extent_delta, origin='lower', vmax=vmax,vmin=vmin, **contour_opts )

	# outlining
	if outline is True:
		def outline(cvalue, vmin=0, vmax=1):
			if contour_cs.cmap.luma(float(cvalue - vmin) / (vmax-vmin)) <= 0.5:
				return (1,1,1,0.2)
			return (0,0,0,0.2)
	if type(outline) is types.FunctionType or isinstance(outline, colors.Colormap):
		outline = [outline(c, vmin=vmin, vmax=vmax) for c in contour_cs.cvalues]
	elif type(outline) is list:
		pass
	elif outline is None:
		pass
	else:
		outline = [outline]*len(contour_cs.cvalues)

	if outline is not None:
		for i,collection in enumerate(contour_cs.collections):
			plt.setp(collection, path_effects=[
				PathEffects.withStroke(linewidth=3, foreground=outline[i])])

	# clabel plotting
	if label:
		clabel_cs = ax.clabel(contour_cs, **clabel_opts)
		if outline is not None:
			for i,clbl in enumerate(clabel_cs):
				plt.setp(clbl, path_effects=[
						PathEffects.withStroke(linewidth=1.5, foreground=outline[np.argmin(np.abs(contour_cs.cvalues-float(clbl.get_text())))])])
	else:
		clabel_cs = None

	# Draw guides on specified contours
	if cguides is True:
		cguides = contour_cs.cvalues
	if cguides is not False:
		_decorate_contour_segments(contour_cs, cguides, cguide_stride, vmin, vmax, cguide_opts, tomax=cguide_tomax, outline=outline, aspect=aspect)

	return imshow_cs, contour_cs, clabel_cs

def _decorate_contour_segments(CS, cvalues, stride=1, vmin=0, vmax=1, options={}, tomax=True, outline=None, aspect=1):
	for i,value in enumerate(cvalues):
		options['color'] = CS.cmap(float(value - vmin) / (vmax-vmin))
		for index in np.where(np.isclose(value, CS.cvalues))[0]:
			for segment in CS.collections[index].get_segments():#for segment in CS.allsegs[index]:
				_decorate_contour_segment(segment, stride=stride, options=options, tomax=tomax, labelled=hasattr(CS,'cl'), outline=outline[i] if outline is not None else None, aspect=aspect)

def _decorate_contour_segment(data, stride=1, options={}, tomax=True, labelled=False, outline=None, aspect=1):
	default_options = {'scale': 0.2,
			'scale_units': 'dots',
			'headaxislength': 2,
			'headlength': 2,
			'headwidth': 2,
			'minshaft': 1,
			'units': 'dots',
			#'angles': 'xy',
			'edgecolor': outline,
			'linewidth': 0 if outline is None else 0.2
		}
	default_options.update(options)

	x = data[::stride,0]
	y = data[::stride,1]

	sign = 1 if tomax else -1
	dx = -sign*np.diff(y)*aspect
	dy = sign*np.diff(x)
	l = np.sqrt(dx**2+dy**2)
	dx /= l
	dy /= l

	x = 0.5*(x+np.roll(x,-1))
	y = 0.5*(y+np.roll(y,-1))

	if labelled:
		x,y,dx,dy = x[1:-2], y[1:-2], dx[1:-1], dy[1:-1]
	else:
		x,y = x[:-1], y[:-1]

	plt.quiver(x, y, dx, dy, **default_options)
