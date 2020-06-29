from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.forms import ModelForm



class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ('name','profession','text','avatar')
        exclude = ()


