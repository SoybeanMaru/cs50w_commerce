# Generated by Django 4.2.5 on 2023-09-26 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listings_item_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='item_img',
            field=models.ImageField(null=True, upload_to='auctions/static/auctions/pictures'),
        ),
    ]
