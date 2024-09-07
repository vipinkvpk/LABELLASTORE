
from datetime import datetime, timedelta
import calendar

import re
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from userprofile.models import Address
from order.models import Order, OrderItem
from dashboard.forms import ProductForm, CategoryForm
from store.models import Product, Variation,variation_category_choice, PriceFilter,ProductOffer
from category.models import Category,Sub_Category,CategoryOffer
from django.db.models.functions import TruncDay,Cast
from order.models import Coupon, UserCoupon
from django.db.models import Sum,DateField
from accounts.models import CustomUser



# from datetime import datetime
from django.utils import timezone

# order = Order.objects.create(created_at=timezone.now()) 

# from django.utils import timezone

# order = Order.objects.get(pk=1)
# order.created_at = timezone.make_aware(order.created_at, timezone=timezone.get_current_timezone())
# order.save()

# Create your views here.
def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None and user.is_superuser:
            request.session['email'] = email
            auth.login(request, user)
            print('admin logged in ')
            # messages.success(request, 'successfully logged in!')
            return redirect('dashboard')
        else:
            print('Not authorised')
            messages.error(request, 'Invalid credentials / Wrong password')
            return redirect('adminlogin')
        
    return render(request, 'dashboard/adminlogin.html')



# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
# @login_required(login_url='adminlogin')
# # Create your views here.
# def dashboard(request):
#     if not request.user.is_superuser:
#         return redirect('adminlogin')

#     delivered_items = OrderItem.objects.filter(status='Delivered')

#     revenue = 0
#     for item in delivered_items:
#         revenue += item.order.total_price

#     top_selling = OrderItem.objects.annotate(total_quantity= Sum('quantity')).order_by('-total_quantity').distinct()[:5]

#     recent_sale = OrderItem.objects.all().order_by('-id')[:5]

#     today = datetime.today()
#     date_range = 7

#     four_days_ago = today - timedelta(days=date_range)

#     # orders = Order.objects.filter(created_at_gte=four_days_ago, created_at_lte=today)
#     orders = Order.objects.filter(created_at__gte=four_days_ago, created_at__lte=today)
#     sales_by_day = orders.annotate(day=TruncDay('created_at')).values('day').annotate(total_sales=Sum('total_price')).order_by('day')
#     print(sales_by_day,"daxii")
#     sales_dates = Order.objects.annotate(sale_date=Cast('created_at', output_field=DateField())).values('sale_date').distinct()

#     context = {
#         'total_users':CustomUser.objects.count(),
#         'sales':OrderItem.objects.count(),
#         'revenue':revenue,
#         'top_selling':top_selling,
#         'recent_sales':recent_sale,
#         'sales_by_day':sales_by_day,
#     }
#     return render(request,'dashboard/admin_home.html',context)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='adminlogin')
def users(request):
    users = CustomUser.objects.all()
    context = {
        'users': users
    }
    return render (request,'dashboard/users.html',context)


def blockuser(request,id):
    user = CustomUser.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        user.save()
        messages.success(request,'user successfully blocked')
    else:
        user.is_active = True
        user.save()
        messages.success(request,'user successfully unblocked')
    return redirect('users')



def adminlogout(request):
    if 'email' in request.session:
        request.session.flush()
    auth.logout(request)
    return redirect('adminlogin')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='adminlogin')
def product_list(request):
    if 'email' in request.session:
        products = Product.objects.all()
        categories = Category.objects.all()
        sub_categories = Sub_Category.objects.all()
        offer =  ProductOffer.objects.all()
        price_range = PriceFilter.objects.all()
        print(price_range,"daxo")
        
        context = {
            'products' : products,
            'category' : categories,
            'sub_category' : sub_categories,
            'offer' : offer,
            'price_range' : price_range,
        }
        return render(request, 'dashboard/product_list.html',context)
    else:
        return redirect('adminlogin')
        # return redirect('dashboard')


def product_delete(request, id):
    products = Product.objects.filter(id=id)
    products.delete()
    return redirect('product_list')


def add_product(request):
    categories = Category.objects.all()
    sub_categories = Sub_Category.objects.all()
    offer =  ProductOffer.objects.all()
    price_range = PriceFilter.objects.all()
    
    context = {
            'category' : categories,
            'sub_category' : sub_categories,
            'offer'        : offer,
            'price_range'  : price_range,
        }
    
    if request.method == "POST":
        product_name = request.POST['product_name']
        stock = request.POST['stock']
        price = request.POST['price']
        description = request.POST['description']
        image = request.FILES.get('image', None)
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get('image2', None)
        image3 = request.FILES.get('image3',None)
        category = request.POST.get('category')
        offer_name  = request.POST.get('offer')
        price_ranges  = request.POST.get('price_range')
        print(category,'sifan')
        sub_category = request.POST.get('sub_category')

        # validation product already exist


        if Product.objects.filter(product_name=product_name).exists():
            messages.error(request, 'Product name already exist')
            return redirect('product_list')
        

        if product_name == '':
            messages.error(request,"name field are empty")
            return redirect('product_list')
        
        
        if not re.search('[a-zA-Z]', product_name):
            messages.error(request, 'Product name should contain at least one alphabet')
            return redirect('product_list')
        

        try:
            check_number = int(price)
            check_number = int(stock)
        except:
            messages.info(request,'number field got unexpected values')
            return redirect('product_list')
        
        #validation for product price and stock less than zero

        check_pos =[int(price),int(stock)]
        for value in check_pos:
            if value < 0 or value == '':
                messages.info(request,'price and quantity should be positive number')
                return redirect('product_list')
            else:
                pass

        
        if image is None or image1 is None or image2 is None or image3 is None:
            messages.error(request, 'Image field is empty.')
            return redirect('product_list')


        try:
            cat = Category.objects.get(category_name=category)
        except Category.DoesNotExist:

    # Handle the case when the category does not exist
            messages.error(request, 'Invalid category')
            return redirect('product_list')

        try:
           sub_cate = Sub_Category.objects.get(sub_category_name=sub_category)
        except Sub_Category.DoesNotExist:

    # Handle the case when the sub-category does not exist
            messages.error(request, 'Invalid sub-category')
            return redirect('product_list')
        

        price_range = PriceFilter.objects.get(price_range=price_ranges)

        new = Product.objects.create(
                product_name=product_name,
                stock=stock,
                price=price,
                images=image,
                image1=image1,
                image2=image2,
                image3=image3,
                category=cat,
                sub_category=sub_cate,
                description=description,
                price_range = price_range,
                
        )

        try:
            offers=ProductOffer.objects.get(offer_name=offer_name)
            new.offer = offers
            new.save()
        except:
            pass


        new.is_available=True
        new.save()

        return redirect('product_list')
    
    return render(request, 'dashboard/product_list.html',context)

    



def product_edit(request, product_id):
    categories = Category.objects.all()
    sub_categories = Sub_Category.objects.all()
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product_name = request.POST.get('product_name')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        offer_name  = request.POST.get('offer')
        price_ranges  = request.POST.get('price_range')
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')

        if Product.objects.filter(product_name=product_name).exclude(id=product_id).exists():
            messages.error(request, 'Product name already exists')
            return redirect('product_list')

        if not (product_name and price):
            messages.error(request, "Name or price field is empty")
            return redirect('product_list')

        if not re.search('[a-zA-Z]', product_name):
            messages.error(request, 'Product name should contain at least one alphabet')
            return redirect('product_list')
        
        try:
            check_number = int(price)
            check_number = int(stock)
        except:
            messages.info(request,'number field got unexpected values')
            return redirect('product_list')
        
        check_pos =[int(price),int(stock)]
        for value in check_pos:
            if value < 0 or value == '':
                messages.info(request,'price and quantity should be positive number')
                return redirect('product_list')
            else:
                pass
        
        
        cat = get_object_or_404(Category, category_name=category)
        sub_cate = get_object_or_404(Sub_Category, sub_category_name=sub_category)
        price_range = PriceFilter.objects.get(price_range=price_ranges)

        product.product_name = product_name
        product.stock = stock
        product.price = price
        product.description = description
        product.category = cat
        product.sub_category = sub_cate
        product.price_range = price_range
        product.is_available = True

        try:
            offers=ProductOffer.objects.get(offer_name=offer_name)
            product.offer = offers
        except:
            pass
        
        if image:
            product.images = image
        if image1:
            product.image1 = image1
        if image2:
            product.image2 = image2
        if image3:
            product.image3 = image3

        product.save()

        return redirect('product_list')

    context = {
        'category': categories,
        'sub_category': sub_categories,
        'product': product,
    }

    return render(request, 'dashboard/product_list.html', context)



#1. EXISTING WORKING CODE

# def category_list(request):
#     category = Category.objects.all()
#     context={
#         'category' : category
#     }

#     return render(request, 'dashboard/category_list.html',context)


# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
# @login_required(login_url='adminlogin')
# def category_list(request):
#     categories = Category.objects.all()
#     category_offers = CategoryOffer.objects.all() # Fetch available category offers
#     context={
#         'category' : categories,
#         'category_offers': category_offers, # Pass category offers to the template
#     }
#     return render(request, 'dashboard/category_list.html',context)


# INITIAL CODE WITHOUT DUPLICATE ITEM VALIDATION
# def add_category(request):
#     if request.method == "POST":
#         category_name = request.POST['category_name']
#         description = request.POST['description']
        
#         if Category.objects.filter(category_name=category_name).exists():
#             messages.error(request, 'Category name already exist')
#             return redirect('category_list')
        

#         if category_name == '':
#             messages.error(request,"name or slug field are empty")
#             return redirect('category_list')
        
#         if not re.search('[a-zA-Z]', category_name):
#             messages.error(request, 'category name should contain at least one alphabet')
#             return redirect('category_list')
            
        

#         new = Category.objects.create(
#                 category_name=category_name,
        
#                 description=description
#         )

#         new.save()

#         return redirect('category_list')
    

#     return render(request, 'dashboard/category_list.html')



#2.  EXISTING CODE WORKING
# reject duplicate categories (case insensitively)

# def add_category(request):
#     if request.method == "POST":
#         category_name = request.POST['category_name']
#         description = request.POST['description']

#         # Check for duplicates case-insensitively
#         if Category.objects.filter(category_name__iexact=category_name).exists():
#             messages.error(request, 'Category name already exists (case-insensitive)')
#             return redirect('category_list')

#         if category_name == '':
#             messages.error(request,"Name field is empty")
#             return redirect('category_list')

#         if not re.search('[a-zA-Z]', category_name):
#             messages.error(request, 'Category name should contain at least one alphabet')
#             return redirect('category_list')
            
#         new = Category.objects.create(
#             category_name=category_name,
#             description=description
#         )

#         new.save()

#         return redirect('category_list')

#     return render(request, 'dashboard/category_list.html')

# def add_category(request):
#     if request.method == "POST":
#         form = CategoryForm(request.POST, request.FILES)  # Use the form
#         if form.is_valid():
#             form.save()
#             return redirect('category_list')
#         else:
#             messages.error(request, form.errors)  # Display form errors
#     else:
#         form = CategoryForm()  # Create an empty form instance

#     context = {
#         'form': form,  # Pass the form to the template
#         'category': Category.objects.all()
#     }
#     return render(request, 'dashboard/category_list.html', context)



def category_delete(request, category_id):
    category=Category.objects.get(id=category_id)
    category.delete()
    return redirect('category_list')





# def category_edit(request, category_id):
#     category = Category.objects.get(id=category_id)

#     if request.method == "POST":
#         category_name = request.POST.get('category_name')
#         description = request.POST.get('description')
        
#         print(category_name)

#         if Category.objects.filter(category_name=category_name).exclude(id=category_id).exists():
#             messages.error(request, 'Product name already exists')
#             return redirect('add_product')
        
#         if category_name == '':
#             messages.error(request,"name or slug field are empty")
#             return redirect('category_list')
        
#         if not re.search('[a-zA-Z]', category_name):
#             messages.error(request, 'category name should contain at least one alphabet')
#             return redirect('category_list')
        

#         category.category_name = category_name
#         category.description = description
#         category.save()

#         return redirect('category_list')

    
#     return render(request, 'dashboard/category_list.html')
    

#3. EXISTING WORKING CODE
# Reject duplicate categories (case insensitively)

# def category_edit(request, category_id):
#     category = Category.objects.get(id=category_id)

#     if request.method == "POST":
#         category_name = request.POST.get('category_name')
#         description = request.POST.get('description')

#         # Check for duplicates case-insensitively (excluding the current category)
#         if Category.objects.filter(category_name__iexact=category_name).exclude(id=category_id).exists():
#             messages.error(request, 'Category name already exists (case-insensitive)')
#             return redirect('category_list')

#         if category_name == '':
#             messages.error(request,"Name field is empty")
#             return redirect('category_list')

#         if not re.search('[a-zA-Z]', category_name):
#             messages.error(request, 'Category name should contain at least one alphabet')
#             return redirect('category_list')

#         category.category_name = category_name
#         category.description = description
#         category.save()

#         return redirect('category_list')

#     return render(request, 'dashboard/category_list.html', {'category': category})


# def category_edit(request, category_id):
#     category = Category.objects.get(id=category_id)
#     category_offers = CategoryOffer.objects.all()

#     if request.method == "POST":
#         form = CategoryForm(request.POST, request.FILES, instance=category)  # Use the form
#         if form.is_valid():
#             form.save()
#             return redirect('category_list')
#         else:
#             messages.error(request, form.errors)  # Display form errors
#     else:
#         form = CategoryForm(instance=category)  # Create a form instance with data

#     context = {
#         'form': form,  # Pass the form to the template
#         'category': category,  # Pass the category instance (optional)
#         'category_offers': category_offers, # Pass category offers to the template
#     }
#     return render(request, 'dashboard/category_list.html', context)


#============================

from django.shortcuts import render, redirect
from .forms import CategoryForm  
from category.models import Category

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminlogin')
def category_list(request):
    categories = Category.objects.all()
    category_offers = CategoryOffer.objects.all() 

    # Create a form instance for adding categories
    add_category_form = CategoryForm()

    context = {
        'category': categories,
        'category_offers': category_offers, 
        'form': add_category_form, # Pass the form for adding
    }
    return render(request, 'dashboard/category_list.html', context)


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('category_list')
        else:
            messages.error(request, form.errors) 
    else:
        form = CategoryForm()

    context = {
        'form': form,
        'category': Category.objects.all()
    }
    return render(request, 'dashboard/category_list.html', context)

def category_edit(request, category_id):
    category = Category.objects.get(id=category_id)
    category_offers = CategoryOffer.objects.all()

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
        else:
            messages.error(request, form.errors)
    else:
        form = CategoryForm(instance=category) 

    context = {
        'form': form, 
        'category': category,
        'category_offers': category_offers,
    }
    return render(request, 'dashboard/category_list.html', context)


#================================================================


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='adminlogin')
def sub_category_list(request):
    sub = Sub_Category.objects.all()
    cat = Category.objects.all()
    context = {

        'sub_category' : sub,
        'category' : cat,

    }
    return render(request, 'dashboard/sub_category_list.html',context)


def add_sub_category(request):
    if request.method == "POST":
        sub_category_name = request.POST['sub_category_name']
        category_name = request.POST['category']

        
        if Sub_Category.objects.filter(sub_category_name=sub_category_name).exists():
            messages.error(request, 'Sub Category name already exist')
            return redirect('sub_category_list')
        

        if sub_category_name == '':
            messages.error(request,"name field are empty")
            return redirect('sub_category_list')
        
        
        
        if not re.search('[a-zA-Z]', sub_category_name):
            messages.error(request, 'sub category name should contain at least one alphabet')
            return redirect('sub_category_list')
        

        category = Category.objects.get(category_name=category_name)
        
        new = Sub_Category.objects.create(
                sub_category_name=sub_category_name,
        
                category=category
        )

        new.save()

        return redirect('sub_category_list')
    

    return render(request, 'dashboard/sub_category_list.html')


def sub_category_delete(request,sub_id):
    sub= Sub_Category.objects.get(id=sub_id)
    sub.delete()
    return redirect('sub_category_list')

def sub_category_edit(request,sub_id):
    sub_category = Sub_Category.objects.get(id=sub_id)

    if request.method == "POST":
        sub_category_name = request.POST.get('sub_category_name')
        
        
        category_name = request.POST.get('category')
        
        if Sub_Category.objects.filter(sub_category_name=sub_category_name).exclude(id=sub_id).exists():
            messages.error(request, 'sub category name already exists')
            return redirect('sub_category_list')

        # if not (category_name):
        #     messages.error(request, "Name  field is empty")
        #     return redirect('product_list')
        

        category = Category.objects.get(category_name=category_name)
        
        sub_category.sub_category_name = sub_category_name
        sub_category.category = category
        
        
        sub_category.save()

        return redirect('sub_category_list')

    
    return render(request, 'dashboard/sub_category_list.html')


# def order_management(request):
#     order_items = OrderItem.objects.all()
#     order = Order.objects.all()


#     context = {
#         'orders' : order,
#     }

#     return render(request, 'dashboard/admin_order_list.html',context)
#

# show recent orders on top

def order_management(request):
    # Get all orders, sorted by created_at in descending order
    order = Order.objects.order_by('-created_at')

    context = {
        'orders' : order,
    }

    return render(request, 'dashboard/admin_order_list.html',context)

def admin_single_order(request,id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return redirect('order_management')
    address_id=order.address.id
    address = Address.objects.get(id=address_id)
    print(address,"aami")
    order_items = OrderItem.objects.filter(order_id=id)
    print(order_items,"aami")

    context ={
        'order_item' : order_items,
        'address'    : address,
        'order'   : order,
    }

    return render (request, 'dashboard/single_order_admin.html', context)


def update_order(request, id):
  if request.method == "POST":
    order_item = get_object_or_404(OrderItem, id=id)
    status = request.POST.get('status')
    order_item.status = status 
    order_item.save()
    
    # return redirect('admin_single_order',id)
    return redirect('admin_single_order',id=order_item.order.id)


    

def coupon_management(request):
    coupon = Coupon.objects.all()

    context = {
        'coupon' : coupon
    }
    return render(request, 'dashboard/admin_coupon.html',context)


def add_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        min_value = request.POST.get('min_value')
        valid_till = request.POST.get('valid_till')
        is_available = request.POST.get('is_available')

        if is_available == None:
            is_available = False

        if int(discount) >30 or int(discount) <= 0 :
            messages.error(request,"discount percentage should be below 30 percentage and more than zero")
            return redirect('coupon_management')


        Coupon.objects.create(
            code=coupon_code,
            discount=discount,
            min_value=min_value,
            valid_till=valid_till,
            active = is_available,
        )

        return redirect('coupon_management')
    

def edit_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        min_value = request.POST.get('min_value')
        valid_till = request.POST.get('valid_till')
        is_available = request.POST.get('is_available')


        if is_available == None:
            is_available = False
        
        if valid_till =="":
            valid_till = coupon.valid_till

        if int(discount) >30 or int(discount) <= 0 :
            messages.error(request,"discount percentage should be below 30 percentage and more than zero")
            return redirect('offer_managment')
        
        coupon.code = coupon_code
        coupon.discount = discount
        coupon.min_value = min_value
        coupon.valid_till = valid_till
        coupon.active = is_available
        coupon.save()
        return redirect('coupon_management')
    
def delete_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.delete()
    return redirect('coupon_management')
    

# ========================================================================
# VARIANTS    

#EXISTING WORKING CODES
# def variants(request):
#     variant = Variation.objects.all()
#     product = Product.objects.all()
    # variation_category_choice = (
    # ('color', 'color'),
    # ('size', 'size'),)   
    
#     context = {
#         'variants' : variant,
#         'products' : product,
#         'choices' : variation_category_choice,

#     }
#     return render(request, 'dashboard/variation.html', context)

# def add_variants(request):
#     if request.method == "POST":
#         product_name = request.POST.get('product')
#         variation_category = request.POST.get('variation_category')
#         variation_value = request.POST.get('variation_value')
#         is_available = request.POST.get('is_available')
#         print(variation_value,"daxo")
#         product = Product.objects.get(product_name=product_name)
#         if is_available == None:
#             is_available = False

#         Variation.objects.create(product=product, variation_category=variation_category,variation_value=variation_value,is_active=is_available)

#         return redirect('variants')
    
# def delete_variants(request, id):
#     variants = Variation.objects.get(id=id)
#     variants.delete()
#     return redirect('variants')


from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
# ... other imports ...

def variants(request):
    variants = Variation.objects.all()
    products = Product.objects.all()
    # variation_category_choice = (
    # ('color', 'color'),
    # ('size', 'size'),)     
    context = {
        'variants': variants,
        'products': products,
        'choices': variation_category_choice, 
    }
    return render(request, 'dashboard/variation.html', context)

def add_variants(request):
    if request.method == "POST":
        product_id = request.POST.get('product') 
        variation_category = request.POST.get('variation_category')
        variation_value = request.POST.get('variation_value')
        is_active = request.POST.get('is_available')
        price = request.POST.get('price')  # Get price from form
        stock = request.POST.get('stock')  # Get stock from form

        product = Product.objects.get(id=product_id)  # Fetch product by ID

        if is_active == None:
            is_active = False

        Variation.objects.create(
            product=product,
            variation_category=variation_category,
            variation_value=variation_value,
            is_active=is_active,
            price=price,
            stock=stock
        )
        return redirect('variants')  

def delete_variants(request, id):
    variants = Variation.objects.get(id=id)
    variants.delete()
    return redirect('variants')

# Add a view to edit variants:
def edit_variants(request, id):
    variant = get_object_or_404(Variation, id=id)
    products = Product.objects.all()
    if request.method == 'POST':
        # Update the variant fields with the form data
        variant.product = Product.objects.get(id=request.POST.get('product'))
        variant.variation_category = request.POST.get('variation_category')
        variant.variation_value = request.POST.get('variation_value')
        variant.is_active = bool(request.POST.get('is_available'))
        variant.price = request.POST.get('price')
        variant.stock = request.POST.get('stock')
        variant.save()
        return redirect('variants')
    context = {
        'variant': variant,
        'products': products,
        'choices': variation_category_choice
    }
    return render(request, 'dashboard/edit_variation.html', context) 

#=====================================================================


def price_range(request):
    choices = PriceFilter.FILTER_CHOICES
    price_range=PriceFilter.objects.all()
    

    context ={
        'price_range' : price_range,
        'choices' : choices,
    }

    return render(request,'dashboard/price_range.html',context)

def add_price_range(request):
    if request.method == 'POST':
        price_range = request.POST.get('price_range')

        if PriceFilter.objects.filter(price_range=price_range).exists():
            messages.error(request, 'price range already exists')
            return redirect('price_range')
        
        PriceFilter.objects.create(price_range=price_range)
    return redirect('price_range')


def delete_price_range(request,id):
    price_range = PriceFilter.objects.get(id=id)
    price_range.delete()
    return redirect('price_range')

def edit_price_range(request,id):
    price_rangee = PriceFilter.objects.get(id=id)
    if request.method == "POST":
        price_ranges = request.POST.get('price_range')

        if PriceFilter.objects.filter(price_range=price_ranges).exclude(id=id).exists():
            messages.error(request,"price range already exist")
            return redirect(price_range)
        
        price_rangee.price_range = price_ranges
        price_rangee.save()
        return redirect('price_range')
    

#==================OFFER MANAGEMENT=========================
# PRODUCT OFFER
def offer_managment(request):
    offer = ProductOffer.objects.all()
    context ={
        'offer' : offer
    }
    return render(request, 'dashboard/offer_managment.html',context)
  
def add_offer(request):
    if request.method == "POST":
        offer_name = request.POST.get('offer_name')
        offer_description = request.POST.get('offer_description')
        discount = request.POST.get('offer_discount')
        valid_till = request.POST.get('valid_till')

        if ProductOffer.objects.filter(offer_name=offer_name).exists():
            messages.error(request,"offer Already exist")
            return redirect('offer_managment')

        if int(discount) >30 or int(discount) <= 0 :
            messages.error(request,"discount percentage should be below 30 percentage and more than zero")
            return redirect('offer_managment')
        
        if valid_till == "":
            messages.error(request,'date field is empty')
            return redirect('offer_managment')
        
        try:
            check_number = int(discount)
        except:
            messages.info(request,'discount field got unexpected values')
            return redirect('offer_managment')

        ProductOffer.objects.create(offer_name=offer_name,offer_description=offer_description,offer_discount = discount,valid_till=valid_till)

        return redirect('offer_managment')
    
def editoffer(request,offer_id):
    offers = ProductOffer.objects.get(id=offer_id)
    if request.method == "POST":
        offer_names = request.POST.get('offer_name')
        offer_descriptions = request.POST.get('offer_description')
        offer_discounts = request.POST.get('offer_discount')
       
        valid_till = request.POST.get('valid_till')

        if valid_till == "":
            valid_till=offers.valid_till

        if int(offer_discounts) >30 or int(offer_discounts) <= 0 :
            messages.error(request,"discount percentage should be below 30 percentage and more than zero")
            return redirect('offer_managment')
        

        offers.offer_name = offer_names
        offers.offer_discount =   offer_discounts
        offers.offer_description = offer_descriptions
        offers.valid_till = valid_till
        offers.save()
        return redirect('offer_managment')

def delete_offer(request,id):
    offer = ProductOffer.objects.get(id=id)
    offer.delete()
    return redirect('offer_managment')


#CATEGORY OFFER
# dashboard/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import ProductOffer
from category.models import CategoryOffer # Import your CategoryOffer model
# ... other imports

# ... Your existing views for ProductOffer ...

def category_offer_management(request):
    category_offers = CategoryOffer.objects.all()
    context = {
        'category_offers': category_offers
    }
    return render(request, 'dashboard/category_offer_management.html', context)

def add_category_offer(request):
    if request.method == 'POST':
        offer_name = request.POST.get('offer_name')
        offer_description = request.POST.get('offer_description')
        discount = request.POST.get('offer_discount')
        valid_till = request.POST.get('valid_till')

        if CategoryOffer.objects.filter(offer_name=offer_name).exists():
            messages.error(request, "Category Offer already exists.")
            return redirect('category_offer_management')

        try:
            discount = int(discount)
            if discount <= 0 or discount > 30:
                raise ValueError
        except ValueError:
            messages.error(request, "Discount percentage should be between 1 and 30.")
            return redirect('category_offer_management')

        if not valid_till:
            messages.error(request, "Expiry Date is required.")
            return redirect('category_offer_management')

        CategoryOffer.objects.create(
            offer_name=offer_name,
            offer_description=offer_description,
            offer_discount=discount,
            valid_till=valid_till
        )
        messages.success(request, "Category Offer added successfully.")
        return redirect('category_offer_management')
    else:
        return redirect('category_offer_management')

def edit_category_offer(request, category_offer_id):
    category_offer = CategoryOffer.objects.get(id=category_offer_id)

    if request.method == 'POST':
        offer_name = request.POST.get('offer_name')
        offer_description = request.POST.get('offer_description')
        discount = request.POST.get('offer_discount')
        valid_till = request.POST.get('valid_till')

        try:
            discount = int(discount)
            if discount <= 0 or discount > 30:
                raise ValueError
        except ValueError:
            messages.error(request, "Discount percentage should be between 1 and 30.")
            return redirect('category_offer_management')

        if not valid_till:
            messages.error(request, "Expiry Date is required.")
            return redirect('category_offer_management')

        category_offer.offer_name = offer_name
        category_offer.offer_description = offer_description
        category_offer.offer_discount = discount
        category_offer.valid_till = valid_till
        category_offer.save()
        messages.success(request, "Category Offer updated successfully.")
        return redirect('category_offer_management')
    else:
        context = {
            'category_offer': category_offer
        }
        return render(request, 'dashboard/category_offer_management.html', context)

def delete_category_offer(request, category_offer_id):
    category_offer = CategoryOffer.objects.get(id=category_offer_id)
    category_offer.delete()
    messages.success(request, "Category Offer deleted successfully.")
    return redirect('category_offer_management')




#==================================================================


# def export_pdf(request):
#     # Retrieve the orders
#     expenses = Order.objects.all()

#     # Prepare the data for the template
#     context = {
#         'expenses': expenses,
#     }

#     # Render the template to HTML
#     rendered_html = render_to_string('pdf_template.html', context)

#     # Create a PDF response
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=Expenses.pdf'

#     # Generate the PDF from the HTML content
#     pisa.CreatePDF(rendered_html, dest=response)

#     return response




def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
                                      str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['user', 'total_price', 'payment_mode', 'tracking_no'])

    expenses = Order.objects.all()
    for expense in expenses:
        writer.writerow([expense.user, expense.total_price, expense.payment_mode, expense.tracking_no])

    return response


def export_pdf(request):
    # Retrieve the orders
    expenses = Order.objects.all()

    # Prepare the data for the template
    context = {
        'expenses': expenses,
    }

    # Render the template to HTML
    rendered_html = render_to_string('pdf_template.html', context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Expenses.pdf'

    # Generate the PDF from the HTML content
    pisa.CreatePDF(rendered_html, dest=response)

    return response

















import calendar
import csv
from io import BytesIO  # For PDF generation

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Count, Q, F
from django.db.models.functions import TruncMonth, ExtractMonth
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# ... other imports ...
from .utils import render_to_pdf  # Add this import

from weasyprint import HTML

@login_required(login_url='adminlogin')
def dashboard(request):
    # ... (existing code for total_users, revenue, etc.)
    if not request.user.is_superuser:
        return redirect('adminlogin')

    delivered_items = OrderItem.objects.filter(status='Delivered')

    revenue = 0
    for item in delivered_items:
        revenue += item.order.total_price

    top_selling = OrderItem.objects.annotate(total_quantity= Sum('quantity')).order_by('-total_quantity').distinct()[:5]

    recent_sale = OrderItem.objects.all().order_by('-id')[:5]

    # today = datetime.today()
    today = timezone.now() # Use timezone.now() here
    date_range = 7

    four_days_ago = today - timedelta(days=date_range)

    # orders = Order.objects.filter(created_at_gte=four_days_ago, created_at_lte=today)
    orders = Order.objects.filter(created_at__gte=four_days_ago, created_at__lte=today)
    # sales_by_day = orders.annotate(day=TruncDay('created_at')).values('day').annotate(total_sales=Sum('total_price')).order_by('day')
    sales_by_day = orders.annotate(
        day=TruncDay('created_at', tz=timezone.get_current_timezone()) # Set timezone here
    ).values('day').annotate(total_sales=Sum('total_price')).order_by('day')
    print(sales_by_day,"daxii")
    sales_dates = Order.objects.annotate(sale_date=Cast('created_at', output_field=DateField())).values('sale_date').distinct()

    # context = {
    #     'total_users':CustomUser.objects.count(),
    #     'sales':OrderItem.objects.count(),
    #     'revenue':revenue,
    #     'top_selling':top_selling,
    #     'recent_sales':recent_sale,
    #     'sales_by_day':sales_by_day,
    # }
    # --- Chart Data (Monthly Sales) ---
    current_year = timezone.now().year
    monthly_sales = Order.objects.filter(created_at__year=current_year) \
                                  .annotate(month=ExtractMonth('created_at')) \
                                  .values('month') \
                                  .annotate(total_sales=Sum('total_price')) \
                                  .order_by('month')

    sales_data = [0] * 12  # Initialize with zeros for all months
    for entry in monthly_sales:
        sales_data[entry['month'] - 1] = entry['total_sales']

    month_labels = [calendar.month_name[i] for i in range(1, 13)]

    # --- Best Selling Products ---
    best_selling_products = OrderItem.objects.values('product__product_name') \
                                             .annotate(total_sold=Sum('quantity')) \
                                             .order_by('-total_sold')[:10]

    # --- Best Selling Categories ---
    best_selling_categories = OrderItem.objects.values('product__category__category_name') \
                                                .annotate(total_sold=Sum('quantity')) \
                                                .order_by('-total_sold')[:10]

    context = {
        'total_users':CustomUser.objects.count(),
        'sales':OrderItem.objects.count(),
        'revenue':revenue,
        'top_selling':top_selling,
        'recent_sales':recent_sale,
        'sales_by_day':sales_by_day,
        # ... (Your existing context variables)
        'sales_data': sales_data,
        'month_labels': month_labels,
        'best_selling_products': best_selling_products,
        'best_selling_categories': best_selling_categories,
    }
    return render(request, 'dashboard/admin_home.html', context)


####### VIP
#last working block of code - for sales_report

# @login_required(login_url='adminlogin')
# def sales_report(request):
#     # --- Filtering Logic ---
#     orders = Order.objects.all()

#     if request.method == 'GET':
#         filter_type = request.GET.get('filter_type')
#         if filter_type == 'day':
#             date = request.GET.get('date')
#             if date:
#                 orders = orders.filter(created_at__date=date)
#         elif filter_type == 'week':
#             # Add logic for week filtering (you'll need to define how you want to handle weeks)
#             week = request.GET.get('week')
#             year = request.GET.get('year')
#             if week and year:
#                 orders = orders.annotate(
#                     week_num=ExtractWeek('created_at'),
#                     year_num=ExtractYear('created_at'), ).filter(Q(week_num=week) & Q(year_num=year)
#                 )
#         elif filter_type == 'month':
#             month = request.GET.get('month')
#             year = request.GET.get('year')
#             if month and year:
#                 orders = orders.filter(created_at__month=month, created_at__year=year) 

#     # --- Aggregate Data ---
#     overall_sales_count = orders.count()
#     overall_order_amount = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0.0 
#     overall_discount = orders.aggregate(Sum('coupon_discount'))['coupon_discount__sum'] or 0.0

#     context = {
#         'orders': orders,
#         'overall_sales_count': overall_sales_count,
#         'overall_order_amount': overall_order_amount,
#         'overall_discount': overall_discount,
#     }
#     return render(request, 'dashboard/sales_report.html', context)








####VIP
#last working block of code - for download_sales_report with pdf all filtter applied

# @login_required(login_url='adminlogin')
# def download_sales_report(request, report_format):
#     # --- Prepare Data --- (Use the same filtering logic from sales_report view)
#     # ... (Your code to filter orders based on request parameters)
#     orders = Order.objects.all()

#     # Calculate the aggregates *before* you pass the context
#     overall_sales_count = orders.count()
#     overall_order_amount = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0.0 
#     overall_discount = orders.aggregate(Sum('coupon_discount'))['coupon_discount__sum'] or 0.0

#     context = {
#         'orders': orders,
#         'overall_sales_count': overall_sales_count,
#         'overall_order_amount': overall_order_amount,
#         'overall_discount': overall_discount,
#     }

#     if report_format == 'pdf':
#         # Generate PDF
#         pdf = render_to_pdf('dashboard/sales_report_pdf.html', context)
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
#         return response 
#     elif report_format == 'excel':
#         # Generate CSV (Excel)
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

#         writer = csv.writer(response)
#         writer.writerow(['Order ID', 'Username', 'Total Amount', 'Discount', 'Paid Amount', 'Date'])
#         for order in orders:
#             writer.writerow([order.id, order.user.username, order.total_price, 
#                              order.coupon_discount, (order.total_price - order.coupon_discount), 
#                              order.created_at.strftime('%Y-%m-%d %H:%M:%S')])

#         return response
#     else:
#         return HttpResponse("Invalid report format")






from django.db.models import Sum
from django.db.models.functions import ExtractYear # Import ExtractYear

# ... other imports ...

# def _filter_orders(request):
#     orders = Order.objects.all()

#     if request.method == 'GET':
#         filter_type = request.GET.get('filter_type')
#         if filter_type == 'day':
#             date = request.GET.get('date')
#             if date:
#                 orders = orders.filter(created_at__date=date)
#         # elif filter_type == 'week':
#         #     # (Add your week filtering logic here)
#         #     # Get the current week's start and end dates
#         #     today = datetime.today()
#         #     start_of_week = today - timedelta(days=today.weekday())  
#         #     end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59) 
#         #     orders = orders.filter(created_at__range=[start_of_week, end_of_week])

#         elif filter_type == 'week':
#             week = request.GET.get('week')
#             year = request.GET.get('year')

#             if week and year:
#                 try:
#                     week = int(week)
#                     year = int(year)
#                 except ValueError:
#                     # Handle invalid input (non-integer week/year)
#                     return orders  # Or display an error message

#                 # Calculate the start date of the chosen week
#                 start_of_week = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w")

#                 # Calculate the end date of the chosen week 
#                 end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)

#                 orders = orders.filter(created_at__range=[start_of_week, end_of_week])
#         elif filter_type == 'month':
#             month = request.GET.get('month')
#             year = request.GET.get('year')
#             if month and year:
#                 orders = orders.filter(created_at__month=month, created_at__year=year)
#     return orders

def _filter_orders(request):
    orders = Order.objects.all()

    if request.method == 'GET':
        filter_type = request.GET.get('filter_type')
        if filter_type == 'day':
            date = request.GET.get('date')
            if date:
                orders = orders.filter(created_at__date=date)
        elif filter_type == 'week':
            week = request.GET.get('week')
            year = request.GET.get('year')

            if week and year:
                # try:
                #     week = int(week)
                #     year = int(year)
                # except ValueError:
                #     return orders 

                start_of_week = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w")
                end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)

                orders = orders.filter(created_at__range=[start_of_week, end_of_week])
        elif filter_type == 'month':
            month = request.GET.get('month')
            year = request.GET.get('year')
            print(month, year, 'month year') # Add this line to debug
            if month and year:
                try:
                    month = int(month)  # Convert month to integer
                    year = int(year)
                except ValueError:
                    return orders  # Or handle invalid input

                # Convert UTC datetimes to your local time before filtering
                orders = orders.filter(
                    created_at__month=month, 
                    created_at__year=year
                ).annotate(
                    local_created_at=timezone.localtime(timezone.now()) 
                )
                # Now use both month and year for filtering
                orders = orders.filter(created_at__month=month, created_at__year=year)
                print(orders.query)  # Add this line to print the SQL quer
    return orders

@login_required(login_url='adminlogin')
def sales_report(request):
    orders = _filter_orders(request)  # Use helper function

    # ... Aggregate Data Calculation (as in previous response) ...
    overall_sales_count = orders.count()
    overall_order_amount = round(orders.aggregate(Sum('total_price'))['total_price__sum'] or 0.0)
    overall_discount = round(orders.aggregate(Sum('coupon_discount'))['coupon_discount__sum'] or 0.0 )

    years = Order.objects.annotate(year=ExtractYear('created_at')).values_list('year', flat=True).distinct().order_by('year')
    print(orders[0].created_at)
    context = {
        'orders': orders,
        # other context variables
        'overall_sales_count': overall_sales_count,
        'overall_order_amount': overall_order_amount,
        'overall_discount': overall_discount,
        'years': years,  # Add 'years' to your context

    }
    return render(request, 'dashboard/sales_report.html', context)

@login_required(login_url='adminlogin')
def download_sales_report(request, report_format):
        # Access filter parameters from GET request
    filter_type = request.GET.get('filter_type')
    date = request.GET.get('date')
    week = request.GET.get('week')
    year = request.GET.get('year') 
    month = request.GET.get('month') 
    orders = _filter_orders(request) # Use the same helper function here

    # ... Aggregate Data Calculation (as in previous response) ...
    overall_sales_count = orders.count()
    overall_order_amount = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0.0
    overall_discount = orders.aggregate(Sum('coupon_discount'))['coupon_discount__sum'] or 0.0

    context = {
        'orders': orders,
        # ... other context variables
        'overall_sales_count': overall_sales_count,
        'overall_order_amount': overall_order_amount,
        'overall_discount': overall_discount,

    }
    # ... rest of your download_sales_report function (from previous response)
    if report_format == 'pdf':
#         # Generate PDF
        pdf = render_to_pdf('dashboard/sales_report_pdf.html', context)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
        


                   
        return response 
    elif report_format == 'excel':
        # Generate CSV (Excel)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Order ID', 'Username', 'Total Amount', 'Discount', 'Paid Amount', 'Date'])

        for order in orders:
            writer.writerow([order.id, order.user.username, order.total_price, 
                             order.coupon_discount, (order.total_price - order.coupon_discount), 
                             order.created_at.strftime('%Y-%m-%d %H:%M:%S')]) 


        return response
    else:
        return HttpResponse("Invalid report format")
