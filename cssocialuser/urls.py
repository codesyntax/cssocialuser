from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.views import password_reset

from django.core.urlresolvers import reverse
from cssocialuser import views
from django.contrib.auth import views as authviews

# default view for our index
urlpatterns = [
    url(r'^$', views.index, name="cssocialuser_index"),
]

# register and social urls
urlpatterns += [
    url(r'^logout$', authviews.logout, name='cssocialuser_logout'),
    url(r'^login$', authviews.login, name='cssocialuser_user_login'),

    url(r'^accounts/password/$',TemplateView.as_view(template_name='/')),
    url(r'^accounts/$',TemplateView.as_view(template_name='/')),

    url(r'^accounts/', include('registration.urls')),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
]

# default profile edit urls
urlpatterns += [
    url(r'^edit-profile$', views.edit_profile, name='cssocialuser_edit_profile'),
    url(r'^edit-profile-photo$', views.edit_profile_photo, name='cssocialuser_edit_profile_photo'),
    url(r'^edit-profile-social$', views.edit_profile_social, name='cssocialuser_edit_profile_social'),

    url(r'^edit-profile-pass$', views.password_change, name='cssocialuser_edit_profile_pass'),
    url(r'^edit-profil-pass-done$', views.password_change_done, name='cssocialuser_edit_profile_pass_done'),
]


