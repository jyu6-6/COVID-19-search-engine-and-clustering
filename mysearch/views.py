from django.shortcuts import render

# Create your views here.
import sqlite3

import math


from mysearch import search_and_cluster
from mysearch.search_and_cluster import search
from mysearch.search_and_cluster import cluster_main


# #test select from db
# con=sqlite3.connect("/Users/taylorw/Desktop/CS525/project/cs525project/db.sqlite3")
# cur=con.cursor()
# field1="0015023cc06b5362d332b3baf348d11567ca2fbb"
# cur.execute("select field2 from clean_data_import where field1=?",(field1,))
# title=cur.fetchone()


def index(request):
    return render(request,'mysearch/index.html')

def cluster_visual(request):
    return render(request,'mysearch/t_SNE_and_kmeans.html')

def topic_visual(request):
    return render(request,'mysearch/lda.html')

def word_cloud(request):
    return render(request,'mysearch/word_cloud.html')

def results_clustering(request):
    return render(request,'mysearch/results_clustering.html')

my_query=""
query_result=[]
num_result=0
page_num=0
fetched_id_titleurl_dict_to_list=[]
results_clusters={}

def search_result(request):
	global my_query
	global query_result
	global num_result
	global page_num
	global fetched_id_titleurl_dict_to_list
	global results_clusters
	fetched_id_titleurl_dict={}

	my_query=request.GET.get("my_query")
	query_result=search.search(my_query)
	num_result=len(query_result)

	results_clusters=cluster_main.get_results_clusters(query_result)

	cluster_main.plot_clusters(query_result)
	cluster_main.plot_wordcloud(query_result)

	if num_result<=7:
		page_num=list(range(1,1))
	else:
		page_num=list((range(1,math.ceil(num_result/7)+1)))

	for each in query_result:
		fetched_titleurl=[]

		con=sqlite3.connect("/Users/taylorw/Desktop/CS525/project/cs525project/db.sqlite3")
		cur=con.cursor()
		cur.execute("select field2,field3 from clean_data_import where field1=?",(each,))
		fetched_titleurl.append(cur.fetchone())
		con.close()

		con=sqlite3.connect("/Users/taylorw/Desktop/CS525/project/cs525project/db.sqlite3")
		cur=con.cursor()
		cur.execute("select field2 from answer where field1=?",(each,))
		fetched_titleurl.append(cur.fetchone())
		con.close()

		fetched_id_titleurl_dict[each]=fetched_titleurl

	fetched_id_titleurl_dict_to_list=list(fetched_id_titleurl_dict.items())

	return render(request,'mysearch/search_result.html',{"my_query":my_query,"num_result":num_result,"page_num":page_num,"query_result":fetched_id_titleurl_dict_to_list[0:7],"results_clusters":results_clusters})

def page_selection(request):
	global fetched_id_titleurl_dict_to_list
	page_number=request.GET.get("page_number")

	display_doc=fetched_id_titleurl_dict_to_list[int(page_number)*7-7:int(page_number)*7]

	return render(request,'mysearch/page_selection.html',{"my_query":my_query,"num_result":num_result,"page_num":page_num,"query_result":display_doc,"results_clusters":results_clusters})

def cluster_page(request):
	global results_clusters
	global fetched_id_titleurl_dict_to_list
	global page_num
	global num_result
	fetched_cluster_content_dict={}
	
	cluster_name=request.GET.get("cluster_name")

	num_result=len(results_clusters[cluster_name])
	if num_result<=7:
		page_num=list(range(1,1))
	else:
		page_num=list((range(1,math.ceil(num_result/7)+1)))

	for each in results_clusters[cluster_name]:
		fetched_titleurl=[]

		con=sqlite3.connect("/Users/taylorw/Desktop/CS525/project/cs525project/db.sqlite3")
		cur=con.cursor()
		cur.execute("select field2,field3 from clean_data_import where field1=?",(each,))
		fetched_titleurl.append(cur.fetchone())
		con.close()

		con=sqlite3.connect("/Users/taylorw/Desktop/CS525/project/cs525project/db.sqlite3")
		cur=con.cursor()
		cur.execute("select field2 from answer where field1=?",(each,))
		fetched_titleurl.append(cur.fetchone())
		con.close()

		fetched_cluster_content_dict[each]=fetched_titleurl

	fetched_id_titleurl_dict_to_list=list(fetched_cluster_content_dict.items())

	return render(request,'mysearch/cluster_page.html',{"my_query":my_query,"num_result":num_result,"page_num":page_num,"query_result":fetched_id_titleurl_dict_to_list[0:7],"results_clusters":results_clusters})








