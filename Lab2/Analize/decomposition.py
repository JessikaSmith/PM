from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.manifold import SpectralEmbedding
from Lab2.Vis import *
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.model_selection import cross_val_score
import pandas as pd


def calculate_loadings(pca):
    return pca.components_.T * np.sqrt(pca.explained_variance_)


class DimRed:

    def __init__(self, sample):
        self.sample = StandardScaler().fit_transform(sample)

    def svd(self):
        u, s, v = np.linalg.svd(self.sample.T)
        return u, s, v

    def compute_scores(self, max_n):
        n_components = np.arange(0, max_n, 5)
        pca = PCA(svd_solver='full')
        fa = FactorAnalysis()
        pca_scores, fa_scores = [], []
        for n in n_components:
            pca.n_components = n
            fa.n_components = n
            pca_scores.append(np.mean(cross_val_score(pca, self.sample)))
            fa_scores.append(np.mean(cross_val_score(fa, self.sample)))
        return pca_scores, fa_scores

    def select_num_comp(self, max_n):
        n_components = np.arange(0, max_n, 5)
        pca_scores, fa_scores = self.compute_scores(max_n)
        print("pca_scores", pca_scores)
        print("fa_scores", fa_scores)
        n_components_pca = n_components[np.argmax(pca_scores)]
        n_components_fa = n_components[np.argmax(fa_scores)]
        self.select_n()
        if n_components_pca == n_components_fa:
            return n_components_pca
        else:
            return [n_components_pca, n_components_fa]

    def select_n(self):
        U, S, V = np.linalg.svd(self.sample)
        eigvals = S ** 2 / np.cumsum(S)[-1]
        plot_n_selection(eigvals, 'scree_plot', 7)

    def pca_svd(self, n):
        pca = PCA(n_components=n)
        pca.fit(list(self.sample))
        # factor loadings
        print(calculate_loadings(pca))
        # principal components scores
        eigen_vectors = pd.DataFrame(pca.components_.T)
        draw_heatmap(eigen_vectors, "PCA eigenvectors")
        print(pca.components_)
        pca_res = pca.fit_transform(list(self.sample))
        # plot_components(pca_res, 'svd_components')

    def spectral_emb(self, n):
        semb = SpectralEmbedding(n_components=n)
        semb.fit(self.sample)
        semb_res = semb.fit_transform(self.sample)
        # plot_components(semb_res, 'spectr_emb_components')

    def fa(self, n):
        fa = FactorAnalysis(n_components=n)
        fa.fit(self.sample)
        print(fa.components_)

    def variance_explained(self):
        # covariance matrix
        cov_mat = np.cov(self.sample.T)
        eig_vals, eig_vecs = np.linalg.eig(cov_mat)
        print('Covariance matrix: \n%s' % cov_mat)
        print('Eigenvectors \n%s' % eig_vecs)
        print('\nEigenvalues \n%s' % eig_vals)
        self.svd()
        tot = sum(eig_vals)
        var_exp = [(i / tot) * 100 for i in sorted(eig_vals, reverse=True)]
        cum_var_exp = np.cumsum(var_exp)
        plot_explained_variance(var_exp, cum_var_exp)