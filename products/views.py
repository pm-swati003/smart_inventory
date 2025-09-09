from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "price", "stock", "supplier"]

def product_list(request):
    qs = Product.objects.all().order_by("name")
    return render(request, "products/product_list.html", {"products": qs})

def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products:product_list")
    else:
        form = ProductForm()
    return render(request, "products/product_form.html", {"form": form})

def product_edit(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("products:product_list")
    else:
        form = ProductForm(instance=obj)
    return render(request, "products/product_form.html", {"form": form})

def product_delete(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("products:product_list")
    return render(request, "products/product_form.html", {"form": None, "product": obj})
