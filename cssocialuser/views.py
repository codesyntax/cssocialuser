from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_list_or_404

from django.contrib.contenttypes.models import ContentType

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
    photo.title_slug = time_slug_string()
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
        

