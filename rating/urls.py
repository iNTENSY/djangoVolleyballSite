from django.urls import path
from django.views.decorators.cache import cache_page


from rating import views

app_name = 'rating'

urlpatterns = [
    path('', cache_page(60*60)(views.TeamsListView.as_view()), name='teamlist'),
]