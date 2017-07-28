from django.shortcuts import render
from django.forms.models import modelform_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.forms.widgets import CheckboxSelectMultiple

from . import models, forms


class ModelFormWidgetMixin:
    """Mixin to override the widgets of default forms."""

    def get_form_class(self):
        return modelform_factory(
            self.model, fields=self.fields, widgets=self.widgets
        )


class CitiesSubscriptionsUpdate(ModelFormWidgetMixin, SuccessMessageMixin,
                                LoginRequiredMixin, UpdateView):
    model = models.Profile
    fields = ['cities']
    success_url = reverse_lazy('subscriptions')
    success_message = 'Subscriptions to DST notifications updated'
    widgets = {
        'cities': CheckboxSelectMultiple,
    }
    template_name = 'summer/subscriptions_update.html'

    def get_object(self, queryset=None):
        return self.request.user.profile


def homepage(request):
    if request.user.is_authenticated:
        cities = request.user.profile.cities.all()
        if not cities:
            cities = models.City.objects.all()
    else:
        cities = models.City.objects.all()

    total_cities = models.City.objects.count()

    return render(request, 'dst/homepage.html', context={
        'total_cities': total_cities,
        'cities': cities
    })


@login_required
def profile(request):
    return render(request, 'dst/profile.html')


class DeactivateUserView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'summer/deactivate_user.html'
    form_class = forms.DeactivateUser
    success_url = reverse_lazy('homepage')
    success_message = 'Your account has been deleted'

    def form_valid(self, form):
        self.request.user.is_active = False
        self.request.user.save()
        logout(self.request)
        return super().form_valid(form)
