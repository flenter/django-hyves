from datetime import datetime
import logging
import sys

from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.core.mail import send_mail
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from generic_confirmation.forms import DeferredForm

from customcore.models import ActionCode, Submission, NewsletterSubscriber
from social.models import ProfileInformation

logger = logging.getLogger()

class CodeValidatingMixin(object):
    """Mixin object containing code validation logic
    """
    def clean_code(self):
        """validate the code
        """

        data = self.cleaned_data['code']

        if not ActionCode.pubjects.filter(
                    code__iexact = data
                ).exclude(
                    used = True
                ).count():
            raise forms.ValidationError(
                _('Code was not found or has already been used')
            )

        return data

class CodeCheckForm(forms.Form, CodeValidatingMixin):
    """Simple form for checking codes
    """
    code = forms.CharField(max_length = 8, min_length = 8)

class NewsletterForm(DeferredForm, ModelForm):
    """Deferred form for confirmed newsletter subscribtions
    """
    class Meta():
        model = NewsletterSubscriber
        fields = ['related_submission']

    def send_notification(
            self,
            sender,
            instance=None,
            user=None,
            *args,
            **kwargs):

        submission = self.cleaned_data['related_submission']

        body = render_to_string(
            'customcore/confirm_email.html',
            {
                'token': instance.token,
                'first_name': submission.first_name,
                'last_name': submission.last_name,
            }
        )

        from django.conf import settings

        subject = settings.CONFIRM_EMAIL_SUBJECT

        send_mail(
            subject,
            body,
            'no-reply@drpepper.nl',
            recipient_list = [self.cleaned_data['related_submission'].email,],
        )

class SubmissionForm(CodeValidatingMixin, ModelForm):
    """Form for the real code information
    """
    code = forms.CharField(max_length = 8, min_length = 8)
    newsletter = forms.NullBooleanField()

    class Meta():
        """Store meta information about this form
        """
        model = Submission
        fields = [
            'code', 'first_name', 'preposition', 'last_name', 'street',
            'number', 'email', 'zipcode', 'city', 'age','newsletter', 'comment',
            'code'
        ]

    @property
    def current_code(self):
        """getter for a current code.

        .. note::
           does_not_exist exception will be raised if a code doesn't exist
        """
        code = self.cleaned_data['code']
        return ActionCode.pubjects.get(code = code)

    def save(self, *args, **kwargs):
        """Store it in the database
        """
        from django.conf import settings

        code = self.current_code
        if (settings.DEBUG and code.code == '__unused'):
            code.used = False
            code.save(*args, **kwargs)
        else:
            code.used = True
            code.save(*args, **kwargs)

        return_value = super(SubmissionForm, self).save(*args, **kwargs)

        # also store the related_code
        self.instance.related_code = code
        self.instance.save(*args, **kwargs)

        if self.cleaned_data['newsletter']:
            form = NewsletterForm({'related_submission':self.instance.id},
            )
            if form.is_valid():
                form.save()
            else:

                logger.error(
                    'Error: a Newsletter form is not valid',
                    exc_info = sys.exc_info(),
                    extra = {
                        'data':{
                            'from_form': self,
                            'submission instance id': self.instance.id,
                            'created form': form
                        }
                    }
                )
        return return_value

class UploadImageForm(forms.Form):
    """Form to hold data for uploading to Hyves (tm)
    """
    title = forms.CharField()
    pimp_image = forms.FileField()

class SelectDateForm(forms.Form):
    """Selecting a range of dates
    """
    start_date = forms.DateField(
        widget = AdminDateWidget,
        required = True,
        initial = datetime.today)

    end_date = forms.DateField(
        widget = AdminDateWidget,
        required = True,
        initial = datetime.today)

    def clean_end_date(self):
        """Validate the dates (end_date should be after start_date)
        """
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']

        if end_date < start_date:
            raise forms.ValidationError(
                _('End date should be after start date')
            )

        return end_date

class PimpProfileForm(forms.ModelForm):

    class Meta:
        model = ProfileInformation
        fields = (
            'pimp_image',
            'pimp_type',
            'pimp_name',
            )
