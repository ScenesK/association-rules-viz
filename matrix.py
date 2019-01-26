import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def matrix(lhs, rhs, size, data=None, color=None, cmap=None, font_size=None):
    if data is not None:
        rows = data[rhs].unique().tolist()
        columns = data[lhs].unique().tolist()
        lhs = data[lhs]
        rhs = data[rhs]
        size = data[size]
        if color:
            color = data[color]
    else:
        rows = pd.Series(rhs).unique().tolist()
        columns = pd.Series(lhs).unique().tolist()
    items = len(size)
    x = np.zeros(items)
    y = np.zeros(items)
    s = np.zeros(items)
    for i in range(items):
        x[i] = columns.index(lhs[i])
        y[i] = rows.index(rhs[i])
        s[i] = size[i] / max(size) * font_size * 15
    if color is not None and (min(color) < 0 or max(color) > 1):
        vmax = np.abs(color).max()
        vmin = -vmax
    else:
        vmax = 1
        vmin = 0

    fig = plt.figure()
    size_per_char = font_size / fig.dpi * 2
    fig.set(
        size_inches=(len(columns) * size_per_char, len(rows) * size_per_char))
    ax = fig.gca()
    pc = ax.scatter(
        x, y, marker='o', s=s, c=color, vmin=vmin, vmax=vmax, cmap=cmap)
    divider = make_axes_locatable(ax)
    width = font_size / fig.dpi / fig.get_figheight()
    cax = divider.append_axes("right", size=width, pad=width * 0.5)
    cbar = fig.colorbar(pc, cax=cax)
    ax.set(
        xlabel='LHS',
        ylabel='RHS',
        xticks=np.arange(len(columns)),
        yticks=np.arange(len(rows)),
        xticklabels=[set(i) for i in columns],
        yticklabels=[set(i) for i in rows])
    ax.xaxis.label.set(size=font_size)
    ax.yaxis.label.set(size=font_size)
    ax.tick_params(labelsize=font_size)
    ax.xaxis.set_tick_params(rotation=90)
    cbar.ax.tick_params(labelsize=font_size)
    plt.show()
