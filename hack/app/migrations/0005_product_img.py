# Generated by Django 4.0.4 on 2022-05-21 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_client_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Url к картинке'),
        ),
    ]