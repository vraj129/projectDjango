from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.http import Http404
from django.http import JsonResponse
from article.models import Article


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


def answer_me(request):
    filename = request.GET.get('filename')
    codeContent = request.GET.get('codeContent')
    publish_title = request.GET.get('publish_title')
    publish_url_title = request.GET.get('publish_url_title')
    publish_meta_keywords = request.GET.get('publish_meta_keywords')
    publish_meta_current_page_url = request.GET.get('publish_meta_current_page_url')
    publish_meta_description = request.GET.get('publish_meta_description')
    publish_meta_image_url = request.GET.get('publish_meta_image_url')
    publish_facebook_sharing_link = request.GET.get('publish_facebook_sharing_link')

    if not filename:
        response_data = {'response': 'Please Enter Filename and then save'}
    elif not publish_title:
        response_data = {'response': 'Please Enter Title and then save'}
    elif not publish_url_title:
        response_data = {'response': 'Please Enter Url Title'}
    elif ' ' in publish_url_title:
        response_data = {'response': 'Please Enter Url Title without Spaces'}
    elif not publish_meta_keywords:
        response_data = {'response': 'Please Enter Meta Keywords'}
    elif not publish_meta_description:
        response_data = {'response': 'Please Enter Meta Description'}
    else:
        print(">>", filename)
        file_location = "templates/articles/" + filename + ".html"
        # Pending --- Check from database if this file exists or Not
        # if yes, dont let user create it with that name
        with open(file_location, 'w') as f:
            f.write(codeContent)
        try:
            print("--------update_or_create-------")
            print(filename)
            Article.objects.filter(url_title="default").update(
                file_location=filename,
                title=publish_title,
                url_title=publish_url_title,
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
