from .models import *
from rest_framework import serializers


class NewsSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = News
       fields = ['name', 'type', 'category', 'text', 'date_on' ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Category
       fields = ['name' ]


class SubscriberSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Subscriber
       fields = ['user', 'category', ]