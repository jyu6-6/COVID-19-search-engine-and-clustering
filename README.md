# COVID-19-search-engine-and-clustering  
This project includes a search engine specially built for the CORD dataset, which contains the search results clustering function. Besides, there are data analysis and visualization both for the whole dataset and your search results. All are presented on a Django-frame website.

## Demo
Here is a [demo website](http://jyu66.pythonanywhere.com/mysearch/) to help you get a taste of this project.  
Tip: If you encounter an error related to 'TkAgg' or 'tk', just refresh the page.

## Data source
[COVID-19 Open Research Dataset Challenge (CORD-19)](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)  
We used the biorxiv_medrxiv/biorxiv_medrxiv/pdf_json data set. 

## Usage
Please be patient and run all of the following steps.  
### Clean raw data
run JSON_to_CSV.py, this should generate a file named 'biorxiv_medrxiv_clean.csv'.  
```
(base) jing@JMacBook ~ % python JSON_to_CSV.py
```
### Set up the paths
Be sure to modify paths in 3 files.  
* mysearch/view.py, set 
```
con=sqlite3.connect("/YOUR_LOCAL_PATH/db.sqlite3")
# 4 lines need to be modified in this file.  
```

* mysearch/search_and_cluster/search.py, set
```
file_path = 'YOUR_LOCAL_PATH_TO/biorxiv_medrxiv_clean.csv'
# 1 line needs to be modified in this file. 
``` 

* mysearch/search_and_cluster/cluster_and_prep.py, set 
```
file_path = 'YOUR_LOCAL_PATH_TO/biorxiv_medrxiv_clean.csv'
# 1 line needs to be modified in this file. 
``` 

### Launch the website
Open terminal, then direct to the COVID-19-search-engine-and-clustering folder.
```
(base) jing@JMacBook ~ % cd YOUR_LOCAL_PATH/COVID-19-search-engine-and-clustering
```
Then type 
```
(base) jing@JMacBook ~ % python manage.py runserver
```
Open your browser, go to http://127.0.0.1:8000/mysearch/ ， then you can search terms of your instrests like 'covid19', 'mask', 'rna' and see the result clusters and visualization!

## Prerequisites
* Linux enviroment  
* Python 3

### set up Python packages
Python packages:  
numpy, pandas, scipy, sklearn, nltk, matplotlib, seaborn, rank_bm25, wordcloud, django. All packages could be installed using pip.
```
(base) jing@JMacBook ~ % pip install PACKAGE_NAME
```
If you have never used tokenization and stopwords in ntlk, please type the codes below in your terminal after installing the nltk package.
```
(base) jing@JMacBook ~ % python3
>>> import nltk
>>> nltk.download('stopwords')
>>> nltk.download('punkt')
```
