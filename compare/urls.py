from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('phones/', views.phone_compare, name='phone_compare'),
    path('Laptops/', views.Laptop_compare, name='Laptop_compare'),
    path('Accessories/', views.Accessories_compare, name='Accessories_compare'),
    path('reviews/', views.reviews, name='reviews'),
    path('contact/', views.contact, name='contact'),

    # Account URLs
    path('account/my-account', views.MY_ACCOUNT, name='my_account'),
    path('account/register', views.REGISTER, name='handleregister'),
    path('account/login', views.LOGIN, name='handlelogin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('account/profile', views.PROFILE, name='profile'),
    path('account/profile/update', views.PROFILE_UPDATE, name='profile_update'),
    path('logout/', views.HandleLogout, name='logout'),
    path('logregister', views.logregister, name='logregister'),

    # Product URLs
    path('product/<slug:slug>', views.PRODUCT_DETAILS, name='product_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Category URLs
    path('catproduct', views.catproduct, name='catproduct'),
    path('category/<str:category_name>/', views.category_page, name='category_page'),

    # **Subcategory URL (fixes your NoReverseMatch)**
    path('subcategory/<int:category_id>/', views.category_products_view, name='subcategory_page'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<str:item_type>/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('search/', views.search, name='search'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
