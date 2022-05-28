from versatileimagefield.fields import VersatileImageField

from django.db import models
from django.core.validators import MinLengthValidator


class Category(models.Model):
    name = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(2, "Name must be greater than 2 characters.")]
    )
    slug = models.SlugField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(2, "Name must be greater than 2 characters.")]
    )
    slug = models.SlugField()
    description = models.TextField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = VersatileImageField(upload_to="product_images/", blank=True, null=True)    
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'
