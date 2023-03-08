from .models import Reservations


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        if self.title:
            context['title'] = self.title
        return context