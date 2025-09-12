from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from testt.models import Test


# Create your views here.

@login_required
def dashboard(request):
    tests = Test.objects.select_related('page').filter(page__user=request.user).order_by('start_date')
    return render(request, 'dashboard/dashboard.html', {'tests': tests})
