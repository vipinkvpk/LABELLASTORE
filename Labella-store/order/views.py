# from datetime import datetime
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.cache import cache_control
# from django.contrib.auth.decorators import login_required
# from carts.models import Cart, CartItem
# from carts.views import _cart_id
# from accounts.models import CustomUser
# from userprofile.models import Address, UserProfile
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib import messages
# from store.models import Product
# from . models import Coupon, Order, OrderItem, ReturnOrder, UserCoupon
# from django.shortcuts import get_object_or_404, render, redirect
# from django.template.loader import render_to_string
# from xhtml2pdf import pisa
# import csv
# import random


# # Create your views here.


# @cache_control(no_cache=True,must_revalidate=True,no_store=True)    
# @login_required(login_url='user_login')
# def checkout(request,total=0, quantity=0, cart_item=None):  
#     try:
#         tax=0
#         grand_total=0
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#         else:        
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             if cart_item.product.offer:
#                 total += (cart_item.product.get_offer_price() * cart_item.quantity)
#             else:
#                 total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
            
#         tax = (2 * total)/100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass
    
#     address = Address.objects.filter(user = request.user)
#     coupons = Coupon.objects.filter(active = True)
#     print(coupons,"daxii")
#     context = {
#         'cart_items' : cart_items,
#         'quantity' : quantity,
#         'total' : total,
#         'tax' : tax,
#         'grand_total' : grand_total,
#         'address' : address,
#         'coupons': coupons,
#         'usercoupon': UserCoupon.objects.filter(user=request.user),
#     }
#     return render(request,'store/checkout.html',context)





# @login_required(login_url='user_login')
# def placeorder(request):
   
#     if request.method == 'POST':

#         # coupon_code = request.POST['coupon']
        
#         neworder = Order()
#         neworder.user = request.user
#         address_id = request.POST['address']
    
#         address = Address.objects.get(id=address_id)
#         neworder.address = address
#         payment_mode = request.POST.get('payment_method')
#         neworder.payment_mode = payment_mode

#         neworder.payment_id = request.POST.get('payment_id')

#         cart = CartItem.objects.filter(user=request.user)
#         cart_total_price = 0
#         for item in cart:
#             if item.product.offer:

#                 cart_total_price = item.product.get_offer_price() * item.quantity

#             else:
#                 cart_total_price += item.product.price * item.quantity
#             # item.product.stock-=item.quantity
#         tax = (2*cart_total_price)/100
#         neworder.total_price = cart_total_price + tax
#         trackno = random.randint(1111111, 9999999)

#         while Order.objects.filter(tracking_no=trackno).exists():
#             trackno = random.randint(1111111, 9999999)
#         neworder.tracking_no = trackno
#         neworder.save()


#         try:
#             instance = UserCoupon.objects.get(user=request.user)

#             if float(cart_total_price) >= float(instance.coupon.min_value):
#                 coupon_discount = (
#                     (float(cart_total_price) * float(instance.coupon.discount))/100)
#                 cart_total_price = float(cart_total_price) - coupon_discount
#                 cart_total_price = format(cart_total_price, '.2f')
#                 coupon_discount = format(coupon_discount, '.2f')

#             instance.delete()
#             neworder.total_price = cart_total_price
#             neworder.save()

#         except:
#             pass


#         neworderitems = CartItem.objects.filter(user=request.user)
#         for item in neworderitems:
#             OrderItem.objects.create(
#                 order=neworder,
#                 product=item.product,
#                 price=item.product.price,
#                 quantity=item.quantity,
                
#             )

#             orderproduct = Product.objects.filter(id=item.product_id).first()
#             orderproduct.stock = orderproduct.stock - item.quantity
#             orderproduct.save()

        

            
#         if (payment_mode== 'wallet_payment'):
            
#             wallet = CustomUser.objects.get(email=request.user)
#             if float(cart_total_price) >= float(wallet.wallet):
#                messages.error(request, 'Wallet does not have the required amount')
#                return redirect(checkout)
            
#             wallet.wallet -= cart_total_price
#             wallet.save()
                

#         # To clear user Cart
#         CartItem.objects.filter(user=request.user).delete()
        

#         context={
#             'order' : OrderItem.objects.filter(order=neworder)
#         }

#     return render(request, 'order/order_success.html', context)



# # @login_required(login_url='user_login')
# # def placeorder(request):
   
# #     if request.method == 'POST':

# #         # coupon_code = request.POST['coupon']
        
# #         neworder = Order()
# #         neworder.user = request.user
# #         address_id = request.POST['address']
    
# #         address = Address.objects.get(id=address_id)
# #         neworder.address = address
# #         payment_mode = request.POST.get('payment_method')
# #         neworder.payment_mode = payment_mode

# #         neworder.payment_id = request.POST.get('payment_id')

# #         cart = CartItem.objects.filter(user=request.user)
# #         cart_total_price = 0
# #         for item in cart:
# #             if item.product.offer:

# #                 cart_total_price = item.product.get_offer_price() * item.quantity

# #             else:
# #                 cart_total_price += item.product.price * item.quantity
# #             # item.product.stock-=item.quantity
# #         tax = (2*cart_total_price)/100
# #         # neworder.total_price = cart_total_price + tax
# #         total_price_with_tax = cart_total_price + tax

# #         # # Check for coupon and apply discount if applicable
# #         try:
# #             instance = UserCoupon.objects.get(user=request.user)
# #             if float(cart_total_price) >= float(instance.coupon.min_value):
# #                 coupon_discount = ((float(cart_total_price) * float(instance.coupon.discount)) / 100)
# #                 total_price_with_tax -= coupon_discount
# #                 total_price_with_tax = format(total_price_with_tax, '.2f')
# #             instance.delete()
# #         except UserCoupon.DoesNotExist:
# #             pass



# #         neworder.total_price = total_price_with_tax
# #         neworder.coupon_discount = coupon_discount  # Save the coupon discount value
# #         print(neworder.coupon_discount, "coupon discount=")

# #         trackno = random.randint(1111111, 9999999)

# #         while Order.objects.filter(tracking_no=trackno).exists():
# #             trackno = random.randint(1111111, 9999999)
# #         neworder.tracking_no = trackno
# #         neworder.save()


# #         try:
# #             instance = UserCoupon.objects.get(user=request.user)

# #             if float(cart_total_price) >= float(instance.coupon.min_value):
# #                 coupon_discount = (
# #                     (float(cart_total_price) * float(instance.coupon.discount))/100)
# #                 cart_total_price = float(cart_total_price) - coupon_discount
# #                 cart_total_price = format(cart_total_price, '.2f')
# #                 coupon_discount = format(coupon_discount, '.2f')

# #             instance.delete()
# #             neworder.total_price = cart_total_price
# #             neworder.save()

# #         except:
# #             pass


# #         neworderitems = CartItem.objects.filter(user=request.user)
# #         for item in neworderitems:
# #             OrderItem.objects.create(
# #                 order=neworder,
# #                 product=item.product,
# #                 price=item.product.price,
# #                 quantity=item.quantity,
                
# #             )

# #             orderproduct = Product.objects.filter(id=item.product_id).first()
# #             orderproduct.stock = orderproduct.stock - item.quantity
# #             orderproduct.save()

        

            
# #         if (payment_mode== 'wallet_payment'):
            
# #             wallet = CustomUser.objects.get(email=request.user)
# #             if float(cart_total_price) >= float(wallet.wallet):
# #                messages.error(request, 'Wallet does not have the required amount')
# #                return redirect(checkout)
            
# #             wallet.wallet -= cart_total_price
# #             wallet.save()
                

# #         # To clear user Cart
# #         CartItem.objects.filter(user=request.user).delete()
        

# #         context={
# #             'order' : OrderItem.objects.filter(order=neworder), 'total_price_with_tax': total_price_with_tax,
# #         }

# #     return render(request, 'order/order_success.html', context)



# #EXISTING CODE - WORKING
# def razarypaycheck(request):
#     cart = CartItem.objects.filter(user=request.user)
#     total_price = 0
    
#     for item in cart:
#         if item.product.offer:
#             total_price += item.product.get_offer_price() * item.quantity
#         else:
#             total_price = total_price + item.product.price * item.quantity
#     try:
#         instance = UserCoupon.objects.get(user=request.user)
#         total_price = instance.total_price
#     except:
#         pass
#     tax = (2*total_price)/100
#     total_price = round(total_price+tax)

#     return JsonResponse({'total_price': total_price})



# # RAZOR PAY COUPON APPLIED AMOUNT IDENTICAL
# # def razarypaycheck(request):
# #     cart = CartItem.objects.filter(user=request.user)
# #     total_price = 0
    
# #     for item in cart:
# #         if item.product.offer:
# #             total_price += item.product.get_offer_price() * item.quantity
# #         else:
# #             total_price = total_price + item.product.price * item.quantity
# #     #Modification-3-START
# #     try:
# #         instance = UserCoupon.objects.get(user=request.user)
# #         # Apply the discount to total_price here
# #         if float(total_price) >= float(instance.coupon.min_value):
# #             coupon_discount = (
# #                 (float(total_price) * float(instance.coupon.discount))/100)
# #             total_price = float(total_price) - coupon_discount
# #     except UserCoupon.DoesNotExist:
# #         pass
# #     #Modification-3-END
# #     tax = (2*total_price)/100
# #     total_price = round(total_price+tax)

# #     return JsonResponse({'total_price': total_price})



# def sample(request):
#     if request.method == 'POST':
#         neworder = Order()
#         neworder.user = request.user
#         address_id = request.POST['address']
#         address = Address.objects.get(id=address_id)
#         neworder.address = address
#         neworder.payment_mode = request.POST.get('payment_method')
#         neworder.payment_id = request.POST.get('payment_id')

#         cart = CartItem.objects.filter(user=request.user)
#         cart_total_price = 0
#         for item in cart:
#             if item.product.offer:
#                 cart_total_price += item.product.get_offer_price() * item.quantity
#             else:
#                 cart_total_price += item.product.price * item.quantity
        
#         try:
#             instance = UserCoupon.objects.get(user=request.user)

#             if float(cart_total_price) >= float(instance.coupon.min_value):
#                 coupon_discount = (
#                     (float(cart_total_price) * float(instance.coupon.discount))/100)
#                 cart_total_price = float(cart_total_price) - coupon_discount
#                 cart_total_price = format(cart_total_price, '.2f')
#                 coupon_discount = format(coupon_discount, '.2f')

#             instance.delete()
#             neworder.total_price = cart_total_price
#             neworder.save()

#         except:
#             pass

#         tax = round((2*cart_total_price)/100)
#         neworder.total_price = cart_total_price + tax
#         trackno = random.randint(1111111, 9999999)
#         while Order.objects.filter(tracking_no=trackno).exists():
#             trackno = random.randint(1111111, 9999999)
#         neworder.tracking_no = trackno
#         neworder.save()

#         neworderitems = CartItem.objects.filter(user=request.user)
#         for item in neworderitems:
#             OrderItem.objects.create(
#                 order=neworder,
#                 product=item.product,
#                 price=item.product.price,
#                 quantity=item.quantity,      
#             )
#             # To decrease the product quantity from available stock
#         orderproduct = Product.objects.filter(id=item.product.id).first()
#         orderproduct.stock = orderproduct.stock - item.quantity
#         orderproduct.save()
#         payment_mode = request.POST.get('payment_method')
#         if (payment_mode== 'Razorpay'):
#             CartItem.objects.filter(user=request.user).delete()
#             return JsonResponse({'status' : "Your order has been succesfully placed"})

#         # To clear user Cart
#         CartItem.objects.filter(user=request.user).delete()
#     return redirect('checkout')


# def orders(request):
#     user = request.user
#     orders = Order.objects.filter(user=user).order_by('-update_at')
#     orderitems = OrderItem.objects.filter(order__in=orders).order_by('-order__update_at')
#     context = {
#         'orders': orders,
#         'orderitems': orderitems,
#     }
#     return render(request, 'order/order_list.html', context)


# #EXISTING CODE
# # @login_required(login_url='user_login')
# # def ordercancel(request):
    
# #     order_id = request.POST.get('order_id')
# #     print("order_id",order_id)
# #     order_item_id= request.POST.get('orderitem_id')
# #     print("order_item_id",order_item_id)
# #     orders = Order.objects.get(id=order_id)
# #     order_items = OrderItem.objects.get(id=order_item_id)

# #     if orders.payment_mode == 'Razorpay' or 'wallet_payment':
# #         wallet = CustomUser.objects.get(email=request.user)
# #         wallet.wallet += orders.total_price
# #         wallet.save()

# #     order_items.product.stock+=order_items.quantity
# #     # order_items.quantity = 0
# #     order_items.status = 'Cancelled'
# #     order_items.save()
# #     return redirect('orders')


# # ORDERR CANCEL ITEM TO RESTOCK
# from django.http import HttpResponse, JsonResponse
# # ... other imports ...

# @login_required(login_url='user_login')
# def ordercancel(request):
#     if request.method == 'POST':
#         order_id = request.POST.get('order_id')
#         order_item_id = request.POST.get('orderitem_id')
#         orders = Order.objects.get(id=order_id)
#         order_items = OrderItem.objects.get(id=order_item_id)

#         if orders.payment_mode in ['Razorpay', 'wallet_payment']:
#             wallet = CustomUser.objects.get(email=request.user)
#             wallet.wallet += orders.total_price
#             wallet.save()

#         # Restock items
#         order_items.product.stock += order_items.quantity
#         order_items.product.save()

#         order_items.status = 'Cancelled'
#         order_items.save()
#         return JsonResponse({'status': 'Order Cancelled Successfully'}) 
#     else:
#         return JsonResponse({'status': 'Invalid request'}) 
#     # return redirect('orders')

    
# def order_return(request,id):
#     order_item = OrderItem.objects.get(id=id)
#     wallet = 0
#     if request.method == "POST":
#         return_reason = request.POST.get('return_reason')
#         return_comment = request.POST.get('return_comment')
#         ReturnOrder.objects.create(order_item=order_item,return_reason= return_reason, return_comment=return_comment)
#         order_item.status = "Returned"
#         order_item.product.stock+= order_item.quantity
#         order_item.save()

#         wallet=CustomUser.objects.get(email=request.user)
#         wallet.wallet += order_item.order.total_price
#         wallet.save()
#         print(wallet.wallet,"daxo")

#     return redirect('orders')

    



# def coupons(request):
#     if request.method == 'POST':
#         coupon_code = request.POST['coupon']
        
        
#         grand_total = request.POST['grand_total']
#         if UserCoupon.objects.filter(user=request.user).exists():
            
#             UserCoupon.objects.filter(user=request.user).delete()

#         coupon_discount = 0
#         if Coupon.objects.get(code=coupon_code):
#             instance = Coupon.objects.get(code=coupon_code)
#             print("shumban")
#             if float(grand_total) >= float(instance.min_value):
#                 coupon_discount = (
#                     (float(grand_total) * float(instance.discount))/100)
                
#                 grand_total = float(grand_total) - coupon_discount
#                 grand_total = format(grand_total, '.2f')
#                 coupon_discount = format(coupon_discount, '.2f')
#                 msg = 'Coupon Applied successfully'
#                 UserCoupon.objects.create(user=request.user, coupon = instance, used = True, total_price = grand_total)
#                 instance.active = False
#                 instance.save()
#                 print(grand_total,'daxo')
#             else:
#                 msg = 'This coupon is only applicable for orders more than ₹' + \
#                     str(instance.min_value) + '\- only!'
        
#             msg = 'Coupon is not valid'

#         response = {
            
#             'grand_total': grand_total,
#             'msg': msg,
#             'coupon_discount': coupon_discount,
#             'coupon_code': coupon_code,
#         }

#     return JsonResponse(response)


# def single_order_details(request,id):
#     try:
#         order = Order.objects.get(id=id)
#     except Order.DoesNotExist:
#         return redirect('orders')
#     address_id=order.address.id
#     address = Address.objects.get(id=address_id)
#     print(address,"aami")
#     order_items = OrderItem.objects.filter(order_id=id)
#     print(order_items,"aami")

#     context ={
#         'order_item' : order_items,
#         'address'    : address,
#         'order'   : order,
#         'coupon_discount': order.coupon_discount,  # Pass the discount to the template

#     }

#     return render (request, 'order/single_order.html', context)




# def export_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=Expenses' + \
#         str(datetime.now()) + '.csv'

#     writer = csv.writer(response)
#     writer.writerow(['user', 'total_price', 'payment_mode', 'tracking_no'])

#     expenses = Order.objects.all()
#     for expense in expenses:
#         writer.writerow([expense.user, expense.total_price, expense.payment_mode,expense.tracking_no])

#     return response




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


# #=============================================================================
# #INVOICE PDF -USER ORDER

# # from django.shortcuts import render, get_object_or_404
# # from django.http import HttpResponse
# # from .models import Order, OrderItem
# # from django.template.loader import get_template
# # from xhtml2pdf import pisa

# # def generate_invoice(request, order_id):
# #     order = get_object_or_404(Order, id=order_id)
# #     order_items = OrderItem.objects.filter(order=order)
# #     template_path = 'order/invoice.html'
# #     context = {
# #         'order': order,
# #         'order_items': order_items,
# #     }
# #     response = HttpResponse(content_type='application/pdf')
# #     response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(order.tracking_no)
# #     template = get_template(template_path)
# #     html = template.render(context)

# #     pisa_status = pisa.CreatePDF(
# #         html, dest=response
# #     )

# #     if pisa_status.err:
# #         return HttpResponse('We had some errors with code %s' % pisa_status.err)
# #     return response




# # from django.shortcuts import render, get_object_or_404
# # from django.http import HttpResponse
# # from .models import Order, OrderItem
# # from django.template.loader import get_template
# # from xhtml2pdf import pisa
# # import logging

# # logger = logging.getLogger(__name__)

# # def generate_invoice(request, order_id):
# #     try:
# #         order = get_object_or_404(Order, id=order_id)
# #         order_items = OrderItem.objects.filter(order=order)
# #         template_path = 'order/invoice.html'
# #         context = {
# #             'order': order,
# #             'order_items': order_items,
# #         }
# #         response = HttpResponse(content_type='application/pdf')
# #         response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(order.tracking_no)
# #         template = get_template(template_path)
# #         html = template.render(context)
# #         pisa_status = pisa.CreatePDF(html, dest=response)

# #         if pisa_status.err:
# #             logger.error('Error while creating PDF: %s', pisa_status.err)
# #             return HttpResponse('We had some errors while creating the PDF file.')

# #         return response
# #     except Exception as e:
# #         logger.error('Exception during PDF generation: %s', e)
# #         return HttpResponse('An error occurred during PDF generation.')





# # from django.shortcuts import render, get_object_or_404
# # from django.http import HttpResponse
# # from .models import Order, OrderItem
# # from django.template.loader import get_template
# # from xhtml2pdf import pisa
# # import logging

# # logger = logging.getLogger(__name__)

# # def generate_invoice(request, order_id):
# #     try:
# #         order = get_object_or_404(Order, id=order_id)
# #         order_items = OrderItem.objects.filter(order=order)
        
# #         # Calculate subtotal and tax
# #         subtotal = sum(item.price * item.quantity for item in order_items)
# #         tax = subtotal * 0.1  # Assuming 10% tax rate
# #         grand_total = subtotal + tax
        
# #         template_path = 'order/invoice.html'
# #         context = {
# #             'order': order,
# #             'order_items': order_items,
# #             'subtotal': subtotal,
# #             'tax': tax,
# #             'grand_total': grand_total,
# #         }
        
# #         response = HttpResponse(content_type='application/pdf')
# #         response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(order.tracking_no)
# #         template = get_template(template_path)
# #         html = template.render(context)
# #         pisa_status = pisa.CreatePDF(html, dest=response)

# #         if pisa_status.err:
# #             logger.error('Error while creating PDF: %s', pisa_status.err)
# #             return HttpResponse('We had some errors while creating the PDF file.')

# #         return response
# #     except Exception as e:
# #         logger.error('Exception during PDF generation: %s', e)
# #         return HttpResponse('An error occurred during PDF generation.')



# # from django.shortcuts import render, get_object_or_404
# # from django.http import HttpResponse
# # from .models import Order, OrderItem
# # from django.template.loader import get_template
# # from xhtml2pdf import pisa
# # import logging

# # logger = logging.getLogger(__name__)

# # def generate_invoice(request, order_id):
# #     try:
# #         order = get_object_or_404(Order, id=order_id)
# #         order_items = OrderItem.objects.filter(order=order)
        
# #         # Calculate subtotal and tax
# #         subtotal = sum(item.price * item.quantity for item in order_items)
# #         # tax = subtotal * 0.1  # Assuming 10% tax rate
# #         tax = (2 * subtotal)/100
# #         grand_total = subtotal + tax
        
# #         # Determine the status of the order
# #         # Here we take the status of the first order item
# #         order_status = order_items.first().status if order_items.exists() else 'No items'
        
# #         template_path = 'order/invoice.html'
# #         context = {
# #             'order': order,
# #             'order_items': order_items,
# #             'subtotal': subtotal,
# #             'tax': tax,
# #             'grand_total': grand_total,
# #             'order_status': order_status,
# #         }
        
# #         response = HttpResponse(content_type='application/pdf')
# #         response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(order.tracking_no)
# #         template = get_template(template_path)
# #         html = template.render(context)
# #         pisa_status = pisa.CreatePDF(html, dest=response)

# #         if pisa_status.err:
# #             logger.error('Error while creating PDF: %s', pisa_status.err)
# #             return HttpResponse('We had some errors while creating the PDF file.')

# #         return response
# #     except Exception as e:
# #         logger.error('Exception during PDF generation: %s', e)
# #         return HttpResponse('An error occurred during PDF generation.')




# # from django.shortcuts import render, get_object_or_404
# # from django.http import HttpResponse
# # from .models import Order, OrderItem, UserCoupon
# # from django.template.loader import get_template
# # from xhtml2pdf import pisa
# # import logging

# # logger = logging.getLogger(__name__)

# # def generate_invoice(request, order_id):
# #     try:
# #         order = get_object_or_404(Order, id=order_id)
# #         order_items = OrderItem.objects.filter(order=order)

# #         # Calculate subtotal
# #         subtotal = sum(item.price * item.quantity for item in order_items)

# #         # Check if a coupon was applied
# #         try:
# #             user_coupon = UserCoupon.objects.get(user=order.user)
# #             coupon_discount = (subtotal * user_coupon.coupon.discount) / 100
# #         except UserCoupon.DoesNotExist:
# #             coupon_discount = 0
        
# #         # Calculate grand total
# #         grand_total = subtotal - coupon_discount

# #         # Order status determination
# #         order_status = order_items.first().status if order_items.exists() else 'No items'

# #         template_path = 'order/invoice.html'
# #         context = {
# #             'order': order,
# #             'order_items': order_items,
# #             'subtotal': subtotal,
# #             'coupon_discount': coupon_discount,
# #             'grand_total': grand_total,
# #             'order_status': order_status,
# #         }

# #         response = HttpResponse(content_type='application/pdf')
# #         response['Content-Disposition'] = f'attachment; filename="invoice_{order.tracking_no}.pdf"'
# #         template = get_template(template_path)
# #         html = template.render(context)
# #         pisa_status = pisa.CreatePDF(html, dest=response)
# #         if pisa_status.err:
# #             logger.error('Error while creating PDF: %s', pisa_status.err)
# #             return HttpResponse('We had some errors while creating the PDF file.')
# #         return response
# #     except Exception as e:
# #         logger.error('Exception during PDF generation: %s', e)
# #         return HttpResponse('An error occurred during PDF generation.')


# # from django.shortcuts import render, get_object_or_404
# # from django.http import HttpResponse
# # from .models import Order, OrderItem, UserCoupon
# # from django.template.loader import get_template
# # from xhtml2pdf import pisa
# # import logging

# # logger = logging.getLogger(__name__)

# # def generate_invoice(request, order_id):
# #     try:
# #         order = get_object_or_404(Order, id=order_id)
# #         order_items = OrderItem.objects.filter(order=order)

# #         # Calculate subtotal
# #         subtotal = sum(item.price * item.quantity for item in order_items)

# #         # Identify if there's a coupon applied
# #         try:
# #             user_coupon = UserCoupon.objects.get(user=order.user)
# #             coupon_discount = (subtotal * user_coupon.coupon.discount) / 100
# #         except UserCoupon.DoesNotExist:
# #             coupon_discount = 0

# #         # Compute grand total
# #         grand_total = subtotal - coupon_discount

# #         # Determine the status of the order
# #         order_status = order_items.first().status if order_items.exists() else 'No items'

# #         template_path = 'order/invoice.html'
# #         context = {
# #             'order': order,
# #             'order_items': order_items,
# #             'subtotal': subtotal,
# #             'coupon_discount': coupon_discount,
# #             'grand_total': grand_total,
# #             'order_status': order_status,
# #         }

# #         response = HttpResponse(content_type='application/pdf')
# #         response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(order.tracking_no)
# #         template = get_template(template_path)
# #         html = template.render(context)
# #         pisa_status = pisa.CreatePDF(html, dest=response)

# #         if pisa_status.err:
# #             logger.error('Error while creating PDF: %s', pisa_status.err)
# #             return HttpResponse('We had some errors while creating the PDF file.')

# #         return response
# #     except Exception as e:
# #         logger.error('Exception during PDF generation: %s', e)
# #         return HttpResponse('An error occurred during PDF generation.')


# # from django.shortcuts import render, get_object_or_404
# # from django.http import HttpResponse
# # from .models import Order, OrderItem, UserCoupon
# # from django.template.loader import get_template
# # from xhtml2pdf import pisa
# # import logging

# # logger = logging.getLogger(__name__)

# # def generate_invoice(request, order_id):
# #     try:
# #         order = get_object_or_404(Order, id=order_id)
# #         order_items = OrderItem.objects.filter(order=order)

# #         # Calculate subtotal
# #         subtotal = sum(item.price * item.quantity for item in order_items)

# #         # Identify if there's a coupon applied
# #         try:
# #             user_coupon = UserCoupon.objects.get(user=order.user)
# #             coupon_discount = (subtotal * user_coupon.coupon.discount) / 100
# #         except UserCoupon.DoesNotExist:
# #             coupon_discount = 0

# #         # Calculate tax
# #         tax = (2 * subtotal) / 100  # Adjust the percentage as necessary

# #         # Compute grand total
# #         grand_total = subtotal + tax - coupon_discount

# #         # Determine the status of the order
# #         order_status = order_items.first().status if order_items.exists() else 'No items'

# #         template_path = 'order/invoice.html'
# #         context = {
# #             'order': order,
# #             'order_items': order_items,
# #             'subtotal': subtotal,
# #             'tax': tax,
# #             'coupon_discount': coupon_discount,
# #             'grand_total': grand_total,
# #             'order_status': order_status,
# #         }

# #         response = HttpResponse(content_type='application/pdf')
# #         response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(order.tracking_no)
# #         template = get_template(template_path)
# #         html = template.render(context)
# #         pisa_status = pisa.CreatePDF(html, dest=response)

# #         if pisa_status.err:
# #             logger.error('Error while creating PDF: %s', pisa_status.err)
# #             return HttpResponse('We had some errors while creating the PDF file.')

# #         return response
# #     except Exception as e:
# #         logger.error('Exception during PDF generation: %s', e)
# #         return HttpResponse('An error occurred during PDF generation.')











# #LAST WORKING -BUT LAYOUT AND AMOUNTS ARE ALL RANDOM AND WRONG

# # from django.shortcuts import render, get_object_or_404
# # from django.http import HttpResponse
# # from .models import Order, OrderItem, UserCoupon
# # from django.template.loader import get_template
# # from xhtml2pdf import pisa
# # import logging

# # logger = logging.getLogger(__name__)
# # def generate_invoice(request, order_id):
# #     try:
# #         order = get_object_or_404(Order, id=order_id)
# #         order_items = OrderItem.objects.filter(order=order)
# #         for item in order_items:
# #             print(item) 
# #                     # Calculate subtotal including tax
# #         grand_total = sum((item.price * item.quantity) for item in order_items)
# #         # Assume tax is 2% of the total
# # #         # Identify if there's a coupon applied
# #         # tax = (2 * (order))/100
        
# #         # subtotal = order.total_price
# #         coupon_discount = order.coupon_discount
# #         print(coupon_discount, "coupon discou =")

# #         # try:
# #         #     user_coupon = UserCoupon.objects.get(user=order.user)
# #         #     coupon_discount = (subtotal * user_coupon.coupon.discount) / 100
# #         # except UserCoupon.DoesNotExist:
# #         #     coupon_discount = 0
# #         # print(coupon_discount, "coupon discou 2= =")

# #         # subtotal=order.total_price

# #         # Compute grand total
# #         subtotal = grand_total - coupon_discount
# #         # applied_coupon_discount = sum((item.applied_coupon_discount for item in order_items))
# #         # grand_total = subtotal - applied_coupon_discount

# #         template_path = 'order/invoice.html'
# #         context = {
# #             'order': order,
# #             'order_items': order_items,
# #             'subtotal': subtotal,
# #             'coupon_discount': coupon_discount,
# #             'grand_total': grand_total,
# #         }
        
# #         response = HttpResponse(content_type='application/pdf')
# #         response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(order.tracking_no)
# #         template = get_template(template_path)
# #         html = template.render(context)
# #         pisa_status = pisa.CreatePDF(html, dest=response)

# #         if pisa_status.err:
# #             logger.error('Error while creating PDF: %s', pisa_status.err)
# #             return HttpResponse('We had some errors while creating the PDF file.')

# #         return response
# #     except Exception as e:
# #         logger.error('Exception during PDF generation: %s', e)
# #         return HttpResponse('An error occurred during PDF generation.')







# def export_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=Expenses' + \
#                                       str(datetime.now()) + '.csv'

#     writer = csv.writer(response)
#     writer.writerow(['user', 'total_price', 'payment_mode', 'tracking_no'])

#     expenses = Order.objects.all()
#     for expense in expenses:
#         writer.writerow([expense.user, expense.total_price, expense.payment_mode, expense.tracking_no])

#     return response


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

































# 2.
#=============================================++++++++++++++++++++++++++++++++++++++++++++++++++
# TO MAKE ALL VAUES UNIFORM
#=============================================++++++++++++++++++++++++++++++++++++++++++++++++++++
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from carts.models import Cart, CartItem
from carts.views import _cart_id
from accounts.models import CustomUser
from userprofile.models import Address, UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from store.models import Product
from . models import Coupon, Order, OrderItem, ReturnOrder, UserCoupon
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import csv
import random


# Create your views here.

@cache_control(no_cache=True,must_revalidate=True,no_store=True)    
@login_required(login_url='user_login')
def checkout(request,total=0, quantity=0, cart_item=None):  
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
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
    
    address = Address.objects.filter(user = request.user)
    coupons = Coupon.objects.filter(active = True)
    print(coupons,"daxii")
    print(coupons,"couponssssss")
    context = {
        'cart_items' : cart_items,
        'quantity' : quantity,
        'total' : total,
        'tax' : tax,
        'grand_total' : grand_total,
        'address' : address,
        'coupons': coupons,
        'usercoupon': UserCoupon.objects.filter(user=request.user),
    }
    return render(request,'store/checkout.html',context)



#EXISTING Placeoder function
@login_required(login_url='user_login')
def placeorder(request):
   
    if request.method == 'POST':

        # coupon_code = request.POST['coupon']
        
        neworder = Order()
        neworder.user = request.user
        address_id = request.POST['address']
    
        address = Address.objects.get(id=address_id)
        neworder.address = address
        payment_mode = request.POST.get('payment_method')
        neworder.payment_mode = payment_mode

        neworder.payment_id = request.POST.get('payment_id')

        cart = CartItem.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            if item.product.offer:

                cart_total_price += item.product.get_offer_price() * item.quantity

            else:
                cart_total_price += item.product.price * item.quantity
            # item.product.stock-=item.quantity
        
        #Modification-1-START
        # Moved tax calculation after coupon application
        #tax = (2*cart_total_price)/100
        #neworder.total_price = cart_total_price + tax

        try:
            instance = UserCoupon.objects.get(user=request.user)

            if float(cart_total_price) >= float(instance.coupon.min_value):
                coupon_discount = (
                    (float(cart_total_price) * float(instance.coupon.discount))/100)
                cart_total_price = float(cart_total_price) - coupon_discount
                # cart_total_price = format(cart_total_price, '.2f')
                # coupon_discount = format(coupon_discount, '.2f')
                neworder.coupon_discount = coupon_discount # Store coupon discount in the order

            instance.delete()
            neworder.total_price = cart_total_price 
            
            tax = (2*cart_total_price)/100 # Calculate tax on discounted price
            neworder.total_price = cart_total_price + tax # Update total price with discount and tax

            neworder.save()

        except:
            tax = (2*cart_total_price)/100
            neworder.total_price = cart_total_price + tax
            #Modification-1-END

        trackno = random.randint(1111111, 9999999)

        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = random.randint(1111111, 9999999)
        neworder.tracking_no = trackno
        neworder.save()


        
        neworderitems = CartItem.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
                
            )

            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.stock = orderproduct.stock - item.quantity
            orderproduct.save()

        

            
        if (payment_mode== 'wallet_payment'):
            
            wallet = CustomUser.objects.get(email=request.user)
            if float(cart_total_price) >= float(wallet.wallet):
               messages.error(request, 'Wallet does not have the required amount')
               return redirect(checkout)
            
            wallet.wallet -= cart_total_price
            wallet.save()
                

        # To clear user Cart
        CartItem.objects.filter(user=request.user).delete()
        
        #Modification-2-START
        # Corrected the context being passed to order_success.html
        context={
            'order' : OrderItem.objects.filter(order=neworder),
            'order_id': neworder.id, # Pass the new order's ID
            'total_price': neworder.total_price, # Pass the order's total price
            'coupon_discount': neworder.coupon_discount, # Pass the order's coupon discount
        }
        #Modification-2-END

    return render(request, 'order/order_success.html', context)




# @login_required(login_url='user_login')
# def placeorder(request):
   
#     if request.method == 'POST':

#         # coupon_code = request.POST['coupon']
        
#         neworder = Order()
#         neworder.user = request.user
#         address_id = request.POST['address']
    
#         address = Address.objects.get(id=address_id)
#         neworder.address = address
#         payment_mode = request.POST.get('payment_method')
#         neworder.payment_mode = payment_mode

#         neworder.payment_id = request.POST.get('payment_id')

#         cart = CartItem.objects.filter(user=request.user)
#         cart_total_price = 0
#         for item in cart:
#             if item.product.offer:

#                 cart_total_price += item.product.get_offer_price() * item.quantity

#             else:
#                 cart_total_price += item.product.price * item.quantity
#             # item.product.stock-=item.quantity
        
#         #Modification-1-START
#         # Moved tax calculation after coupon application
#         #tax = (2*cart_total_price)/100
#         #neworder.total_price = cart_total_price + tax

#         try:
#             instance = UserCoupon.objects.get(user=request.user)

#             if float(cart_total_price) >= float(instance.coupon.min_value):
#                 coupon_discount = (
#                     (float(cart_total_price) * float(instance.coupon.discount))/100)
#                 cart_total_price = float(cart_total_price) - coupon_discount
#                 # cart_total_price = format(cart_total_price, '.2f')
#                 # coupon_discount = format(coupon_discount, '.2f')
#                 neworder.coupon_discount = coupon_discount # Store coupon discount in the order

#             instance.delete()
#             neworder.total_price = cart_total_price 
            
#             tax = (2*cart_total_price)/100 # Calculate tax on discounted price
#             neworder.total_price = cart_total_price + tax # Update total price with discount and tax

#             neworder.save()

#         except:
#             tax = (2*cart_total_price)/100
#             neworder.total_price = cart_total_price + tax
#             #Modification-1-END

#         trackno = random.randint(1111111, 9999999)

#         while Order.objects.filter(tracking_no=trackno).exists():
#             trackno = random.randint(1111111, 9999999)
#         neworder.tracking_no = trackno
#         neworder.save()


        
#         neworderitems = CartItem.objects.filter(user=request.user)
#         for item in neworderitems:
#             OrderItem.objects.create(
#                 order=neworder,
#                 product=item.product,

#                 # product_name=item.product.product_name,  # Store the product name

#                 # price=item.product.price,
#                 # quantity=item.quantity,
#             # Snapshot data at the time of order:
#                 product_name=item.product.product_name,  
#                 # price=item.product.price if not item.product.offer else item.product.get_offer_price(), 
#                 # quantity=item.quantity,
#                 product_price=item.product.price if not item.product.offer else item.product.get_offer_price(), 
#                 quantity=item.quantity,
#                 image=item.product.images.first() if item.product.images.exists() else None  # Snapshot image (if needed)        
#             )

#             orderproduct = Product.objects.filter(id=item.product_id).first()
#             orderproduct.stock = orderproduct.stock - item.quantity
#             orderproduct.save()

        

            
#         if (payment_mode== 'wallet_payment'):
            
#             wallet = CustomUser.objects.get(email=request.user)
#             if float(cart_total_price) >= float(wallet.wallet):
#                messages.error(request, 'Wallet does not have the required amount')
#                return redirect(checkout)
            
#             wallet.wallet -= cart_total_price
#             wallet.save()
                

#         # To clear user Cart
#         CartItem.objects.filter(user=request.user).delete()
        
#         #Modification-2-START
#         # Corrected the context being passed to order_success.html
#         context={
#             'order' : OrderItem.objects.filter(order=neworder),
#             'order_id': neworder.id, # Pass the new order's ID
#             'total_price': neworder.total_price, # Pass the order's total price
#             'coupon_discount': neworder.coupon_discount, # Pass the order's coupon discount
#         }
#         #Modification-2-END

#     return render(request, 'order/order_success.html', context)



def razarypaycheck(request):
    cart = CartItem.objects.filter(user=request.user)
    total_price = 0
    
    for item in cart:
        if item.product.offer:
            total_price += item.product.get_offer_price() * item.quantity
        else:
            total_price = total_price + item.product.price * item.quantity
    #Modification-3-START
    try:
        instance = UserCoupon.objects.get(user=request.user)
        # Apply the discount to total_price here
        if float(total_price) >= float(instance.coupon.min_value):
            coupon_discount = (
                (float(total_price) * float(instance.coupon.discount))/100)
            total_price = float(total_price) - coupon_discount
    except UserCoupon.DoesNotExist:
        pass
    #Modification-3-END
    tax = (2*total_price)/100
    total_price = round(total_price+tax)

    return JsonResponse({'total_price': total_price})




def sample(request):
    if request.method == 'POST':
        neworder = Order()
        neworder.user = request.user
        address_id = request.POST['address']
        address = Address.objects.get(id=address_id)
        neworder.address = address
        neworder.payment_mode = request.POST.get('payment_method')
        neworder.payment_id = request.POST.get('payment_id')

        cart = CartItem.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            if item.product.offer:
                cart_total_price += item.product.get_offer_price() * item.quantity
            else:
                cart_total_price += item.product.price * item.quantity

        #Modification-4-START
        # Moved tax calculation and coupon discount application
        # try:
        #     instance = UserCoupon.objects.get(user=request.user)

        #     if float(cart_total_price) >= float(instance.coupon.min_value):
        #         coupon_discount = (
        #             (float(cart_total_price) * float(instance.coupon.discount))/100)
        #         cart_total_price = float(cart_total_price) - coupon_discount
        #         cart_total_price = format(cart_total_price, '.2f')
        #         coupon_discount = format(coupon_discount, '.2f')

        #     instance.delete()
        #     neworder.total_price = cart_total_price
        #     neworder.save()

        # except:
        #     pass

        # tax = round((2*cart_total_price)/100)
        # neworder.total_price = cart_total_price + tax

        try:
            instance = UserCoupon.objects.get(user=request.user)

            if float(cart_total_price) >= float(instance.coupon.min_value):
                coupon_discount = (
                    (float(cart_total_price) * float(instance.coupon.discount))/100)
                cart_total_price = float(cart_total_price) - coupon_discount
                # cart_total_price = format(cart_total_price, '.2f')
                # coupon_discount = format(coupon_discount, '.2f')
                neworder.coupon_discount = coupon_discount # Store coupon discount in the order

            instance.delete()
            neworder.total_price = cart_total_price
            
            tax = (2*cart_total_price)/100 # Calculate tax on discounted price
            neworder.total_price = cart_total_price + tax # Update total price with discount and tax

            neworder.save()

        except:
            tax = (2*cart_total_price)/100
            neworder.total_price = cart_total_price + tax
        #Modification-4-END
        trackno = random.randint(1111111, 9999999)
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = random.randint(1111111, 9999999)
        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = CartItem.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,      
            )
            # To decrease the product quantity from available stock
        orderproduct = Product.objects.filter(id=item.product.id).first()
        orderproduct.stock = orderproduct.stock - item.quantity
        orderproduct.save()
        payment_mode = request.POST.get('payment_method')
        if (payment_mode== 'Razorpay'):
            CartItem.objects.filter(user=request.user).delete()
            return JsonResponse({'status' : "Your order has been succesfully placed"})

        # To clear user Cart
        CartItem.objects.filter(user=request.user).delete()
    return redirect('checkout')
    


def orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-update_at')
    orderitems = OrderItem.objects.filter(order__in=orders).order_by('-order__update_at')
    context = {
        'orders': orders,
        'orderitems': orderitems,
    }
    return render(request, 'order/order_list.html', context)
    # return render(request, 'order/order_success.html', context)



def ordercancel(request):
    
    order_id = request.POST.get('order_id')
    print("order_id",order_id)
    order_item_id= request.POST.get('orderitem_id')
    print("order_item_id",order_item_id)
    orders = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.get(id=order_item_id)

    if orders.payment_mode == 'Razorpay' or 'wallet_payment':
        wallet = CustomUser.objects.get(email=request.user)
        wallet.wallet += orders.total_price
        wallet.save()

    order_items.product.stock+=order_items.quantity
    # order_items.quantity = 0
    order_items.status = 'Cancelled'
    order_items.save()
    return redirect('orders')



#===========#ORDER CANCEL ITEM TO RESTOCK CODE -LAST REVIEW MWETIONED===========
from django.http import HttpResponse, JsonResponse
# ... other imports ...

@login_required(login_url='user_login')
def ordercancel(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order_item_id = request.POST.get('orderitem_id')
        orders = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.get(id=order_item_id)

        if orders.payment_mode in ['Razorpay', 'wallet_payment']:
            wallet = CustomUser.objects.get(email=request.user)
            wallet.wallet += orders.total_price
            wallet.save()

        # Restock items
        order_items.product.stock += order_items.quantity
        order_items.product.save()

        order_items.status = 'Cancelled'
        order_items.save()
        
        return JsonResponse({'status': 'Order Cancelled Successfully'}) 
        
    else:
        return JsonResponse({'status': 'Invalid request'}) 
    return redirect('single_order_details')
    
    
def order_return(request,id):
    order_item = OrderItem.objects.get(id=id)
    wallet = 0
    if request.method == "POST":
        return_reason = request.POST.get('return_reason')
        return_comment = request.POST.get('return_comment')
        ReturnOrder.objects.create(order_item=order_item,return_reason= return_reason, return_comment=return_comment)
        order_item.status = "Returned"
        order_item.product.stock+= order_item.quantity
        order_item.save()

        wallet=CustomUser.objects.get(email=request.user)
        wallet.wallet += order_item.order.total_price
        wallet.save()
        print(wallet.wallet,"daxo")

    return redirect('orders')

    



def coupons(request):
    if request.method == 'POST':
        coupon_code = request.POST['coupon']
        
        
        grand_total = request.POST['grand_total']
        if UserCoupon.objects.filter(user=request.user).exists():
            
            UserCoupon.objects.filter(user=request.user).delete()

        coupon_discount = 0
        if Coupon.objects.get(code=coupon_code):
            instance = Coupon.objects.get(code=coupon_code)
            print("shumban")
            if float(grand_total) >= float(instance.min_value):
                coupon_discount = (
                    (float(grand_total) * float(instance.discount))/100)
                
                grand_total = float(grand_total) - coupon_discount
                grand_total = format(grand_total, '.2f')
                coupon_discount = format(coupon_discount, '.2f')
                msg = 'Coupon Applied successfully'
                UserCoupon.objects.create(user=request.user, coupon = instance, used = True, total_price = grand_total)
                instance.active = False
                instance.save()
                print(grand_total,'daxo')
            else:
                msg = 'This coupon is only applicable for orders more than ₹' + \
                    str(instance.min_value) + '\- only!'
        
            msg = 'Coupon is not valid'

        response = {
            
            'grand_total': grand_total,
            'msg': msg,
            'coupon_discount': coupon_discount,
            'coupon_code': coupon_code,
        }

    return JsonResponse(response)


def single_order_details(request,id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return redirect('orders')
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

    return render (request, 'order/single_order.html', context)

# def single_order_details(request, id):
#     order = get_object_or_404(Order, id=id)
#     address = order.address # Access address directly from the order
#     order_items = OrderItem.objects.filter(order_id=id).select_related(
#         'product'
#     )  # Use select_related for optimization

#     # Access product details directly from order_items
#     for order_item in order_items:
#         print(order_item.product.product_name)  # Access product name from the prefetched data 

#     context = {
#         'order_item': order_items,
#         'address': address,
#         'order': order,
#     }

#     return render(request, 'order/single_order.html', context)



def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['user', 'total_price', 'payment_mode', 'tracking_no'])

    expenses = Order.objects.all()
    for expense in expenses:
        writer.writerow([expense.user, expense.total_price, expense.payment_mode,expense.tracking_no])

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













#INVOICE PDF -USER ORDER


# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
# from .models import Order, OrderItem, UserCoupon
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# import logging

# logger = logging.getLogger(__name__)
# def generate_invoice(request, order_id):
#     try:
#         #Modification-5-START
#         order = get_object_or_404(Order, id=order_id)
#         order_items = OrderItem.objects.filter(order=order)

#         # Calculate subtotal
#         subtotal = sum((item.price * item.quantity) for item in order_items)

#         # Get coupon discount from the order
#         coupon_discount = order.coupon_discount if order.coupon_discount else 0 

#         # Calculate grand total
#         grand_total = subtotal - coupon_discount 

#         template_path = 'order/invoice.html'
#         context = {
#             'order': order,
#             'order_items': order_items,
#             'subtotal': subtotal,
#             'coupon_discount': coupon_discount,
#             'grand_total': grand_total,
#         }
#         #Modification-5-END
        
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(order.tracking_no)
#         template = get_template(template_path)
#         html = template.render(context)
#         pisa_status = pisa.CreatePDF(html, dest=response)

#         if pisa_status.err:
#             logger.error('Error while creating PDF: %s', pisa_status.err)
#             return HttpResponse('We had some errors while creating the PDF file.')

#         return response
#     except Exception as e:
#         logger.error('Exception during PDF generation: %s', e)
#         return HttpResponse('An error occurred during PDF generation.')

# #MODIFIED INVOICE
# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
# from .models import Order, OrderItem, UserCoupon
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# import logging

# logger = logging.getLogger(__name__)
# def generate_invoice(request, order_id):
#     try:
#         order = get_object_or_404(Order, id=order_id)
#         order_items = OrderItem.objects.filter(order=order)

#         # Calculate subtotal including tax
#         subtotal = sum((item.price * item.quantity) for item in order_items)
#         tax = (2 * subtotal)/100
#         subtotal_with_tax=subtotal+tax


#         # Get coupon discount from the order
#         coupon_discount = order.coupon_discount if order.coupon_discount else 0 

#         # Calculate grand total
#         grand_total = subtotal_with_tax - coupon_discount

#         template_path = 'order/invoice.html'
#         context = {
#             'order': order,
#             'order_items': order_items,
#             'subtotal': subtotal_with_tax, # Pass subtotal including tax
#             'coupon_discount': coupon_discount,
#             'grand_total': grand_total,
#             'shipping_address' : order.address, # Pass shipping address
#             'order_status' : order.status # Pass order status
#         }
        
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(order.tracking_no)
#         template = get_template(template_path)
#         html = template.render(context)
#         pisa_status = pisa.CreatePDF(html, dest=response)

#         if pisa_status.err:
#             logger.error('Error while creating PDF: %s', pisa_status.err)
#             return HttpResponse('We had some errors while creating the PDF file.')

#         return response
#     except Exception as e:
#         logger.error('Exception during PDF generation: %s', e)
#         return HttpResponse('An error occurred during PDF generation.')



# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
# from .models import Order, OrderItem, UserCoupon
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# import logging

# logger = logging.getLogger(__name__)

# def generate_invoice(request, order_id):
#     try:
#         order = get_object_or_404(Order, id=order_id)
#         order_items = OrderItem.objects.filter(order=order)

#         # Calculate subtotal including tax
#         subtotal = sum((item.price * item.quantity) for item in order_items)
#         tax = (2 * subtotal) / 100
#         subtotal_with_tax = subtotal + tax

#         # Get coupon discount from the order
#         coupon_discount = order.coupon_discount if order.coupon_discount else 0

#         # Calculate grand total
#         grand_total = subtotal_with_tax - coupon_discount

#         # Get the order status from the first order item (assuming all items have the same status)
#         order_status = order_items.first().status if order_items.exists() else 'N/A'

#         template_path = 'order/invoice.html'
#         context = {
#             'order': order,
#             'order_items': order_items,
#             'subtotal': subtotal_with_tax,  # Pass subtotal including tax
#             'coupon_discount': coupon_discount,
#             'grand_total': grand_total,
#             'shipping_address': order.address,  # Pass shipping address
#             'order_status': order_status,  # Pass order status from OrderItem
#         }

#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(
#             order.tracking_no
#         )
#         template = get_template(template_path)
#         html = template.render(context)
#         pisa_status = pisa.CreatePDF(html, dest=response)

#         if pisa_status.err:
#             logger.error('Error while creating PDF: %s', pisa_status.err)
#             return HttpResponse('We had some errors while creating the PDF file.')

#         return response
#     except Exception as e:
#         logger.error('Exception during PDF generation: %s', e)
#         return HttpResponse('An error occurred during PDF generation.')


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Order, OrderItem, UserCoupon
from django.template.loader import get_template
from xhtml2pdf import pisa
import logging

logger = logging.getLogger(__name__)

def generate_invoice(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)
        order_items = OrderItem.objects.filter(order=order)

        # Calculate values for each item and store in a list
        invoice_items = []
        for item in order_items:
            total_price = item.quantity * item.price
            invoice_items.append({
                'item': item,
                'total_price': total_price 
            })

        # Calculate subtotal including tax
        subtotal = sum((item.price * item.quantity) for item in order_items)
        tax = (2 * subtotal) / 100
        subtotal_with_tax = subtotal + tax

        # Get coupon discount from the order
        coupon_discount = order.coupon_discount if order.coupon_discount else 0

        # Calculate grand total
        grand_total = subtotal_with_tax - coupon_discount

        # Get the order status from the first order item (assuming all items have the same status)
        order_status = order_items.first().status if order_items.exists() else 'N/A'

        template_path = 'order/invoice.html'
        context = {
            'order': order,
            'invoice_items': invoice_items,  # Pass the calculated item totals
            'subtotal': subtotal_with_tax,  # Pass subtotal including tax
            'coupon_discount': coupon_discount,
            'grand_total': grand_total,
            'shipping_address': order.address,  # Pass shipping address
            'order_status': order_status,  # Pass order status from OrderItem
        }

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(
            order.tracking_no
        )
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            logger.error('Error while creating PDF: %s', pisa_status.err)
            return HttpResponse('We had some errors while creating the PDF file.')

        return response
    except Exception as e:
        logger.error('Exception during PDF generation: %s', e)
        return HttpResponse('An error occurred during PDF generation.')

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++











#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# NOT CORRECT- COUPON DISCOUNT AMOUNT NOT AT ALL CORRECT- GRANT TOTAL VALUE GOES NEGATIVE---
# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
# from .models import Order, OrderItem, UserCoupon
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# import logging

# logger = logging.getLogger(__name__)

# def generate_invoice(request, order_id):
#     try:
#         order = get_object_or_404(Order, id=order_id)
#         order_items = OrderItem.objects.filter(order=order)

#         # Calculate values for each item and store in a list
#         invoice_items = []
#         for item in order_items:
#             total_price = item.quantity * item.price
#             invoice_items.append({
#                 'item': item,
#                 'total_price': total_price
#             })

#         # Calculate subtotal
#         subtotal = sum((item.price * item.quantity) for item in order_items)

#         # Calculate tax
#         tax = (2 * subtotal) / 100

#         # Calculate subtotal with tax
#         subtotal_with_tax = subtotal + tax

#         # NOW, calculate the coupon discount based on subtotal_with_tax
#         coupon_discount = 0
#         if order.coupon_discount:
#             coupon_discount = (subtotal_with_tax * order.coupon_discount) / 100

#         # Calculate grand total
#         grand_total = subtotal_with_tax - coupon_discount

#         # Get the order status from the first order item (assuming all items have the same status)
#         order_status = order_items.first().status if order_items.exists() else 'N/A'

#         template_path = 'order/invoice.html'
#         context = {
#             'order': order,
#             'invoice_items': invoice_items,  # Pass the calculated item totals
#             'subtotal': subtotal, # Pass subtotal without tax
#             'tax': tax, # Pass the tax amount
#             'subtotal_with_tax': subtotal_with_tax, # Pass subtotal including tax
#             'coupon_discount': coupon_discount,
#             'grand_total': grand_total,
#             'shipping_address': order.address,  # Pass shipping address
#             'order_status': order_status,  # Pass order status from OrderItem
#         }

#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(
#             order.tracking_no
#         )
#         template = get_template(template_path)
#         html = template.render(context)
#         pisa_status = pisa.CreatePDF(html, dest=response)

#         if pisa_status.err:
#             logger.error('Error while creating PDF: %s', pisa_status.err)
#             return HttpResponse('We had some errors while creating the PDF file.')

#         return response
#     except Exception as e:
#         logger.error('Exception during PDF generation: %s', e)
#         return HttpResponse('An error occurred during PDF generation.')








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


