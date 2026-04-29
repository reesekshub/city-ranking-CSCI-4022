import load_data as ld
from itertools import combinations
import sklearn.cluster as cluster
import sklearn.mixture as mixture

# load dataframes
diff_df = ld.load_comparison_data("./data/modality_deltas")
ratio_df = ld.load_comparison_data("./data/bike_over_drive")
ratio_df.dropna(inplace=True)
unlabeled_diff_df = diff_df.copy()
unlabeled_diff_df = unlabeled_diff_df.apply(lambda x: sorted(x), axis=1, result_type="expand")

# Compute all calculated K-means clusters
def generate_kmeans_clusters():
    cluster_labels = [] # list of clusters, each of which is a list of cities in that cluster
    # diff clusters, n_clusters = 5, determined by elbow method in kmeans_cluster.ipynb
    n_diff_clusters = 5
    km = cluster.KMeans(n_clusters=n_diff_clusters, random_state=0)
    km.fit(diff_df)
    # add clusters in city list form to cluster_labels
    for i in range(n_diff_clusters):
        cluster_labels.append(diff_df.index[km.labels_ == i].tolist())

    # ratio clusters, n_clusters = 6
    n_ratio_clusters = 6
    km = cluster.KMeans(n_clusters=n_ratio_clusters, random_state=0)
    km.fit(ratio_df)
    # add clusters in city list form to cluster_labels
    for i in range(n_ratio_clusters):
        cluster_labels.append(ratio_df.index[km.labels_ == i].tolist())


    # unlabeled diff clusters, n_clusters = 5
    n_unlabeled_diff_clusters = 5
    km = cluster.KMeans(n_clusters=n_unlabeled_diff_clusters, random_state=0)
    km.fit(unlabeled_diff_df)
    # add clusters in city list form to cluster_labels
    for i in range(n_unlabeled_diff_clusters):
        cluster_labels.append(unlabeled_diff_df.index[km.labels_ == i].tolist())

    return cluster_labels

# compute GMM Clusters
def generate_gmm_clusters() -> list:
    cluster_labels = [] # list of clusters, each of which is a list of cities in that cluster
    # diff clusters, n_components = 14, determined by AIC/BIC in gmm_cluster.ipynb
    n_diff_clusters = 14
    gmm = mixture.GaussianMixture(n_components=n_diff_clusters, random_state=42, reg_covar = 1e-3)
    gmm.fit(diff_df)
    # add clusters in city list form to cluster_labels
    for i in range(n_diff_clusters):
        cluster_labels.append(diff_df.index[gmm.predict(diff_df) == i].tolist())

    # ratio clusters, n_components = 10
    n_ratio_clusters = 10
    gmm = mixture.GaussianMixture(n_components=n_ratio_clusters, random_state=42, reg_covar = 1e-5)
    gmm.fit(ratio_df)
    # add clusters in city list form to cluster_labels
    for i in range(n_ratio_clusters):
        cluster_labels.append(ratio_df.index[gmm.predict(ratio_df) == i].tolist())

    # unlabeled diff clusters, n_components = 8
    n_unlabeled_diff_clusters = 8
    gmm = mixture.GaussianMixture(n_components=n_unlabeled_diff_clusters, random_state=42, reg_covar = 1e-3)
    gmm.fit(unlabeled_diff_df)
    # add clusters in city list form to cluster_labels
    for i in range(n_unlabeled_diff_clusters):
        cluster_labels.append(unlabeled_diff_df.index[gmm.predict(unlabeled_diff_df) == i].tolist())

    return cluster_labels


# Generate frequent itemsets of size n from a cluster
# basically just combinations of cluster
# if this is super slow I'll revisit it
def generate_frequent_itemsets(cluster, n):
    itemsets = [list(comb) for comb in combinations(cluster, n)]
    return itemsets



