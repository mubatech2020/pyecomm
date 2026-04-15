from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product, Profile
import datetime
# Create your views here.

def orders(request, pk):
    if  request.user.is_authenticated and request.user.is_superuser:
         
        #  get the specific order with the id from the database us the pk(primarykey)

         order = Order.objects.get(id=pk)

        # get each item in the orders
         items = OrderItem.objects.filter(order=pk)

        #  check if the form is filled

         if request. POST:
          status  = request.POST['shipping_status']
           # check whether is true or false.
          if status == "true":
               #get order
               order = Order.objects.filter(id=pk)
               #update order

               now = datetime.datetime.now()
               order.update(shipped=True, date_shipped=now)
               messages.success(request, "Shipping status Updated  Successfully to shipped")
               return redirect('home')
          else:
              #get order
               order = Order.objects.filter(id=pk)
               #update order
               order.update(shipped=False)

               messages.success(request, "Shipping status Updated  Successfully to not shipped")
               return redirect('home')
        
        
         return render (request, "payment/orders.html",{"order":order, "items":items })
    else:
      messages.success(request, "Access Denied")
      return redirect('home')


def not_shipped_dash(request):
    if  request.user.is_authenticated and request.user.is_superuser:
         orders = Order.objects.filter(shipped=False)

         if request. POST:
            status  = request.POST['shipping_status']
            num  = request.POST['num']
           
            # grab with the num input feild order


            order = Order.objects.filter(id=num)
             #grab date time
            now = datetime.datetime.now()
             #Update orders

            order.update(shipped=True, date_shipped=now)
             #redirect page
            messages.success(request, "Shipping status Updated  Successfully to shipped")
            return redirect('home')
         
              



         return render (request, "payment/not_shipped_dash.html",{"orders":orders})
    else:
      messages.success(request, "Access Denied")
      return redirect('home')

def shipped_dash(request):
     if  request.user.is_authenticated and request.user.is_superuser:
          orders = Order.objects.filter(shipped=True)



          if request. POST:
            status  = request.POST['shipping_status']
            num  = request.POST['num']
           
         
               # grab with the num input feild order


            order = Order.objects.filter(id=num)
             #grab date time
            now = datetime.datetime.now()
             #Update orders
           
            order.update(shipped=False)
             #redirect page
            messages.success(request, "Shipping status Updated  Successfully to  not shipped")
            return redirect('home')
     
          return render (request, "payment/shipped_dash.html",{"orders":orders})
     else:
          messages.success(request, "Access Denied")
          return redirect('home')

def process_order(request):
     if request.POST:
      
     # get the cart staffs to get the amount
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities =   cart.get_quants

        totals = cart.cart_total()


       #   Get billing info from the lastpage
        payment_form = PaymentForm(request.POST or None )


     
       
      #   Get shipping  session 

        my_shipping = request.session.get('my_shipping')

        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']

      # print(my_shipping)
        shipping_address =  f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping ['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        # print(shipping_address)
        amount_paid = totals
        #gather order info

        if request.user.is_authenticated:
           user = request.user

           create_order = Order(user=user,  full_name=full_name,  email=email,  shipping_address= shipping_address,   amount_paid=amount_paid)
           create_order.save()
              #add order items



              # get the order id
           order_id= create_order.pk
             #pk stands for the primary key


            # get product info
           for product in cart_products():
              # get product info
              product_id = product.id
              if product.is_sale:
                  price = product.saleprice
              else:
                    price = product.price


                   # Get the quantity

              for key, value in quantities().items():

                 if int(key) == product.id:
                      #  print (value) 
                      # thats the quantity

                     #lets create order item

                     create_order_item =OrderItem(order_id=order_id, product_id=product_id, user=user, quantity= value, price=price)

                     create_order_item.save()


        #delete our cart
           for key in list(request.session.keys()):
                if key == "session_key":
                    
                    #Delete the  key
                     del request.session[key]
                     
       #delete  the cart from our database
                current_user = Profile.objects.filter(user__id= request.user.id)

                #delete  the cart in database

                current_user.update(oldcart="")
                



           messages.success(request, "Order  Placed")
           return redirect('home')

        else:
            # if the user is not logged in
            create_order = Order(full_name=full_name,  email=email,  shipping_address= shipping_address,   amount_paid=amount_paid)
            create_order.save()


                   # get the order id
            order_id= create_order.pk
             #pk stands for the primary key


            # get product info
            for product in cart_products():
              # get product info
              product_id = product.id
              if product.is_sale:
                  price = product.saleprice
              else:
                    price = product.price


                   # Get the quantity

              for key, value in quantities().items():

                 if int(key) == product.id:
                      #  print (value) 
                      # thats the quantity

                     #lets create order item

                     create_order_item =OrderItem(order_id=order_id, product_id=product_id,  quantity= value, price=price)

                     create_order_item.save()

            #delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    
                    #Delete the  key
                     del request.session[key]


            messages.success(request, "Order  Placed")
            return redirect('home')
      
       

     else:
         messages.success(request, "Access denied")
         return redirect('home')



def payment_success(request):


    return render(request, 'payment/payment_success.html', {})
 







def checkout(request):

    
# get the cart staffs
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities =   cart.get_quants

    totals = cart.cart_total()

    if request.user.is_authenticated:
         
         
         
         shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        #  shipping_user = ShippingAddress.objects.get(shipping_user=request.user)
         # This won't crash if the address is missing
        #  shipping_user = ShippingAddress.objects.filter(shipping_user=request.user).first()


         
         shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

         return render (request, "payment/checkout.html",{"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
       
       #checkout as Guestx
       shipping_form = ShippingForm(request.POST or None)

       return render (request, "payment/checkout.html",{"cart_products":cart_products,"quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    



def billing_info(request):
     
    if request.POST:
     # get the cart
       cart = Cart(request)
       cart_products = cart.get_prods
       quantities =   cart.get_quants
       totals = cart.cart_total()

    #    create session with shipping infoxx
       my_shipping =  request.POST
       request.session['my_shipping']= my_shipping
     
         #check whether the user is loged in
       if request.user.is_authenticated:
            #get the billing form
             billing_form = PaymentForm()
             return render (request, "payment/billing_info.html",{"cart_products":cart_products,"quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
       else:
           billing_form = PaymentForm()
           return render (request, "payment/billing_info.html",{"cart_products":cart_products,"quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
             
       shipping_form = request.POST
       return render (request, "payment/billing_info.html",{"cart_products":cart_products,"quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
          messages.success(request, "Access denied")
          return redirect('home')

    