# Generated by Django 4.0.4 on 2022-05-18 10:44

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='product_images/'),
        ),
    ]
