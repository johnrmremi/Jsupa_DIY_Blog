# Generated by Django 3.2.7 on 2021-09-02 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment_user_name_commented'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user_name_commented',
            field=models.CharField(default='jsupa', max_length=100, verbose_name='name'),
        ),
    ]