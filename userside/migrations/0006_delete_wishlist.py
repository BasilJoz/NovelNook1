# Generated by Django 4.2.3 on 2023-10-04 10:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("userside", "0005_remove_wishlist_books_wishlist_books"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Wishlist",
        ),
    ]