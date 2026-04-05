from django.contrib import admin
from .models import Smartphone, Review, Contact,Main_Categoty ,Categoty,Product,Laptop,accessories

admin.site.register(Smartphone)
admin.site.register(accessories)
admin.site.register(Laptop)
admin.site.register(Review)
admin.site.register(Contact)
admin.site.register(Main_Categoty)
admin.site.register(Categoty)

admin.site.register(Product)



