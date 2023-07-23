# Generated by Django 4.1.3 on 2023-07-23 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_user_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_status',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='', max_length=100, unique=True),
        ),
    ]