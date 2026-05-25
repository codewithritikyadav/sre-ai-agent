from django.shortcuts import render, redirect

from .models import Incident
from .forms import IncidentForm


def dashboard(request):

    incidents = Incident.objects.all().order_by('-created_at')

    form = IncidentForm()

    if request.method == 'POST':

        form = IncidentForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('dashboard')

    return render(
        request,
        'dashboard.html',
        {
            'incidents': incidents,
            'form': form
        }
    )