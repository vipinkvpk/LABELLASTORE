# Generated by Django 5.0.4 on 2024-08-02 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_product_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='variation',
            name='stock',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
