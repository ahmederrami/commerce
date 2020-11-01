from django.urls import path
from . import views

#----------------
from django.conf import settings
from django.conf.urls.static import static

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("category/<int:id>", views.category_listings, name="category_listings"),
    path("listing/<int:id>/", views.listing_detail, name="listing_detail"),
    path("addtowatchlist/<int:id>/", views.addto_watchlist, name="addto_watchlist"),
    path("removefromwatchlist/<int:id>/", views.removefrom_watchlist, name="removefrom_watchlist"),
    path("addAuctionListing", views.addListing, name="addAuctionListing"),
    path("closelisting/<int:id>/", views.close_listing, name="close_listing"),
    path("watchlist", views.watchlist, name="watchlist"),    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]

#----------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)