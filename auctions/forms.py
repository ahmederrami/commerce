from django import forms
from .models import AuctionListing, Bid, Comment

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields =("title","description","startingBid","image","category",)

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ("bid",)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)
