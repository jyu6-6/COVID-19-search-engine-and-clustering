# COVID-19-search-engine-and-clustering

## Usage
Download the whole project, open terminal, then direct to the COVID-19-search-engine-and-clustering folder.
```
(base) jing@JMacBook ~ % cd YOUR_LOCAL_PATH/ COVID-19-search-engine-and-clustering
```
Then type 
```
python manage.py runserver
```
Open your browser, go to http://127.0.0.1:8000/mysearch/ ， then you can search terms of your instrests like 'covid19', 'mask', 'rna' and see the result clusters and visualization!

## Prerequisites
Linux enviroment  
Python 3

### set up python packages
Python packages:  
numpy, pandas, scipy, sklearn, nltk, matplotlib, seaborn, rank_bm25, wordcloud, django. All packages could be installed using pip.
```
pip install PACKAGE_NAME
```
If you have never used tokenization and stopwords in ntlk, please type the codes below in your terminal after installing the nltk package.
```
(base) jing@JMacBook ~ % python3
```
After logging into the python enviroment, type
```
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```
