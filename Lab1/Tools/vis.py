"""

"""

from plotly.plotly import image
from plotly.offline import download_plotlyjs, plot
import plotly.graph_objs as go
import numpy as np

path_to_figure = 'Figures\\'


def plot_histogram(sample, name):
    x = np.array(sample)
    data = [go.Histogram(x=x)]
    fig = go.Figure(data=data)
    image.save_as(fig, filename=path_to_figure + name)


def plot_kernel_density(sample, y, name):
    x = np.array(sample)
    y = np.array(y)
    trace = go.Scatter(
        x=x,
        y=y
    )
    data = [trace]
    fig = go.Figure(data=data)
    image.save_as(fig, filename=path_to_figure + name)


def plot_on_one_graph(sample, xx, y, name, kernels):
    print(y)
    x = np.array(sample)
    trace_list = []
    for t in range(len(y)):
        xr = np.array(xx)
        z = np.array(y[t])
        trace_list += [go.Scatter(
            x=xr,
            y=z,
            name=kernels[t]
        )]
    data = [go.Histogram(x=x, name='sample')]
    data += trace_list
    fig = go.Figure(data=data)
    image.save_as(fig, filename=path_to_figure + name)


def q_q_biplot(sample, theory, name):
    trace = go.Scatter(
        x=np.array(theory),
        y=np.array(sample),
        mode='markers'
    )
    layout = dict(
        xaxis=dict(title='Theoretical'),
        yaxis=dict(title='Sample')
    )
    fig = go.Figure(data=[trace], layout=layout)

    image.save_as(fig, filename=path_to_figure + name)

