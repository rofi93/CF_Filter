import requests

from django.db.models import F
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

        indexes = ContestInfo.objects.all().values('id', 'index').distinct().order_by(F('index'))
        print(len(indexes))
        for index in indexes:
            print(index)

        return render(request, 'test.html', context)


class Home(View):
    context = {}
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        self.context['problems'] = Problem.objects.all().order_by('-contest_info__contest__contest_id',
                                                                  'contest_info__index')[:100]
        self.get_context()

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        division = request.POST.get('division')
        index = request.POST.get('index')
        tags = request.POST.getlist('tags')

        divisions = []
        problems = Problem.objects.all()

        if division:
            if division == '0':
                divisions.append(0)
            else:
                divisions.append(3)
            if division == '1' or division == '3':
                divisions.append(1)
            if division == '2' or division == '3':
                divisions.append(2)

            problems = problems.filter(contest_info__contest__kind__division__number__in=divisions)

        if index:
            problems = problems.filter(contest_info__index__contains=index)

        if tags:
            problems = problems.filter(tags__id__in=tags)

        self.context['problems'] = problems.order_by('-contest_info__contest__contest_id', 'contest_info__index')
        self.get_context()

        return render(request, self.template_name, self.context)

    def get_context(self):
        self.context['divisions'] = Division.objects.all().order_by('number')
        self.context['indexes'] = ContestInfo.objects.all().values('index').distinct().order_by(F('index'))
        self.context['tags'] = Tag.objects.all().order_by('name')
