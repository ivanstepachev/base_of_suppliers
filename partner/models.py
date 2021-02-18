from django.db import models
from django.conf import settings
from user.models import CustomUser
import datetime


class Partner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_partner = models.BooleanField(default=False)
    name = models.CharField(max_length=43)
    code = models.CharField(max_length=12, default='')
    mentor = models.ForeignKey('self', on_delete=models.SET_DEFAULT,
                               default=1, related_name='partners')
    balance = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class Action(models.Model):

    STATUS_CHOICES = (
        ('following', 'Уникальный переход по ссылке'),
        ('partner_pay', 'Оплата по ссылке'),
        ('grandpartner_pay', 'Оплата от партнера'),
    )

    verb = models.CharField(max_length=128)
    status = models.CharField(max_length=62, choices=STATUS_CHOICES, default='following')
    to_partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='actions')
    to_grand_partner = models.ForeignKey(Partner, on_delete=models.PROTECT, related_name='grand_actions')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.verb

    class Meta:
        ordering = ('-date',)


class Payment(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.PROTECT, related_name='payments')
    amount = models.IntegerField()
    confirm = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Выплата {self.partner} на сумму {self.amount}'

