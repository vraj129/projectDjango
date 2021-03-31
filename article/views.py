from django.shortcuts import render, Http404
from .models import Article, Viewer
from django.contrib.auth.models import User
from .utils import get_client_ip
import os
from django.conf import settings

# To convert urls
# Ex:url that has spaces will be converted into %20
import urllib.parse
# Pdf
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


# Create your views here.
def dynamic_article(request, url_title):
    request.session['url_to_go'] = request.path

    try:
        # If you remove lower() from here,
        # please remove it from website/views.py - def new: also
        url_title = url_title.lower()
        article_data_obj = Article.objects.get(url_title=url_title)
    except Article.DoesNotExist:
        raise Http404("No Such Article found")

    # Getting file location
    file_location = article_data_obj.file_location

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
        "this_article": article_data_obj,
        "file_content": file_content,
        "share_string": share_string,
        "share_link": share_link,
    }

    # Inserting Viewer Details - Start
    article_instance = Article.objects.get(pk=article_data_obj.id)
    if request.user.is_authenticated:
        user_instance = User.objects.get(pk=request.user.id)

    # MOBILE = 'M'
    if request.user_agent.is_mobile:
        device_agent = 'M'

    # TABLET = 'T'
    elif request.user_agent.is_tablet:
        device_agent = 'T'

    # PC = 'P'
    elif request.user_agent.is_pc:
        device_agent = 'P'

    # NONE = 'N'
    else:
        device_agent = 'N'

    if request.user.is_authenticated:
        # obj, created = Viewer.objects.update_or_create(
        obj, created = Viewer.objects.get_or_create(
            article_id=article_instance,
            user_id=user_instance,
            ip_address=get_client_ip(request),

            device_agent=device_agent,
            is_touch_capable=request.user_agent.is_touch_capable,
            is_bot=request.user_agent.is_bot,

            browser_family=request.user_agent.browser.family,
            browser_version=request.user_agent.browser.version_string,

            os_family=request.user_agent.os.family,
            os_version=request.user_agent.os.version_string,

            device_agent_family=request.user_agent.device.family
        )
        print("=======--", created)
        pass

    # Inserting Viewer Details - Ends

    return render(request, 'article.html', article_data)


# def render_to_pdf(template_src, context_dict):
#     template = get_template(template_src)
#     context = dict(context_dict)
#     html = template.render(context)
#     result = BytesIO()
#
#     pdf = pisa.pisaDocument(
#         BytesIO(html.encode("iso-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(
#             result.getvalue(), content_type='application/pdf')
#     return HttpResponse(
#         'we had some errors<pre>%s</pre>' % escape(html))


def dynamic_article_as_pdf(request, url_title):
    request.session['url_to_go'] = request.path
    try:
        # If you remove lower() from here,
        # please remove it from website/views.py - def new: also
        url_title = url_title.lower()
        article_data_obj = Article.objects.get(url_title=url_title)
    except Article.DoesNotExist:
        raise Http404("No Such Article found")

    # Getting file location
    file_location = article_data_obj.file_location

    # Reading File
    file_ = open(os.path.join(settings.BASE_DIR, file_location))
    file_content = file_.read()

    article_data = {
        "this_article_title": article_data_obj.title,
        "file_content": file_content,
        "project_name": settings.PROJECT_NAME,
    }

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(500, 500, article_data["project_name"])
    p.drawString(200, 200, article_data["this_article_title"])
    p.drawString(100, 100, article_data["file_content"])

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='article.pdf')
