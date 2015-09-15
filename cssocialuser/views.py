# -*- encoding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_list_or_404

from django.contrib.contenttypes.models import ContentType
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import PasswordChangeForm
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from photologue.models import Photo
from cssocialuser.forms import ProfileForm, ProfilePhotoForm
from cssocialuser.utils.slug import time_slug_string
from django.utils.translation import ugettext as _

def index(request):
    """ """
    h = {}
    return render_to_response('cssocialuser/base.html', h, context_instance=RequestContext(request))



@login_required
def edit_profile(request):
    """ """
    tab = 'personal'
    user= request.user
    profile = user
    if request.method == 'POST':
         posta=request.POST.copy()
         profileform = ProfileForm(posta, instance=profile)
         if profileform.is_valid():
            profileform.save()
            messages.add_message(request, messages.SUCCESS, _('New user data saved.'), fail_silently=True)
            return HttpResponseRedirect(reverse('cssocialuser_edit_profile'))
    else:
        profileform = ProfileForm(instance=profile)

    return render_to_response('profile/edit_personal.html', locals(), context_instance=RequestContext(request))


def handle_uploaded_file(f,title):
    """ """
    photo = Photo()
    photo.title = u'%s %s' % (title, time_slug_string())
    photo.slug = time_slug_string()
    photo.image = f
    photo.save()
    return photo


@login_required
def edit_profile_photo(request):
    """ """
    tab = 'photo'
    user = request.user
    profile = user
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = handle_uploaded_file(request.FILES['avatarpic'], profile.get_fullname())
            profile.photo = photo
            profile.save()

    else:
        form = ProfilePhotoForm()
    return render_to_response('profile/edit_photo.html', locals(), context_instance=RequestContext(request))


@login_required
def edit_profile_social(request):
    """ """
    tab = 'social'
    user = request.user
    profile = user
    return render_to_response('profile/edit_social.html', locals(), context_instance=RequestContext(request))

def update_session_auth_hash(request, user):
    """
    Updating a user's password logs out all sessions for the user if
    django.contrib.auth.middleware.SessionAuthenticationMiddleware is enabled.
    This function takes the current request and the updated user object from
    which the new session hash will be derived and updates the session hash
    appropriately to prevent a password change from logging out the session
    from which the password was changed.
    """
    if hasattr(user, 'get_session_auth_hash') and request.user == user:
        request.session[HASH_SESSION_KEY] = user.get_session_auth_hash()

@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='profile/edit_pass.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('cssocialuser_edit_profile_pass_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
        'tab': 'pass',
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

@login_required
def password_change_done(request,
                         template_name='profile/edit_pass_done.html',
                         current_app=None, extra_context=None):
    context = {
        'title': _('Password change successful'),
        'tab': 'pass',
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
