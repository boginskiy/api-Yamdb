# Generated by Django 2.2.16 on 2022-09-18 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_user_confirmation_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.IntegerField(null=True, verbose_name='Код подтверждения'),
        ),
    ]
