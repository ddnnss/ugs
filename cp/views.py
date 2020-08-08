from django.http import HttpResponseRedirect
from django.shortcuts import render
from customuser.models import *
from pages.models import *
from pages.forms import FeedbackForm
from blog.models import *

def users(request):
    allUsers = User.objects.filter(is_superuser=False)
    profilePage = True
    return render(request, 'cp/users.html', locals())

def user(request,id):
    profilePage = True
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
    profilePage = True
    allBets = Bet.objects.filter(is_complete=True).order_by('-id')
    return render(request, 'cp/bets.html', locals())

def bet(request,id):
    profilePage = True
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

def posts(request):
    profilePage = True
    allPosts = BlogPost.objects.all()
    return render(request, 'cp/posts.html', locals())

def post(request,id):
    if request.POST:
        print(request.POST)
        post = BlogPost.objects.get(id=request.POST.get('p_id'))
        post.category_id = request.POST.get('category')
        post.text = request.POST.get('text')
        post.name =  name=request.POST.get('name')
        if request.POST.get('is_active') == '0':
            post.is_active=False
        else:
            post.is_active = True
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    profilePage = True
    post = BlogPost.objects.get(id=id)
    allCats = BlogCategory.objects.all()
    return render(request, 'cp/post.html', locals())

def new_post(request):
    if request.POST:
        print(request.POST)
        if request.POST.get('new_category'):
            BlogCategory.objects.create(name=request.POST.get('new_category'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            post = BlogPost.objects.create(category_id=request.POST.get('category'),
                                           text=request.POST.get('text'),
                                           name=request.POST.get('name'),
                                           image=request.FILES.get('preview_img'),
                                           image_post=request.FILES.get('full_img'),
                                           short_description=request.POST.get('short'),
                                           is_active= request.POST.get('is_active')
                                           )
            post.category_id = request.POST.get('category')
            post.text = request.POST.get('text')
            post.save()
            return HttpResponseRedirect('/cp/posts')


    profilePage = True

    allCats = BlogCategory.objects.all()
    return render(request, 'cp/new_post.html', locals())

def withdraws(request):
    profilePage = True
    allWithdraws = Withdraw.objects.all()
    return render(request, 'cp/withdraws.html', locals())

def withdraw(request,id):
    profilePage = True
    withdrawInfo = Withdraw.objects.get(id=id)
    return render(request, 'cp/withdraw.html', locals())

def messages(request):
    profilePage = True
    allMessages = MessageForm.objects.all().order_by('is_open')
    return render(request, 'cp/messages.html', locals())

def message(request,id):
    profilePage = True
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
    profilePage = True
    allPayments = Payment.objects.all()
    return render(request, 'cp/payments.html', locals())

def feedbacks(request):
    profilePage = True
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