
from django.contrib import admin
from django.urls import path
from. import views
from  payment.views import verify_payment

urlpatterns = [
    path('payment_success', views.payment_success, name='payment_success'),
    path('checkout', views.checkout, name='checkout'),
    path('billing_info', views.billing_info, name='billing_info'),
    path('process_order', views.process_order, name='process_order'),
    path('shipped_dash', views.shipped_dash, name='shipped_dash'),
    path('not_shipped_dash', views.not_shipped_dash, name='not_shipped_dash'),
    path('orders/<int:pk>', views.orders, name='orders'),
    #  paystack
    path('make_payment', views.make_payment, name='make_payment'),
    path('verify_payment/<slug:ref>/', views.verify_payment, name='verify_payment'),
       
    #  path('/verify_payment/<slug:ref>/<int:pk>/', views.verify_payment, name='verify_payment'),

# //paystack2
#    path('payment/<int:order_id>/', views.initialize_payment, name='initialize_payment'),
#    path('payment/verify/', views.verify_payment2, name='verify_payment2'),
   path('payment/failed/', views.failed, name='failed'),
   path('payment/thanks/', views.thanks, name='thanks'),
   path('pay/<int:order_id>/', views.initialize_payment, name='initialize_payment'),
   path('verify/', views.verify_payment2, name='verify_payment2'),
  


# 
#    path('verify/', views.verify_payment2, name='verify_payment2'),
  
   
   
]