from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.views import password_reset

from django.core.urlresolvers import reverse

#default view for our index
urlpatterns = patterns('cssocialuser.views',
    url(r'^$','index', name="cssocialuser_index"),
    )

#register and social urls
urlpatterns += patterns('',
    url(r'^logout$','django.contrib.auth.views.logout', name='cssocialuser_logout'),
    url(r'^login$','django.contrib.auth.views.login', name='cssocialuser_user_login'),

    url(r'^accounts/password/$',TemplateView.as_view(template_name='/')),
    url(r'^accounts/$',TemplateView.as_view(template_name='/')),
        
    (r'^accounts/', include('registration.urls')),
    (r'^social/', include('social_auth.urls')),
)

#default profile edit urls
urlpatterns += patterns('cssocialuser.views',
    url(r'^edit-profile$','edit_profile', name='cssocialuser_edit_profile'),
    url(r'^edit-profile-photo$','edit_profile_photo', name='cssocialuser_edit_profile_photo'),    
    url(r'^edit-profile-social$','edit_profile_social', name='cssocialuser_edit_profile_social'),    
)


