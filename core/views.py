from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, Category
from products.forms import ProductForm, CategoryForm


def home(request):
    category_id = request.GET.get('category')

    if category_id:
        products = Product.objects.filter(category_id=category_id).order_by('-id')
    else:
        products = Product.objects.all().order_by('-id')

    categories = Category.objects.all().order_by('name')

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    context = {
        'products': products,
        'categories': categories,
        'active_category': category_id,
        'cart_count': cart_count,
    }

    return render(request, 'core/home.html', context)


def dashboard(request):
    categories = Category.objects.all().order_by('name')
    product_count = Product.objects.count()
    category_count = Category.objects.count()

    context = {
        'categories': categories,
        'product_count': product_count,
        'category_count': category_count,
    }

    return render(request, 'core/dashboard.html', context)


def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm()

    return render(request, 'core/product_form.html', {
        'form': form,
        'title': "Mahsulot qo'shish",
        'button_text': "Saqlash"
    })


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'core/product_form.html', {
        'form': form,
        'title': "Mahsulotni tahrirlash",
        'button_text': "Yangilash"
    })


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('dashboard')

    return render(request, 'core/product_delete.html', {
        'product': product
    })


def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CategoryForm()

    return render(request, 'core/category_form.html', {
        'form': form,
        'title': "Bo'lim qo'shish",
        'button_text': "Saqlash"
    })


def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'core/category_form.html', {
        'form': form,
        'title': "Bo'limni tahrirlash",
        'button_text': "Yangilash"
    })


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('dashboard')

    return render(request, 'core/category_delete.html', {
        'category': category
    })


def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    quantity = request.GET.get('quantity', 1)

    try:
        quantity = int(quantity)
    except ValueError:
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart = request.session.get('cart', {})
    product_id = str(product.id)

    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    cart_count = sum(cart.values())

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        item_total = product.price * quantity
        total_price += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count,
    }

    return render(request, 'core/cart.html', context)


def cart_remove(request, pk):
    cart = request.session.get('cart', {})
    product_id = str(pk)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_clear(request):
    request.session['cart'] = {}
    return redirect('cart_detail')
