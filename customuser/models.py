import decimal
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.template.loader import render_to_string

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('Эл. почта', unique=True)
    email_add = models.EmailField('Эл. почта', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    phone_add = models.CharField('Телефон', max_length=50, blank=True, null=True)
    profile_ok = models.BooleanField(default=False)
    avatar = models.ImageField('Фото профиля', upload_to='avatar/', blank=True)
    balance = models.DecimalField('Баланс', decimal_places=2,max_digits=10,default=1)
    sex = models.BooleanField('Пол', blank=True, null=True, default=True)
    birthday = models.DateField('ДР', blank=True, null=True)
    country = models.CharField('Страна', max_length=150, blank=True, null=True)
    billing_country = models.CharField('Страна', max_length=150, blank=True, null=True)
    town = models.CharField('Город', max_length=150, blank=True, null=True)
    billing_town = models.CharField('Город', max_length=150, blank=True, null=True)
    house = models.CharField('Дом', max_length=150, blank=True, null=True)
    billing_house = models.CharField('Дом', max_length=150, blank=True, null=True)
    address = models.CharField('Адрес', max_length=150, blank=True, null=True)
    billing_address = models.CharField('Адрес', max_length=150, blank=True, null=True)
    billing_post = models.CharField('Индекс', max_length=150, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    @property
    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            # return 'data:image/png;base64,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'
            return '/static/img/no_ava.svg'
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.first_name and not self.last_name:
            return f'{self.first_name}'
        elif not self.first_name and not self.last_name:
            return f'Анонимный пользователь'

    def get_messages(self):
        allMessages = Message.objects.filter(user=self)
        return allMessages

class MessageForm(models.Model):
    first_name = models.CharField('Имя', max_length=50, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    email = models.CharField('EMail', max_length=50, blank=True, null=True)
    subject = models.CharField('Тема', max_length=50, blank=True, null=True)
    text = models.TextField('Сообщение',  blank=True, null=True)
    is_open = models.BooleanField(default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, null=True)

class UserCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    yandex_wallet = models.CharField('Кошелек ЯД', max_length=50, blank=True, null=True)
    qiwi_wallet = models.CharField('Кошелек Qiwi', max_length=50, blank=True, null=True)
    webmoney_wallet = models.CharField('Кошелек Webmonye', max_length=50, blank=True, null=True)
    card_number = models.CharField('Номер карты', max_length=50, blank=True, null=True)
    card_vcv = models.CharField('CVC', max_length=50, blank=True, null=True)
    card_valid = models.CharField('VALID', max_length=50, blank=True, null=True)

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=True)
    text = models.TextField(null=True,blank=True)
    is_viewed = models.BooleanField(default=False)

    class Meta:
        ordering = ('-id',)

def message_post_save(sender, instance, created, **kwargs):
    if not instance.is_viewed:
        msg_html = render_to_string('email/notify.html',{'text':instance.text})
        send_mail(f'Оповещение на сайте ugscash.ru', None, 'UGSsupport@ugscash.ru',
                  [instance.user.email],
                  fail_silently=False, html_message=msg_html)

class Log(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=True)
    text = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return f'Лог действий пользователя ID: {self.user.id}'

    class Meta:
        verbose_name = "Лог действий"
        verbose_name_plural = "Логи действий"



class Bet(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=True)
    amount = models.DecimalField('Ставка', decimal_places=2,max_digits=10,default=0)
    image = models.ImageField('Фото', upload_to='bet/', blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    coefficient = models.DecimalField('Коэффициент ', decimal_places=2,max_digits=10,default=0)
    cashback = models.IntegerField('Возврат %', default=0)
    bet_result = models.BooleanField('Результат', blank=True,null=True)
    bet_result_amount = models.DecimalField('Результат сумма', decimal_places=2,max_digits=10,default=0)
    team = models.CharField(max_length=255,null=True,blank=True)
    is_no_winner = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, null=True)

    def __str__(self):
        return f'Ставка пользователя ID: {self.user.id} на сумму {self.amount}'

    def get_team(self):
        if self.is_no_winner:
            return 'Ничья'
        else:
            return self.team
    class Meta:
        verbose_name = "Ставка пользователя"
        verbose_name_plural = "Ставки пользователей"



class Payment(models.Model):
    payment_id=models.CharField(max_length=255,null=True,blank=True)
    payment_url=models.TextField(null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=True)
    card = models.ForeignKey(UserCard,on_delete=models.CASCADE,blank=True,null=True)
    amount = models.DecimalField('Сумма', decimal_places=2,max_digits=10,default=0)
    status = models.BooleanField('Статус платежа',default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, null=True)

    class Meta:
        ordering = ('-id',)

class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    card = models.ForeignKey(UserCard, on_delete=models.CASCADE, blank=False, null=True)
    amount = models.DecimalField('Сумма', decimal_places=2, max_digits=10, default=0)
    status = models.BooleanField('Статус платежа', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Дата изменеия', auto_now=True, null=True)

class BalanceFreeze(models.Model):
    bet = models.ForeignKey(Bet,on_delete=models.CASCADE,blank=True,null=True)
    withdraw = models.ForeignKey(Withdraw,on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=True)
    amount = models.DecimalField('Сумма', decimal_places=2,max_digits=10,default=0)

    def __str__(self):
        return f'Резервирование {self.amount} на балансе пользователя ID: {self.user.id}'

    class Meta:
        verbose_name = "Резервирование на балансе"
        verbose_name_plural = "Резервирование на балансе"

def withdraw_post_save(sender, instance, created, **kwargs):
    if created:
        instance.user.balance -= decimal.Decimal(instance.amount)
        instance.user.save()
        BalanceFreeze.objects.create(withdraw=instance, user=instance.user, amount=instance.amount)
        Log.objects.create(user=instance.user,
                           text=f'Пользователь ID:{instance.user.id} запросил вывод на сумму {instance.amount} руб')
        Message.objects.create(user=instance.user,
                               text=f'Запрос на вывод {instance.amount} руб успешно отправлен, сумма вывода заблокирована на счете')

    else:
        if instance.status:
            Log.objects.create(user=instance.user,
                               text=f'Пользователь ID:{instance.user.id} получил вывод на сумму {instance.amount} руб')
            Message.objects.create(user=instance.user,
                                   text=f'Запрос на вывод {instance.amount} руб успешно выполнен')
            BalanceFreeze.objects.get(withdraw=instance).delete()

def payment_post_save(sender, instance, created, **kwargs):
    if created:
        Log.objects.create(user=instance.user,
                           text=f'Пользователь ID:{instance.user.id} инициировал платеж ID {instance.id} на сумму {instance.amount}')
    else:
        if instance.status:
            instance.user.balance += instance.amount
            instance.user.save()
            Log.objects.create(user=instance.user,
                               text=f'Пользователь ID:{instance.user.id} завершил платеж ID {instance.id} на сумму {instance.amount}')
            Message.objects.create(user=instance.user,
                                   text=f'Ваш счет пополнен на сумму {instance.amount}')

def bet_post_save(sender, instance, created, **kwargs):
    if created:
        # instance.user.balance -= instance.amount
        # instance.user.save()
        # BalanceFreeze.objects.create(bet=instance, user=instance.user, amount=instance.amount)
        Log.objects.create(user=instance.user,
                           text=f'Пользователь ID:{instance.user.id} зарегистрировал ставку на сумму {instance.amount}')
    else:
        if instance.is_complete and not instance.bet_result_amount:
            try:
                BalanceFreeze.objects.get(bet=instance, user=instance.user, amount=instance.amount)

            except:
                BalanceFreeze.objects.create(bet=instance, user=instance.user, amount=instance.amount)
                instance.user.balance -= instance.amount
                instance.user.save()
            print('money done')
        if not instance.bet_result_amount:
            if instance.bet_result == True:
                print('win')
                instance.user.balance += instance.amount * decimal.Decimal(instance.coefficient)
                instance.user.save()
                Log.objects.create(user=instance.user,
                                   text=f'Пользователь ID:{instance.user.id} выиграл ставку на сумму {instance.amount} с коэффициентом {instance.coefficient}')
                Message.objects.create(user=instance.user,text=f'Ставка на сумму {instance.amount} от {instance.created_at.strftime("%d-%m-%y %H:%M")} с'
                                                               f' коэфициетном {instance.coefficient} сыграла положительно,'
                                                               f' Ваш счет пополнен на {instance.amount * decimal.Decimal(instance.coefficient):.2f} руб')
                BalanceFreeze.objects.get(bet=instance).delete()
                instance.bet_result_amount = instance.amount * decimal.Decimal(instance.coefficient)
                instance.save()
            elif instance.bet_result == False:
                instance.user.balance = instance.user.balance + ( instance.amount * decimal.Decimal(int(instance.cashback) / 100))
                instance.user.save()
                Log.objects.create(user=instance.user,
                                   text=f'Пользователь ID:{instance.user.id} провыиграл ставку на сумму {instance.amount} с кешбеком {instance.cashback} %')
                instance.bet_result_amount = instance.amount * decimal.Decimal(int(instance.cashback) / 100)
                Message.objects.create(user=instance.user,
                                       text=f'Ставка на сумму {instance.amount} от {instance.created_at.strftime("%d-%m-%y %H:%M")} с'
                                            f' коэфициетном {instance.coefficient} сыграла отрицательно,'
                                            f' Ваш счет пополнен на {instance.bet_result_amount:.2f} руб,'
                                            f' кешбек {int(instance.cashback):.2f} %')
                BalanceFreeze.objects.get(bet=instance).delete()
                instance.save()
            else:
                print('unkown')

post_save.connect(withdraw_post_save, sender=Withdraw)
post_save.connect(payment_post_save, sender=Payment)
post_save.connect(bet_post_save, sender=Bet)
post_save.connect(message_post_save, sender=Message)

