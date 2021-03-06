from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',  'password1', 'password2', )
        error_messages = {
            'email': {
                'unique': "Указанный адрес уже кем-то используется",
            }, }

class ChangeAvatar(ModelForm):
    class Meta:
        model = User
        fields = ('avatar',)
        exclude = ()

class NewBet(ModelForm):
    class Meta:
        model = Bet
        fields = ('amount','image','team','is_no_winner','url','comment')
        exclude = ()

class NewMessageForm(ModelForm):
    class Meta:
        model = MessageForm
        fields = ('first_name','last_name','email','phone','subject','text')
        exclude = ()

class UpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',
                  'email_add',
                  'first_name',
                  'last_name',
                  'birthday',
                  'sex',
                  'phone',
                  'phone_add',
                  'country',
                  'billing_country',
                  'town',
                  'billing_town',
                  'billing_post',
                  'house',
                  'billing_house',
                  'address',
                  'billing_address',
                  )

        error_messages = {
             'email': {
                 'unique': "Указанный адрес уже кем-то используется",
             },}


