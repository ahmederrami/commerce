# Generated by Django 2.2.12 on 2020-09-25 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200925_2032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='imageUrl',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(blank=True, upload_to='img/cars/'),
        ),
    ]