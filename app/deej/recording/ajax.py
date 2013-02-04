from django import forms
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.conf import settings

from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
import requests


class RecordForm(forms.Form):
    track = forms.CharField(max_length=254, label="Track Name")


@login_required
@dajaxice_register
def start(request, form):
    form = RecordForm(form)
    if form.is_valid():
        r = requests.post(settings.SOUNDKICK_URL, params={'command': "record",
                                                          'track': form.cleaned_data["track"],
                                                          'artist': request.user.username, })
        return r.text
    else:
        return None


@login_required
@dajaxice_register
def stop(request):
    r = requests.post(settings.SOUNDKICK_URL, params={'command': "stop", })
    return r.text


@login_required
@dajaxice_register
def status(request):
    r = requests.get(settings.SOUNDKICK_URL)
    return r.text
