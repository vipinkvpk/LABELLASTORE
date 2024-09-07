from django.db import models
from django.urls import reverse
from category.models import Category, Sub_Category
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils.text import slugify


# Create your models here.
# Price Filter
class PriceFilter(models.Model):
    FILTER_CHOICES = (
        ('100 TO 1000', '100 TO 1000'),
        ('1000 TO 10000', '1000 TO 10000'),
        ('10000 TO 20000', '10000 TO 20000'),
        ('20000 TO 30000', '20000 TO 30000'),
        ('30000 TO 40000', '30000 TO 40000'),
        ('40000 TO 50000', '40000 TO 50000'),
        ('50000 and above', '50000 and above'),
    )
    price_range = models.CharField(choices=FILTER_CHOICES, max_length=60)
    
    def __str__(self):
        return self.price_range


class ProductOffer(models.Model):
    offer_name = models.CharField(max_length=100)
    offer_description = models.TextField(max_length=500, blank=True)
    valid_from = models.DateField(auto_now_add=True)
    valid_till = models.DateField()
    offer_discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(30)])
    

    def __str__(self):
        return self.offer_name

    
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug         = models.SlugField(max_length=200, unique=True)
    description  = models.TextField(max_length=500, blank=True)
    offer        = models.ForeignKey(ProductOffer,on_delete=models.SET_NULL, null=True)
    price_range = models.ForeignKey(PriceFilter,on_delete=models.CASCADE)
    price        = models.IntegerField()
    images       = models.ImageField(upload_to='photos/products')
    image1       = models.ImageField(upload_to='product')
    image2       = models.ImageField(upload_to='product')
    image3       = models.ImageField(upload_to='product')
    stock        = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modified_data= models.DateField(auto_now=True)


    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def get_offer_price(self):
        return int(round(self.price-(self.price*(self.offer.offer_discount/100))))

    def __str__(self):
        return self.product_name




class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)
    
variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    price = models.IntegerField(null=True, blank=True)  # Add price field
    stock = models.IntegerField(null=True, blank=True)  # Add stock field
    objects = VariationManager()

    def __str__(self):
        return self.variation_value

    # You might want to override the save method to handle cases 
    # where price/stock is not set for a variation, potentially inheriting
    # from the parent product. Example:
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price  # Inherit from product if not set
        if not self.stock:
            self.stock = self.product.stock  # Inherit from product if not set
        super().save(*args, **kwargs)  
    




# Removal of stock field from Product model only to Variation model

# from django.db import models
# from django.urls import reverse
# from django.utils.text import slugify
# from django.core.validators import MinValueValidator, MaxValueValidator

# # ... (Your other model imports for Category, Sub_Category, etc.)

# class PriceFilter(models.Model):
#     FILTER_CHOICES = (
#         ('100 TO 1000', '100 TO 1000'),
#         ('1000 TO 10000', '1000 TO 10000'),
#         ('10000 TO 20000', '10000 TO 20000'),
#         ('20000 TO 30000', '20000 TO 30000'),
#         ('30000 TO 40000', '30000 TO 40000'),
#         ('40000 TO 50000', '40000 TO 50000'),
#         ('50000 and above', '50000 and above'),
#     )
#     price_range = models.CharField(choices=FILTER_CHOICES, max_length=60)

#     def __str__(self):
#         return self.price_range


# class ProductOffer(models.Model):
#     offer_name = models.CharField(max_length=100)
#     offer_description = models.TextField(max_length=500, blank=True)
#     valid_from = models.DateField(auto_now_add=True)
#     valid_till = models.DateField()
#     offer_discount = models.IntegerField(
#         validators=[MinValueValidator(0), MaxValueValidator(100)]
#     )  

#     def __str__(self):
#         return self.offer_name


# class Product(models.Model):
#     product_name = models.CharField(max_length=200, unique=True)
#     slug = models.SlugField(max_length=200, unique=True)
#     description = models.TextField(max_length=500, blank=True)
#     offer = models.ForeignKey(
#         ProductOffer, on_delete=models.SET_NULL, null=True, blank=True
#     )
#     price_range = models.ForeignKey(PriceFilter, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField for prices
#     images = models.ImageField(upload_to='photos/products')
#     image1 = models.ImageField(upload_to='product', blank=True)
#     image2 = models.ImageField(upload_to='product', blank=True)
#     image3 = models.ImageField(upload_to='product', blank=True)
#     is_available = models.BooleanField(default=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)
#     created_date = models.DateField(auto_now_add=True)
#     modified_data = models.DateField(auto_now=True)

#     def save(self, *args, **kwargs):
#         # ... other logic

#         # If the product is being marked as unavailable,
#         # make sure all variations are also marked as unavailable
#         if not self.is_available:
#             self.variations.update(is_available=False)

#         super(Product, self).save(*args, **kwargs)

#     def get_url(self):
#         return reverse('product_detail', args=[self.category.slug, self.slug])

#     def get_offer_price(self):
#         if self.offer:
#             discount = self.price * (self.offer.offer_discount / 100)
#             return self.price - discount
#         return self.price

#     def get_total_stock(self):
#         return sum(variation.stock for variation in self.variations.all())

#     def __str__(self):
#         return self.product_name


# class VariationManager(models.Manager):
#     def colors(self):
#         return super(VariationManager, self).filter(
#             variation_category='color', is_active=True
#         )

#     def sizes(self):
#         return super(VariationManager, self).filter(
#             variation_category='size', is_active=True
#         )


# variation_category_choice = (('color', 'color'), ('size', 'size'))


# class Variation(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
#     variation_category = models.CharField(max_length=100, choices=variation_category_choice)
#     variation_value = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     created_date = models.DateTimeField(auto_now=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField for variation prices
#     stock = models.IntegerField(default=0) 
#     objects = VariationManager()

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['product', 'variation_category', 'variation_value'], name='unique_variation')
#         ] 

#     def __str__(self):
#         return self.variation_value

#     def save(self, *args, **kwargs):
#         # If the variation is saved as unavailable, set stock to 0
#         if not self.is_available:
#             self.stock = 0

#         # If variation price is not set, use the product price
#         if not self.price:
#             self.price = self.product.price

#         super(Variation, self).save(*args, **kwargs)