#!/usr/bin/python

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter,LogFormatterMathtext,NullFormatter,LogLocator

class MPLStyle(object):
	'''
	The base style, which adds nothing to the default style, but allows access to
	the utility methods.
	'''

	def __call__(self,f=None):
		self.polish(f)

	def __get_figure(self,f):
		if f is None:
			return plt.gcf()
		if isinstance(f,(int,long)):
			return plt.figure(f)
		return f

	def __get_axes(self,a):
		if a is None:
			return plt.gca()
		return a

	############## CONTEXT MANAGEMENT ######################################
	def __enter__(self):
		self.__old_rcParams = plt.rcParams.copy()
		self.set_params()
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		plt.rcParams = self.__old_rcParams

	def set_params(self):
		pass

	############## Figure methods ##########################################

	def polish(self,f=None):
		self._polish(self.__get_figure(f))

	def _polish(self,f):
		pass

	############## Axes methods ############################################

	def label_plot(self,label=None,ax=None,**kwargs):
		self._label_plot(label,self.__get_axes(ax),**kwargs)

	def _label_plot(self,label,ax,x=0.05,y=0.9):
		if isinstance(label,str):

			if x > 0.5:
				halign = "right"
			else:
				halign = "left"

			if y > 0.5:
				valign = "top"
			else:
				valign = "bottom"

			ax.text(x,y,label,
					 horizontalalignment=halign,
				     verticalalignment=valign,
				     transform = ax.transAxes,
				     fontsize = 'x-large',
				     color = 'white',
				     bbox=dict(facecolor='black', alpha=0.5, pad=10))

	def set_axes_lim(self,ax=None,x_lim=None,y_lim=None,x_space=False,y_space=True):

		xlim = ax.get_xlim()
		if x_lim[0] is None:
			x_lim[0] = xlim[0]
		if x_lim[1] is None:
			x_lim[1] = xlim[1]

		ylim = ax.get_ylim()
		if y_lim[0] is None:
			y_lim[0] = ylim[0]
		if y_lim[1] is None:
			y_lim[1] = ylim[1]

		# Neaten axis limits
		if x_lim is not None:
			delta=0
			if x_space:
				delta = 0.1*abs(x_lim[0]-x_lim[1])
			ax.set_xlim((x_lim[0]-delta,x_lim[1]+delta))
		if y_lim is not None:
			delta=0
			if y_space:
				delta = 0.1*abs(y_lim[0]-y_lim[1])
			ax.set_ylim((y_lim[0] - delta, y_lim[1] + delta))

	def twinx(self,ax=None,f=None):
		ax = self.__get_axes(ax)
		ax_twin = ax.twinx()

		def update(ax_0):
			ax_twin.set_ylim(*ax_0.get_ylim())
			g = (lambda x:x) if f is None else f
			ax_twin.set_yticklabels(g(ax_0.get_yticks()))

		ax.callbacks.connect('ylim_changed', update)
		update(ax)
		return ax_twin

	def twiny(self,ax=None,f=None):
		ax = self.__get_axes(ax)
		ax_twin = ax.twiny()

		def update(ax_0):
			ax_twin.set_xlim(*ax_0.get_xlim())
			g = (lambda x:x) if f is None else f
			ax_twin.set_xticklabels(g(ax_0.get_xticks()))

		ax.callbacks.connect('xlim_changed', update)
		update(ax)
		return ax_twin

	def savefig(self,filename,f=None,polish=True):
		fig = self.__get_figure(f)
		if polish:
			self.polish(fig)
		plt.savefig(filename)

class SampleStyle(MPLStyle):

	def set_params(self):
		plt.rc('text.latex',unicode=True)
		plt.rcParams['font.sans-serif'] = "sans-serif"
		plt.rcParams['text.latex.preamble'] = [r"\usepackage[greek,english]{babel} \usepackage{textcomp}",r"""\DeclareRobustCommand{\greektext}{%
			  \fontencoding{LGR}\selectfont\def\encodingdefault{LGR}}
			\DeclareRobustCommand{\textgreek}[1]{\leavevmode{\greektext #1}}
			\DeclareFontEncoding{LGR}{}{}
			\DeclareTextSymbol{\~}{LGR}{126}""",
			"""% New definition of square root:
			% it renames \sqrt as \oldsqrt
			\let\oldsqrt\sqrt
			% it defines the new \sqrt in terms of the old one
			\def\sqrt{\mathpalette\DHLhksqrt}
			\def\DHLhksqrt#1#2{%
			\setbox0=\hbox{$#1\oldsqrt{#2\,}$}\dimen0=\ht0
			\advance\dimen0-0.2\ht0
			\setbox2=\hbox{\vrule height\ht0 depth -\dimen0}%
			{\box0\lower0.4pt\box2}}"""] # TODO: FIX FONTS AND LATEX DEFINITIONS AGAIN
		plt.rcParams['figure.figsize'] = [6,3]

		plt.rcParams['legend.fontsize'] = 'small'
		plt.rcParams['legend.loc'] = 'best'

		plt.rcParams['text.usetex'] = True
		plt.rc('font', family='serif')
		plt.rcParams['axes.formatter.limits'] = [-2, 2]
		plt.rcParams['axes.titlesize'] = 14
		plt.rcParams['axes.labelsize'] = 12
		plt.rcParams['lines.linewidth'] = 2.
		plt.rcParams['axes.formatter.use_mathtext'] = True

		plt.rcParams['savefig.bbox'] = 'tight'
		plt.rcParams['savefig.pad_inches'] = 0.2
		plt.rcParams['savefig.transparent'] =  True

	def _polish(self,f):
		# Handle properties of axes directly
		#a = plt.gca() # Current set of axes
		formatter_scalar = ScalarFormatter(useOffset=True,useMathText=False)
		formatter_scalar.set_powerlimits((-3,3))
		formatter_log = LogFormatterMathtext(base=10.0,labelOnlyBase=False)

		# Neaten axes formatters
		for ax in f.get_axes():

			if not isinstance(ax.xaxis.get_major_formatter(),NullFormatter):
				if ax.xaxis.get_scale() == "log":
					ax.xaxis.set_major_locator(LogLocator(base=10.0, subs=[1.0], numdecs=1))
					ax.xaxis.set_major_formatter(formatter_log)
				else:
					ax.xaxis.set_major_formatter(formatter_scalar)
			if not isinstance(ax.yaxis.get_major_formatter(),NullFormatter):
				if ax.yaxis.get_scale() == "log":
					ax.yaxis.set_major_locator(LogLocator(base=10.0, subs=[1.0], numdecs=1))
					ax.yaxis.set_major_formatter(formatter_log)
					#ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=[10], numdecs=1)) # why is this necessary?
				else:
					ax.yaxis.set_major_formatter(formatter_scalar)

class RevTexColumn(MPLStyle):

	def set_params(self):
		# Global properties
		plt.rcParams['figure.figsize'] = [3.8,2]
		plt.rcParams['text.latex.preamble'] = [r"\usepackage[greek,english]{babel} \usepackage{textcomp}",r"""\DeclareRobustCommand{\greektext}{%
			  \fontencoding{LGR}\selectfont\def\encodingdefault{LGR}}
			\DeclareRobustCommand{\textgreek}[1]{\leavevmode{\greektext #1}}
			\DeclareFontEncoding{LGR}{}{}
			\DeclareTextSymbol{\~}{LGR}{126}""",
			"""% New definition of square root:
			% it renames \sqrt as \oldsqrt
			\let\oldsqrt\sqrt
			% it defines the new \sqrt in terms of the old one
			\def\sqrt{\mathpalette\DHLhksqrt}
			\def\DHLhksqrt#1#2{%
			\setbox0=\hbox{$#1\oldsqrt{#2\,}$}\dimen0=\ht0
			\advance\dimen0-0.2\ht0
			\setbox2=\hbox{\vrule height\ht0 depth -\dimen0}%
			{\box0\lower0.4pt\box2}}"""]


		# Font sizes and styles
		plt.rcParams['text.usetex'] = True
		plt.rc('text.latex',unicode=True)
		plt.rcParams['font.sans-serif'] = "sans-serif"
		plt.rc('font', family='serif')
		plt.rcParams.update(
			{
				'font.size': 8,
				'xtick.labelsize': 9,
				'ytick.labelsize': 9,
				'axes.formatter.use_mathtext': True,
				'axes.titlesize': 14,
				'axes.labelsize': 10,

			}
		)

		# Axis ticks and styles
		plt.rcParams['axes.formatter.limits'] = [-2, 2]

		# Plot line widths / etc
		plt.rcParams['lines.linewidth'] = 2.

		# Legend
		plt.rcParams['legend.fontsize'] = 'small'
		plt.rcParams['legend.loc'] = 'best'

		# Savefig
		plt.rcParams.update(
			{
				'savefig.bbox': 'tight',
				'savefig.pad_inches': 0,
				'savefig.transparent': True
			}
		)

	def _polish(self,f):
		# Handle properties of axes directly
		#a = plt.gca() # Current set of axes
		formatter_scalar = ScalarFormatter(useOffset=True,useMathText=False)
		formatter_scalar.set_powerlimits((-3,3))
		formatter_log = LogFormatterMathtext(base=10.0,labelOnlyBase=False)

		# Neaten axes formatters
		for ax in f.get_axes():

			if not isinstance(ax.xaxis.get_major_formatter(),NullFormatter):
				if ax.xaxis.get_scale() == "log":
					ax.xaxis.set_major_locator(LogLocator(base=10.0, subs=[1.0], numdecs=1))
					ax.xaxis.set_major_formatter(formatter_log)
				else:
					ax.xaxis.set_major_formatter(formatter_scalar)
			if not isinstance(ax.yaxis.get_major_formatter(),NullFormatter):
				if ax.yaxis.get_scale() == "log":
					ax.yaxis.set_major_locator(LogLocator(base=10.0, subs=[1.0], numdecs=1))
					ax.yaxis.set_major_formatter(formatter_log)
					#ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=[10], numdecs=1)) # why is this necessary?
				else:
					ax.yaxis.set_major_formatter(formatter_scalar)
