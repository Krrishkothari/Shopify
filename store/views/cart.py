from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from store.models.product import Product

class Cart(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # You can initialize any class-level attributes here if needed

    def get(self, request):
        try:
            # Initialize cart in session if it doesn't exist
            if 'cart' not in request.session:
                request.session['cart'] = {}
            
            cart = request.session.get('cart', {})
            ids = list(cart.keys())
            
            # Safeguard: If cart is empty, return empty list
            products = Product.get_product_by_id(ids) if ids else []
            
            return render(request, 'cart.html', {'products': products})
        except KeyError as e:
            # Handle if there's an issue accessing the session dictionary
            return HttpResponse(f"Session error: {str(e)}", status=400)
        except Exception as e:
            # General exception handling for any other unexpected errors
            return HttpResponse(f"An error occurred: {str(e)}", status=500)