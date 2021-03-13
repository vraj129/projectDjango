from django.shortcuts import render, Http404
from .models import Article

import os
from django.conf import settings

# To convert urls
# Ex:url that has spaces will be converted into %20
import urllib.parse


# Create your views here.
def dynamic_article(request, url_title):
    # Mobile device detection Starts
    # Let's assume that the visitor uses an iPhone...
    request.user_agent.is_mobile  # returns True
    request.user_agent.is_tablet  # returns False
    request.user_agent.is_touch_capable  # returns True
    request.user_agent.is_pc  # returns False
    request.user_agent.is_bot  # returns False

    # Accessing user agent's browser attributes
    request.user_agent.browser  # returns Browser(
    # family=u'Mobile Safari', version=(5, 1), version_string='5.1')
    request.user_agent.browser.family  # returns 'Mobile Safari'
    request.user_agent.browser.version  # returns (5, 1)
    request.user_agent.browser.version_string   # returns '5.1'

    # Operating System properties
    request.user_agent.os  # returns OperatingSystem(
    # family=u'iOS', version=(5, 1), version_string='5.1')
    request.user_agent.os.family  # returns 'iOS'
    request.user_agent.os.version  # returns (5, 1)
    request.user_agent.os.version_string  # returns '5.1'

    # Device properties
    request.user_agent.device  # returns Device(family='iPhone')
    request.user_agent.device.family  # returns 'iPhone'
    # Mobile device detection Ends

    request.session['url_to_go'] = request.path

    try:
        # If you remove lower() from here,
        # please remove it from website/views.py - def new: also
        url_title = url_title.lower()
        article_data = Article.objects.get(url_title=url_title)
    except Article.DoesNotExist:
        raise Http404("No Such Article found")

    # Getting file location
    file_location = article_data.file_location

    # Reading File
    file_ = open(os.path.join(settings.BASE_DIR, file_location))
    file_content = file_.read()

    # Url quote_plus
    absolute_url = request.build_absolute_uri()

    absolute_url_string = "Check out this awesome site. " + absolute_url
    share_string = urllib.parse.quote(absolute_url_string, safe='')

    # Ex: http://127.0.0.1:8000/article/demo will be converted to
    # http%3A%2F%2F127.0.0.1%3A8000%2Farticle%2Fdemo
    share_link = urllib.parse.quote(absolute_url, safe='')

    article_data = {
        "this_article": article_data,
        "file_content": file_content,
        "share_string": share_string,
        "share_link": share_link,
    }

    return render(request, 'article.html', article_data)
