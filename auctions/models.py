from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.username}"
    
class Listings(models.Model):
    item_name = models.CharField(max_length=60)
    item_des = models.TextField(max_length=300)
    item_price = models.FloatField()
    item_image = models.ImageField(upload_to="item_images/", null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name}"
    
class Bids(models.Model):
    bid_price = models.FloatField()
    bid_at = models.DateTimeField(auto_now_add=True)
    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"User{self.user_id} bidded at listing{self.listing_id} at {self.bid_at} with price: {self.bid_price}"
    
class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    comm_text = models.TextField(max_length=200)
    comment_at = models.DateTimeField(auto_now_add=True)


class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE)









