# Generated by Django 4.2.5 on 2023-09-26 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_remove_listings_item_img_listings_item_imge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listings',
            old_name='item_imge',
            new_name='item_imgae',
        ),
    ]
