# COVID-19-search-engine-and-clustering  
The main purpose of this tool is to serve the research community members, whether it be scholars, grad school students, or science enthusiasts. Since the outbreak of the coronavirus pandemic, researchers around the world have been trying to get a basic understanding of this situation, how it originated, what’s the biological explanation behind this, and most importantly, how to prevent the potential further damage to human kind. There are multiple areas surrounding this issue, from sociology, chemistry to biology, and different scholars has their own unique understanding of this situation, therefore the amount of information and papers related to this disease might be overwhelming to some people, hence our tool would help filter the unwanted materials and render the most relevant ones to those who needed it based on their own preferences.  

This project includes a search engine specially built for the CORD dataset, you could search and see the results are splited into different clusters and the main topic each cluster represents for. Besides, there are data analysis and visualization both for the whole dataset and your search results. All are presented on a Django-framed website.

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

## References
* [search engine](https://www.kaggle.com/dgunning/cord-research-engine-bm25-specter-embeddings#2.-Loading-Research-Papers)  
* [clustering](https://www.kaggle.com/maksimeren/covid-19-literature-clustering)  
* [visualization](https://www.kaggle.com/maksimeren/covid-19-literature-clustering)
