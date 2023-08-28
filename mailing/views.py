from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.decorators import user_passes_test

from blogpost.models import BlogPost
from mailing.forms import NewsletterForm, MessageForm, ClientForm
from mailing.models import Newsletter, Message, Client


class NewsletterListView(ListView):
    model = Newsletter
    template_name = 'mailing/newsletter/newsletter_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        if is_moderator(self.request.user):
            return queryset

        return queryset.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_mailings = Newsletter.objects.count()
        active_mailings = Newsletter.objects.filter(status=Newsletter.STARTED).count()
        unique_clients = Client.objects.count()
        random_articles = BlogPost.objects.order_by('?')[:3]

        context['title'] = 'Рассылки'
        context['total_mailings'] = total_mailings
        context['active_mailings'] = active_mailings
        context['unique_clients'] = unique_clients
        context['random_articles'] = random_articles
        return context


class NewsletterCreateView(PermissionRequiredMixin, CreateView):
    model = Newsletter
    template_name = 'mailing/newsletter/newsletter_form.html'
    form_class = NewsletterForm
    success_url = reverse_lazy('mailing:index')
    permission_required = 'mailing.can_create_newsletter'

    def form_valid(self, form):
        if form.is_valid():
            new_newsletter = form.save(commit=False)
            new_newsletter.author = self.request.user
            new_newsletter.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание рассылки'
        return context


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    template_name = 'mailing/newsletter/newsletter_form.html'
    form_class = NewsletterForm
    login_url = reverse_lazy('users:login')
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author != self.request.user:
            return HttpResponseForbidden("Вы не можете редактировать рассылку другого пользователя.")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mailing:newsletter', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование рассылки'
        return context


class NewsletterDetailView(DetailView):
    model = Newsletter
    template_name = 'mailing/newsletter/newsletter_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allowed_statuses'] = [Newsletter.CREATED, Newsletter.STARTED]
        return context


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    template_name = 'mailing/newsletter/newsletter_confirm_delete.html'
    success_url = reverse_lazy('mailing:index')
    login_url = reverse_lazy('users:login')
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author != self.request.user:
            return HttpResponseForbidden("Вы не можете удалить рассылку другого пользователя.")

        return super().dispatch(request, *args, **kwargs)


class MessageCreateView(CreateView):
    model = Message
    template_name = 'mailing/message/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        if form.is_valid():
            new_newsletter = form.save(commit=False)
            new_newsletter.author = self.request.user
            new_newsletter.save()

        return super().form_valid(form)


class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message/message_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сообщения'
        return context


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message/message_detail.html'


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message/message_form.html'
    login_url = reverse_lazy('users:login')
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author != self.request.user:
            return HttpResponseForbidden("Вы не можете редактировать сообщение другого пользователя.")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mailing:message_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование сообщения'
        return context


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailing/message/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author != self.request.user:
            return HttpResponseForbidden("Вы не можете удалить сообщение другого пользователя.")

        return super().dispatch(request, *args, **kwargs)


class ClientCreateView(CreateView):
    model = Client
    template_name = 'mailing/client/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client/client_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Клиенты'
        return context


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client/client_detail.html'


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client/client_form.html'
    login_url = reverse_lazy('users:login')
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author != self.request.user:
            return HttpResponseForbidden("Вы не можете редактировать клиентов другого пользователя.")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mailing:client_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование клиента'
        return context


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'mailing/client/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author != self.request.user:
            return HttpResponseForbidden("Вы не можете удалить клиента другого пользователя.")

        return super().dispatch(request, *args, **kwargs)


def is_moderator(user):
    return user.groups.filter(name="Модератор").exists()


@user_passes_test(is_moderator)
@require_POST
def start_newsletter(request, pk):
    if request.user.is_authenticated:
        newsletter = Newsletter.objects.get(pk=pk)
        if newsletter.status == Newsletter.CREATED:
            newsletter.status = Newsletter.STARTED
        elif newsletter.status == Newsletter.STARTED:
            newsletter.status = Newsletter.CREATED
        newsletter.save()
        return JsonResponse({'status': newsletter.get_status_display()})
