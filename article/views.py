from django.shortcuts import render
from .models import Article


# Create your views here.
def dynamic_article(request, url_title):
    article_data = Article.objects.get(url_title=url_title)
    article_data = {
        "this_article": article_data
    }
    return render(request, 'article.html', article_data)
