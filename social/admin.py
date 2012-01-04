from django.contrib import admin
from django.contrib.admin import ModelAdmin

from social.models import UserAssociation, ProfileInformation


class UserAssociationAdmin(ModelAdmin):
    list_display = ('userid', 'user', 'expires')

admin.site.register(UserAssociation, UserAssociationAdmin)
admin.site.register(ProfileInformation)
