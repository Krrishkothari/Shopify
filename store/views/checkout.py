from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Product
from store.models.orders import Order

class OrderProcessor:
    @staticmethod
    def create_order(customer_id, product, price, address, phone, quantity):
        """Create and save a single order"""
        order = Order(
            customer=Customer(id=customer_id),
            product=product,
            price=price,
            address=address,
            phone=phone,
            quantity=quantity
        )
        order.save()
        return order

class CartManager:
    @staticmethod
    def process_cart_items(cart, customer_id, address, phone):
        """Process all items in cart and create orders"""
        if not cart:
            return False
            
        products = Product.get_product_by_id(list(cart.keys()))
        
        for product in products:
            quantity = cart.get(str(product.id))
            OrderProcessor.create_order(
                customer_id=customer_id,
                product=product,
                price=product.price,
                address=address,
                phone=phone,
                quantity=quantity
            )
        
        return True

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer_id = request.session.get('customer')
        cart = request.session.get('cart', {})
        
        # Use cart manager to process all items
        CartManager.process_cart_items(
            cart=cart, 
            customer_id=customer_id, 
            address=address, 
            phone=phone
        )
        
        # Clear the cart after checkout
        request.session['cart'] = {}
        
        return redirect('cart')