import json

from django.contrib import messages

from django.contrib.auth import login, logout,authenticate
from django.shortcuts import render, get_object_or_404
from .forms import *
from customuser.models import *

from django.http import JsonResponse, HttpResponseRedirect


def login_req(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    user = authenticate(username=request_body['email'], password=request_body['password'])
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'success'}, safe=False)
    else:
        return JsonResponse({'status':'error'}, safe=False)

def register(request):
    print(request.POST)
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    data = request.POST.copy()

    form = SignUpForm(request_body)
    print(form.errors)
    if form.is_valid():
        new_user = form.save(data)
        new_user.is_social_reg = False
        new_user.save()
        login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
        return JsonResponse({'status': 'success'}, safe=False)
    else:

        return JsonResponse({'status':'error','errors': form.errors}, safe=False)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def change_avatar(request):
    form = ChangeAvatar(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
        form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def profile_index(request):
    profilePage = True
    profile_index = 'active'
    return render(request, 'user/profile_index.html', locals())

def profile_edit(request):
    profilePage = True
    profile_edit = 'active'
    return render(request, 'user/edit_profile.html', locals())

def profile_finance(request):
    profilePage = True
    profile_finance = 'active'
    return render(request, 'user/finances.html', locals())

def profile_balance(request):
    profilePage = True
    profile_balance = 'active'
    return render(request, 'user/balance.html', locals())

def profile_archive(request):
    profilePage = True
    profile_archive = 'active'
    return render(request, 'user/arhive.html', locals())
