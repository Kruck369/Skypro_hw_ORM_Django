import random
import string

from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from django.core.mail import send_mail

from users.forms import UserRegisterForm, UserProfileForm, UserLoginForm
from users.models import User


class UserLoginView(LoginView):
    model = User
    form_class = UserLoginForm


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = "Вы успешно зарегистрировались. Можете войти на сайт!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uid64': uid, 'token': token})
        current_site = get_current_site(self.request)
        send_mail(
            'Потдвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
            'tripicto369@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return redirect('users:email_confirmation_sent')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserConfirmEmailView(View):
    def get(self, request, uid64, token):
        try:
            uid = urlsafe_base64_decode(uid64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


class PasswordResetView(View):
    template_name = 'users/password_reset_form.html'
    success_template_name = 'users/password_reset_success.html'
    failed_template_name = 'users/password_reset_failed.html'

    def generate_and_send_password(self, user_email):
        password_length = 10
        random_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(password_length))

        hashed_password = make_password(random_password)

        user = User.objects.get(email=user_email)
        user.password = hashed_password
        user.save()

        subject = 'Ваш новый пароль'
        message = f'Ваш новый пароль: {random_password}'
        from_email = 'tripicto369@gmail.com'
        recipient_list = [user_email]

        send_mail(subject, message, from_email, recipient_list)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user_email = request.POST.get('email')
        if User.objects.filter(email=user_email).exists():
            self.generate_and_send_password(user_email)
            return render(request, self.success_template_name)
        else:
            return render(request, self.failed_template_name)


