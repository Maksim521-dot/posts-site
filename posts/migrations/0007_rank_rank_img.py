# Generated by Django 3.2.23 on 2024-04-28 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_rank_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='rank',
            name='rank_img',
            field=models.CharField(default='⭒', max_length=50, verbose_name='Значок звания'),
        ),
    ]
