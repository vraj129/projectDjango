from django.shortcuts import render, redirect
from django.contrib.auth.models import auth


def base(request):
    request.session['url_to_go'] = request.path
    return render(request, 'base.html')


def home(request):
    request.session['url_to_go'] = request.path
    return render(request, 'home.html')


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
