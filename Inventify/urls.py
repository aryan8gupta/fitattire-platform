from django.contrib import admin
from django.urls import path
from Inventify import base
from django.conf.urls.static import static

from Inventify import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', views.health_check),

    path('', views.index),
    path('products-2/', views.products_2),
    path('product-display/<str:qr_id>/', views.product_display),
    path('invoice/<str:invoice_id>/', views.invoice),

    path('download-images/', views.download_images_zip, name='download_images'),
    path('download-videos/', views.download_videos_zip, name='download_videos'),
    path('api/decrease-credits/', views.decrease_credits, name='decrease_credits'),

    path('login/', views.login),
    # path('login2/', views.login),
    path('logout/', views.logout, name='logout'),

    path('dashboard/', views.dashboard),

    # Shop Owners ----------------------->
    path('employee/', views.employee),
    path('employee-signup/', views.employee_signup),

    path('add-products/', views.add_products),
    path('upload', views.upload_image),
    path('in-stock/', views.in_stock_products),
    path('products-sold/', views.products_sold_view),


    path('contact/', views.contact_us),
    path('analytics/', views.analytics),

    # path('barcode/', views.barcode),

    path('exchange/', views.exchange),
    path("get-product-sold/", views.get_product_sold_by_qrcode),
    path("get-product/", views.get_product_by_qrcode),
    path("get-garment/", views.get_garment_image),

    path('sales/', views.sales),
    path("search-whatsapp-number/", views.search_whatsapp_number),
    path("add-whatsapp-number/", views.add_whatsapp_number),

    # For scanning QR-codes
    path('scan/', views.scan_qr, name='scan_qr'),
    
    # ----------------------------------->
    
    # Admin ----------------------->
    path('shops/', views.shops),
    path('shops-add/', views.shops_add),
    path('users-details/', views.users_details),
    path('admin-only-user_signup-5famtsp89f1/', views.users_signup),
    # ----------------------------------->
    
    path('delete/', views.delete),
    path('detail/', views.detail),
    path('update/', views.update),
    path('app-settings/', views.app_settings),
    path('subscription/', views.subscription),
    path('subscription-upgrade/', views.subs_upgrade),

] + static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)