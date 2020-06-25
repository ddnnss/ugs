from django.urls import path
from . import views

urlpatterns = [
   path('users', views.users, name='cp_users'),
   path('user/<id>', views.user, name='cp_user'),
   path('bets', views.bets, name='cp_bets'),
   path('bet/<id>', views.bet, name='cp_bet'),
   path('withdraws', views.withdraws, name='cp_withdraws'),
   path('withdraw/<id>', views.withdraw, name='cp_withdraw'),
   path('messages', views.messages, name='cp_messages'),
   path('message/<id>', views.message, name='cp_message'),
   path('del_message/<id>', views.del_message, name='del_message'),
   path('withdraw_ok/<id>', views.withdraw_ok, name='withdraw_ok'),
   path('withdraw_cancel/<id>', views.withdraw_cancel, name='withdraw_cancel'),
   path('payments', views.payments, name='cp_payments'),


]
