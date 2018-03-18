from plotly.plotly import image
from plotly.offline import download_plotlyjs, plot
import plotly.graph_objs as go
import numpy as np

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
    image.save_as(fig, filename=path_to_figure + title + '.jpeg')
