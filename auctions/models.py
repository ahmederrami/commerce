from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from PIL import Image

class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'
    
    def nbWatchedListings(self):
        return len(self.watchedListings.all().filter(active=True))

class Category(models.Model):
    category = models.CharField(max_length=16)
    createdBy = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category}"

    def activeListings(self):
        return self.listings.filter(active=True)

class AuctionListing(models.Model):
    listedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=16)
    description = models.TextField()
    startingBid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='img/%Y/%m/%d/', blank=True) #%Y/%m/%d/
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)
    closed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wonListings", blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    watchedBy = models.ManyToManyField(User, related_name='watchedListings', blank=True)
    
    class Meta:
        ordering = ('-created',)

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

    class Meta:
        ordering = ('-commentDate',)

class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    bidBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userBids')
    bidDate = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"bid : {self.bid}, bidBy : {self.bidBy}, bidDate : {self.bidDate}"
    
    def get_bid(self):
        return self.bid