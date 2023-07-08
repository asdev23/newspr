from modeltranslation.translator import TranslationOptions, register, translator
from .models import News, Category

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields=['title','body']


class CategoryTranslationOptions(TranslationOptions):
    fields=['name']
translator.register(Category,CategoryTranslationOptions)