# # BM25L Indexing
import nltk
import string
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi

stop_words = set(stopwords.words('english'))


# tokenization, removing stop words, stemming
def preparing(data):
    ps = PorterStemmer()
    tokens = []
    for i in range(len(data)):
        tokens_i = data.loc[i]['abstract'].translate(str.maketrans('', '', string.punctuation))
        tokens_i = word_tokenize(tokens_i)
        tokens_i = [w for w in tokens_i if not w in stop_words]
        tokens_i = [ps.stem(w) for w in tokens_i]
        tokens.append(tokens_i)
    data['tokens'] = tokens
    return data


def _get_bm25L(index_tokens):
    """
    input: data.tokens
    output: e.g.<rank_bm25.BM25L object at 0x11d64c190>
    """
    has_tokens = index_tokens.apply(len).sum() > 0
    if not has_tokens:
        index_tokens.loc[0] = ['no', 'tokens']
    return BM25Okapi(index_tokens.tolist())
