from plotly.plotly import image
from plotly.offline import download_plotlyjs, plot
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

path_to_figure = 'Figures\\'


def plot_components(components, title):
    trace = go.Scatter(
        x=np.array(components[:, 0]),
        y=np.array(components[:, 1]),
        mode='markers'
    )
    layout = dict(
        title='Components',
        xaxis=dict(title='1st component'),
        yaxis=dict(title='2nd component')
    )
    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename=title + '.html')
    # image.save_as(fig, filename=path_to_figure + title + '.jpeg')


def plot_n_selection(eigvalues, title, num=7):
    trace = go.Scatter(
        x=np.array([i for i in range(1, num + 1)]),
        y=np.array(eigvalues[:num]),
    )
    layout = dict(
        title='Scree Plot',
        xaxis=dict(title='Principal Component'),
        yaxis=dict(title='Eigenvalue')
    )
    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename=title + '.html')
    # image.save_as(fig, filename=path_to_figure + title + '.jpeg')


def plot_explained_variance(var_exp, cum_var_exp):
    trace1 = go.Bar(
        x=['PC %s' % i for i in range(1, 7)],
        y=var_exp,
        showlegend=False)
    trace2 = go.Scatter(
        x=['PC %s' % i for i in range(1, 7)],
        y=cum_var_exp,
        name='cumulative explained variance')
    data = [trace1, trace2]
    layout = go.Layout(
        yaxis=dict(title='Explained variance in percent'),
        title='Explained variance by different principal components')
    fig = go.Figure(data=data, layout=layout)
    plot(fig)


def draw_heatmap(df, title):
    ax = plt.axes()
    sns.heatmap(df)
    ax.set_title(title)
    plt.show()
