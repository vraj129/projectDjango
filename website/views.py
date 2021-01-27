from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.http import Http404
from django.http import JsonResponse
import os


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
        file_name = request.POST['file-name']

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

    if filename is None:
        response_data = {'response': 'Enter Filename'}
    else:
        file_location = "static/articles/" + filename + ".html"
        # Pending --- Check from database if this file exists or Not
        # if yes, dont let user create it with that name
        with open(file_location, 'w') as f:
            f.write(codeContent)
        response_data = {'response': f'Saved: {filename}.html'}
    return JsonResponse(response_data)
