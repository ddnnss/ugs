import json

from django.contrib import messages
from datetime import datetime
from django.contrib.auth import login, logout,authenticate
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

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

def new_bet(request):
    form = NewBet(request.POST, request.FILES)
    if request.user.balance >= float(request.POST.get('amount')):
        print('balance is ok')
        if form.is_valid():
            new_bet = form.save(commit=False)
            new_bet.user = request.user
            new_bet.save()
        else:
            print('balance is bad')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def profile_index(request):
    profilePage = True
    profile_index = 'active'
    lastBets = Bet.objects.all().order_by('-created_at')
    return render(request, 'user/profile_index.html', locals())

def profile_edit(request):
    if request.POST:
        print(request.POST)
        form = UpdateForm(request.POST, instance=request.user)
        print(form.errors)
        if form.is_valid():
            user = form.save()

    profilePage = True
    profile_edit = 'active'
    form = UpdateForm()
    return render(request, 'user/edit_profile.html', locals())

def profile_finance(request):
    profilePage = True
    profile_finance = 'active'
    current_month = datetime.now().month
    allPayments_temp = Payment.objects.filter(user=request.user)
    time_filter = None
    filter_month = None
    summ_filter = None

    if request.GET.get('time') and request.GET.get('time') != 'all':
        time_filter = request.GET.get('time')
        if time_filter == 'c_m':
            filter_month = current_month
        elif time_filter == 'l_m':
            filter_month = current_month - 1
            if filter_month == 0:
                filter_month = 12

    if request.GET.get('summ') and request.GET.get('summ') != 'all':
        summ_filter = int(request.GET.get('summ'))
    if time_filter and summ_filter:
        allPayments = allPayments_temp.filter(created_at__month=filter_month,amount__gte=summ_filter)
    elif time_filter:
        allPayments = allPayments_temp.filter(created_at__month=filter_month)
    elif summ_filter:
        allPayments = allPayments_temp.filter(amount__gte=summ_filter)
    else:
        allPayments = allPayments_temp

    return render(request, 'user/finances.html', locals())

def profile_balance(request):
    profilePage = True
    profile_balance = 'active'
    return render(request, 'user/balance.html', locals())

def profile_archive(request):
    profilePage = True
    profile_archive = 'active'
    allBets_temp = Bet.objects.filter(user=request.user).order_by('-created_at')
    current_month = datetime.now().month
    time_filter = None
    filter_month = None
    summ_filter = None

    if request.GET.get('time') and request.GET.get('time') != 'all':
        time_filter = request.GET.get('time')
        if time_filter == 'c_m':
            filter_month = current_month
        elif time_filter == 'l_m':
            filter_month = current_month - 1
            if filter_month == 0:
                filter_month = 12

    if request.GET.get('summ') and request.GET.get('summ') != 'all':
        summ_filter = int(request.GET.get('summ'))
    if time_filter and summ_filter:
        allBets = allBets_temp.filter(created_at__month=filter_month, amount__gte=summ_filter)
    elif time_filter:
        allBets = allBets_temp.filter(created_at__month=filter_month)
    elif summ_filter:
        allBets = allBets_temp.filter(amount__gte=summ_filter)
    else:
        allBets = allBets_temp


    return render(request, 'user/arhive.html', locals())

def new_payment(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    new_pay = Payment.objects.create(user=request.user,amount=int(request_body['amount']))
    new_pay.save()
    return JsonResponse({'status': 'ok', 'p_id': new_pay.id}, safe=False)


@csrf_exempt
def pay_complete(request):

    req = request.POST
    # notification_type = req.get('notification_type')
    # amount = req.get('amount')
    # codepro  = req.get('codepro')
    # withdraw_amount = req.get('withdraw_amount')
    # unaccepted = req.get('unaccepted')
    # label = json.loads(req.get('label'))
    # datetime  = req.get('datetime')
    # sender = req.get('sender')
    # sha1_hash = req.get('sha1_hash')
    # operation_id = req.get('operation_id')

    print(req)

def add_payment(request):
    if request.POST.get('card'):
        request.user.card_number = request.POST.get('card')
        request.user.save()
    if request.POST.get('ya'):
        request.user.yandex_wallet = request.POST.get('ya')
        request.user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))