import json
import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from datetime import datetime,timedelta
from django.contrib.auth import login, logout,authenticate
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from random import choices
import string
from .forms import *
from customuser.models import *
import settings
import uuid
import requests
from django.utils.http import urlquote

from django.http import JsonResponse, HttpResponseRedirect

logger = logging.getLogger('django', )

def print_log(text):
    logger.info('--------------------------------------------')
    logger.info(f'{datetime.now()} | {text}')
    logger.info('---------------------------------------------')

def login_req(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    user = authenticate(username=request_body['email'], password=request_body['password'])
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'success'}, safe=False)
    else:
        return JsonResponse({'status':'error'}, safe=False)

def register(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    data = request.POST.copy()
    form = SignUpForm(request_body)
    if form.is_valid():
        new_user = form.save(data)
        new_user.is_social_reg = False
        new_user.save()
        login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
        msg_html = render_to_string('email/new_user.html')
        send_mail(f'Регистрация на сайте ugscash.ru', None, 'no-reply@ugscash.ru',
                  [new_user.email],
                  fail_silently=False, html_message=msg_html)
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
            if new_bet.image:
                response = {'id':new_bet.id,'img':new_bet.image.url.split('/')[3],'team':new_bet.get_team(),'amount':new_bet.amount}
            else:
                response = {'id':new_bet.id,'img': new_bet.url, 'team': new_bet.get_team(), 'amount': new_bet.amount}
            return JsonResponse(response, safe=False)
        else:
            print('balance is bad')
            return JsonResponse({'status': 'error'}, safe=False)
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def complete_bets(request):
    print(request.POST)
    bets = request.POST.get('bets').split(',')
    print(bets)
    for b in bets:
        try:
            bet = Bet.objects.get(id=int(b))
            bet.is_complete = True
            bet.save()
            messages.success(request, 'Все ставки успешно зарегистрированы')
        except:
            messages.success(request, 'Возникла ошибка при регистрации ставок')
            pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def password_recovery(request):
    if request.POST:
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
            user.set_password(new_password)
            user.save()
            msg_html = render_to_string('email/new_password.html',{'new_password':new_password})
            send_mail(f'Новый пароль на сайте ugscash.ru', None, 'no-reply@ugscash.ru',
                      [email],
                      fail_silently=False, html_message=msg_html)
            messages.success(request, 'Спасибо, Ваш новый пароль выслан на почту')
        except:
            messages.success(request, 'Проверьте введенные данные')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def profile_index(request):
    if request.user.is_authenticated:
        profilePage = True
        profile_index = 'active'
        pageTitle = 'Личный кабинет | UGS'
        pageDescription = 'Сервис создан для игроков, которые любят и будут рисковать. UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы'
        lastBets = Bet.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'user/profile_index.html', locals())

def profile_edit(request):
    if request.user.is_authenticated:
        if request.POST:
            form = UpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                user = form.save(commit=False)
                user.sex = bool(int(request.POST.get('sex')))
                user.save()
        pageTitle = 'Личный кабинет | UGS'
        pageDescription = 'Сервис создан для игроков, которые любят и будут рисковать. UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы'
        profilePage = True
        profile_edit = 'active'
        form = UpdateForm()
        return render(request, 'user/edit_profile.html', locals())

def profile_finance(request):
    if request.user.is_authenticated:
        profilePage = True
        profile_finance = 'active'
        current_month = datetime.now().month
        allPayments_temp = Payment.objects.filter(user=request.user)
        time_filter = None
        filter_month = None
        summ_filter = None
        p_c = False

        if request.GET.get('pay_complete'):
            p_c =True

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
        pageTitle = 'Личный кабинет | UGS'
        pageDescription = 'Сервис создан для игроков, которые любят и будут рисковать. UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы'
        return render(request, 'user/finances.html', locals())

def profile_balance(request):
    if request.user.is_authenticated:
        if request.POST:
            print(request.POST)
            if request.POST.get('amount'):
                """запрос на вывод"""
                Withdraw.objects.create(user=request.user,
                                        card_id=int(request.POST.get('cid')),
                                        amount=float(request.POST.get('amount')))
                messages.success(request, f'Спасибо, Ваш запрос на вывод {request.POST.get("amount")} руб. принят')
            if request.POST.get('add_card'):
                """запрос на добавление плтежной системы"""
                if request.POST.get('add_card') == '0':
                    """запрос на добавление карты"""
                    UserCard.objects.create(user=request.user,
                                            card_number=request.POST.get('card'),
                                            card_valid=request.POST.get('valid'),
                                            card_vcv=request.POST.get('cvc'))
                if request.POST.get('add_card') == '1':
                    """запрос на добавление ya кошелька"""
                    UserCard.objects.create(user=request.user,
                                           yandex_wallet=request.POST.get('ya'))
                if request.POST.get('add_card') == '2':
                    """запрос на добавление qiwi кошелька"""
                    UserCard.objects.create(user=request.user,
                                            qiwi_wallet=request.POST.get('qw'))
                if request.POST.get('add_card') == '3':
                    """запрос на добавление webmoney кошелька"""
                    UserCard.objects.create(user=request.user,
                                            webmoney_wallet=request.POST.get('wm'))
            if request.POST.get('remove_card'):
                UserCard.objects.get(user=request.user,id=request.POST.get('remove_card')).delete()


            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        profilePage = True
        profile_balance = 'active'
        cards = UserCard.objects.filter(user=request.user).order_by('-card_number')
        ya_wallet = settings.YA_WALLET
        success_url = settings.SUCCES_URL
        pageTitle = 'Личный кабинет | UGS'
        pageDescription = 'Сервис создан для игроков, которые любят и будут рисковать. UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы'
        return render(request, 'user/balance.html', locals())

def profile_archive(request):
    if request.user.is_authenticated:
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
        pageTitle = 'Личный кабинет | UGS'
        pageDescription = 'Сервис создан для игроков, которые любят и будут рисковать. UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы'

        return render(request, 'user/arhive.html', locals())

def new_payment(request):
    print((datetime.now()+timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%S+03:00'))
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    p_id = uuid.uuid4()
    if request_body['card_id'] != 0:
        card = UserCard.objects.get(id=request_body['card_id'])
    else:
        card = None
    new_pay = Payment.objects.create(user=request.user,
                                     card=card,
                                     payment_id=p_id,
                                     amount=float(request_body['amount'])
                                     )
    new_pay.save()
    if request_body['pay_type'] == 'yandex':
        return JsonResponse({'status': 'ok', 'p_id': new_pay.id, 'pay_type': request_body['pay_type']}, safe=False)
    if request_body['pay_type'] == 'qiwi':
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            "Authorization": f'Bearer {settings.QIWI_SECRET}'
        }
        data ={
            "amount": {
                "currency": "RUB",
                "value": f'{"{:.2f}".format(round(float(request_body["amount"]), 2))}'
            },
            "comment": f'Пополнение счета {request.user.first_name} {request.user.last_name}. Номер : {new_pay.id}',
            "expirationDateTime": f"{(datetime.now()+timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%S+03:00')}",
            "customer": {

                    'phone': UserCard.objects.get(id=request_body['card_id']).qiwi_wallet,
                    'email': request.user.email,
                    'account': request.user.id,


            },

            "customFields": {},
            }
        respond = requests.put(f'https://api.qiwi.com/partner/bill/v1/bills/{new_pay.id}', headers=headers,data=json.dumps(data))
        print(respond.json())
        pay_url = respond.json()['payUrl']
        return_url = urlquote(u'{}'.format(settings.SUCCES_URL))
        full_url= f'{pay_url}&paySource=qw&allowedPaySources=qw&successUrl={return_url}'
        return JsonResponse({'pay_url':full_url,'status': 'ok', 'p_id': new_pay.id, 'pay_type': request_body['pay_type']}, safe=False)







@csrf_exempt
def pay_complete(request):

    req = request.POST
    try:
        payment = Payment.objects.get(id=int(req.get('label')))
        payment.status = True
        payment.save()
    except:
        pass
    return JsonResponse({'status': 'ok'}, safe=False)\

@csrf_exempt
def pay_qiwi_complete(request):
    print_log(request.GET)
    print_log(request.POST)

    # req = request.POST
    # try:
    #     payment = Payment.objects.get(id=int(req.get('label')))
    #     payment.status = True
    #     payment.save()
    # except:
    #     pass
    return JsonResponse({'status': 'ok'}, safe=False)

def new_message(request):
    form = NewMessageForm(request.POST)
    if form.is_valid():
        form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
def view_notify(request):
    temp = Message.objects.filter(user=request.user)
    if temp:
        for i in temp:
            i.is_viewed = True
            i.save()
    return JsonResponse({'status': 'ok'}, safe=False)