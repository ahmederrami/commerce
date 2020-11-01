from django.contrib import admin
from .models import User, Category, AuctionListing, Comment, Bid

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =['category']
    
@admin.register(AuctionListing)
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ['title','description', 'image', 'category','listedBy'] 
    list_filter = ['startingBid']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['listing', 'comment', 'commentedBy']

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['listing', 'bid', 'bidBy']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email', 'password']
