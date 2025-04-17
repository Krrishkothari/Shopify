from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View
import re

class signup(View):
    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Store user input in case validation fails
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            password=password
        )

        error_message = self.validateCustomer(customer)

        if error_message:
            return render(request, 'signup.html', {'error': error_message, 'values': value})

        # Hash password before saving
        customer.password = make_password(password)
        customer.save()

        return redirect('index')

    # Function to validate customer data using regular expressions
    def validateCustomer(self, customer):
        # Regular expression patterns
        name_pattern = r'^[A-Za-z]{4,}$'  # At least 4 alphabetic characters
        phone_pattern = r'^\d{10,}$'  # At least 10 digits
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # Standard email format
        
        # Enhanced password validation patterns
        password_length_pattern = r'.{8,}'  # At least 8 characters
        password_uppercase_pattern = r'[A-Z]'  # At least one uppercase letter
        password_digit_pattern = r'[0-9]'  # At least one digit
        password_special_pattern = r'[!@#$%^&*(),.?":{}|<>]'  # At least one special character
        
        if not customer.first_name:
            return 'First name is required'
        elif not re.match(name_pattern, customer.first_name):
            return 'First name must be at least 4 alphabetic characters'
        
        if not customer.last_name:
            return 'Last name is required'
        elif not re.match(name_pattern, customer.last_name):
            return 'Last name must be at least 4 alphabetic characters'
        
        if not customer.phone:
            return 'Phone number is required'
        elif not re.match(phone_pattern, customer.phone):
            return 'Phone number must be at least 10 digits'
        
        if not customer.email:
            return 'Email is required'
        elif not re.match(email_pattern, customer.email):
            return 'Please enter a valid email address'
        
        if not customer.password:
            return 'Password is required'
        elif not re.search(password_length_pattern, customer.password):
            return 'Password must be at least 8 characters long'
        elif not re.search(password_uppercase_pattern, customer.password):
            return 'Password must contain at least one uppercase letter'
        elif not re.search(password_digit_pattern, customer.password):
            return 'Password must contain at least one digit'
        elif not re.search(password_special_pattern, customer.password):
            return 'Password must contain at least one special character (!@#$%^&*(),.?":{}|<>)'
        
        # Check if email already exists in database
        if Customer.objects.filter(email=customer.email).exists():
            return 'Email already exists'
        
        return None