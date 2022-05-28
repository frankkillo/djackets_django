from unicodedata import category
from versatileimagefield.serializers import VersatileImageFieldSerializer

from django.utils.text import slugify

from rest_framework import serializers

from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
              ("full_size", "url"),
              ("thumbnail", "thumbnail__300x200"),
        ],
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "image",
            "get_absolute_url"
        ]


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "products",
            "get_absolute_url"
        ]