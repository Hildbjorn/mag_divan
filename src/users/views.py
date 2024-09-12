from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView, ListView

from core.utils import Communications
from users.forms import ProfileCreationForm, ProfileUpdateForm
from users.models import Profile

from users.token import account_activation_token

__all__ = (
    'SignUpView',
    'CustomLoginView',
    'CustomLogoutView',
    'ProfileUpdateView',
    'ProfileDeleteView',
    'AllUsersView',
    'profile_activate',
    'email_confirm_done'
)


class SignUpView(SuccessMessageMixin, CreateView):
    """
    Класс регистрации нового пользователя
    """
    form_class = ProfileCreationForm
    template_name = 'registration/signup.html'

    # success_message = "Регистрация прошла успешно."

    def get_success_url(self):
        return reverse("email_confirm_done")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        email = user.email
        user.save()
        # получаем адрес нашего сайта
        current_site = get_current_site(self.request)
        html_message = loader.render_to_string(
            'users/email_confirm_mail.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
        )
        subject = "Подтверждение E-mail"

        communications = Communications(subject=subject,
                                        html_message=html_message,
                                        html_message_to_team=None,
                                        email=email)
        communications.email_to_customer()
        return super().form_valid(form)


def email_confirm_done(request):
    """
    Функция просмотра страницы об успешной отправке e-mail с подтверждением
    """
    return render(request, 'users/email_confirm_done.html')


def profile_activate(request, uidb64, token):
    """
    Функция активации пользователя после подтверждения e-mail
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Profile.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        e_mail = user.email
        user_count = Profile.objects.all().count()
        user.save()
        # Отправка сообщения в Telegram
        massage = "На сайте " + request.get_host() + " \nзарегистрирован новый пользователь." + "\n" + \
                  "..................................................." + "\n" + "\n" + \
                  "<b>e-mail:</b> " + "\n" + str(e_mail) + "\n" + "\n" + \
                  "..................................................." + "\n" + \
                  "Всего пользователей: " + "<b>" + str(user_count) + "</b>"
        communications = Communications(t_massage=massage)
        communications.telegram_to_team()
        # **********************************************************************
        return render(request, 'users/email_confirm_complete.html')
    else:
        return render(request, 'users/email_confirm_denied.html')


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Класс обновления данных пользователя
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')
    success_message = "Данные успешно обновлены."

    def get_object(self, **kwargs):
        return get_object_or_404(Profile, id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.get_object()
        return context

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.save()
        return super().form_valid(form)


class CustomLoginView(LoginView):
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and 'logout' in next_url:
            return self.get_redirect_url() or self.get_default_redirect_url()
        return super().get_success_url()


class CustomLogoutView(LogoutView):
    def get_default_redirect_url(self):
        return reverse('home')


class ProfileDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Profile
    success_url = reverse_lazy('home')
    success_message = 'Профиль пользователя удален'

    def get_template_names(self, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            template_name = 'registration/superuser_delete_denied.html'
        else:
            template_name = 'users/profile_delete.html'
        return template_name

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class AllUsersView(LoginRequiredMixin, ListView):
    """
    Класс просмотра информации обо всех пользователях.
    Внимание! Просмотр доступен только Суперпользователям.
    """
    model = Profile

    def get_template_names(self, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            template_name = 'users/all_users.html'
        else:
            template_name = 'access_denied.html'
        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_users"] = Profile.objects.all()
        return context
