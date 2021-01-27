from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.http import Http404


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
