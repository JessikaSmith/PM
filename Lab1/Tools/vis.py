from plotly.plotly import image
from plotly.offline import download_plotlyjs, plot
import plotly.graph_objs as go
import numpy as np
import statsmodels.api as sm
import pylab

# test
from scipy.stats import norm
import matplotlib.pyplot as plt

path_to_figure = 'Figures\\'


def plot_histogram(sample, name):
    x = np.array(sample)
    data = [go.Histogram(x=x, histnorm='probability',autobinx=False,
                         xbins=dict(start=0, end=26, size=26 / 18))]
    layout = dict(
        xaxis=dict(title="values")
    )
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename=name + '.html')
    # image.save_as(fig, filename=path_to_figure + name)


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


def sample_plot(sample, x, y, name, nbinsx=20):
    sample = np.array(sample)
    trace = [go.Scatter(
        x=np.array(x),
        y=np.array(y),
    )]
    layout = dict(
        xaxis=dict(title="values")
    )
    data = [go.Histogram(x=sample, histnorm='probability', nbinsx=nbinsx)]
    data += trace
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename=name + ".html")
    # image.save_as(fig, filename=path_to_figure + name)


def plot_on_one_graph(sample, xx, y, name, kernels):
    # x = np.array(sample)
    trace_list = []
    for t in range(len(y)):
        xr = np.array(xx)
        z = np.array(y[t])
        trace_list += [go.Scatter(
            x=xr,
            y=z,
            name=kernels[t]
        )]
    # data = [go.Histogram(x=x, histnorm='probability')]
    data = trace_list
    fig = go.Figure(data=data)
    plot(fig, name + ".html")
    # image.save_as(fig, filename=path_to_figure + name)


def q_q_biplot_test(sample, theory_params, name):
    sm.qqplot(np.array(sample), line='s', loc=theory_params[0], scale=theory_params[1])
    pylab.savefig(path_to_figure + name, bbox_inches='tight')


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
    plot(fig)
    # image.save_as(fig, filename=path_to_figure + name)


def _test_print_norm(m, s, int):
    fig, ax = plt.subplots(1, 1)
    int = np.linspace(0, 26, 26)
    print(norm.pdf(int, loc=m, scale=s))
    # ax.plot(int, norm.pdf(int, loc=m, scale=s), 'r-', lw=5, alpha=0.6, label='norm pdf')
    # fig.show()
