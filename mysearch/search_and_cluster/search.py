# # main search function
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from mysearch import search_and_cluster
from mysearch.search_and_cluster import BM25_indexing
from mysearch.search_and_cluster import data_cleaning
import numpy as np

# data preprocessing
file_path = '/Users/taylorw/Desktop/CS525/project/biorxiv_medrxiv_clean.csv'
data = data_cleaning.data_loader(file_path)
data = data_cleaning.clean_title(data)
data = data_cleaning.clean_abstract(data)
data = data_cleaning.drop_missing(data)
data = data_cleaning.fill_nulls(data)

# get data tokens and set index
data = BM25_indexing.preparing(data)
bm25 = BM25_indexing._get_bm25L(data.tokens)
stop_words = set(stopwords.words('english'))

def search(query):
    ps = PorterStemmer()
    tokenized_query = word_tokenize(query)
    tokenized_query = [w for w in tokenized_query if not w in stop_words]
    tokenized_query = [ps.stem(w) for w in tokenized_query]
    doc_scores = np.array(bm25.get_scores(tokenized_query))
    results_idx = doc_scores.nonzero()[0]
    results_scores = doc_scores[results_idx]
    results_scores = list(results_scores)
    sorted_idx = [x for _,x in sorted(zip(results_scores, results_idx))]
    results_ids = data.loc[sorted_idx]['paper_id'].tolist()
    return results_ids

if __name__ == '__main__':
    search('rna')