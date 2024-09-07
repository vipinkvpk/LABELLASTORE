from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Variation
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Cart, CartItem
from store.models import Product, Variation
from django.contrib.auth.decorators import login_required
from wishlist.models import Wishlist

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart(request ,total=0, quantity=0, cart_item=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            print(cart_items,"da")
        else:        
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

            
        for cart_item in cart_items:
            if cart_item.product.offer:
                total += (cart_item.product.get_offer_price() * cart_item.quantity)
            else:
                total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total 
    }
    # for cart_item in cart_items:
    #     cart_item.stock_limit = cart_item.product.stock  # Assuming 'stock' is the field in your Product model

    return render(request,'store/cart.html', context)



def remove_cart_item(request, product_id, cart_item_id):
    # cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')






#EXISTING WORKING FUNCTION
# def add_cart(request, product_id):
#     current_user = request.user
#     product = Product.objects.get(id=product_id)
    
#     if current_user.is_authenticated:
#         product_variation = []
        
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]
                
#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except Variation.DoesNotExist:
#                     pass
        
        

#         is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product, user=current_user)
#             ex_var_list = []
#             id_list = []

#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id_list.append(item.id)

#             match_found = False
#             for ex_vars in ex_var_list:
#                 if set(ex_vars) == set(product_variation):
#                     match_found = True
#                     break

#             if match_found:
#                 index = ex_var_list.index(ex_vars)
#                 item_id = id_list[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()


                
#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, user=current_user)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#         else:
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 user=current_user,
#             )
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()

        
            
#         return redirect('cart')


#     else:
#         product_variation = []
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]
                
#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except Variation.DoesNotExist:
#                     pass
        
#         try:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create(
#                 cart_id=_cart_id(request)
#             )
#             cart.save()
            

#         is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product, cart=cart)
#             ex_var_list = []
#             id_list = []

#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id_list.append(item.id)

#             match_found = False
#             for ex_vars in ex_var_list:
#                 if set(ex_vars) == set(product_variation):
#                     match_found = True
#                     break

#             if match_found:
#                 index = ex_var_list.index(ex_vars)
#                 item_id = id_list[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()
#                 # return HttpResponse('true')
#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#                 # return HttpResponse('false')
#         else:
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 cart=cart,
#             )
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()

        
            
#         return redirect('cart')

# def add_cart(request, product_id):
#     from_wishlist = request.GET.get('from_wishlist', False)  # Check for wishlist context
#     current_user = request.user
#     product = Product.objects.get(id=product_id)
    
#     if current_user.is_authenticated:
#         product_variation = []
        
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]
                
#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except Variation.DoesNotExist:
#                     pass
        
        

#         is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

#         if from_wishlist:
#             if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product, user=current_user)
#             ex_var_list = []
#             id_list = []

#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id_list.append(item.id)

#             match_found = False
#             for ex_vars in ex_var_list:
#                 if set(ex_vars) == set(product_variation):
#                     match_found = True
#                     break

#             if match_found:
#                 index = ex_var_list.index(ex_vars)
#                 item_id = id_list[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()


                
#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, user=current_user)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#         else:
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 user=current_user,
#             )
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()

        
            
#         return redirect('cart')


#     else:
#         product_variation = []
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]
                
#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except Variation.DoesNotExist:
#                     pass
        
#         try:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create(
#                 cart_id=_cart_id(request)
#             )
#             cart.save()
            

#         is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product, cart=cart)
#             ex_var_list = []
#             id_list = []

#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id_list.append(item.id)

#             match_found = False
#             for ex_vars in ex_var_list:
#                 if set(ex_vars) == set(product_variation):
#                     match_found = True
#                     break

#             if match_found:
#                 index = ex_var_list.index(ex_vars)
#                 item_id = id_list[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()
#                 # return HttpResponse('true')
#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#                 # return HttpResponse('false')
#         else:
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 cart=cart,
#             )
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()

        
            
#         return redirect('cart')


# add_cart functionality checking avoidingg duplicates in the cart
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Variation
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Product, Variation, Cart, CartItem
from django.contrib.auth.decorators import login_required
from wishlist.models import Wishlist




def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    from_wishlist = request.GET.get('from_wishlist', False)  # Check for wishlist context

    if current_user.is_authenticated:
        product_variation = []

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                variation_value__iexact=value)
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

        if from_wishlist:
            # Handle ALL wishlist scenarios here
            if is_cart_item_exists:
                # Check for matching variations and increment if found
                cart_item = CartItem.objects.filter(product=product, user=current_user)
                ex_var_list = []
                id_list = []

                for item in cart_item:
                    existing_variation = item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id_list.append(item.id)

                match_found = False
                for ex_vars in ex_var_list:
                    if set(ex_vars) == set(product_variation):
                        match_found = True
                        index = ex_var_list.index(ex_vars)
                        item_id = id_list[index]
                        item = CartItem.objects.get(product=product, id=item_id)
                        # Check Stock before incrementing
                        if item.quantity < item.product.stock: 
                            item.quantity += 1
                            item.save()
                        else:
                            # Handle out of stock scenario (e.g., message to user)
                            pass
                        break 

            else: 
                # No existing item, but check for matching variations BEFORE creating
                match_found = False
                cart_items = CartItem.objects.filter(product=product, user=current_user)
                for item in cart_items:
                    existing_variation = item.variations.all()
                    if set(existing_variation) == set(product_variation):
                        match_found = True
                        # Increment quantity if a match is found
                        if item.quantity < item.product.stock:
                            item.quantity += 1
                            item.save()
                        else:
                            # Handle out of stock
                            pass
                        break 

                if not match_found:
                    # Only create a new item if no matching variations exist
                    cart_item = CartItem.objects.create(
                        product=product,
                        quantity=1,
                        user=current_user,
                    )
                    if len(product_variation) > 0:
                        cart_item.variations.clear()
                        cart_item.variations.add(*product_variation)
                    cart_item.save()

        else:  # Not from wishlist 
            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(product=product, user=current_user)
                ex_var_list = []
                id_list = []

                for item in cart_item:
                    existing_variation = item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id_list.append(item.id)

                match_found = False
                for ex_vars in ex_var_list:
                    if set(ex_vars) == set(product_variation):
                        match_found = True
                        break

                if match_found:
                    index = ex_var_list.index(ex_vars)
                    item_id = id_list[index]
                    item = CartItem.objects.get(product=product, id=item_id)
                    item.quantity += 1
                    item.save()


                    
                else:
                    item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                    if len(product_variation) > 0:
                        item.variations.clear()
                        item.variations.add(*product_variation)
                    item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    quantity=1,
                    user=current_user,
                )
                if len(product_variation) > 0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
                cart_item.save()

        return redirect('cart')


    else: #user is not authenticated
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    pass
        
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
            cart.save()
            

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            ex_var_list = []
            id_list = []

            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id_list.append(item.id)

            match_found = False
            for ex_vars in ex_var_list:
                if set(ex_vars) == set(product_variation):
                    match_found = True
                    break

            if match_found:
                index = ex_var_list.index(ex_vars)
                item_id = id_list[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
                # return HttpResponse('true')
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
                # return HttpResponse('false')
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        
            
        return redirect('cart')





# def remove_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product = get_object_or_404(Product, id=product_id)
#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()

#             carts = CartItem.objects.filter(user=request.user).order_by('id')
#             total_price = 0
            
#             for item in carts:
#                 if item.product.offer:
#                     total_price=total_price + item.product.get_offer_price() * item.quantity
#                 else:
#                     total_price=total_price + item.product.price * item.quantity
#             if product.offer:
#                 single_pro_total = product.get_offer_price() * item.quantity
#             else:
#                 single_pro_total = product.price*cart_item.quantity

#             return JsonResponse({'status' : 'updated succesfully','sub_total': total_price,'single_pro_total': single_pro_total})
#         else:
#             cart_item.delete()
#     except:
#         return JsonResponse({'status' : 'Failed'})

# from django.http import HttpResponse, JsonResponse
# ... other imports

# ... (your other view functions) ...

# def remove_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product = get_object_or_404(Product, id=product_id)
#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
#         if cart_item.quantity >= 1:
#             cart_item.quantity -= 1
#             cart_item.save()

#             carts = CartItem.objects.filter(user=request.user).order_by('id')
#             total_price = 0
            
#             for item in carts:
#                 if item.product.offer:
#                     total_price=total_price + item.product.get_offer_price() * item.quantity
#                 else:
#                     total_price=total_price + item.product.price * item.quantity
#             if product.offer:
#                 single_pro_total = product.get_offer_price() * item.quantity
#             else:
#                 single_pro_total = product.price*cart_item.quantity

#             return JsonResponse({'status' : 'updated succesfully',
#                                  'sub_total': total_price,
#                                  'single_pro_total': single_pro_total,
#                                  'new_quantity': cart_item.quantity }) # <-- Added new_quantity
#         else:
#             cart_item.delete()
#             return JsonResponse({'status' : 'deleted successfully'}) 
#     except:
#         return JsonResponse({'status' : 'Failed'})

# from django.http import HttpResponse, JsonResponse
# # ... other imports

# # ... (your other view functions) ...

# def remove_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product = get_object_or_404(Product, id=product_id)

#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

#         if cart_item.quantity >= 1:
#             cart_item.quantity -= 1
#             cart_item.save()

#         # Check if quantity is 0 after decrementing 
#         if cart_item.quantity == 0:
#             cart_item.delete()

#         # Recalculate totals (always)
#         carts = CartItem.objects.filter(user=request.user).order_by('id')
#         total_price = 0
#         for item in carts:
#             if item.product.offer:
#                 total_price += item.product.get_offer_price() * item.quantity
#             else:
#                 total_price += item.product.price * item.quantity

#         if product.offer:
#             single_pro_total = product.get_offer_price() * cart_item.quantity
#         else:
#             single_pro_total = product.price * cart_item.quantity

#         return JsonResponse({
#             'status': 'updated successfully',
#             'sub_total': total_price,
#             'single_pro_total': single_pro_total,
#             'new_quantity': cart_item.quantity
#         })

#     except Exception as e: 
#         return JsonResponse({'status': 'Failed', 'message': str(e)})

# # ... (your other view functions) ...

# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import get_object_or_404, redirect, render
# from carts.models import Cart, CartItem
# from django.core.exceptions import ObjectDoesNotExist
# from store.models import Product, Variation
# from django.http import HttpResponse
# from django.shortcuts import redirect
# from .models import Cart, CartItem
# from store.models import Product, Variation
# from django.contrib.auth.decorators import login_required
# from wishlist.models import Wishlist


# # ... (rest of your view functions) ...

# def remove_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product = get_object_or_404(Product, id=product_id)

#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

#         if cart_item.quantity >= 1:
#             cart_item.quantity -= 1
#             cart_item.save()

#         # Check if quantity is 0 after decrementing
#         if cart_item.quantity == 0:
#             cart_item.delete()

#         # Recalculate totals (always)
#         carts = CartItem.objects.filter(user=request.user).order_by('id')
#         total_price = 0
#         for item in carts:
#             if item.product.offer:
#                 total_price += item.product.get_offer_price() * item.quantity
#             else:
#                 total_price += item.product.price * item.quantity

#         if product.offer:
#             single_pro_total = product.get_offer_price() * cart_item.quantity
#         else:
#             single_pro_total = product.price * cart_item.quantity

#         return JsonResponse({
#             'status': 'updated successfully',
#             'sub_total': total_price,
#             'single_pro_total': single_pro_total,
#             'new_quantity': cart_item.quantity
#         })

#     except Exception as e:
#         return JsonResponse({'status': 'Failed', 'message': str(e)})

# # ... (rest of your view functions) ...

# def remove_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product = get_object_or_404(Product, id=product_id)

#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

#         # Store the original quantity
#         original_quantity = cart_item.quantity

#         if cart_item.quantity >= 1:
#             cart_item.quantity -= 1
#             cart_item.save()

#         # Check if quantity is 0 after decrementing
#         if cart_item.quantity == 0:
#             cart_item.delete()

#         # Recalculate totals (always)
#         carts = CartItem.objects.filter(user=request.user).order_by('id')
#         total_price = 0
#         for item in carts:
#             if item.product.offer:
#                 total_price += item.product.get_offer_price() * item.quantity
#             else:
#                 total_price += item.product.price * item.quantity

#         # Calculate single product total using the ORIGINAL quantity
#         if product.offer:
#             single_pro_total = product.get_offer_price() * original_quantity
#         else:
#             single_pro_total = product.price * original_quantity

#         return JsonResponse({
#             'status': 'updated successfully',
#             'sub_total': total_price,
#             'single_pro_total': single_pro_total,
#             'new_quantity': cart_item.quantity
#         })

#     except Exception as e:
#         return JsonResponse({'status': 'Failed', 'message': str(e)})

# from django.shortcuts import get_object_or_404, redirect
# from django.http import JsonResponse
# from .models import Product, Cart, CartItem
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.decorators import login_required
 

# def remove_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product = get_object_or_404(Product, id=product_id)

#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

#         # Store the original quantity
#         original_quantity = cart_item.quantity

#         # Decrement quantity only if it's greater than 1
#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()

#         # Recalculate totals
#         carts = CartItem.objects.filter(user=request.user).order_by('id')
#         total_price = 0
#         for item in carts:
#             if item.product.offer:
#                 total_price += item.product.get_offer_price() * item.quantity
#             else:
#                 total_price += item.product.price * item.quantity

#         # Calculate single product total using the ORIGINAL quantity
#         if product.offer:
#             single_pro_total = product.get_offer_price() * original_quantity
#         else:
#             single_pro_total = product.price * original_quantity

#         return JsonResponse({
#             'status': 'updated successfully',
#             'sub_total': total_price,
#             'single_pro_total': single_pro_total,
#             'new_quantity': cart_item.quantity # Return the current quantity
#         })

#     except Exception as e:
#         return JsonResponse({'status': 'Failed', 'message': str(e)})


# from django.shortcuts import get_object_or_404, redirect
# from django.http import JsonResponse
# from .models import Product, Cart, CartItem
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.decorators import login_required
 

# def remove_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product = get_object_or_404(Product, id=product_id)

#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

#         # Decrement quantity only if it's greater than 1
#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()

#         # Recalculate totals
#         carts = CartItem.objects.filter(user=request.user).order_by('id')
#         total_price = 0
#         for item in carts:
#             if item.product.offer:
#                 total_price += item.product.get_offer_price() * item.quantity
#             else:
#                 total_price += item.product.price * item.quantity

#         # Calculate single product total using the UPDATED quantity
#         if product.offer:
#             single_pro_total = product.get_offer_price() * cart_item.quantity 
#         else:
#             single_pro_total = product.price * cart_item.quantity 

#         return JsonResponse({
#             'status': 'updated successfully',
#             'sub_total': total_price,
#             'single_pro_total': single_pro_total,
#             'new_quantity': cart_item.quantity
#         })

#     except Exception as e:
#         return JsonResponse({'status': 'Failed', 'message': str(e)})



# from django.shortcuts import get_object_or_404, redirect
# from django.http import JsonResponse
# from .models import Product, Cart, CartItem
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.decorators import login_required


# def remove_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product = get_object_or_404(Product, id=product_id)

#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(
#                 product=product, user=request.user, id=cart_item_id
#             )
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(
#                 product=product, cart=cart, id=cart_item_id
#             )

#         # Decrement quantity only if it's greater than 1
#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()  # Make sure this correctly saves the changes

#         # **Recalculate the Cart Total**
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(user=request.user)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart)

#         total_price = 0
#         for item in cart_items:
#             if item.product.offer:
#                 total_price += item.product.get_offer_price() * item.quantity
#             else:
#                 total_price += item.product.price * item.quantity

#         # Calculate single product total using the UPDATED quantity
#         if product.offer:
#             single_pro_total = product.get_offer_price() * cart_item.quantity
#         else:
#             single_pro_total = product.price * cart_item.quantity

#         return JsonResponse(
#             {
#                 "status": "updated successfully",
#                 "sub_total": total_price,  # Send the recalculated cart total
#                 "single_pro_total": single_pro_total,
#                 "new_quantity": cart_item.quantity,
#             }
#         )

#     except Exception as e:
#         return JsonResponse({"status": "Failed", "message": str(e)})



# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from .models import Product, Cart, CartItem

# def remove_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product = get_object_or_404(Product, id=product_id)

#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

#         # Decrement the quantity
#         if cart_item.quantity > 1:  # Decrement only if the quantity is greater than 1
#             cart_item.quantity -= 1
#             cart_item.save()
#         else:
#             cart_item.delete()  # If quantity is 1, delete the cart item

#         # Recalculate totals
#         carts = CartItem.objects.filter(user=request.user).order_by('id') if request.user.is_authenticated else CartItem.objects.filter(cart=cart).order_by('id')
#         total_price = sum((item.product.get_offer_price() if item.product.offer else item.product.price) * item.quantity for item in carts)

#         # Calculate single product total using the UPDATED quantity
#         single_pro_total = (product.get_offer_price() if product.offer else product.price) * cart_item.quantity if cart_item.quantity > 0 else 0

#         return JsonResponse({
#             'status': 'updated successfully',
#             'sub_total': total_price,
#             'single_pro_total': single_pro_total,
#             'new_quantity': cart_item.quantity if cart_item.quantity > 0 else 0
#         })

#     except Exception as e:
#         return JsonResponse({'status': 'Failed', 'message': str(e)})


# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from .models import Product, Cart, CartItem

# def remove_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product = get_object_or_404(Product, id=product_id)

#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))  # Make sure _cart_id(request) is defined
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()
#             status = 'updated successfully'
#         else:
#             status = 'minimum reached'

#         # Recalculate totals
#         carts = CartItem.objects.filter(user=request.user).order_by('id') if request.user.is_authenticated else CartItem.objects.filter(cart=cart).order_by('id')
#         total_price = sum((item.product.get_offer_price() if item.product.offer else item.product.price) * item.quantity for item in carts)

#         single_pro_total = (product.get_offer_price() if product.offer else product.price) * cart_item.quantity

#         return JsonResponse({
#             'status': status,
#             'sub_total': total_price,
#             'single_pro_total': single_pro_total,
#             'new_quantity': cart_item.quantity
#         })

#     except Exception as e:
#         return JsonResponse({'status': 'Failed', 'message': str(e)})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Cart, CartItem

def remove_cart(request):
    product_id = request.POST.get('product_id')
    cart_item_id = request.POST.get('cart_item_id')
    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # Make sure _cart_id(request) is defined
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            status = 'updated successfully'
        else:
            # Don't delete - quantity remains 1
            status = 'minimum reached'

        # Recalculate totals CORRECTLY (using existing cart_item)
        carts = CartItem.objects.filter(user=request.user).order_by('id') if request.user.is_authenticated else CartItem.objects.filter(cart=cart).order_by('id')
        total_price = sum((item.product.get_offer_price() if item.product.offer else item.product.price) * item.quantity for item in carts)

        # Use the updated cart_item for single_pro_total 
        single_pro_total = (product.get_offer_price() if product.offer else product.price) * cart_item.quantity

        return JsonResponse({
            'status': status,
            'sub_total': total_price,
            'single_pro_total': single_pro_total,
            'new_quantity': cart_item.quantity
        })

    except Exception as e:
        return JsonResponse({'status': 'Failed', 'message': str(e)})




# # EXISTING CODE
# def increment_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product_qty = int(request.POST.get('qty'))
#     product = get_object_or_404(Product, id=product_id)
#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        
#         if cart_item.product.stock<product_qty:
#             return JsonResponse({'status':"not"})
                
#         cart_item.quantity += 1
#         cart_item.save()

#         carts = CartItem.objects.filter(user=request.user).order_by('id')
#         total_price = 0
#         for item in carts:
#             if item.product.offer:
#                 total_price += item.product.get_offer_price() * item.quantity     
#             else: 
#                 total_price=total_price+ item.product.price * item.quantity

#         if product.offer:
#             single_pro_total= product.get_offer_price() * item.quantity
#         else:
#             single_pro_total = product.price*cart_item.quantity

#         return JsonResponse({'sub_total': total_price,'single_pro_total': single_pro_total })
#     except:
#         return JsonResponse({'sub_total': total_price,'single_pro_total': single_pro_total})


# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import get_object_or_404, redirect, render
# from carts.models import Cart, CartItem
# from django.core.exceptions import ObjectDoesNotExist
# from store.models import Product, Variation
# from django.http import HttpResponse
# from django.shortcuts import redirect
# from .models import Product, Variation, Cart, CartItem
# from django.contrib.auth.decorators import login_required
# from wishlist.models import Wishlist

# # ... other views ...

# def increment_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product = get_object_or_404(Product, id=product_id)
#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        
#         # Check if incrementing would exceed stock
#         if cart_item.quantity + 1 > product.stock:
#             return JsonResponse({'status': 'exceeded', 'message': 'Maximum limit reached'}) 

#         cart_item.quantity += 1
#         cart_item.save()

#         carts = CartItem.objects.filter(user=request.user).order_by('id')
#         total_price = 0
#         for item in carts:
#             if item.product.offer:
#                 total_price += item.product.get_offer_price() * item.quantity     
#             else: 
#                 total_price=total_price+ item.product.price * item.quantity

#         if product.offer:
#             single_pro_total= product.get_offer_price() * item.quantity
#         else:
#             single_pro_total = product.price*cart_item.quantity

#         return JsonResponse({'sub_total': total_price, 
#                              'single_pro_total': single_pro_total,
#                              'new_quantity': cart_item.quantity })
#     except:
#         return JsonResponse({'status': 'failed'})

# # ... other views ...

# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import get_object_or_404, redirect, render
# from carts.models import Cart, CartItem
# from django.core.exceptions import ObjectDoesNotExist
# from store.models import Product, Variation
# from django.http import HttpResponse
# from django.shortcuts import redirect
# from .models import Product, Variation, Cart, CartItem
# from django.contrib.auth.decorators import login_required
# from wishlist.models import Wishlist

# # Create your views here.


# def increment_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product_qty = int(request.POST.get('qty'))
#     product = get_object_or_404(Product, id=product_id)
#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        
#         if cart_item.product.stock<product_qty:
#             return JsonResponse({'status': 'error', 'message': 'Quantity exceeds available stock'})
                
#         cart_item.quantity += 1
#         cart_item.save()

#         carts = CartItem.objects.filter(user=request.user).order_by('id')
#         total_price = 0
#         for item in carts:
#             if item.product.offer:
#                 total_price += item.product.get_offer_price() * item.quantity     
#             else: 
#                 total_price=total_price+ item.product.price * item.quantity

#         if product.offer:
#             single_pro_total= product.get_offer_price() * item.quantity
#         else:
#             single_pro_total = product.price*cart_item.quantity

#         return JsonResponse({'sub_total': total_price,'single_pro_total': single_pro_total })
#     except Exception as e:
#         # Log the error for debugging:
#         print("Error in increment_cart:", e)
#         return JsonResponse({'status': 'error', 'message': 'An error occurred'})


# from django.http import HttpResponse, JsonResponse
# ... other imports ...

# def increment_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product = get_object_or_404(Product, id=product_id)
#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

#         # Only increment if quantity is less than stock
#         if cart_item.quantity < cart_item.product.stock:
#             cart_item.quantity += 1
#             cart_item.save()

#             # Calculate sub_total (assuming you're using 'offer' for discounted prices)
#             carts = CartItem.objects.filter(user=request.user).order_by('id')
#             total_price = 0
#             for item in carts:
#                 if item.product.offer:
#                     total_price += item.product.get_offer_price() * item.quantity
#                 else:
#                     total_price += item.product.price * item.quantity

#             # Calculate single_pro_total
#             if product.offer:
#                 single_pro_total = product.get_offer_price() * cart_item.quantity
#             else:
#                 single_pro_total = product.price * cart_item.quantity

#             return JsonResponse({
#                 'status': 'success',
#                 'sub_total': total_price,
#                 'single_pro_total': single_pro_total
#             })
#         else:
#             return JsonResponse({
#                 'status': 'out_of_stock'
#             })
#     except:
#         return JsonResponse({'status': 'failed'}) 

# from django.http import HttpResponse, JsonResponse

# # ... other imports ...

# def increment_cart(request):
#     product_id = request.POST.get('product_id')
#     cart_item_id = request.POST.get('cart_item_id')
#     product = get_object_or_404(Product, id=product_id)
    
#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

#         # Only increment if quantity is less than stock
#         if cart_item.quantity < cart_item.product.stock:
#             cart_item.quantity += 1
#             cart_item.save()
            
#             # Recalculate cart totals
#             if request.user.is_authenticated:
#                 carts = CartItem.objects.filter(user=request.user).order_by('id')
#             else:
#                 carts = CartItem.objects.filter(cart=cart, is_active=True)

#             total_price = 0
#             for item in carts:
#                 if item.product.offer:
#                     total_price += item.product.get_offer_price() * item.quantity
#                 else:
#                     total_price += item.product.price * item.quantity

#             # Calculate single_pro_total
#             if product.offer:
#                 single_pro_total = product.get_offer_price() * cart_item.quantity
#             else:
#                 single_pro_total = product.price * cart_item.quantity

#             return JsonResponse({
#                 'status': 'success',  
#                 'sub_total': total_price,
#                 'single_pro_total': single_pro_total
#             })
#         else:
#             return JsonResponse({
#                 'status': 'not',  
#                 'message': 'Sorry, no more items available in stock'  
#             })

#     except Exception as e:
#         print(f"Error in increment_cart: {e}") 
#         return JsonResponse({'status': 'failed', 'message': 'An error occurred'}) 

# carts/views.py

from django.http import HttpResponse, JsonResponse
# ... other imports

# ... other views

def increment_cart(request):
    product_id = request.POST.get('product_id')
    cart_item_id = request.POST.get('cart_item_id')
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        # Check stock BEFORE incrementing
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()

            carts = CartItem.objects.filter(user=request.user).order_by('id')
            total_price = 0
            for item in carts:
                if item.product.offer:
                    total_price += item.product.get_offer_price() * item.quantity     
                else: 
                    total_price += item.product.price * item.quantity

            if product.offer:
                single_pro_total = product.get_offer_price() * cart_item.quantity
            else:
                single_pro_total = product.price * cart_item.quantity

            return JsonResponse({
                'status': 'success',  # Indicate success
                'sub_total': total_price,
                'single_pro_total': single_pro_total,
                'new_quantity': cart_item.quantity  # Send back new quantity
            })
        else:
            # Return an error status if out of stock
            return JsonResponse({'status': 'out_of_stock'}) 
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}) 







































