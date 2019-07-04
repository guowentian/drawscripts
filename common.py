import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import pickle
import os
import pylab
import matplotlib
import csv
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import LinearLocator

# convert from 0-255 byte format to [0,1] float format
def convert_color_map(map):
    ret = []
    for tuple in map:
        new_tuple = (tuple[0] / 255.0, tuple[1] / 255.0, tuple[2] / 255.0)
        ret.append(new_tuple)
    return ret

OPT_FONT_NAME = 'Helvetica'
TICK_FONT_SIZE = 13
LABEL_FONT_SIZE = 13
TITLE_FONT_SIZE = 16
LEGEND_FONT_SIZE = 16
LABEL_FP = FontProperties(style='normal', size=LABEL_FONT_SIZE)
LEGEND_FP = FontProperties(style='normal', size=LEGEND_FONT_SIZE)
TICK_FP = FontProperties(style='normal', size=TICK_FONT_SIZE)

MARKERS = (['o', 's', 'v', "^", "h", "v", ">", "x", "d", "<", "|", "", "|", "_"])
# you may want to change the color map for different figures
# a dark color scheme
COLOR_MAP = ('#F15854', '#5DA5DA', '#60BD68',  '#B276B2', '#DECF3F', '#F17CB0', '#B2912F', '#FAA43A', '#AFAFAF')
# a light color scheme obtained from http://tableaufriction.blogspot.com/2012/11/finally-you-can-use-tableau-data-colors.html
# COLOR_MAP = convert_color_map(((174,199,232), (255,187,120), (152, 223, 138), (255,152,150), (197, 176, 213), (247,182,210)))
# you may want to change the patterns for different figures
PATTERNS = ([ "//", "\\\\", "////", "o", "\\\\", "o", "//", "..", "o", "\\\\", "//"])
LABEL_WEIGHT = 'bold'
LINE_WIDTH = 3.0
MARKER_SIZE = 0.0
MARKER_FREQUENCY = 1000

# By default matplotlib use type 3 font, which is not appreciated by many publishers.
# Thus, we force to use type 1.
# matplotlib.rcParams['ps.useafm'] = True
# matplotlib.rcParams['pdf.use14corefonts'] = True
# We can also force to use type 42 (a.k.a TrueType). type 42 seems more advanced and modern than type 1.
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
# LaTex has powerful support to typeset the complex formulas, and we can enable it by this setting.
# But in most of the cases, we simply use the built-in mathtext that is enough to represent many formulas.
# matplotlib.rcParams['text.usetex'] = True

# font size and family
matplotlib.rcParams['xtick.labelsize'] = TICK_FONT_SIZE
matplotlib.rcParams['ytick.labelsize'] = TICK_FONT_SIZE
matplotlib.rcParams['axes.titlesize'] = TITLE_FONT_SIZE
matplotlib.rcParams['axes.labelsize'] = LABEL_FONT_SIZE
matplotlib.rcParams['legend.fontsize'] = LEGEND_FONT_SIZE
#matplotlib.rcParams['font.family'] = OPT_FONT_NAME

# there are some embedding problems if directly exporting the pdf figure using matplotlib.
# so we generate the eps format first and convert it to pdf.
def ConvertEpsToPdf(dir_filename):
  os.system("epstopdf --outfile " + dir_filename + ".pdf " + dir_filename + ".eps")
  os.system("rm -rf " + dir_filename + ".eps")

# set the text label indicating the speedups of cur versus base for each rectangle
def label_times(ax, rects, base, cur):
    for idx, rect in enumerate(rects):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1 * (height),
                'x%.1f' % float(cur[idx] / base[idx]),
                ha='center', va='bottom', size=8.5, rotation=0)

# read csv file copied from excel
def read_file_universal(filename):
    data = []
    # When we copy the cells from excel and paste into a text file,
    # the text file is mixed with unrecognized newline character that
    # we cannot read with the normal csv reader.
    # Thus, we have to read in the universal mode
    with open(filename, "rU") as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')
        for row in rows:
            float_list = []
            for str in row:
                float_list.append(float(str))
            data.append(float_list)
    return data

# add the legend for the figure (with multiple subfigures)
# using the given patterns and colors
def add_legend(legend_labels, color_map=COLOR_MAP, patterns=PATTERNS, fontsize=LEGEND_FONT_SIZE, ncol=None):
    handles = []
    for i in range(len(legend_labels)):
        handles.append(mpatches.Patch(hatch=patterns[i], facecolor=color_map[i], edgecolor='black'))
    if ncol == None:
        ncol = len(legend_labels)
    fig_leg = plt.figlegend(labels=legend_labels,
                            loc='lower center',
                            handles=handles,
                            ncol=ncol,
                            fontsize=fontsize)
    fig_leg.get_frame().set_edgecolor('black')

# Used to permutate a list so that we can use a different orders of
# COLOR_MAP and PATTERNS
def get_reorder_list(i, list):
    ret = []
    for j in range(len(list)):
        p = (i+j) % len(list)
        ret.append(list[p])
    return ret