import numpy as np
import pandas as pd
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def graph(lhs,
          rhs,
          support,
          confidence,
          lift,
          data=None,
          fig_scale=2,
          font_size=None,
          cmap=None):
    if data is None:
        data = pd.DataFrame(
            dict(
                lhs=lhs,
                rhs=rhs,
                support=support,
                confidence=confidence,
                lift=lift))
        lhs = 'lhs'
        rhs = 'rhs'
        support = 'support'
        confidence = 'confidence'
        lift = 'lift'
    centers = data[lhs].unique()
    graphs = centers.size
    rows = np.ceil(np.sqrt(graphs)).astype(int)
    cols = np.ceil(graphs / rows).astype(int)
    g = nx.DiGraph()
    fig, axes = plt.subplots(
        rows, cols, figsize=(cols * fig_scale, rows * fig_scale))
    data.loc[:, support] = data[support] / data[support].max() * 500

    for i, ((row, col), ax) in enumerate(np.ndenumerate(axes)):
        ax.axis('off')
        if col == cols - 1:
            divider = make_axes_locatable(ax)
            width = 0.25
            cax = divider.append_axes("right", size=width, pad=0.25)
            cbar = fig.colorbar(pc, cax=cax)
            cbar.set_label('lift', size=font_size)
            cbar.ax.tick_params(labelsize=font_size)
        if i >= graphs:
            continue
        center = centers[i]
        g = nx.DiGraph()
        g.add_node(center, label=', '.join(center), size=0, color=0)
        for node in data.loc[data[lhs] == center, rhs]:
            name = (center, node)
            index = data.index[(data[lhs] == center) & (data[rhs] == node)]
            g.add_node(
                name,
                label=', '.join(node),
                size=data.loc[index, support],
                color=data.loc[index, lift])
            g.add_edge(
                center, name, weight=data.loc[index, confidence].values[0])
        pos = nx.spring_layout(g)
        pos[center] = np.zeros(2)
        nodelist = g.nodes
        sizes = nx.get_node_attributes(g, 'size')
        node_size = np.array([sizes[key] for key in nodelist])
        colors = nx.get_node_attributes(g, 'color')
        node_color = [colors[key] for key in nodelist]
        vmax = np.abs(data[lift]).max()
        vmin = -vmax
        pc = nx.draw_networkx_nodes(
            g,
            pos,
            node_size=node_size,
            node_color=node_color,
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            ax=ax)
        labels = nx.get_node_attributes(g, 'label')
        nx.draw_networkx_labels(g, pos, labels, font_size=font_size, ax=ax)
        edgelist = g.edges
        weights = nx.get_edge_attributes(g, 'weight')
        edge_width = np.array([weights[key] for key in edgelist
                               ]) / data[confidence].max() * 3
        nx.draw_networkx_edges(g, pos, width=edge_width, alpha=0.5, ax=ax)
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        ax.set(
            xlim=[-np.abs(xlim).max(), np.abs(xlim).max()],
            ylim=[-np.abs(ylim).max(), np.abs(ylim).max()])
        pc.set(clip_on=False)
        for child in ax.get_children():
            if isinstance(child, mpl.text.Text):
                child.set(clip_on=False)
        nx.draw_networkx_nodes()
    plt.show()
