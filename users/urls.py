from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('', views.logout_user, name='logout'),
    path('registration/', views.RegistrationUserView.as_view(), name='registration'),
    path('login/', views.AuthUserView.as_view(), name='login'),
    path('profile/<int:pk>', views.ProfileUserView.as_view(), name='profile'),
    path('sendemail/<str:email>', views.SendEmailVerificationView.as_view(), name='send-email'),
    path('verify/<str:email>/<uuid:code>', views.EmailVerificationView.as_view(), name='email-verification'),
]