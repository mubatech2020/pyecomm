from django.shortcuts import render ,redirect
from .models import Product,Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django  import forms
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


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
            messages.success(request,'you have logged in successfully')
            return redirect(home)
        else:
            messages.error(request,'wrong username or password entered')
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
          messages.success(request,'you have registered successfully')
          return redirect(home)
       else:
          messages.error(request,'wrong username or password entered')
          return redirect(login)  
     else:
      return render(request,'register.html',{'form':form})



