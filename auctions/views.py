from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Bids, Comments, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()
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
        print("===start test===")
        print(item_image)
        print("===end test===")

        listing = Listings(item_name =item_name,
                           item_price =item_price,
                           item_des = item_des,
                           item_image = item_image,
                           user_id = request.user)
        listing.save()

        return render(request, "auctions/index.html")


def listing(request, listing_id):
    if request.method == "GET":
        return render(request, "auctions/listing.html", {
            "listing": Listings.objects.filter(pk=listing_id).first(),
            "users": User.objects.all(),
            "comments": Comments.objects.filter(listing_id=listing_id)
        })
    

def comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST['comment']
        comments = Comments(comm_text = comment,
                            listing_id = Listings.objects.filter(pk=listing_id).first(),
                            user_id = request.user)
        comments.save()
        return render(request, "auctions/listing.html", {
            "listing": Listings.objects.filter(pk=listing_id).first(),
            "users": User.objects.all(),
            "comments": Comments.objects.filter(listing_id=listing_id)
        })

def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        print("=====", listing_id)
        watchlist = Watchlist(user_id = request.user,
                              listing_id = Listings.objects.get(pk=listing_id))
        watchlist.save()
        return render(request, "auctions/listing.html", {
            "listing": Listings.objects.filter(pk=listing_id).first(),
            "users": User.objects.all(),
            "comments": Comments.objects.filter(listing_id=listing_id)
        })
    if request.method == "GET":
        return render(request, "auctions/watchlist.html", {
            "watchlist": Watchlist.objects.filter(user_id = request.user),
            "Listings" : Listings.objects.all()
        })


def closed(request):
    return