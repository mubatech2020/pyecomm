from store.models import Product

class Cart():
     def __init__(self, request):
       self.session = request.session 
     # get sesion key if it exists

       cart =  self.session.get('session_key')

       #  if the user is new no session. create one for the user 
       if 'session_key' not in request.session:
         cart = self.session['session_key'] ={}

        #  this make sure cart is available  on all pages
       self.cart = cart 
# addding to cart
     def add(self, product,quantity):
        product_id = str(product.id)
        product_qty=  str(quantity)

        #check if the product is already added to cart
        if product_id in self.cart:
             pass
        else :
         #   self.cart [product_id] = {'price': str (product.price)}
           self.cart[product_id] = int(product_qty)


        self.session.modified = True


     def __len__(self):
        return len (self.cart)
     
     def get_prods(self):
        
        #get idds from cart
        products_ids = self.cart.keys()
       # use ids to lookup products in database model

        products = Product.objects.filter(id__in=products_ids)  

        return products       
     

     def get_quants(self):
        
        #get idds from cart
        quantities = self.cart
       

        return quantities 
     
     def cart_total(self):
           #get prodduct IDS

          products_ids = self.cart.keys()
          quantities = self.cart
          # use ids to lookup products in database model

          products = Product.objects.filter(id__in=products_ids)

          total=0  
         #   {'thats the id index': thats is the value which is the quantity according to the data coming from our code }
         #  data example {'4':3, '2':4}

          for key, value in quantities.items():
             # convert key string into integer so we can do the maths
             key =int(key)
             for product in products:
                
                if product.id == key:

                   if product.is_sale:
                     total = total + (product.saleprice * value )

                   else:
                    total = total + (product.price * value )
                return total
         

     def update(self,product,quantity):
        

         #  this is how the data  shows  the {'product id': quantity }
         
      #   { '4':3, '5':2}
        
        product_id = str(product)
        product_qty= int(quantity)
        

        #get cart
        ourcart = self.cart

        # Update Dictionary/cart

        ourcart[product_id] = product_qty

        self.session.modified = True

        thing = self.cart 

        return thing 
     
       


     def delete(self,product):

      #  this is how the data  shows  the {'product id': quantity }
         
      #   { '4':3, '5':2}
        
      product_id = str(product)
         
      if product_id in self.cart:
          del self.cart[product_id]

      self.session.modified = True
