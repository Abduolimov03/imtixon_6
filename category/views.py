from django.shortcuts import render, get_object_or_404
from category.models import Category, Product
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import ProductForm
from django.views.generic import  DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Comment, Product







class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'update_product.html'
    success_url = reverse_lazy('product_list')

class ProductDelete(DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('product_list')


def category_list(request):
    query = request.GET.get('q', '')
    if query:
        categories = Category.objects.filter(
            Q(name__icontains=query)
        )
    else:
        categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def product_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    query = request.GET.get('q', '')
    if query:
        products = products.filter(
            brand__icontains = query
        )

    return render(request, 'product_by_category.html', {
        'category': category,
        'products': products
    })

@login_required
def add_comment(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(product=product, user=request.user, text=text)
    return redirect('product_by_category', product.category.id)