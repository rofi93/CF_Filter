import requests

from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.views.generic.base import View


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

        return render(request, self.template_name, self.context)
