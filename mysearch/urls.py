from django.urls import path

from . import views

urlpatterns = [
	#/mysearch/
    path('', views.index, name='index'),
    #/mysearch/search_result
    path('search_result/', views.search_result, name='search_result'),
    path('search_result/page_selection/', views.page_selection, name='page_selection'),
    path('search_result/cluster_page/', views.cluster_page, name='cluster_page'),
    path('cluster_visual/', views.cluster_visual, name='cluster_visual'),
    path('topic_visual/', views.topic_visual, name='topic_visual'),
    path('search_result/word_cloud/', views.word_cloud, name='word_cloud'),
    path('search_result/results_clustering/', views.results_clustering, name='results_clustering'),
]
