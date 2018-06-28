from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib.auth import views as authviews

from cssocialuser import views

urlpatterns = [
    url(r'^$', views.index, name="cssocialuser_index"),
    url(r'^logout$', authviews.logout, name='cssocialuser_logout'),
    url(r'^login$', authviews.login, name='cssocialuser_user_login'),
    url(r'^accounts/password/$',TemplateView.as_view(template_name='/')),
    url(r'^accounts/$',TemplateView.as_view(template_name='/')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    # url(r'^social/', include('social_django.urls', namespace='social')),
    url(r'^social/', include('social_django.urls', namespace='social')),
    url(r'^edit-profile$', views.edit_profile, name='cssocialuser_edit_profile'),
    url(r'^edit-profile-photo$', views.edit_profile_photo, name='cssocialuser_edit_profile_photo'),
    url(r'^edit-profile-social$', views.edit_profile_social, name='cssocialuser_edit_profile_social'),
    url(r'^edit-profile-pass$', views.password_change, name='cssocialuser_edit_profile_pass'),
    url(r'^edit-profil-pass-done$', views.password_change_done, name='cssocialuser_edit_profile_pass_done'),
]
