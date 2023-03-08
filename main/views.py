from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Reservations
from .forms import PostForm
from .serializers import PostSerializer
from .utils import TitleMixin

""" 
    Сделать рассылку на почту (телеграм?) оповещение о событии
    Сделать телеграм-бота, с возможностью записи пользователя (DRF)
"""

class MainPageView(TitleMixin, ListView):
    queryset = Post.objects.select_related('category')\
        .values('pk', 'date_time_start', 'date_time_end', 'description', 'category__rank', 'reservation')\
        .filter(on_main=True)\
        .order_by('-date_time_start')[:3]
    template_name = 'base.html'
    context_object_name = 'posts'
    title = 'Волейбол'


class PostListView(TitleMixin, ListView):
    queryset = Post.objects.select_related('category')\
        .values('pk', 'date_time_start', 'date_time_end', 'description', 'category__rank', 'reservation')\
        .filter(
        on_main=True,
        date_time_start__gte=timezone.now()
    )\
        .order_by('-date_time_start')
    template_name = 'post_templates/all_posts.html'
    context_object_name = 'posts'
    title = 'Все публикации'


class PostDetailView(TitleMixin, DetailView):
    model = Post
    template_name = 'post_templates/post_detail.html'
    context_object_name = 'post'
    title = 'Детали'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        players = Reservations.objects.get(post=self.object).players.all()
        string_of_players = ''
        for player in players:
            string_of_players += f'{player}' if player != players.last() else str(player)
        context['players_today'] = string_of_players
        return context


class PostCreateView(TitleMixin, LoginRequiredMixin, CreateView):
    login_url = 'users:login'
    success_url = reverse_lazy('main:all-post')

    form_class = PostForm
    template_name = 'post_templates/new_post.html'
    context_object_name = 'form'
    title = 'Создание публикации'


class SubscribeButtonView(View):
    def post(self, request, *args, **kwargs):
        global reservation

        post_pk = request.POST.get('post_pk')
        print(post_pk)
        username = request.user

        try:
            reservation = Reservations.objects.get(title_id=post_pk)
            if username in reservation.players.all():
                reservation.players.remove(username)
            else:
                reservation.players.add(username)
        except ObjectDoesNotExist:
            reservation = Reservations.objects.create(title_id=post_pk)
            reservation.players.add(username)
        return redirect('main:all-post')



class PostAPIView(APIView):

    def get(self, request):
        posts = Post.objects.all().values()
        serializer_for_queryset = PostSerializer(instance=posts, many=True)
        return Response({'posts': serializer_for_queryset.data})

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_post = Post.objects.create(
            date_time_start=request.data['date_time_start'],
            date_time_end=request.data['date_time_end'],
            description=request.data['description'],
            category_id=request.data['category_id'],
            reservation=request.data['reservation'],
            on_main=request.data['on_main']
        )
        return Response({'post': PostSerializer(new_post).data})
