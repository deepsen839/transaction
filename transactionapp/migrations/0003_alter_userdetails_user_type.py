# Generated by Django 4.1.3 on 2022-11-12 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactionapp', '0002_alter_userdetails_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='user_type',
            field=models.IntegerField(default=2),
        ),
    ]
