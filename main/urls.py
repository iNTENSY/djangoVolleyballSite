from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='page'),
    path('new-post/', views.PostCreateView.as_view(), name='new-post'),
    path('all-posts/', views.PostListView.as_view(), name='all-post'),
    path('all-posts/<int:pk>', views.PostDetailView.as_view(),  name='post-detail'),
    path('add/', views.SubscribeButtonView.as_view(), name='subscribe'),
    path('api/v1/postlist', views.PostAPIView.as_view()),
]