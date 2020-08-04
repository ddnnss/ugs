from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from customuser.forms import NewMessageForm


def index(request):
    nonLK = True
    allFaqFirst = Faq.objects.filter(is_first=True)
    allFaqSecond = Faq.objects.filter(is_first=False)
    pageTitle = 'Кэшбэк ставки на спорт | Cash Back с проигрышей | Кэшбэк со ставок '
    pageDescription = 'Получайте 💰 кэшбэк с проигрышей в букмекерских компаниях! 💯% гарантия вывода, 💥 всевозможные способы вывода, 🔝 легальные букмекеры. UGSCASH.RU – лучший cash back сервис! У Вас есть возможность вернуть до 50% от проигрыша в букмекерских компаниях!'
    return render(request, 'pages/index.html', locals())

def about(request):
    nonLK = True
    pageTitle = 'О системе UGS - кэшбэк сервис кто мы и чем сможем помочь'
    pageDescription = 'Подробная информация о сервисе, который создан для игроков, которые любят и будут рисковать 💥 UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы.'
    allFeedbacks = Feedback.objects.all()
    return render(request, 'pages/about.html', locals())

def feedbacks(request):
    nonLK = True
    pageTitle = 'Отзывы о системе UGS наших постоянных клиентов'
    pageDescription = 'UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы.'
    allFeedbacks = Feedback.objects.all()
    return render(request, 'pages/feedbacks.html', locals())

def contacts(request):
    nonLK = True
    pageTitle = 'UGS | Контакты | КЭШБЭК СЕРВИС В СТАВКАХ НА СПОРТ'
    pageDescription = 'Сервис создан для игроков, которые любят и будут рисковать. UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы'
    allFaqFirst = Faq.objects.filter(is_first=True)
    allFaqSecond = Faq.objects.filter(is_first=False)
    form = NewMessageForm()
    return render(request, 'pages/contacts.html', locals())

def robots(request):
    robotsTxt = f"User-agent: *\nDisallow: /admin/\nDisallow: /user/\nHost: https://ugscash.ru/\nSitemap: https://ugscash.ru/sitemap.xml"
    return HttpResponse(robotsTxt, content_type="text/plain")

def customhandler404(request, exception, template_name='404.html'):
    pageTitle = 'UGS | Ошибка 404 | КЭШБЭК СЕРВИС В СТАВКАХ НА СПОРТ'
    pageDescription = 'Сервис создан для игроков, которые любят и будут рисковать. UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы'
    return render(request, 'pages/404.html', None,None,status=404)


def receiver(request):
    return render(request, 'pages/receiver.html', locals())