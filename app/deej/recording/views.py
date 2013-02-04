from django.template import Context, loader
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from .ajax import RecordForm


@login_required
def index(request):
    record_form = RecordForm(request.POST or None)
    if request.method == "POST" and record_form.is_valid():
        print("valid")

    return render(request, "recording.index.html", {'record_form': record_form, })
