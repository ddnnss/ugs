from django.urls import path
from . import views

urlpatterns = [
   path('users', views.users, name='cp_users'),
   path('user/<id>', views.user, name='cp_user'),
   path('bets', views.bets, name='cp_bets'),
   path('bet/<id>', views.bet, name='cp_bet'),
   path('posts', views.posts, name='cp_posts'),
   path('post/<id>', views.post, name='cp_post'),
   path('new_post', views.new_post, name='cp_new_post'),
   path('withdraws', views.withdraws, name='cp_withdraws'),
   path('withdraw/<id>', views.withdraw, name='cp_withdraw'),
   path('messages', views.messages, name='cp_messages'),     
   path('message/<id>', views.message, name='cp_message'),
   path('feedbacks', views.feedbacks, name='cp_feedbacks'),
   path('feedbacks/add', views.feedbacks_add, name='cp_feedbacks_add'),
   path('feedback_del/<id>', views.feedback_del, name='cp_feedback_del'),
   path('del_message/<id>', views.del_message, name='del_message'),
   path('withdraw_ok/<id>', views.withdraw_ok, name='withdraw_ok'),
   path('withdraw_cancel/<id>', views.withdraw_cancel, name='withdraw_cancel'),
   path('payments', views.payments, name='cp_payments'),


]
