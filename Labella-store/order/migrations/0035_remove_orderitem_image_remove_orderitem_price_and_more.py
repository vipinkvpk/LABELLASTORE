# Generated by Django 5.0.4 on 2024-08-12 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0034_orderitem_image_orderitem_product_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='image',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='price',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product_name',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='_product_name',
            field=models.CharField(blank=True, editable=False, max_length=200, null=True),
        ),
    ]
