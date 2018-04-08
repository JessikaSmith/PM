from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.decomposition import PCA
from Lab3.Visualization import *

class Clustering:

    def __init__(self, data, y):
        self.data = data
        self.target = y

    def pca(self, n):
        pca = PCA(n_components=n)
        pca.fit(self.data.values)
        pca_res = pca.fit_transform(list(self.data.values))
        return pca_res


    def dbscan(self, **kwargs):
        db = DBSCAN(eps=0.5, min_samples=5,
                               metric='euclidean', metric_params=None, algorithm='auto')
        db.fit(self.data)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels_true = self.target
        labels = db.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        print('Estimated number of clusters: %d' % n_clusters_)
        print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
        print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
        print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
        print("Adjusted Rand Index: %0.3f"
              % metrics.adjusted_rand_score(labels_true, labels))
        print("Adjusted Mutual Information: %0.3f"
              % metrics.adjusted_mutual_info_score(labels_true, labels))
        print("Silhouette Coefficient: %0.3f"
              % metrics.silhouette_score(self.data, labels))
        reduced_data = self.pca(2)
        # plot_clusters(reduced_data, n_clusters_, labels, core_samples_mask)


    def kmedoids(self):
        pass

    def agglomerative(self):
        sklearn.cluster.AgglomerativeClustering(n_clusters=2, affinity='euclidean', memory = None,
                                                connectivity = None, compute_full_tree ='auto',
                                                linkage ='ward')

