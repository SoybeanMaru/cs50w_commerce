from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .models import User, Listings, Bids, Comments, Watchlist


def index(request):
    listings = Listings.objects.all().order_by('-pk') #Reverse order by pk
    return render(request, "auctions/index.html", {
        "listings": listings
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

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
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html")
    if request.method =="POST":
        item_name = request.POST['item_name']
        item_price = request.POST['item_price']
        item_des = request.POST['item_des']
        item_image = request.FILES.get('item_image')
        item_category = request.POST['category']


        listing = Listings(item_name =item_name,
                           item_price =item_price,
                           item_des = item_des,
                           item_image = item_image,
                           user_id = request.user,
                           is_closed = False,
                           category = item_category)
        listing.save()

        return render(request, "auctions/index.html")


def listing(request, listing_id):
    largest_bid = Bids.objects.filter(listing_id=listing_id).aggregate(Max('bid_price'))['bid_price__max']
    bids = Bids.objects.filter(listing_id=listing_id)
    number_of_bids = len(bids)
    if request.method == "GET":
        is_in_watchlist = Watchlist.objects.filter(user_id=request.user, listing_id=listing_id).exists()
        winner = Bids.objects.filter(listing_id=listing_id, user_id=request.user).first()
        print(winner)
        
        return render(request, "auctions/listing.html", {
            "listing": Listings.objects.filter(pk=listing_id).first(),
            "users": User.objects.all(),
            "comments": Comments.objects.filter(listing_id=listing_id),
            "is_in_watchlist" : is_in_watchlist,
            "number_of_bids" : number_of_bids,
            "largest_bid": largest_bid,
            "winner": winner,
        })
    
    if request.method == "POST":
        current_listing = Listings.objects.get(pk=listing_id)
        
        if 'CLOSE' in request.POST:
            print("=====WE CLOSING=====")
            current_listing.is_closed = True
            current_listing.save()
            return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id})) 
        
        
        
        bid_price = float(request.POST['bid_price'])
        starting_price = current_listing.item_price
        print("Starting PRICE:", starting_price)
        print("BID PRICE:", bid_price)
        # FIRST TIME BID
        if number_of_bids == 0:
            if bid_price < starting_price:
                return render(request, "auctions/error.html", {
                    "message": "Your bidding needs to be larger than the current starting price"
                })
            else:
                adding_bid = Bids(bid_price=bid_price,
                                  user_id=request.user,
                                  listing_id = Listings.objects.get(pk=listing_id))
                adding_bid.save()
                return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id})) 
        
        #NOT FIRST TIME BID
        if number_of_bids > 0:
            if bid_price < largest_bid or bid_price < starting_price:
                return render(request, "auctions/error.html", {
                    "message": "Your bidding needs to be larger than the current largest bid"
                })
            else:
                adding_bid = Bids(bid_price=bid_price,
                                  user_id=request.user,
                                  listing_id= Listings.objects.get(pk=listing_id))
                adding_bid.save()
                return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))


    

def comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST['comment']
        comments = Comments(comm_text = comment,
                            listing_id = Listings.objects.filter(pk=listing_id).first(),
                            user_id = request.user)
        comments.save()
        return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']

        #REMOVE FROM WATCHLIST
        if "REMOVE" in request.POST:
            print("===Removing===")
            watchlist = Watchlist.objects.get(user_id = request.user, listing_id=listing_id)
            watchlist.delete()

            return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id})) 
        
        #ADD TO WATCHLIST
        watchlist = Watchlist(user_id = request.user,
                              listing_id = Listings.objects.get(pk=listing_id))
        watchlist.save()
        return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))
    if request.method == "GET":
        return render(request, "auctions/watchlist.html", {
            "watchlist": Watchlist.objects.filter(user_id = request.user),
            "Listings" : Listings.objects.all()
        })


def closed(request):
    return