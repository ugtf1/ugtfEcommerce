from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Product

def home(request):
    products = Product.objects.filter(is_active=True).order_by("-created_at")[:12]
    categories = Category.objects.all()
    return render(request, "core/home.html", {"products": products, "categories": categories})

def category_list(request):
    categories = Category.objects.all()
    return render(request, "core/category_list.html", {"categories": categories})

def product_list(request):
    products = Product.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "core/product_list.html", {"products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "core/product_detail.html", {"product": product})

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_active=True)
    return render(request, "core/product_list.html", {"products": products, "category": category})

def search(request):
    q = request.GET.get("q", "").strip()
    products = []
    if q:
        products = Product.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(category__name__icontains=q)
        ).filter(is_active=True)
    return render(request, "core/search_results.html", {"query": q, "products": products})