from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('seller-index/',views.seller_index,name='seller-index'),
    path('checkout/',views.checkout,name='checkout'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('change-password/',views.change_password,name='change-password'),
    path('profile/',views.profile,name='profile'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('new-password/',views.new_password,name='new-password'),
    path('seller-add-product/',views.seller_add_product,name='seller-add-product'),
    path('seller-view-product/',views.seller_view_product,name='seller-view-product'),
    path('seller-product-details/<int:pk>/',views.seller_product_details,name='seller-product-details'),
    path('seller-edit-product/<int:pk>/',views.seller_edit_product,name='seller-edit-product'),
    path('seller-delete-product/<int:pk>/',views.seller_delete_product,name='seller-delete-product'),
    path('seller-view-laptops/',views.seller_view_laptops,name='seller-view-laptops'),
    path('seller-view-cameras/',views.seller_view_cameras,name='seller-view-cameras'),
    path('seller-view-accessories/',views.seller_view_accessories,name='seller-view-accessories'),
    path('product-details/<int:pk>/',views.product_details,name='product-details'),
    path('add-to-wishlist/<int:pk>/',views.add_to_wishlist,name='add-to-wishlist'),

]