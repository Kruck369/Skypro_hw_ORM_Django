from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from main.forms import ProductForm, VersionForm
from main.models import Product, Version


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продукты'
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'description', 'preview', 'price', 'category')
    success_url = reverse_lazy('products:index')

    def form_valid(self, form):
        form.instance.date_of_creation = timezone.now()
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()
            new_mat.user = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание продукта'
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('products:index')
    login_url = reverse_lazy('users:login')
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.user != self.request.user:
            return HttpResponseForbidden("Вы не можете удалить продукт другого пользователя.")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление продукта'
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    login_url = reverse_lazy('users:login')
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.user != self.request.user:
            return HttpResponseForbidden("Вы не можете удалить продукт другого пользователя.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()
            form.instance.date_of_correction = timezone.now()

        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('products:product', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование продукта'
        SubjectFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = SubjectFormset(instance=self.object)
        return context
