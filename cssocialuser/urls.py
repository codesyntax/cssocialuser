from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.views import password_reset

from django.core.urlresolvers import reverse

#default view for our index
urlpatterns = patterns('cssocialprofile.views',
    url(r'^$','index', name="cssocialprofile_index"),
    )

#register and social urls
urlpatterns += patterns('',
    url(r'^logout$','django.contrib.auth.views.logout', name='cssocialprofile_logout'),
    url(r'^login$','django.contrib.auth.views.login', name='cssocialprofile_user_login'),

    url(r'^accounts/password/$',TemplateView.as_view(template_name='/')),
    url(r'^accounts/$',TemplateView.as_view(template_name='/')),
        
    (r'^accounts/', include('registration.urls')),
    (r'^social/', include('social_auth.urls')),
)

#default profile edit urls
urlpatterns += patterns('cssocialprofile.views',
    url(r'^edit-profile$','edit_profile', name='cssocialprofile_edit_profile'),
    url(r'^edit-profile-photo$','edit_profile_photo', name='cssocialprofile_edit_profile_photo'),    
    url(r'^edit-profile-social$','edit_profile_social', name='cssocialprofile_edit_profile_social'),    
)


"""
    url(r'^sarea','uztarria.profile.views.profile_edit_social', {'tab':'social'},name='erabiltzailea_perfila_edit_social'),
    url(r'^argazkia','uztarria.profile.views.profile_edit_photo', {'tab':'photo'}, name='erabiltzailea_perfila_edit_photo'),
    url(r'^pasahitza','uztarria.profile.views.profile_edit', {'tab':'password'}, name='erabiltzailea_perfila_edit_password'),
    url(r'^mota','uztarria.profile.views.profile_edit_type', {'tab':'type'}, name='erabiltzailea_perfila_edit_type'),    
    url(r'^','uztarria.profile.views.profile_edit', {'tab':'personal'}, name='erabiltzailea_perfila_edit'),
"""  
