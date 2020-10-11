from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from PIL import Image

class User(AbstractUser):
    def __str__(self):
        return f'username : {self.username}'
    
    def nbWatchedListings(self):
        return len(self.watchedListings.all().filter(active=True))

class AuctionListing(models.Model):
    listedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=16)
    description = models.TextField()
    startingBid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='img/%Y/%m/%d/', blank=True)
    category = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    watchedBy = models.ManyToManyField(User, related_name='watchedListings', blank=True)
    
    
    def __str__(self):
        return f"{self.title}, starting bid :${self.startingBid}, maxBid : {self.max_bid()}, active :{self.active}, created : {self.created}"
    
    def max_bid(self):
        if self.bids.all():
            return max(item.get_bid() for item in self.bids.all())
        else:
            return self.startingBid

    def get_absolute_url(self):
        return reverse('auctions:listing_detail', args=[self.id])

class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=200)
    commentedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    commentDate = models.DateTimeField(auto_now_add=True)

class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    bidBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userBids')
    bidDate = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"title : {self.title}, bid : {self.bid}, bidBy : {self.bidBy}, bidDate : {self.bidDate}"
    
    def get_bid(self):
        return self.bid