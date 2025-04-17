from django.shortcuts import render, redirect
from store.models.product import Product
from store.models.category import Category
from django.views import View
from django.http import HttpResponse

# Base cart handler class
class CartHandler:
    def add_to_cart(self, cart, product_id):
        try:
            if not cart:
                cart = {}
            
            quantity = cart.get(product_id)
            if quantity:
                cart[product_id] = quantity + 1
            else:
                cart[product_id] = 1
            
            return cart
        except Exception as e:
            print(f"Error adding to cart: {str(e)}")
            return cart

    def remove_from_cart(self, cart, product_id):
        try:
            quantity = cart.get(product_id)
            if quantity:
                if quantity <= 1:
                    cart.pop(product_id)
                else:
                    cart[product_id] = quantity - 1
            
            return cart
        except KeyError as e:
            print(f"Error removing from cart - key not found: {str(e)}")
            return cart
        except Exception as e:
            print(f"Error removing from cart: {str(e)}")
            return cart

# Specific cart handler implementations
class StandardCartHandler(CartHandler):
    pass

class Index(View):
    def __init__(self):
        self.cart_handler = StandardCartHandler()
    
    def post(self, request):
        try:
            product_id = request.POST.get('product')
            remove = request.POST.get('remove')
            
            # Initialize cart if not exists
            cart = request.session.get('cart', {})
            
            # Use polymorphic cart handling
            if remove:
                cart = self.cart_handler.remove_from_cart(cart, product_id)
            else:
                cart = self.cart_handler.add_to_cart(cart, product_id)
            
            request.session['cart'] = cart
            print('Cart:', request.session['cart'])
            return redirect('index')
        except KeyError as e:
            print(f"Session KeyError: {str(e)}")
            return HttpResponse("Error processing cart operation", status=400)
        except Exception as e:
            print(f"Unexpected error in POST: {str(e)}")
            return HttpResponse("An unexpected error occurred", status=500)

    def get(self, request):
        try:
            categories = Category.objects.all()  
            category_id = request.GET.get('category')  

            # Filter products based on selected category
            if category_id:
                products = Product.objects.filter(category=category_id)
            else:
                products = Product.objects.all()

            # Debugging: Print session data to console
            print('You are:', request.session.get('email'))

            context = {
                'categories': categories,
                'products': products,
                'selected_category': int(category_id) if category_id else None,  # Highlight selected category
            }

            return render(request, 'index.html', context)
        except ValueError as e:
            print(f"Value error (possibly with category_id conversion): {str(e)}")
            return HttpResponse("Invalid category format", status=400)
        except Exception as e:
            print(f"Unexpected error in GET: {str(e)}")
            return HttpResponse("An unexpected error occurred", status=500)