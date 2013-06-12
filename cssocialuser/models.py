from django.db import models
from django.contrib.auth.models import User
from photologue.models import Photo
from cssocialprofile.utils.load_images import loadUrlImage
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin,UserManager
from django.utils import timezone
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.twitter import TwitterBackend
from social_auth.backends import OpenIDBackend

USERTYPE_CHOICES = getattr(settings,'USERTYPE_CHOICES', ((0,'Erabiltzailea'),(1,'Kidea'),(2,'Nor publikoa'),(3,'Kazetaria'),(4,'Administratzailea')))
AUTH_PROFILE_MODULE = getattr(settings,'AUTH_PROFILE_MODULE', 'cssocialprofile.CSSocialProfile')
SOURCE_CHOICES = ((0,'-'),(1,'Register'),(2,'Twitter'),(3,'Facebook'),(4,'OpenId'),)
DEFAULT_PROFILE_PHOTO = getattr(settings,'DEFAULT_PROFILE_PHOTO', 'anonymous-user')


def get_user_data(backend, details, response, social_user, uid, user, *args, **kwargs):
    if backend.__class__ == FacebookBackend:
        user.facebook_extra_values(response, details, **kwargs)      
    elif backend.__class__ == TwitterBackend:
        user.twitter_extra_values(response, details, **kwargs)
    elif backend.__class__ == OpenIDBackend:
        user.set_openid_extra_values(response, details, **kwargs)
    return True    


class MyUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')

        email = UserManager.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_active=True, is_superuser=False,
                          last_login=now, **extra_fields)
 
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, username, email, password, **extra_fields):
        u = self.create_user(username, email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

   
class CSAbstractSocialUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=254, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    phone = models.CharField(_('Phone Number'), max_length=25, blank=True, null=True,)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)    

    fullname = models.CharField(_('Full name'), max_length=200, blank=True,null=True)
    bio = models.TextField(_('Biography/description'),null=True,blank=True)
    usertype =  models.PositiveSmallIntegerField(choices = USERTYPE_CHOICES, default = 0)
    
    added_source = models.PositiveSmallIntegerField(choices = SOURCE_CHOICES, default = 0)
    photo = models.ForeignKey(Photo,null=True, blank=True)
    
    twitter_id = models.CharField(max_length=100, blank=True,null=True)
    facebook_id = models.CharField(max_length=100, blank=True,null=True)
    openid_id = models.CharField(max_length=100, blank=True,null=True)
    googleplus_id = models.CharField(max_length=100, blank=True,null=True)


    added = models.DateTimeField(auto_now_add=True,editable=False)
    modified =models.DateTimeField(auto_now=True,editable=False)

    #objects = MyUserManager()

    USERNAME_FIELD = 'username'

    def get_facebook_photo(self, response):
        """ """
        import facebook.djangofb as facebook
        import pdb;pdb.set_trace()
        facebook = facebook.Facebook(settings.FACEBOOK_API_KEY, settings.FACEBOOK_API_SECRET)
        uid = response.get('id')
        user_data = facebook.users.getInfo(uid, ['first_name', 'last_name','pic_big',])[0]
        if user_data:   
            img_url = user_data['pic_big']
            img_title = u'Facebook: ' + user_data['first_name'] + u' ' + user_data['last_name']
            return loadUrlImage(img_url,img_title)
        else:
            return None


    def set_facebook_extra_values(self, response, details, **kwargs):
        """ """
        self.facebook_id = response.get('id')

        if self.usertype == 0:
            self.usertype = 1
        
        if self.added_source == 0:
            #First time logging in
            self.added_source = 3
            self.mota = 1
        if not self.photo:
            self.photo = self.get_facebook_photo(response)
        self.username = slugify(user.username)
        self.save()
        return True


    def set_twitter_extra_values(self, response, details, **kwargs):
        """ """
        if not self.photo:
            self.photo = self.get_twitter_photo(response)
        self.twitter_id = response.get('screen_name','')

        if self.usertype == 0:
            self.usertype = 1
        if self.added_source == 0:
            self.added_source = 2

        if not self.bio:
            self.bio = response.get('description','')         

        if not self.fullname:
            self.fullname = response.get('name','')    

        self.save()
        return True

    def get_twitter_photo(self, response):
        """ """
        img_url = response.get('profile_image_url')
        img_url=img_url.replace('_normal.','.')
        username = response.get('screen_name')
        return loadUrlImage(img_url,u'twitter: ' + username)


    def set_openid_extra_values(self, response, details, **kwargs):
        """ """
        if response.status == 'success':
            user.openid_id = response.getDisplayIdentifier()
            if user.added_source == 0:
                user.mota = 1
                user.added_source = 4
        profile.save()
        return True


    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.fullname

    def is_jounalist(self):
        """ """
        return self.usertype==3

    def is_member(self):
        """ """
        return self.usertype==1


    def get_photo(self):
        """ """
        if self.photo:
            return self.photo
        try:
            return Photo.objects.get(title_slug=DEFAULT_PROFILE_PHOTO)
        except:
            return None

    def get_fullname(self):
        """ """
        if self.fullname:
            return self.fullname
        else:
            return u'%s' % (self.get_full_name()) or self.username            

    def __unicode__(self):
        return u'%s' % (self.username)

    class Meta:
        abstract = True

