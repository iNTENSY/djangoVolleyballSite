from django.views.generic import ListView, TemplateView

from .models import Teams


class TeamsListView(ListView):
    queryset = Teams.objects.select_related('players') \
        .values('name', 'score', 'players__username', 'image').order_by('-score')
    template_name = 'teams_templates/teams_rating.html'
    context_object_name = 'rating_list'