# Generated by Django 4.2.5 on 2023-09-26 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='item_img',
            field=models.ImageField(null=True, upload_to='auctions/pictures'),
        ),
    ]
