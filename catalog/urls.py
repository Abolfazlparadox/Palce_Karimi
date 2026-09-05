from django.urls import path
from . import views


app_name = 'catalog'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),
    path('shop/', views.shop_page, name='shop'),
    path('terms-and-faq/', views.terms_faq, name='terms_faq'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('product/<str:slug>/', views.product_detail, name='product_detail'),
    path('category/<str:slug>/', views.category_detail, name='category_products'),
]
