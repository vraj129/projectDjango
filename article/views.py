from django.shortcuts import render, Http404
from .models import Article


# Create your views here.
def dynamic_article(request, url_title):
    request.session['url_to_go'] = request.path

    try:
        article_data = Article.objects.get(url_title=url_title)
    except Article.DoesNotExist:
        raise Http404("No Such Article found")

    article_data = {
        "this_article": article_data
    }
    return render(request, 'article.html', article_data)


def demo(request):
    return render(request, 'demo.html', {})
