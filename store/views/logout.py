from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View

class logout(View):
    def get(self, request):
        request.session.clear()
        return redirect('login')