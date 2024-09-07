from django.db import models
from userprofile.models import Address
from store.models import Product
from accounts.models import CustomUser
from django.core.validators import MinValueValidator,MaxValueValidator
# # Create your models here.


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null= False)
    payment_id = models.CharField(max_length=250, null=True)
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    coupon_discount = models.FloatField(null=True, default=0.0, blank=True)  # Add this field
    
    
    def __str__(self):
        return str(self.tracking_no)
    

# EXISTING WRKING ORDERITEM- PREVIOUS ORDER DETAILS GET CHANGED ISSUE
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped',"Shipped"),
        ('Out for delivery',"Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
    )
    status = models.CharField(max_length=150,choices=STATUS, default='Order Confirmed')

    def _str_(self):
        return f"{self.order.id, self.order.tracking_no}"




# ORDER DETAILS NOT AVAILABLE
# from django.db import models

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     price = models.FloatField(null=False)
#     quantity = models.IntegerField(null=False)

#     # Store product details at the time of order:
    # product_name = models.CharField(max_length=250, null=False, blank=True) 
    # product_price = models.FloatField(null=False)
    # quantity = models.IntegerField(null=False)
#     image = models.ImageField(upload_to='photos/order_items', blank=True, null=True)
    
#     STATUS = (
#         ('Order Confirmed', 'Order Confirmed'),
#         ('Shipped',"Shipped"),
#         ('Out for delivery',"Out for delivery"),
#         ('Delivered', 'Delivered'),
#         ('Cancelled','Cancelled'),
#         ('Returned','Returned'),
#     )
#     status = models.CharField(max_length=150,choices=STATUS, default='Order Confirmed')

#     def save(self, *args, **kwargs):
#         # Automatically populate product details when a new OrderItem is created
#         if not self.pk:  # Only run this when the OrderItem is being created, not updated.
#             self.product_name = self.product.product_name
#             # Store the product image:
#         #     self.image = self.product.images.first() if self.product.images.exists() else None 
#         # super().save(*args, **kwargs)

#     def _str_(self):
#         return f"{self.order.id, self.order.tracking_no, {self.product_name}}"




    # def __str__(self):
    #     return f"{self.order.id}, {self.order.tracking_no}, {self.product_name}"



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#for product fdetails not changing- not wking

# from django.db import models
# from userprofile.models import Address
# from store.models import Product
# from accounts.models import CustomUser
# from django.core.validators import MinValueValidator, MaxValueValidator

# ... (Other models)

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     # Store product details at the time of order creation:
#     _product_name = models.CharField(max_length=200, editable=False, null=True, blank=True)
#     _price = models.FloatField(null=True, blank=True)  # Store the price at the time of order
#     quantity = models.IntegerField(null=False)
#     STATUS = (
#         # ... (existing statuses)
#         ('Order Confirmed', 'Order Confirmed'),
#         ('Shipped',"Shipped"),
#         ('Out for delivery',"Out for delivery"),
#         ('Delivered', 'Delivered'),
#         ('Cancelled','Cancelled'),
#         ('Returned','Returned'),
#     )
#     status = models.CharField(max_length=150, choices=STATUS, default='Order Confirmed')

#     def __str__(self):
#         return f"{self.order.id}, {self.order.tracking_no}"

#     def save(self, *args, **kwargs):
#         # Only store product details if they haven't been stored before
#         if not self._product_name:
#             self._product_name = self.product.product_name
#         if not self._price:
#             self._price = self.product.price 
#         super().save(*args, **kwargs)

#     # Properties for accessing product name and price
#     @property
#     def product_name(self):
#         return self._product_name 

#     @property
#     def price(self):
#         return self._price 
    
# # # ... (Rest of your models)
    

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class ReturnOrder(models.Model):
    order_item = models.ForeignKey(OrderItem,on_delete=models.CASCADE)
    return_reason = models.CharField(max_length=100,null=True)
    return_comment = models.TextField(max_length=500,null=True)
    
    def __str__(self):
        return f"{self.id}"
    

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(30)])
    min_value = models.IntegerField(validators=[MinValueValidator(0)])
    valid_from = models.DateField(auto_now_add=True)
    valid_till = models.DateField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
    

class UserCoupon(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    total_price = models.FloatField(null=True)

    def __str__(self):
        return str(self.id)
    

    


