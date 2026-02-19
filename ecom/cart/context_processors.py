from .cart import Cart

# create context-processors so cart can work on  all pages 

def cart(request):
       return {'cart': Cart(request)}