from django import forms
from django.contrib.auth.models import User
from cssocialprofile.models import CSSocialProfile
from django.utils.translation import ugettext as _

class ProfileForm(forms.ModelForm):

    class Meta:
        model = CSSocialProfile
        fields = ('fullname','bio',)
        
class ProfilePhotoForm(forms.Form):
    """ """
    avatarpic  = forms.ImageField(label=_('Your picture'),help_text=_('Please upload a picture of you. Supported formats: jpg, png, gif.'))
    
    def clean_argazkia(self):
        """ """
        avatarpic = self.cleaned_data['avatarpic']
        name = avatarpic.name
        try:
            name.encode('ascii')
        except:
            raise forms.ValidationError(_('The name of the picture (%s) has an unsupported character. Please rename it before uploading.') % name)            

        format = name.split('.')[-1]
        if format.lower().strip()==u'bmp':
            raise forms.ValidationError(_("The picture is not in one of our supported formats. We don't support BMP files. Please change it"))      
         