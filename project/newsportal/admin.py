from django.contrib import admin
from .models import News, Category
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
    model = Category


class MyModelAdmin(TranslationAdmin):
    model = News

admin.site.register(News)
admin.site.register(Category)

