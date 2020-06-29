from django.http import HttpResponseRedirect
from django.shortcuts import render
from customuser.models import *
from pages.models import *
from pages.forms import FeedbackForm

def users(request):
    allUsers = User.objects.filter(is_superuser=False)
    return render(request, 'cp/users.html', locals())

def user(request,id):
    user = User.objects.get(id=id)
    if request.POST:
        user.balance = float(request.POST.get('balance'))
        user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    userBets = Bet.objects.filter(user=user).order_by('-id')
    userFreeze = BalanceFreeze.objects.filter(user=user)
    userFreezeSumm = 0
    for i in userFreeze:
        userFreezeSumm += i.amount
        print(i.amount)
    userPayments = Payment.objects.filter(user=user)
    return render(request, 'cp/user.html', locals())

def bets(request):
    allBets = Bet.objects.all().order_by('-id')
    return render(request, 'cp/bets.html', locals())

def bet(request,id):
    bet = Bet.objects.get(id=id)
    if request.POST:
        bet.cashback = request.POST.get('cb')
        bet.coefficient = float(request.POST.get('cc'))
        if request.POST.get('result') != 'none':
            if request.POST.get('result') == '1':
                bet.bet_result = True
            if request.POST.get('result') == '0':
                bet.bet_result = False
        bet.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    result = 'None'
    if bet.bet_result == True:
        result = '1'
    elif bet.bet_result == False:
        result = '0'
    return render(request, 'cp/bet.html', locals())

def withdraws(request):
    allWithdraws = Withdraw.objects.all()
    return render(request, 'cp/withdraws.html', locals())

def withdraw(request,id):
    withdrawInfo = Withdraw.objects.get(id=id)
    return render(request, 'cp/withdraw.html', locals())

def messages(request):
    allMessages = MessageForm.objects.all().order_by('is_open')
    return render(request, 'cp/messages.html', locals())

def message(request,id):
    messageInfo = MessageForm.objects.get(id=id)
    messageInfo.is_open = True
    messageInfo.save()
    return render(request, 'cp/message.html', locals())

def del_message(request,id):
    MessageForm.objects.get(id=id).delete()
    return HttpResponseRedirect('/cp/messages')

def withdraw_ok(request,id):
    withdrawInfo = Withdraw.objects.get(id=id)
    withdrawInfo.status = True
    withdrawInfo.save()
    return HttpResponseRedirect('/cp/withdraws')

def withdraw_cancel(request,id):
    withdrawInfo = Withdraw.objects.get(id=id)
    withdrawInfo.user.balance += withdrawInfo.amount
    BalanceFreeze.objects.get(withdraw=withdrawInfo).delete()
    Log.objects.create(user=withdrawInfo.user,
                       text=f'Отмена запроса ID {withdrawInfo.id} на вывод {withdrawInfo.amount} руб')
    Message.objects.create(user=withdrawInfo.user,
                           text=f'Отмена запроса на вывод {withdrawInfo.amount} руб, заблокированные средства возвращены на счет')
    withdrawInfo.user.save()
    withdrawInfo.delete()
    return HttpResponseRedirect('/cp/withdraws')


def payments(request):
    allPayments = Payment.objects.all()
    return render(request, 'cp/payments.html', locals())

def feedbacks(request):
    allFeedbacks = Feedback.objects.all()
    return render(request, 'cp/feedbacks.html', locals())

def feedbacks_add(request):
    if request.POST:
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cp/feedbacks')
    form = FeedbackForm()
    return render(request, 'cp/feedbacks_add.html', locals())

def feedback_del(request,id):
    Feedback.objects.get(id=id).delete()
    return HttpResponseRedirect('/cp/feedbacks')