import requests

from django.shortcuts import render
from django.views.generic.base import View

from .models import Contest, ContestInfo, Division, Kind, Problem, Tag


# Create your views here.

def test(request):
    if request.method == 'GET':
        url = 'http://codeforces.com/api/contest.list'
        response = requests.get(url).json()

        context = {}
        context['results'] = response['result']

        return render(request, 'test.html', context)


class Home(View):
    context = {}
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        self.context['problems'] = Problem.objects.all().order_by('-contest_info__contest__contest_id',
                                                                  'contest_info__index')
        return render(request, self.template_name, self.context)
