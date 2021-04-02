# TODO: Implement Spectral Clustering as given in https://arxiv.org/abs/1710.10468

from spectralcluster import SpectralClusterer


class SpectralClustering():
    """docstring for SpectralClustering"""
    def __init__(self, min_clusters, max_clusters, p_percentile, gaussian_blur_sigma):
        self.clusterer = SpectralClusterer(
            min_clusters=min_clusters,
            max_clusters=max_clusters,
            p_percentile=p_percentile,
            gaussian_blur_sigma=gaussian_blur_sigma
        )
        

    # N x D array containing data samples to be clustered
    def predict(self, data):
        return self.clusterer.predict(data)
