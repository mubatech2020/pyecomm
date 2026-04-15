from django.shortcuts import render ,redirect
from .models import Product,Category,Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django  import forms
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
# call this to have multiple search inputs
from django.db.models import Q
import json
# Import the cart from the cart app and cart.py the whole cart class
from cart.cart import Cart
from cart.views import cart_summary

def search(request):
     
      #determine if they filled the form
    if request.method == 'POST':
        searched = request.POST['searched']
  #query the products model to get products for db
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
             messages.success(request, "That  Product does not exist Please Try again")
             return render(request, 'search.html', {})
        else:


         return render(request, 'search.html', {'searched':searched})
        

       
        
    else: 

        return render(request, 'search.html', {})
  

def update_info(request):
      if request.user.is_authenticated:
        #   current_user = User.objects.get(id=request.user.id) 

        # making sure user profile is matched the profileid

 # Get current user
       
          current_user = Profile.objects.get(user__id=request.user.id) 

           # Get current user shipping  userinformation
          shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
          # we are either posting the user form  or none or  the current login user
          form = UserInfoForm(request.POST or None, instance=current_user)


        # Get current user shipping  form
          shipping_form =ShippingForm(request.POST or None, instance=shipping_user)

          #get shipping form

          if form.is_valid() or shipping_form.is_valid():
            #    Saving user form
              form.save()
            #   Saving shipping form
              shipping_form.save()
            
              messages.success(request, "Your Info Has Been Updated Sucessfully")
              return redirect('home')
          return render(request, 'update_info.html', {'form':form , 'shipping_form':shipping_form})
      else:
          messages.error(request, "You Must Be logged In")
          return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
       # Did they fill out the form

        if request.method  == 'POST':
             form = ChangePasswordForm(current_user, request.POST)
             if form.is_valid():
                form.save()
                messages.success(request, "password changed successfully")
                return redirect('login')
                #   if you want to autimatically login after changing paasword do this
                #      login(request, current_user) 
                #      return redirect('update_user')
             else:
                 for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form':form})
    else:
         messages.error(request, "You Must Be logged In")
       
def update_user(request):
      if request.user.is_authenticated:
          current_user = User.objects.get(id=request.user.id) 
          # we are either posting the user form  or none or  the current login user
          user_form = UpdateUserForm(request.POST or None, instance=current_user)
          if user_form.is_valid():
              user_form.save()
              # if the update happen we want to login again  with the updated  details from the user happens in the background
              login(request, current_user)
              messages.success(request, "User Has Been Updated Sucessfully")
              return redirect('home')
          return render(request, 'update_user.html', {'user_form':user_form})
      else:
          messages.error(request, "You Must Be logged In")
          return redirect('home')
      

def category(request,foo):
    
    # replace hyphens with spaces
    foo = foo.replace('-',' ') 

    try:
        category = Category.objects.get(name=foo)   
        products  = Product.objects.filter(Category=category)
        return render(
            request,
            'category.html',
            {'products': products, 'category': category}
        )
    # except: 
    #      messages.success(request,"This category doesn't exist") 
    #      return redirect('home')

    except Category.DoesNotExist:
       messages.error(request, "Category does not exist")
       return redirect('home')


def product(request,pk):
     product= Product.objects.get(id=pk)
     return render(request, 'product.html', {'product':product})
   
def category_summary(request):
    #  grab all the ctegories from the category model
    categories = Category.objects.all()

    return render(
            request,
            'category_summary.html',
            {"categories":categories}
        )

def home(request):
    products= Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
     return render(request,'about.html')

def login_user(request):

    if request.method =="POST" :
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request,user)
          
        #   save the cart so anytime a user login they will see their  saved cart items
        #    get the user profile objects
            current_user = Profile.objects.get(user__id=request.user.id)

            # get the saved parts from database
            saved_cart = current_user.oldcart
            # convert database string back to python dictionary

            if saved_cart:
                # convert to python dictionary using json
                converted_cart = json.loads(saved_cart)
        #add the loaded  cart dictionary to our session
        #get the cart
                cart = Cart(request)
                # loop through the cart and add item from the database

                for key,value in converted_cart.items() :
                    cart.db_add(product=key, quantity=value)


            messages.success(request,'you have logged in successfully')
            return redirect(home)
        else:
            messages.success(request,'wrong username or password entered')
            return redirect(login)            
    else:
      return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('you have logged out'))
    return redirect(home)    

def register_user(request):
     form=SignUpForm()
     if request.method == "POST" :
       form = SignUpForm(request.POST)  
       if form.is_valid():
          form.save() 
          username=form.cleaned_data['username']
          password=form.cleaned_data['password1']
         
         # log in user
          user= authenticate(username=username, password=password)
          login(request,user)
          messages.success(request,'your  username  has been created successfully . Kindly , fill Billing information')
          return redirect(update_info)
       else:
          messages.error(request,'wrong username or password entered')
          return redirect(login)  
     else:
      return render(request,'register.html',{'form':form})



