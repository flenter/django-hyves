import datetime

from django.db import models

from django.contrib.auth.models import User

from social.utils import generate_password

class UserAssociationManager(models.Manager):
    """Manager for the UserAssociation model. Makes it easier to create/update an
    object through an oauth access token
    """
    def get_or_create_from_token(self, token):
        
        """A get_or_create method, but gets/creates both a user as well as a
        UserAssociation based on the specified token
        """
        
        db_tokens = self.filter(
            userid = token.userid,
        )


        if len(db_tokens):
            db_token = db_tokens[0]
            created = False
        else:
            db_token = UserAssociation(userid = token.userid)
            created = True
        
        db_token.token = token.key
        db_token.secret = token.secret
        if(token.expiredate):
            db_token.expires = datetime.datetime.fromtimestamp(token.expiredate)
        db_token.methods = token.methods
        
        if not db_token.id:
            while 1:
                user, created = User.objects.get_or_create(username = generate_password(30))
            
                if created:
                    user.is_active = True
 
                    
                    user.set_password(db_token.get_password())
                    user.save()
                    
                    break
        
            db_token.user = user
            
        
        db_token.save()
        return db_token, created

class UserAssociation(models.Model):
    """Store the access token information 
    """
    userid = models.TextField(max_length = 255, null = True)
    user = models.ForeignKey(User, unique = True)
    token = models.TextField(max_length = 255, null = True)
    secret = models.TextField(max_length = 255, null = True)
    expires = models.DateTimeField(null = True)
    methods = models.TextField(max_length = 255, null = True)
    
    def expired(self):
        return datetime.datetime.now() < self.expires
    
    @property
    def key(self):
        return self.token
    
    def get_password(self):
        from django.conf import settings
        return settings.CONSUMER_SECRET + self.userid
    
    def __unicode__(self):
        return self.userid
    
    objects = UserAssociationManager()

from django.contrib.auth.models import User

from django.db.models.signals import post_save

class ProfileInformation(models.Model):
    """Additional profile information.
    
    .. note::
        Hyves only allows you to store id's and such permanently. All
        additional information can be stored for 24 hours or you need to ask
        the user's permission.
    """
    user = models.ForeignKey(User, unique = True)
    #age = models.CharField(max_length = 10, null=True)
    pimp_image = models.FileField(upload_to = 'pimps', blank = True, null=True)
    pimp_type = models.CharField(max_length = 255, blank = True, null=True)
    pimp_name = models.CharField(max_length = 255, blank = True, null=True)
    
    def __unicode__(self):
        return unicode(self.user)

from django.db.utils import DatabaseError
def handle_user_save(sender, instance, **kwargs):
    """
    Create related profile when a user is saved.. (should this not yet exist)
    """
    try:
        profile, created = ProfileInformation.objects.get_or_create(user = instance)
    except DatabaseError:
        
        pass
post_save.connect(handle_user_save, sender = User)

