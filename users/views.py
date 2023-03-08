from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views import View
from django.views.generic import CreateView, DetailView, TemplateView

from .forms import UserRegistrationForm, UserAuthenticationForm
from .models import User, EmailVerification
from .tasks import send_email_verification


def logout_user(request):
    logout(request)
    return redirect('main:page')


class RegistrationUserView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'user_templates/registration.html'
    context_object_name = 'form'

    def get_success_url(self):  # Возврат пользователя на страницу, если форма прошла валидацию
        return reverse_lazy('users:login')


class AuthUserView(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'user_templates/login.html'

    def get_success_url(self):
        return reverse_lazy('main:page')


class ProfileUserView(DetailView):
    model = User
    template_name = 'user_templates/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileUserView, self).get_context_data(**kwargs)
        user = User.objects.get(id = self.kwargs['pk'])
        context['player'] = user
        return context


class EmailVerificationView(TemplateView):
    template_name = 'user_templates/emailverification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists():
            user.is_verified = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return redirect('users:profile')


class SendEmailVerificationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        template_name = 'user_templates/sendemail.html'
        user = request.user
        try:
            user_email_verification = EmailVerification.objects.get(user=user)
        except ObjectDoesNotExist:
            user_email_verification = None

        if user.email and not user.is_verified:
            if user_email_verification is not None and user_email_verification.expiration < now():
                user_email_verification.delete()
                send_email_verification.delay(user.id)
                return render(request, template_name, {'answer': 'Сообщение успешно отправлено!'})
            else:
                send_email_verification.delay(user.id)
                return render(request, template_name, {'answer': 'Вам уже было отправлено сообщение!'})
        else:
            return render(request, template_name,
                          {'answer': 'У нас нет Вашей электронной почты или вы уже были верифицированы!'}
                          )
