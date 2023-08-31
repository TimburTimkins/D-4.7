from django.urls import path
from .views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, ArtCreate, ArtUpdate, ArtDelete, multiply, NP_Search, subscriptions


urlpatterns = [
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('news/search', NP_Search.as_view(), name='news_search'),
    path('multiply/', multiply),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArtCreate.as_view(), name='art_create'),
    path('articles/<int:pk>/update/', ArtUpdate.as_view(), name='art_update'),
    path('articles/<int:pk>/delete/', ArtDelete.as_view(), name='art_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]