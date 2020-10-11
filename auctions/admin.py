from django.contrib import admin
from .models import User, AuctionListing, Bid

# Register your models here.

@admin.register(AuctionListing)
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ['id','title','description', 'image', 'active'] 
    list_filter = ['startingBid']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email', 'password']
