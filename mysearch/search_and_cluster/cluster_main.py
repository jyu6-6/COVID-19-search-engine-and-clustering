from mysearch import search_and_cluster


from mysearch.search_and_cluster import cluster_prep

data, X = cluster_prep.prep()  # X is the matrix after text vectorization

def get_results_clusters(results_id):
    results_clusters = {}
    clusters = data.loc[data['paper_id'].isin(results_id)].groupby(['named_cluster']).sum().index
    for c in clusters:
        results_clusters[c] = data.loc[data['named_cluster'] == c, 'paper_id'].tolist()
    return results_clusters


from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TKAgg',warn=False, force=True)
import seaborn as sns
pca = PCA(n_components=0.95, random_state=42)
tsne = TSNE(verbose=1, perplexity=100, random_state=42, learning_rate=10)
def plot_clusters(results_id):
    global X
    idx = data.loc[data['paper_id'].isin(results_id)].index
    y = data.loc[data['paper_id'].isin(results_id), 'named_cluster'].tolist()
    y = np.array(y)
    X_embedded = X[idx, :]
    X_embedded = pca.fit_transform(X_embedded)
    X_embedded = tsne.fit_transform(X_embedded)
    # sns settings
    sns.set(rc={'figure.figsize': (8, 5)})
    sns.set_style("white")
    # colors
    palette = sns.hls_palette(np.unique(y).shape[0], l=.4, s=.9)
    # plot
    ax1 = sns.scatterplot(X_embedded[:, 0], X_embedded[:, 1], hue=y, legend='full', palette=palette)
    ax1.legend(loc='center right', bbox_to_anchor=(1.6, 0.5), ncol=1)
    ax1.set_title('Cluster distribution of your search results')
    fig = ax1.get_figure()
    fig.savefig("mysearch/static/mysearch/improved_cluster_tsne.png")
    #plt.show()
    return


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords
stopwords = set(STOPWORDS)
def plot_wordcloud(results_id):
    text = data.loc[data['paper_id'].isin(results_id), 'processed_text'].tolist()
    dt_cloud = WordCloud(stopwords=stopwords, background_color='white').generate(' '.join(text))
    fig, ax = plt.subplots(figsize=(10, 6.18))
    ax.imshow(dt_cloud, interpolation='bilinear')
    ax.set_title(' ')
    ax.axis('off')
    fig.savefig("mysearch/static/mysearch/word_cloud.png")
    #plt.show()
    return


