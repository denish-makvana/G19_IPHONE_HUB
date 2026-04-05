from django.shortcuts import redirect, render, get_object_or_404
from .models import Smartphone, Review, Contact, Main_Categoty, Categoty,Product,Laptop,accessories,Wishlist
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q  # Import for searching multiple fields



# ------------------------ HOME PAGE ------------------------
def home(request):
    # --- Phones ---
    phones = Smartphone.objects.all()
    for phone in phones:
        prices = {
            'amazon': (phone.amazon_price, phone.amazon_link),
            'flipkart': (phone.flipkart_price, phone.flipkart_link),
            'croma': (phone.croma_price, phone.croma_link),
        }
        best_site = min(prices, key=lambda x: prices[x][0])
        phone.best_buy_link = prices[best_site][1]

    # --- Laptops ---
    laptops = Laptop.objects.all()
    for laptop in laptops:
        prices = {
            'amazon': (laptop.amazon_price, laptop.amazon_link),
            'flipkart': (laptop.flipkart_price, laptop.flipkart_link),
            'croma': (laptop.croma_price, laptop.croma_link),
        }
        best_site = min(prices, key=lambda x: prices[x][0])
        laptop.best_buy_link = prices[best_site][1]

    # --- Accessories ---
    accessory_items = accessories.objects.all()  # renamed variable to avoid conflict
    for accessory in accessory_items:
        prices = {
            'amazon': (accessory.amazon_price, accessory.amazon_link),
            'flipkart': (accessory.flipkart_price, accessory.flipkart_link),
            'croma': (accessory.croma_price, accessory.croma_link),
        }
        best_site = min(prices, key=lambda x: prices[x][0])
        accessory.best_buy_link = prices[best_site][1]

    context = {
        'phones': phones,
        'laptops': laptops,
        'accessories': accessory_items,
        'main_category': Main_Categoty.objects.all(),
    }
    return render(request, 'compare/home.html', context)


# ------------------------ ABOUT PAGE ------------------------
def about(request):
    return render(request, 'compare/about.html')


# ------------------------ PHONE COMPARISON ------------------------
def phone_compare(request):
    # Fetch all smartphones first
    phones = Smartphone.objects.all()
    main_category = Main_Categoty.objects.all()

    # --- Price filtering ---
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        phones = phones.filter(amazon_price__gte=price_min)  # assuming amazon_price as main
    if price_max:
        phones = phones.filter(amazon_price__lte=price_max)

    # --- Best buy link calculation ---
    for phone in phones:
        prices = {
            'amazon': (phone.amazon_price, phone.amazon_link),
            'flipkart': (phone.flipkart_price, phone.flipkart_link),
            'croma': (phone.croma_price, phone.croma_link),
        }
        best_site = min(prices, key=lambda x: prices[x][0])
        phone.best_buy_link = prices[best_site][1]

    paginator = Paginator(phones, 4)  # 12 items per page
    page_number = request.GET.get('page')
    serviceDataFinal = paginator.get_page(page_number)
    context = {
        'phones': phones,
        'main_category': main_category,
        'serviceDataFinal': serviceDataFinal,
    }
    return render(request, 'compare/phones.html', context)


#-----------------------------laptopcompare---------------

def Laptop_compare(request):
    # Fetch all laptops first
    laptops = Laptop.objects.all()
    main_category = Main_Categoty.objects.all()

    # --- Price filtering ---
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        laptops = laptops.filter(amazon_price__gte=price_min)  # Assuming amazon_price is the main price
    if price_max:
        laptops = laptops.filter(amazon_price__lte=price_max)

    # --- Best buy link calculation ---
    for laptop in laptops:
        prices = {
            'amazon': (laptop.amazon_price, laptop.amazon_link),
            'flipkart': (laptop.flipkart_price, laptop.flipkart_link),
            'croma': (laptop.croma_price, laptop.croma_link),
        }
        best_site = min(prices, key=lambda x: prices[x][0])
        laptop.best_buy_link = prices[best_site][1]
        paginator = Paginator(laptops, 4)  # 12 items per page
        page_number = request.GET.get('page')
        DataFinal = paginator.get_page(page_number)
    context = {
        'laptops': laptops,
        'main_category': main_category,
        'DataFinal':DataFinal,
    }
    return render(request, 'compare/laptops.html', context)



#-----------------------Assesoris------------------------
def Accessories_compare(request):
    # Fetch all accessories
    items = accessories.objects.all()
    main_category = Main_Categoty.objects.all()

    # --- Price filtering ---
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        items = items.filter(amazon_price__gte=price_min)  # assuming amazon_price as main price
    if price_max:
        items = items.filter(amazon_price__lte=price_max)

    # --- Best buy link calculation ---
    for item in items:
        prices = {
            'amazon': (item.amazon_price, item.amazon_link),
            'flipkart': (item.flipkart_price, item.flipkart_link),
            'croma': (item.croma_price, item.croma_link),
        }
        best_site = min(prices, key=lambda x: prices[x][0])
        item.best_buy_link = prices[best_site][1]
        paginator = Paginator(items, 4)  # 12 items per page
        page_number = request.GET.get('page')
        datas = paginator.get_page(page_number)
    context = {
        'items': items,  # keeping 'phones' key for template consistency
        'main_category': main_category,
        'datas':datas,
    }
    return render(request, 'compare/Accessories.html', context)




# ------------------------ REVIEWS ------------------------
def reviews(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'compare/reviews.html', {'reviews': reviews})


# ------------------------ CONTACT ------------------------
def contact(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        name = request.POST.get('name')

        Contact.objects.create(
            email=email,
            subject=subject,
            message=message,
            name=name
        )
        messages.success(request, "Message sent successfully!")
        return redirect('home')

    return render(request, 'compare/contact.html')


# ------------------------ ACCOUNT PAGES ------------------------
def MY_ACCOUNT(request):
    return render(request, 'account/my_account.html')

def logregister(request):
    return render(request, 'registration/Register.html')


# ------------------------ REGISTER ------------------------
def REGISTER(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('login')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('login')

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.success(request, 'Account created successfully!')
        return redirect('login')

    return redirect('login')


# ------------------------ PROFILE ------------------------
@login_required(login_url='/accounts/login/')
def PROFILE(request):
    return render(request, 'profile/profile.html')


@login_required(login_url='/accounts/login/')
def PROFILE_UPDATE(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        if password:
            user.set_password(password)
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return redirect('profile')


# ------------------------ LOGOUT ------------------------
def HandleLogout(request):
    logout(request)
    return redirect('home')


# ------------------------ LOGIN ------------------------
def LOGIN(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')

    return render(request, 'registration/login.html')


# ------------------------ PRODUCT DETAILS ------------------------
def PRODUCT_DETAILS(request, slug):
    product = get_object_or_404(Smartphone, slug=slug)
    context = {'product': product}
    return render(request, 'product/product_detail.html', context)


# ------------------------ ALL PRODUCTS ------------------------
def catproduct(request):
    products = Smartphone.objects.all()
    phones = Smartphone.objects.all()

    for phone in phones:
        prices = {
            'amazon': (phone.amazon_price, phone.amazon_link),
            'flipkart': (phone.flipkart_price, phone.flipkart_link),
            'croma': (phone.croma_price, phone.croma_link),
        }
        # Best price link
        best_site = min(prices, key=lambda x: prices[x][0])
        phone.best_buy_link = prices[best_site][1]




    main_category = Main_Categoty.objects.all()
    return render(request, 'Main/catproducts.html', {
        'products': products,

        'phones': phones,
        'main_category': Main_Categoty.objects.all(),
    })


# ------------------------ CATEGORY-WISE PRODUCTS ------------------------
def category_products_view(request, category_id):
    selected_category = get_object_or_404(Categoty, id=category_id)

    # Fetch products only from selected category
    products = Smartphone.objects.filter(category=selected_category)

    if not products.exists():
        messages.warning(request, "Is category me koi product available nahi hai!")

    context = {
        'products': products,
        'selected_category': selected_category,
        'main_category': Main_Categoty.objects.all(),
    }
    return render(request, 'compare/catproducts.html', context)




# views.py


def category_page(request, category_name):
    # category_name = 'phone', 'laptop', or 'accessory'
    products = Product.objects.filter(category=category_name)

    # Optional: filter by price or other fields via GET parameters
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    context = {
        'products': products,
        'category_name': category_name,
    }
    return render(request, 'compare/category_page.html', context)


def product_detail(request, product_id):
    # Get single product
    product = get_object_or_404(Product, id=product_id)

    context = {
        'product': product
    }
    return render(request, 'compare/product_detail.html', context)


# ------------------------ WISHLIST ------------------------



@login_required(login_url='/accounts/login/')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items,
        'main_category': Main_Categoty.objects.all(),
    }
    return render(request, 'compare/wishlist.html', context)

@login_required(login_url='/accounts/login/')
def add_to_wishlist(request, item_type, item_id):
    user = request.user

    # Map item_type to model and wishlist field
    item_map = {
        'smartphone': (Smartphone, 'smartphone'),
        'laptop': (Laptop, 'laptop'),
        'accessory': (accessories, 'accessory'),
        'product': (Product, 'product'),
    }

    if item_type not in item_map:
        messages.error(request, "Invalid item type!")
        return redirect('home')

    Model, field_name = item_map[item_type]

    try:
        item = Model.objects.get(id=item_id)
    except Model.DoesNotExist:
        messages.error(request, f"{item_type.capitalize()} not found!")
        return redirect('home')

    # Check if already in wishlist
    filter_kwargs = {'user': user, field_name: item}
    if Wishlist.objects.filter(**filter_kwargs).exists():
        messages.info(request, "Already in wishlist!")
    else:
        Wishlist.objects.create(**filter_kwargs)
        messages.success(request, "Added to wishlist ❤️")

    return redirect('wishlist')




@login_required(login_url='/accounts/login/')
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    wishlist_item.delete()
    messages.success(request, "Item removed from wishlist ❌")
    return redirect('wishlist')




# -------------------- SEARCH --------------------
def search(request):
    query = request.GET.get('q')
    phones = []
    laptops = []
    accs = []

    if query:
        # PHONES
        for phone in Smartphone.objects.filter(name__icontains=query):
            prices = []
            if phone.amazon_price: prices.append(('amazon', phone.amazon_price, phone.amazon_link))
            if phone.flipkart_price: prices.append(('flipkart', phone.flipkart_price, phone.flipkart_link))
            if phone.croma_price: prices.append(('croma', phone.croma_price, phone.croma_link))
            best = min(prices, key=lambda x: x[1]) if prices else None
            phones.append({'obj': phone, 'best_store': best})

        # LAPTOPS
        for laptop in Laptop.objects.filter(name__icontains=query):
            prices = []
            if laptop.amazon_price: prices.append(('amazon', laptop.amazon_price, laptop.amazon_link))
            if laptop.flipkart_price: prices.append(('flipkart', laptop.flipkart_price, laptop.flipkart_link))
            if laptop.croma_price: prices.append(('croma', laptop.croma_price, laptop.croma_link))
            best = min(prices, key=lambda x: x[1]) if prices else None
            laptops.append({'obj': laptop, 'best_store': best})

        # ACCESSORIES
        for acc in accessories.objects.filter(name__icontains=query):
            prices = []
            if acc.amazon_price: prices.append(('amazon', acc.amazon_price, acc.amazon_link))
            if acc.flipkart_price: prices.append(('flipkart', acc.flipkart_price, acc.flipkart_link))
            if acc.croma_price: prices.append(('croma', acc.croma_price, acc.croma_link))
            best = min(prices, key=lambda x: x[1]) if prices else None
            accs.append({'obj': acc, 'best_store': best})

    return render(request, 'compare/search.html',{'query': query, 'phones': phones, 'laptops': laptops, 'accs': accs})
