from django.conf.urls import url
from django.views.generic import TemplateView

from summer.views import (
    homepage, profile, CitiesSubscriptionsUpdate, DeactivateUserView
)

urlpatterns = [
    url(r'^accounts/profile/$', profile, name='profile'),
    url(r'^accounts/delete/$', DeactivateUserView.as_view(),
        name='deactivate_account'),

    url(r'^subscriptions/$', CitiesSubscriptionsUpdate.as_view(),
        name='subscriptions'),
    url(r'^about/$', TemplateView.as_view(template_name='summer/about.html'),
        name='about'),
    url(r'^robots.txt$', TemplateView.as_view(
        template_name='summer/robots.txt', content_type='text/plain'
    )),

    url(r'^$', homepage, name='homepage'),
]
