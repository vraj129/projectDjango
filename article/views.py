from django.shortcuts import render, Http404
from .models import Article

import os
from django.conf import settings

# To convert urls
# Ex:url that has spaces will be converted into %20
import urllib.parse


# Create your views here.
def dynamic_article(request, url_title):
    request.session['url_to_go'] = request.path

    try:
        # If you remove lower() from here,
        # please remove it from website/views.py - def new: also
        article_data = Article.objects.get(url_title=url_title.lower())
    except Article.DoesNotExist:
        raise Http404("No Such Article found")

    # Getting file location
    file_location = article_data.file_location

    # Reading File
    file_ = open(os.path.join(settings.BASE_DIR, file_location))
    file_content = file_.read()

    # Url quote_plus
    aaa = request.build_absolute_uri()
    share_string = urllib.parse.quote(aaa, safe='')
    # Ex: http://127.0.0.1:8000/article/demo will be converted to
    # http%3A%2F%2F127.0.0.1%3A8000%2Farticle%2Fdemo

    # share_string = quote_plus()
    article_data = {
        "this_article": article_data,
        "file_content": file_content,
        "share_string": share_string,
    }

    return render(request, 'article.html', article_data)
