from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    listedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    title = models.CharField(max_length=16)
    description = models.CharField(max_length=64)
    startingBid = models.FloatField()
    imageUrl = models.URLField(max_length=200)
    category = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} : ${self.startingBid}"

class WatchList(models.Model):
    title = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    watchedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    watchedDate = models.DateTimeField(default=datetime.datetime.now)

class Comment(models.Model):
    title = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    commentedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    commentDate = models.DateTimeField(default=datetime.datetime.now)

class BidList(models.Model):
    title = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bid = models.FloatField()
    bidBy = models.ForeignKey(User, on_delete=models.CASCADE)
    bidDate = models.DateTimeField(default=datetime.datetime.now)