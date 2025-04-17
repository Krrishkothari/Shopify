from django.urls import path
from .views.home import Index
from .views.signup import signup
from .views.login import Login  
from .views.logout import logout
from .views.cart import Cart
from .views.checkout import CheckOut
from .views.orders import OrderView
from .views.search import search
from .middlewares.auth import auth_middleware


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),  
    path('logout/', logout.as_view(), name='logout'),
    path('cart/', Cart.as_view(), name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('search', search, name='search'),
]
