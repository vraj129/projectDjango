from django.shortcuts import render, Http404
from .models import Article, Viewer, Hashtag, Report
from django.contrib.auth.models import User
from .utils import get_client_ip
import os
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
import re

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
            defaults={

                'device_agent': device_agent,
                'is_touch_capable': request.user_agent.is_touch_capable,
                'is_bot': request.user_agent.is_bot,

                'browser_family': request.user_agent.browser.family,
                'browser_version': request.user_agent.browser.version_string,

                'os_family': request.user_agent.os.family,
                'os_version': request.user_agent.os.version_string,

                'device_agent_family': request.user_agent.device.family
            },
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


def new(request, slug=None):
    if not request.user.is_superuser:
        # raise Http404("Not a superuser")
        raise Http404
    request.session['url_to_go'] = request.path

    if request.method == 'POST':
        session_for_url_title = False
        session_for_filename = False

        # If you remove lower() from here,
        # please remove it from article/views.py - def dynamic_article: also

        # Converting to lower so that unique user can search in any case in url
        url_title = request.POST["url_title"].lower()
        file_name = request.POST["file_name"].lower()

        try:
            Article.objects.get(url_title=url_title)
            print("This url title exists")
            messages.error(request, "This url title already exists.")
        except Article.DoesNotExist:
            if not url_title:
                messages.error(request, "Blank Url not Allowed.")
            elif not bool(re.match("^[A-Za-z0-9_-]*$", url_title)):
                messages.error(request, "Only letters, numbers, underscores "
                               "and dashes are Allowed")
            else:
                session_for_url_title = True

        try:
            Article.objects.get(file_location="templates/articles/"
                                + file_name + ".html")
            print("This Filename title exists")
            messages.error(request, "This filename already exists.")
        except Article.DoesNotExist:
            if not url_title:
                messages.error(request, "Blank Filename not Allowed.")
            elif not bool(re.match("^[A-Za-z0-9_-]*$", url_title)):
                messages.error(request, "Only letters, numbers, underscores "
                               "and dashes are Allowed")
            else:
                session_for_filename = True

        if session_for_url_title and session_for_filename:
            article_object = Article(file_location="templates/articles/"
                                     + file_name + ".html",
                                     title=url_title,
                                     url_title=url_title)
            article_object.save()
            request.session['url_title'] = url_title
            request.session['file_name'] = file_name

    if 'url_title' not in request.session:
        return render(request, 'askTitle.html')

    return render(request, 'new.html')


def edit(request, slug=None):
    pass


def discardArticle(request):
    if 'url_title' in request.session:
        request.session.pop('url_title')
    if 'file_name' in request.session:
        request.session.pop('file_name')
    return new(request)


def publish(request):
    if not request.user.is_superuser:
        # raise Http404("Not a superuser")
        raise Http404
    request.session['url_to_go'] = request.path

    if request.method == 'POST':
        pass
    # file_name = request.POST['file-name']

    return render(request, 'publish.html')


def save_article(request):
    filename = request.GET.get('filename')
    codeContent = request.GET.get('codeContent')
    publish_title = request.GET.get('publish_title')
    publish_meta_keywords = request.GET.get('publish_meta_keywords')
    publish_meta_description = request.GET.get('publish_meta_description')

    if 'file_name' in request.session:
        filename = request.session['file_name']
    if 'url_title' in request.session:
        publish_url_title = request.session['url_title']

    if not publish_title:
        response_data = {'response': 'Please Enter Title and then save'}
    elif not publish_url_title:
        response_data = {'response': 'Please Enter Url Title'}
    elif ' ' in publish_url_title:
        response_data = {'response': 'Please Enter Url Title without Spaces'}
    else:
        file_location = "templates/articles/" + filename + ".html"
        with open(file_location, 'w') as f:
            f.write(codeContent)
        try:
            Article.objects.update_or_create(
                url_title=publish_url_title,
                defaults={
                    'file_location': file_location,
                    'title': publish_title,
                    'meta_keywords': publish_meta_keywords,
                    'meta_description': publish_meta_description,
                }
            )
            response_data = {'response': f'Saved: {filename}.html'}
        except Exception as e:
            print(e)
            print("-----Some issue--------")
            response_data = {'response': 'Unknown Error Occured'}
    return JsonResponse(response_data)


def get_categories(request):
    search_string = request.GET.get('search_string')
    search_string = search_string.split(",")[-1].strip()

    # If string is empty
    if not search_string:
        response_data = {'response': '  '}
    else:
        # i is for insensitive case search
        queryset = Hashtag.objects.filter(category_name__istartswith=search_string)
        values_list = list(queryset.values())
        print("vv", values_list)
        response_data = {'response': values_list}
        print("rd", response_data["response"][0]["category_name"])
    return JsonResponse(response_data)


def confirm_publish(request):
    filename = request.GET.get('filename')
    codeContent = request.GET.get('codeContent')
    publish_title = request.GET.get('publish_title')
    # publish_meta_keywords = request.GET.get('publish_meta_keywords')
    # publish_meta_current_page_url = request.GET.get('publish_meta_current_page_url')
    # publish_meta_description = request.GET.get('publish_meta_description')
    # publish_meta_image_url = request.GET.get('publish_meta_image_url')
    # publish_facebook_sharing_link = request.GET.get('publish_facebook_sharing_link')

    if 'file_name' in request.session:
        filename = request.session['file_name']
    if 'url_title' in request.session:
        publish_url_title = request.session['url_title']

    if not publish_title:
        response_data = {'response': 'Please Enter Title and then save'}
    elif not publish_url_title:
        response_data = {'response': 'Please Enter Url Title'}
    elif ' ' in publish_url_title:
        response_data = {'response': 'Please Enter Url Title without Spaces'}
    else:
        file_location = "templates/articles/" + filename + ".html"
        with open(file_location, 'w') as f:
            f.write(codeContent)
        try:
            Article.objects.update_or_create(
                url_title=publish_url_title,
                defaults={
                    'publish_status': True
                }
            )
            print("Published")
            response_data = {'response': 'Published Successfully'}
        except Exception as e:
            print(e)
            print("-----Some issue--------")
            response_data = {'response': 'Unknown Error Occured'}
    return JsonResponse(response_data)


def report_article(request):
    report_reason_radio = request.GET.get('report_reason_radio')
    print(report_reason_radio)
    report_reason_text = request.GET.get('report_reason_text')
    article_id = request.GET.get('this_article_id')
    user_id = request.GET.get('this_user_id')

    print(article_id, user_id)

    if not report_reason_text:
        response_data = {'response': 'Please Enter Reason'}
    elif not report_reason_radio:
        response_data = {'response': 'Please Select an option.'}

    # elif Report.objects.filter(article_id=article_id, user_id=user_id).count() > 0:
    #     response_data = {'response': 'You have already Reported this Article'}
    #     print("You have already Reported this post")
    else:
        try:
            article_instance = Article.objects.get(pk=article_id)
            user_instance = User.objects.get(pk=user_id)
            print(article_instance)
            print(user_instance)

            r, created = Report.objects.get_or_create(
                article_id=article_instance,
                user_id=user_instance,
                defaults={
                    'reason': report_reason_radio,
                    'brief_reason': report_reason_text
                }
            )

            if not created:
                response_data = {'response': 'You have already Reported this Article'}
                print("Already reported")

            else:
                response_data = {
                    'response': ('Thank you for for taking time to report '
                                 'If it violates our Community Guidelines, '
                                 'we will definately take action towards it. '
                                 'By reporting this, '
                                 'you prove to an important part of our Community.')}
            print(report_reason_radio)
            print(report_reason_text)
        except Exception as e:
            print(e)
            print("-----Some issue--------")
            response_data = {'response': 'Unknown Error Occured'}
    return JsonResponse(response_data)
