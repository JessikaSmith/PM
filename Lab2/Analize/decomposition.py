from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.manifold import SpectralEmbedding
from Lab2.Vis import *
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.model_selection import cross_val_score
import pandas as pd
from factor_analyzer import FactorAnalyzer


def calculate_loadings(pca):
    return pca.components_.T * np.sqrt(pca.explained_variance_)


class DimRed:

    def __init__(self, sample):
        self.sample = StandardScaler().fit_transform(sample)

    def covariances_matrix(self):
        return self.sample.T*self.sample/((len(self.sample[0]))-1)

    def svd(self):
        u, s, v = np.linalg.svd(self.sample.T)
        return u, s, v

    def compute_scores(self, max_n):
        n_components = np.arange(0, max_n, 1)
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
        n_components = np.arange(0, max_n, 1)
        pca_scores, fa_scores = self.compute_scores(max_n)
        print("pca_scores", pca_scores)
        print("fa_scores", fa_scores)
        n_components_pca = n_components[np.argmax(pca_scores)]
        n_components_fa = n_components[np.argmax(fa_scores)]
        self.select_n(max_n)
        if n_components_pca == n_components_fa:
            return n_components_pca
        else:
            return [n_components_pca, n_components_fa]

    def select_n(self, n):
        U, S, V = self.svd()
        eigvals = S ** 2 / np.cumsum(S)[-1]
        plot_n_selection(eigvals, 'scree_plot', n)

    def pca_svd(self, n):
        pca = PCA(n_components=n)
        pca.fit(list(self.sample))
        # factor loadings
        print(calculate_loadings(pca))
        # principal components scores
        eigen_vectors = pd.DataFrame(pca.components_.T)
        #print(eigen_vectors)
        #draw_heatmap(eigen_vectors, "PCA eigenvectors (svd)")

        print(pca.components_)
        pca_res = pca.fit_transform(list(self.sample))
        draw_heatmap(pca_res, "Scores")
        print(pca_res)
        # plot_components(pca_res, 'svd_components')

    def spectral_emb(self, n):
        semb = SpectralEmbedding(n_components=n)
        semb.fit(self.sample)
        semb_res = semb.fit_transform(self.sample)
        # plot_components(semb_res, 'spectr_emb_components')

    def fa(self, n):
        fa = FactorAnalysis(n_components=n)
        fa.fit(self.sample)
        print('fa_components: ',fa.components_)
        fa = FactorAnalyzer()
        fa.analyze(pd.DataFrame(data=self.sample),
                   n_factors=n,
                   method='minres')
        draw_heatmap(fa.loadings, "Loadings")

    def variance_explained(self, num_comp = 20):
        # covariance matrix
        cov_mat = np.cov(self.sample.T)
        eig_vals, eig_vecs = np.linalg.eig(cov_mat)
        print('Covariance matrix: \n%s' % cov_mat)
        print('Eigenvectors \n%s' % eig_vecs)
        print('\nEigenvalues \n%s' % eig_vals)
        eigen_vectors_df = pd.DataFrame(eig_vecs.T[:num_comp])
        draw_heatmap(eigen_vectors_df.T, "PCA eigenvectors (eigendecomposition)")
        u, s, v = self.svd()
        # draw_heatmap(s.T, "PCA eigenvectors (svd)")
        tot = sum(eig_vals)
        var_exp = [(i / tot) * 100 for i in sorted(eig_vals, reverse=True)]
        cum_var_exp = np.cumsum(var_exp)
        plot_explained_variance(var_exp, cum_var_exp, num_comp)