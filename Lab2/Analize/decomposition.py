import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import SpectralEmbedding
from Lab2.Vis import *
from sklearn.preprocessing import StandardScaler
import numpy as np

class DimRed:

    def __init__(self, sample):
        self.sample = sample

    def preprocess(self):
        return StandardScaler().fit_transform(self.sample.values)

    def select_n(self):
        data = self.preprocess()
        U, S, V = np.linalg.svd(data)
        eigvals = S ** 2 / np.cumsum(S)[-1]
        plot_n_selection(eigvals, 'scree_plot')

    def pca_svd(self, n):
        pca = PCA(n_components=n)
        data = self.preprocess()
        pca.fit(list(data))
        print(pca.explained_variance_)
        print(len(pca.components_[0]))
        pca_res = pca.fit_transform(list(data))
        #plot_components(pca_res, 'svd_components')

    def spectral_emb(self, n):
        semb = SpectralEmbedding(n_components=n)
        data = self.preprocess()
        semb.fit(data)
        semb_res = semb.fit_transform(data)
        #plot_components(semb_res, 'spectr_emb_components')
