# Generated by Django 3.1.2 on 2020-10-11 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20201010_2153'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BidList',
            new_name='Bid',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='title',
            new_name='listing',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='title',
            new_name='listing',
        ),
    ]