from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Category, AuctionListing, Bid
from .forms import AuctionListingForm, BidForm, CommentForm


def index(request):
    activeListing= AuctionListing.objects.filter(active=True)
    wonListing= None
    watchlist= None # To use index.html for watchlist
    if request.user.is_authenticated:
        # add listing won by this user
        wonListing= AuctionListing.objects.filter(closed=True).filter(winner=request.user)

    return render(request, "auctions/index.html",{
        'activeListing': activeListing,
        'wonListing': wonListing,
        'watchlist' : watchlist
    })

def categories(request):
    categories= Category.objects.all()

    return render(request, "auctions/categories.html",{
        'categories': categories
    })

def category_listings(request, id):
    category = get_object_or_404(Category, id=id)
    activeListing = category.listings.filter(active=True)
    wonListing= None
    if request.user.is_authenticated:
        # add listing won by this user
        wonListing= AuctionListing.objects.filter(closed=True).filter(winner=request.user)

    return render(request, "auctions/index.html",{
        'activeListing': activeListing,
        'wonListing': wonListing,
        'watchlist' : None
    })

def listing_detail(request, id):
    listing_detail = get_object_or_404(AuctionListing, id=id)
    comments = listing_detail.comments.all()
    
    new_comment = None
    message_success = None
    message_failure = None
    message = None

    if request.method == 'POST':
        # A comment or a bid was posted
        comment_form = CommentForm(data=request.POST)
        bid_form = BidForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.commentedBy = request.user
            new_comment.listing = listing_detail
            new_comment.save()
            message_success = "Your comment was added"
        else:
            comment_form = CommentForm()
            if bid_form.is_valid():
                if float(request.POST.get("bid")) - float(listing_detail.max_bid())<=0:
                    message_failure = "Your bid must be greater than the current price"
                    bid_form = BidForm()
                else:
                    new_bid = bid_form.save(commit=False)
                    new_bid.bidBy = request.user
                    new_bid.listing = listing_detail
                    new_bid.save()
                    message_success = "Your bid was added"
            else:
                bid_form = BidForm()
    
    comment_form = CommentForm()
    bid_form = BidForm()

    return render(request, 'auctions/listing_detail.html',{
        'listing_detail': listing_detail,
        'comment_form' : comment_form,
        'bid_form' : bid_form,
        'message_success' : message_success,
        'message_failure' : message_failure
    })

def addListing(request):

    message_success = None
    message_failure = None

    if request.method == 'POST':
        # A listing was posted

        listing_form = AuctionListingForm(request.POST, request.FILES)
        if listing_form.is_valid():
            new_listing = listing_form.save(commit=False)
            new_listing.image = listing_form.cleaned_data.get("image")
            new_listing.listedBy = request.user
            new_listing.save()
            message_success = "Your listing was added"
        else:
            message_failure = "Your data is not valid "
    else:
        listing_form = AuctionListingForm()

    return render(request, 'auctions/auction_listing.html', {
        'listing_form' : listing_form,
        'message_success' : message_success,
        'message_failure' : message_failure,
    })

def close_listing(request, id):
    listing = AuctionListing.objects.get(id=id)
    listing.closed = True
    if listing.bids.all():
        max_bid = listing.max_bid()
        listing.winner = Bid.objects.get(bid=max_bid).bidBy
    listing.active = False
    listing.save()

    return render(request, 'auctions/listing_detail.html',{
        'listing_detail': listing
    })

def addto_watchlist(request, id):
    listing = AuctionListing.objects.get(id=id)
    user = request.user
    listing.watchedBy.add(user)

    activeListing= AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html",{
        'activeListing': activeListing,
        'wonListing': None,
        'watchlist' : None
    })

def removefrom_watchlist(request, id):
    listing = AuctionListing.objects.get(id=id)
    user = request.user
    listing.watchedBy.remove(user)

    activeListing= AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html",{
        'activeListing': activeListing,
        'wonListing': None,
        'watchlist' : None
    })

def watchlist(request):
    user=request.user
    watchlist = user.watchedListings.all().filter(active=True)

    return render(request, 'auctions/index.html', {
        'activeListing': None,
        'wonListing': None,
        'watchlist' : watchlist
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
