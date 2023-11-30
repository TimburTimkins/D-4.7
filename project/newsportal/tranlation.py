from .models import Category, News
from modeltranslation.translator import register, TranslationOptions


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name', 'type', 'category', 'date_on', 'text')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name')