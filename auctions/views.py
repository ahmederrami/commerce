from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, AuctionListing, Bid
from .forms import BidForm, CommentForm


def index(request):
    activeListing= AuctionListing.objects.filter(active=True)

    return render(request, "auctions/index.html",{
        'activeListing': activeListing
    })

def listing_detail(request, id):
    listing_detail = get_object_or_404(AuctionListing, id=id)
    comments = listing_detail.comments.all()
    
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.commentedBy = request.user
            new_comment.listing = listing_detail
            new_comment.save()
    else:
        comment_form = CommentForm()            

    return render(request, 'auctions/listing_detail.html',{
        'listing_detail': listing_detail,
        'comments' : comments,
        'new_comment' : new_comment,
        'comment_form' : comment_form
    })

def addto_watchlist(request, id):
    listing = AuctionListing.objects.get(id=id)
    user = request.user
    listing.watchedBy.add(user)

    activeListing= AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html",{
        'activeListing': activeListing
    })

def removefrom_watchlist(request, id):
    listing = AuctionListing.objects.get(id=id)
    user = request.user
    listing.watchedBy.remove(user)

    activeListing= AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html",{
        'activeListing': activeListing
    })

def watchlist(request):
    user=request.user
    wlist = user.watchedListings.all().filter(active=True)
    return render(request, 'auctions/watchlist.html', {
        "watchlist":wlist
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            # ----------
            #request.session['user']=user
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
