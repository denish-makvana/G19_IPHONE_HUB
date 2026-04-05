from django.db import models
from django.utils.text import slugify
from django.contrib import admin
from django.contrib.auth.models import User



class Main_Categoty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Categoty(models.Model):
    main_categoty = models.ForeignKey(Main_Categoty, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name + ' -- ' + self.main_categoty.name

class Smartphone(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='phones/')


    amazon_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    flipkart_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    croma_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amazon_link = models.URLField(null=True, blank=True)
    flipkart_link = models.URLField(null=True, blank=True)
    croma_link = models.URLField(null=True, blank=True)
    category = models.ForeignKey('Categoty', on_delete=models.CASCADE, related_name='products',null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)



class Laptop(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='phones/')


    amazon_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    flipkart_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    croma_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amazon_link = models.URLField(null=True, blank=True)
    flipkart_link = models.URLField(null=True, blank=True)
    croma_link = models.URLField(null=True, blank=True)
    category = models.ForeignKey('Categoty', on_delete=models.CASCADE, related_name='Laptop',null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)


class accessories(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='phones/')


    amazon_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    flipkart_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    croma_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amazon_link = models.URLField(null=True, blank=True)
    flipkart_link = models.URLField(null=True, blank=True)
    croma_link = models.URLField(null=True, blank=True)
    category = models.ForeignKey('Categoty', on_delete=models.CASCADE, related_name='accessories',null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

class Review(models.Model):
    name = models.CharField(max_length=100)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject=models.CharField(null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



# models.py
CATEGORY_CHOICES = [
    ('phone', 'Phone'),
    ('laptop', 'Laptop'),
    ('accessory', 'Accessory'),
]

class Product(models.Model):
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="products/")

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    smartphone = models.ForeignKey(Smartphone, on_delete=models.CASCADE, null=True, blank=True)
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE, null=True, blank=True)
    accessory = models.ForeignKey(accessories, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.smartphone:
            return f"{self.user.username} - {self.smartphone.name}"
        elif self.laptop:
            return f"{self.user.username} - {self.laptop.name}"
        elif self.accessory:
            return f"{self.user.username} - {self.accessory.name}"
        elif self.product:
            return f"{self.user.username} - {self.product.name}"
        return f"{self.user.username} - Wishlist Item"
