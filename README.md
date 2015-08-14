MPLKit
================

`mplkit` is a Python 2 (Python 3 support may be added later) toolkit for users of `matplotlib` that provides the following modules:

 - `mplkit.cmap`: Utility wrappers around colormaps that reverse, invert, desaturate or concatenate existing colormaps, allowing for simple colormap manipulation.
 - `mplkit.plot`: A helper function for plotting contours `contour_image` (`matplotlib.pyplot.contour`) over a surface plot (`matplotlib.pyplot.imshow`), with several advanced annotation and styling features.
 - `mplkit.style`: A set of styles for matplotlib that allow for more general power than simply setting rcParams (though that is supported too). The collection of example styles is (for the moment) quite small. This can act as a wrapper around `matplotlib` styles also. Small tweaks to these styles may be made from release to release.

For more documentation, refer to the source code itself or use the python `help` function on the respective modules.

Installation
------------

If you use `pip`, you can run:

	$ pip install mplkit

Otherwise, installing this module is as easy as:

	$ python2 setup.py install

If you run Arch Linux, you can instead run:

	$ makepkg -i
