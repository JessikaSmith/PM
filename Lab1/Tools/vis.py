"""

"""

from plotly.plotly import image
from plotly.offline import download_plotlyjs, plot
import plotly.graph_objs as go
import numpy as np

# test
from scipy.stats import norm
import matplotlib.pyplot as plt

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
    data = trace_list
    fig = go.Figure(data=data)
    plot(fig)
    # image.save_as(fig, filename=path_to_figure + name)


def q_q_biplot(sample, theory, name):
    trace1 = go.Scatter(
        x=np.array(theory),
        y=np.array(sample),
        mode='markers'
    )
    trace2 = go.Scatter(
        x=np.array(theory),
        y=np.array(theory),
        mode='line'
    )
    layout = dict(
        xaxis=dict(title='Theoretical'),
        yaxis=dict(title='Sample')
    )
    fig = go.Figure(data=[trace1, trace2], layout=layout)

    image.save_as(fig, filename=path_to_figure + name)


def _test_print_norm(m, s, int):
    fig, ax = plt.subplots(1, 1)
    int = np.linspace(0, 26, 26)
    print(norm.pdf(int, loc=m, scale=s))
    #ax.plot(int, norm.pdf(int, loc=m, scale=s), 'r-', lw=5, alpha=0.6, label='norm pdf')
    #fig.show()
