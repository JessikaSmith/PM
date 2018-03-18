import numpy as np
from sklearn.decomposition import PCA

class DimRed:

    def __init__(self, sample):
        self.sample = sample

    def pca(self, n):
        pca = PCA(n_components=n)
        print(list(self.sample.values))
        pca.fit(list(self.sample.values))
        print(pca.explained_variance_ratio_)
        pca_res = pca.fit_transform(list(self.sample.values))


    # def