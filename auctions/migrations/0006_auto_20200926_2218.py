# Generated by Django 2.2.12 on 2020-09-26 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200926_1715'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlisting',
            old_name='createdDate',
            new_name='created',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='startingBid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='bidlist',
            name='bid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]