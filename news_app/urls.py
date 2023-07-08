from django.urls import path
from .views import NewsList, NewsDetail, HomeView, ContactView, Page404, \
    MahalliyView, XorijView, TexnoView, SportView, SearchListView, \
    UpdateNews, DeleteNews, CreateNews, admin_page_view

urlpatterns=[
    path('',HomeView, name='home'),
    path('contact', ContactView, name='contact'),
    path('page404', Page404, name='page404'),
    path('adminpage/', admin_page_view, name='admin_page'),
    path('list',NewsList,name='news_list'),
    path('create/',CreateNews.as_view(),name='create'),
    path('mahalliy/',MahalliyView.as_view(),name='mahalliy'),
    path('xorij/', XorijView.as_view(), name='xorij'),
    path('texno/', TexnoView.as_view(), name='texno'),
    path('sport/', SportView.as_view(), name='sport'),
    path('searchresult/',SearchListView.as_view(), name='search_results'),
    path('<slug>/delete',DeleteNews.as_view(),name='delete'),
    path('<slug>/edit',UpdateNews.as_view(),name='update'),
    path('<slug:news>/',NewsDetail,name='news_detail'),
    path('adminpage/', admin_page_view, name='admin_page'),
]