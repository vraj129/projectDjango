from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.http import Http404
from django.http import JsonResponse
from article.models import Article, Hashtag, Report
from django.contrib import messages
import re
# from django import forms


def base(request):
    request.session['url_to_go'] = request.path
    return render(request, 'base.html')


def home(request):
    request.session['url_to_go'] = request.path
    return render(request, 'home.html')


def new2(request):
    print(request)
    a = other_func(request)
    return a


def other_func(request):
    return render(request, 'edit.html')


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


def publish(request):
    if not request.user.is_superuser:
        # raise Http404("Not a superuser")
        raise Http404
    request.session['url_to_go'] = request.path

    if request.method == 'POST':
        pass
    # file_name = request.POST['file-name']

    return render(request, 'publish.html')


# def explore(request):
#     request.session['url_to_go'] = request.path
#     return render(request, 'explore.html')


def terms_and_conditions(request):
    request.session['url_to_go'] = request.path
    return render(request, 'terms_and_conditions.html')


def contact(request):
    request.session['url_to_go'] = request.path
    return render(request, 'contact.html')


def logout(request):
    auth.logout(request)
    # Above line removes session, but still this is written for safe side
    if 'url_to_go' in request.session:
        request.session.pop('url_to_go')
    return redirect('/')


def answer_categories(request):
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


def answer_me(request):
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


def discardArticle(request):
    if 'url_title' in request.session:
        request.session.pop('url_title')
    if 'file_name' in request.session:
        request.session.pop('file_name')
    return new(request)


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
