import datetime
from operator import itemgetter
import string

import requests

from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.views.generic.base import View

from .crons import get_soup
from .models import Contest, ContestInfo, Division, Kind, Problem, Tag


# Create your views here.

def test(request):
    if request.method == 'GET':
        url = 'http://codeforces.com/api/contest.list'
        response = requests.get(url).json()

        context = {}
        context['results'] = sorted(response['result'], key=itemgetter('id'), reverse=True)
        '''start = datetime.datetime.now()
        count = 0
        for contest_ in context['results']:
            phase = contest_.get('phase')
            if phase and phase != 'FINISHED':
                continue

            count += 1
            name = contest_.get('name')
            contest_id = contest_.get('id')
            duration = contest_.get('durationSeconds')
            start_time = contest_.get('startTimeSeconds')

            contest_url = url + str(contest_id)
            end_time = datetime.datetime.fromtimestamp(start_time + duration)

            if name.find('Alpha Round') > -1 or name.find('Round #100') > -1:
                kind = Kind.objects.get(division__number=3)
            elif name.find('Div. 1') > -1 and name.find('Div. 2') > -1:
                kind = Kind.objects.get(division__number=3)
            elif name.find('Div. 1') > -1:
                kind = Kind.objects.get(division__number=1)
            elif name.find('Div. 2') > -1:
                kind = Kind.objects.get(division__number=2)
            else:
                if name.find('Beta Round') > -1:
                    kind = Kind.objects.get(division__number=3)
                else:
                    kind = Kind.objects.get(division__number=0)

        end = datetime.datetime.now()
        print(end-start)
        print(count)'''
        '''count1 = count2 = 0
        start = datetime.datetime.now()
        context = {}
        contests = Contest.objects.all().order_by('contest_id')

        if len(contests) > 200:
            contests = contests[:5]

        for contest in contests:
            sibling = None
            soup = get_soup(contest.contest_url)

            count1 += 1

            contest_name = contest.name
            contest_name = contest_name.replace('Alpha', '').replace('Beta', '')
            while contest_name.find('  ') > -1:
                contest_name = contest_name.replace('  ', ' ')
            index1 = contest_name.find('Codeforces Round #')
            index2 = contest_name.find(' ', index1)

            if index1 > -1:
                if index2 == -1:
                    index2 = len(contest_name)

                division = None
                contest_name = contest_name[index1:index2].strip(string.punctuation)
                if contest.kind.division.number == 1:
                    division = 2
                elif contest.kind.division.number == 2:
                    division = 1

                if division:
                    sibling = Contest.objects.filter(name__contains=contest_name, kind__division__number=division,
                                                     end_time=contest.end_time)

                if sibling:
                    sibling = sibling[0]
            #print(sibling, contest)
            #continue

            problems = soup.find_all('td', {'class': 'id'})

            url = 'http://codeforces.com'

            for problem_ in problems:
                problem = None
                child = problem_.find('a')
                problem_url = url + child.get('href', '')
                problem_index = child.get_text().strip()
                next_sibling = problem_.find_next_sibling()
                problem_name = next_sibling.find('a').get_text().strip()

                if sibling:
                    problem = Problem.objects.filter(name=problem_name, contest_info__contest=sibling)

                if problem:
                    problem = problem[0]
                else:
                    count2 += 1
                    # problem = Problem.objects.create(name=problem_name)
                continue

                contest_info, created = ContestInfo.objects.get_or_create(contest=contest, index=problem_index,
                                                                          problem_url=problem_url)
                problem.contest_info.add(contest_info)
                problem.save()
                print(problem.id, contest_info)

                new_soup = get_soup(problem_url)
                tags = new_soup.find_all('span', {'class': 'tag-box'})

                for tag_ in tags:
                    tag_name = tag_.get_text().strip()
                    tag_description = tag_.get('title')
                    tag, created = Tag.objects.get_or_create(name=tag_name, description=tag_description)
                    problem.tags.add(tag)
                    problem.save()

            #contest.done = True
            #contest.save()
            #print(contest.name)
        end = datetime.datetime.now()
        print(end-start)
        print(count1, count2)'''
        return render(request, 'test.html', context)


class Home(View):
    context = {}
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
