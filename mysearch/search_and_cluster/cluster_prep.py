from mysearch import search_and_cluster

from mysearch.search_and_cluster import data_cleaning



import time
tic = time.time()
# data loading and preprocessing
file_path = '/Users/taylorw/Desktop/CS525/project/biorxiv_medrxiv_clean.csv'
data = data_cleaning.data_loader(file_path)
data = data_cleaning.clean_title(data)
data = data_cleaning.clean_abstract(data)
data = data_cleaning.drop_missing(data)
data = data_cleaning.fill_nulls(data)


# clustering prep
import string
import collections
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

results_text = data.text.tolist()

stop_words = stopwords.words('english') + ['abov', 'ani', 'arent', 'becaus', 'becau', 'befor', 'couldnt', 'didnt',
                                           'doe', 'doesnt', 'dont', 'dure', 'ha', 'hadnt', 'hasnt', 'havent', 'hi',
                                           'isnt', 'mightnt', 'mustnt', 'neednt', 'onc', 'onli', 'ourselv', 'shant',
                                           'shouldnt', 'shouldv', 'thatll', 'themselv', 'thi', 'veri', 'wa', 'wasnt',
                                           'werent', 'whi', 'wont', 'wouldnt', 'youd', 'youll', 'yourselv', 'youv'] + [
                 'czi', 'elsevier', 'pmc', 'shes', 'shouldve', 'youre', 'youve']

custom_stop_words = [
    'doi', 'preprint', 'copyright', 'peer', 'reviewed', 'org', 'https', 'et', 'al', 'author', 'figure',
    'rights', 'reserved', 'permission', 'used', 'using', 'biorxiv', 'medrxiv', 'license', 'fig', 'fig.',
    'al.', 'Elsevier', 'PMC', 'CZI', 'www'
]

for w in custom_stop_words:
    if w not in stop_words:
        stop_words.append(w)


def process_text(text, stem=False):
    """ Tokenize text and stem words removing punctuation """
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)

    if stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]

    return tokens


def cluster_results(texts, clusters=20):
    """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means """
    vectorizer = TfidfVectorizer(tokenizer=process_text,
                                 analyzer='word',
                                 stop_words=stop_words,
                                 max_df=0.5,
                                 min_df=0.1,
                                 lowercase=True)

    tfidf_model = vectorizer.fit_transform(texts)
    pca = PCA(n_components=0.95, random_state=42)
    tfidf_model = pca.fit_transform(tfidf_model.toarray())
    km_model = KMeans(n_clusters=clusters)
    km_model.fit(tfidf_model)

    clustering = collections.defaultdict(list)

    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)
    return tfidf_model, clustering

vec_texts, clusters = cluster_results(results_text)

data['cluster'] = None
for cluster in clusters:
    data['cluster'].loc[clusters[cluster]] = cluster

text_stop_words = stop_words + ['peerreviewed', 'cases', 'mar', 'number', 'feb', 'patients', 'without', 'httpsdoiorg', 'authorfunder','made', 'holder', 'granted', 'display', 'file', 'medRxiv', 'time']
def text_tokenizer(text):
    mytokens = text.translate(str.maketrans('', '', string.punctuation))
    mytokens = word_tokenize(mytokens)
    mytokens = [w for w in mytokens if not w in text_stop_words]
    mytokens = ' '.join(mytokens)
    return mytokens
data["processed_text"] = data["text"].apply(text_tokenizer)


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

vectorizers = []
for ii in range(0, 20):
    # Creating a vectorizer
    vectorizers.append(
        CountVectorizer(stop_words=text_stop_words, lowercase=True, token_pattern='[a-zA-Z\-][a-zA-Z\-]{2,}'))

vectorized_data = []
for current_cluster, cvec in enumerate(vectorizers):
    vectorized_data.append(
        cvec.fit_transform(data.loc[data['cluster'] == current_cluster].processed_text.tolist()))


NUM_TOPICS_PER_CLUSTER = 10
lda_models = []
for ii in range(0, 20):
    # Latent Dirichlet Allocation Model
    lda = LatentDirichletAllocation(n_components=NUM_TOPICS_PER_CLUSTER, max_iter=10, learning_method='online',
                                    verbose=False, random_state=42)
    lda_models.append(lda)

clusters_lda_data = []
for current_cluster, lda in enumerate(lda_models):
    if vectorized_data[current_cluster] != None:
        clusters_lda_data.append((lda.fit_transform(vectorized_data[current_cluster])))


def selected_topics(model, vectorizer, top_n=3):
    current_words = []
    keywords = []

    for idx, topic in enumerate(model.components_):
        words = [(vectorizer.get_feature_names()[i], topic[i]) for i in topic.argsort()[:-top_n - 1:-1]]
        for word in words:
            if word[0] not in current_words:
                keywords.append(word)
                current_words.append(word[0])

    keywords.sort(key=lambda x: x[1])
    keywords.reverse()
    return_values = []
    for ii in keywords:
        return_values.append(ii[0])
    return return_values
all_keywords = []
for current_vectorizer, lda in enumerate(lda_models):
    if vectorized_data[current_vectorizer] != None:
        all_keywords.append(selected_topics(lda, vectorizers[current_vectorizer]))


data['named_cluster'] = None
for j in range(len(all_keywords)):
    data.loc[data['cluster'] == j, 'named_cluster'] = all_keywords[j][0].upper()

def prep():
    toc = time.time()
    t = toc - tic
    print('The prep preocess takes', t, 'seconds')
    return data, vec_texts

if __name__ == '__main__':
    prep()