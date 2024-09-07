from django.urls import path
from . import views

urlpatterns = [
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('', views.dashboard,name='dashboard'),
    path('users/', views.users,name='users'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('<int:id>/blockuser/', views.blockuser, name='blockuser'),
    # path('update/<int:user_id>', views.update,name='update'),
    # path('delete/<int:user_id>', views.delete,name='delete'),


    #PRODUCT MANAGEMENT
    path('product_list/', views.product_list, name='product_list'),
    path('<int:id>/product_delete/', views.product_delete, name='product_delete'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_edit/<int:product_id>/',views.product_edit,name='product_edit'),
        

    #CATEGORY MANAGEMENT
    path('category_list/', views.category_list, name='category_list'),
    path('add_category/', views.add_category, name='add_category'),
    path('category_delete/<int:category_id>/', views.category_delete, name='category_delete'),
    path('category_edit/<int:category_id>/', views.category_edit, name='category_edit'),
    path('sub_category_list/', views.sub_category_list, name='sub_category_list'),
    path('sub_category_delete/<int:sub_id>/', views.sub_category_delete, name='sub_category_delete'),
    path('add_sub_category/', views.add_sub_category, name='add_sub_category'),
    path('sub_category_edit/<int:sub_id>/', views.sub_category_edit, name='sub_category_edit'),


    #ORDER MANAGEMENT
    path('order_management/', views.order_management, name='order_management'),
    path('update-order/<int:id>', views.update_order, name='update_order'),


    #COUPON MANAGEMENT
    path('coupon_management/', views.coupon_management, name='coupon_management'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('edit_coupon/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    path('delete_coupon/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),


    #VARIANTS
    path('variants/', views.variants, name='variants'),
    path('add_variants/', views.add_variants, name='add_variants'),
    path('edit_variants/<int:id>/', views.edit_variants, name='edit_variants'),
    path('delete_variants/<int:id>/', views.delete_variants, name='delete_variants'),



    path('admin_single_order/<int:id>/', views.admin_single_order, name='admin_single_order'),


    #PRICE RANGE
    path('price_range/', views.price_range, name='price_range'),
    path('add_price_range/', views.add_price_range, name='add_price_range'),
    path('delete_price_range/<int:id>/', views.delete_price_range, name='delete_price_range'),
    path('edit_price_range/<int:id>/', views.edit_price_range, name='edit_price_range'),
    
    #PRODUCT OFFERS
    path('offer_managment/', views.offer_managment, name='offer_managment'),
    path('add_offer/', views.add_offer, name='add_offer'),
    path('editoffer/<int:offer_id>/', views.editoffer, name='editoffer'),
    path('delete_offer/<int:id>/', views.delete_offer, name='delete_offer'),

    # CATEGORY OFFERS
    path('category_offer_management/', views.category_offer_management, name='category_offer_management'),
    path('add_category_offer/', views.add_category_offer, name='add_category_offer'),
    path('edit_category_offer/<int:category_offer_id>/', views.edit_category_offer, name='edit_category_offer'),
    path('delete_category_offer/<int:category_offer_id>/', views.delete_category_offer, name='delete_category_offer'),
    

    path('export_csv/',views.export_csv, name="export_csv"),
    path('export_pdf/', views.export_pdf, name='export_pdf'),



    #SALES REPORT
    path('sales-report/', views.sales_report, name='sales-report'),
    path('download-sales-report/<str:report_format>/', views.download_sales_report, name='download-sales-report'),


]
