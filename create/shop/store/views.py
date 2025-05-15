from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CustomUser
from .forms import ProductForm, CustomUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        if user:
            login(request, user)
            return redirect('product_list')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products, 'role': request.user.role})

@login_required
def add_product(request):
    if request.user.role == 'manager':
        form = ProductForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, 'add_product.html', {'form': form})
    return redirect('product_list')

@login_required
def edit_product(request, pk):
    if request.user.role in ['manager', 'assistant_manager']:
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST or None, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, 'edit_product.html', {'form': form})
    return redirect('product_list')

@login_required
def delete_product(request, pk):
    if request.user.role in ['manager', 'assistant_manager']:
        product = get_object_or_404(Product, pk=pk)
        product.delete()
    return redirect('product_list')
