from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class CategoryOffer(models.Model):
    offer_name = models.CharField(max_length=100)
    offer_description = models.TextField(max_length=500, blank=True)
    valid_from = models.DateField(auto_now_add=True)
    valid_till = models.DateField()
    offer_discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(30)])

    def __str__(self):
        return self.offer_name


class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=100 ,unique=True)
    description = models.TextField(max_length=225,blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    offer = models.ForeignKey(CategoryOffer, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural= 'categories'

    def get_url(self):
        return reverse('products_by_category', args={self.slug})
    
        

    def __str__(self):
        return self.category_name
    

class Sub_Category(models.Model):
    sub_category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.sub_category_name)
        super(Sub_Category, self).save(*args, **kwargs)


    class Meta:
        verbose_name = 'sub category'
        verbose_name_plural = 'sub categories'

    def get_url(self):
        return reverse('products_by_sub_category',args=[self.slug])

    def __str__(self):
        return self.sub_category_name
