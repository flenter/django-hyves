from django.db import models
from core.models import PublishItem
from core.fields import CodeField

from social.models import UserAssociation

class ActionCode(PublishItem):
    """An action code
    """
    code = CodeField(max_length=8, unique=True)
    used = models.BooleanField(default = False)
  
    def __unicode__(self):
        return self.code

class Submission(PublishItem):
    """Store a submission
    """
    related_token = models.ForeignKey(UserAssociation, null = True)
    related_code = models.ForeignKey(ActionCode, null = True)
    first_name = models.CharField(max_length = 255)
    preposition = models.CharField(max_length = 255, blank = True, null = True)
    last_name = models.CharField(max_length = 255)
    street = models.CharField(max_length = 255)
    number = models.CharField(max_length = 10)
    zipcode = models.CharField(max_length = 7)
    city = models.CharField(max_length = 255)
    age = models.CharField(max_length = 5)
    comment = models.TextField()
    email = models.EmailField()
    #newsletter = models.NullBooleanField()
    #betray_your_friend = models.CharField(max_length = 255)

    def __unicode__(self):
        return self.first_name + u' ' + self.last_name

class NewsletterSubscriber(PublishItem):
    """Stores each confirmed newsletter subscriber
    """
    related_submission = models.ForeignKey(Submission)
    
