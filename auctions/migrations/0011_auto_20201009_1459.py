# Generated by Django 3.1.2 on 2020-10-09 14:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20201007_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='watchedBy',
            field=models.ManyToManyField(blank=True, related_name='watchedListings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(blank=True, upload_to='img/%Y/%m/%d/'),
        ),
        migrations.DeleteModel(
            name='WatchList',
        ),
    ]