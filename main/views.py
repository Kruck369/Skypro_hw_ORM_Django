from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from main.models import Product


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продукты'
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object




class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'description', 'preview', 'price')
    success_url = reverse_lazy('products:index')

    def form_valid(self, form):
        form.instance.date_of_creation = timezone.now()
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание продукта'
        return context


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление продукта'
        return context


class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name', 'description', 'preview', 'price', 'is_published')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()
            form.instance.date_of_correction = timezone.now()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('products:product', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование продукта'
        return context
