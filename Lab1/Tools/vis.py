"""

"""

from plotly.offline import download_plotlyjs, plot
import plotly.graph_objs as go
import numpy as np

path_to_figure = 'Figures\\'

def plot_histogram(sample, name):

    x = np.array(sample)
    data = [go.Histogram(x=x)]
    plot(data, filename=path_to_figure+name)

    return

def plot_kernel_density(sample, y, name):

    x = np.array(sample)
    y = np.array(y)
    trace = go.Scatter(
        x=x,
        y=y
    )
    data = [trace]
    plot(data, filename=path_to_figure+name)


def plot_on_one_graph(sample,xx, y, name, kernels):

    x = np.array(sample)
    trace_list = []
    for t in range(len(y)):
        xr = np.array(xx[t])
        z = np.array(y[t])
        trace_list += [go.Scatter(
            x=xr,
            y=z,
            name=kernels[t]
        )]
    data = [go.Histogram(x=x, name='sample')]
    data += trace_list
    plot(data, filename=path_to_figure + name)

