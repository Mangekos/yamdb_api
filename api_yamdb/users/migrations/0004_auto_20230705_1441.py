# Generated by Django 2.2.16 on 2023-07-05 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230702_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='пароль'),
        ),
    ]
