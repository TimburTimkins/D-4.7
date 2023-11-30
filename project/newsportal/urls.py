from django.urls import path, include
from .views import NewsportalList, NewsList, ArtList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, ArtCreate, ArtUpdate, ArtDelete, multiply, NP_Search, subscriptions
from django.views.decorators.cache import cache_page
from rest_framework import routers
from newsportal import views


router = routers.DefaultRouter()
router.register(r'news', views.NewsViewset)
router.register(r'categories', views.CategoryViewset)
router.register(r'subscribers', views.SubscriberViewest)


urlpatterns = [
    path('newsportal/', NewsportalList.as_view(), name='news_list'),
    path('newsportal/news/', NewsList.as_view(), name='news_list'),
    path('newsportal/articles/', ArtList.as_view(), name='news_list'),
    path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('news/search', NP_Search.as_view(), name='news_search'),
    path('multiply/', multiply),
    path('sltr/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArtCreate.as_view(), name='art_create'),
    path('articles/<int:pk>/update/', ArtUpdate.as_view(), name='art_update'),
    path('articles/<int:pk>/delete/', ArtDelete.as_view(), name='art_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]