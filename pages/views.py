from django.shortcuts import render
from .models import Faq
def index(request):
    allFaqFirst = Faq.objects.filter(is_first=True)
    allFaqSecond = Faq.objects.filter(is_first=False)

    return render(request, 'pages/index.html', locals())

def about(request):
    return render(request, 'pages/about.html', locals())

def contacts(request):
    allFaqFirst = Faq.objects.filter(is_first=True)
    allFaqSecond = Faq.objects.filter(is_first=False)
    return render(request, 'pages/contacts.html', locals())