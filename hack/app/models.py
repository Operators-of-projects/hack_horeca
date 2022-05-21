from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.db import models


def validate_rating(value: float):
    if value < 0:
        raise ValidationError(_(f': {value}'))


class Client(models.Model):
    # user = models.OneToOneField(User, verbose_name='Пользователи', on_delete=models.CASCADE)
    name = models.CharField(max_length=256, verbose_name='ФИО', )
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    balance = models.IntegerField(default=0)
    rating = models.FloatField(validators=[validate_rating], default=0)
    long = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)


class Vendor(models.Model):
    # user = models.OneToOneField(User, verbose_name='Пользователи', on_delete=models.CASCADE)
    name = models.CharField(max_length=256, verbose_name='ФИО', )
    description = models.TextField(verbose_name='Описание', default='')
    photo = models.CharField(max_length=512, verbose_name='Фотография', blank=True, null=True)
    balance = models.IntegerField(default=0)
    rating = models.FloatField(validators=[validate_rating], default=0)
    long = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    status = models.BooleanField(default=False)
    is_product = models.BooleanField()
    is_services = models.BooleanField()


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название организации')
    status = models.BooleanField(default=False)
    price = models.IntegerField()
    img = models.CharField(max_length=512, verbose_name='Url к картинке', blank=True, null=True)
    vendor = models.ForeignKey(Vendor,
                               verbose_name='Вендор',
                               on_delete=models.CASCADE,
                               related_name='products',
                               blank=True,
                               null=True)


class Transaction(models.Model):
    transaction_statuses = [
        (1, 'created'),
        (2, 'viewed'),
        (3, 'done'),
    ]
    vendor_responses = [
        (1, 'waiting'),
        (2, 'on may way'),
        (3, 'denied'),
    ]
    client = models.ForeignKey(Client,
                               verbose_name='Клиент',
                               on_delete=models.CASCADE,
                               related_name='transactions',
                               blank=True,
                               null=True)
    vendor = models.ForeignKey(Vendor, verbose_name='Вендор', on_delete=models.CASCADE, related_name='transactions')
    status = models.IntegerField(choices=transaction_statuses, verbose_name='Статус транзакции', default=1)
    product = models.ManyToManyField(Product, verbose_name='Товары', related_name='transactions')
    response = models.IntegerField(choices=vendor_responses,
                                   verbose_name='Ответ вендора',
                                   blank=True,
                                   null=True)
    cost = models.IntegerField(default=0, blank=True, null=True)


class Report(models.Model):
    transaction = models.ForeignKey(Transaction, verbose_name='Транзакция', on_delete=models.CASCADE, related_name='report')
    score = models.IntegerField()
    comment = models.TextField()

