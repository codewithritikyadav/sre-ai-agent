from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .models import Incident

from .forms import IncidentForm


@login_required
def dashboard(request):

    # Show only logged-in user's incidents
    incidents = Incident.objects.filter(
        user=request.user
    ).order_by('-created_at')

    form = IncidentForm()

    # Create New Incident
    if request.method == 'POST':

        form = IncidentForm(request.POST)

        if form.is_valid():

            incident = form.save(commit=False)

            # Assign current user
            incident.user = request.user

            incident.save()

            return redirect('dashboard')

    # Dashboard Analytics
    total_incidents = incidents.count()

    critical_incidents = incidents.filter(
        severity='Critical'
    ).count()

    high_incidents = incidents.filter(
        severity='High'
    ).count()

    avg_score = 0

    if total_incidents > 0:

        total_score = sum(
            incident.anomaly_score
            for incident in incidents
        )

        avg_score = round(
            total_score / total_incidents,
            2
        )

    context = {

        'incidents': incidents,

        'form': form,

        'total_incidents': total_incidents,

        'critical_incidents': critical_incidents,

        'high_incidents': high_incidents,

        'avg_score': avg_score,
    }

    return render(
        request,
        'dashboard.html',
        context
    )