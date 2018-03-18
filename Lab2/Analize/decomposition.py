import numpy as np
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.manifold import SpectralEmbedding
from Lab2.Vis import *
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.model_selection import cross_val_score


def calculate_loadings(pca):
    return pca.components_.T * np.sqrt(pca.explained_variance_)


class DimRed:

    def __init__(self, sample):
        self.sample = sample

    def compute_scores(self, max_n):
        X = self.preprocess()
        n_components = np.arange(0, max_n, 5)
        pca = PCA(svd_solver='full')
        fa = FactorAnalysis()

        pca_scores, fa_scores = [], []
        for n in n_components:
            pca.n_components = n
            fa.n_components = n
            pca_scores.append(np.mean(cross_val_score(pca, X)))
            fa_scores.append(np.mean(cross_val_score(fa, X)))

        return pca_scores, fa_scores

    def select_num_comp(self,max_n):
        n_components = np.arange(0, max_n, 5)
        pca_scores, fa_scores = self.compute_scores(max_n)
        n_components_pca = n_components[np.argmax(pca_scores)]
        n_components_fa = n_components[np.argmax(fa_scores)]
        self.select_n()
        if n_components_pca == n_components_fa:
            return n_components_pca
        else:
            return [n_components_pca, n_components_fa]


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
        print(calculate_loadings(pca))
        # principal components scores
        pca.components_
        pca_res = pca.fit_transform(list(data))
        # plot_components(pca_res, 'svd_components')

    def spectral_emb(self, n):
        semb = SpectralEmbedding(n_components=n)
        data = self.preprocess()
        semb.fit(data)
        semb_res = semb.fit_transform(data)
        # plot_components(semb_res, 'spectr_emb_components')

    def fa(self, n):
        fa = SpectralEmbedding(n_components=n)
