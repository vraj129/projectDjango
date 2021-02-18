from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.http import Http404
from django.http import JsonResponse
from article.models import Article, Group
from django.contrib import messages


def base(request):
    request.session['url_to_go'] = request.path
    return render(request, 'base.html')


def home(request):
    request.session['url_to_go'] = request.path
    return render(request, 'home.html')


def new(request):
    if not request.user.is_superuser:
        # raise Http404("Not a superuser")
        raise Http404
    request.session['url_to_go'] = request.path

    if request.method == 'POST':
        session_for_url_title = False
        session_for_filename = False

        url_title = request.POST["url_title"]
        file_name = request.POST["file_name"]

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
        queryset = Group.objects.filter(category_name__istartswith=search_string)
        values_list = list(queryset.values())
        print("vv", values_list)
        response_data = {'response': values_list}
        print("rd", response_data["response"][0]["category_name"])
    return JsonResponse(response_data)


def answer_me(request):
    filename = request.GET.get('filename')
    codeContent = request.GET.get('codeContent')
    publish_title = request.GET.get('publish_title')
    publish_meta_keywords = request.GET.get('publish_meta_keywords')
    publish_meta_current_page_url = request.GET.get('publish_meta_current_page_url')
    publish_meta_description = request.GET.get('publish_meta_description')
    publish_meta_image_url = request.GET.get('publish_meta_image_url')
    publish_facebook_sharing_link = request.GET.get('publish_facebook_sharing_link')

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
            Article.objects.filter(url_title=publish_url_title).update(
                file_location=file_location,
                title=publish_title,
                meta_keywords=publish_meta_keywords,
                meta_current_page_url=publish_meta_current_page_url,
                meta_description=publish_meta_description,
                meta_image_url=publish_meta_image_url,
                facebook_sharing_link=publish_facebook_sharing_link,
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
