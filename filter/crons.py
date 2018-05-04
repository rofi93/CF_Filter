import datetime
import string

from bs4 import BeautifulSoup
import requests

from .models import Contest, ContestInfo, Division, Kind, Problem, Tag


def add_new_contest():
    try:
        api_url = 'http://codeforces.com/api/contest.list'
        response = requests.get(api_url).json()
    except:
        response = {}
        response['result'] = []

    result = response['result']
    url = 'http://codeforces.com/contest/'
    for contest_ in result:
        phase = contest_.get('phase')
        if phase and phase != 'FINISHED':
            continue

        name = contest_.get('name')
        contest_id = contest_.get('id')
        duration = contest_.get('durationSeconds')
        start_time = contest_.get('startTimeSeconds')

        contest_url = url + str(contest_id)
        end_time = datetime.datetime.fromtimestamp(start_time + duration)

        if name.find('Alpha Round') > -1 or name.find('Round #100') > -1 or name.find('Good Bye') > -1:
            kind = Kind.objects.get(division__number=3)
        elif name.find('Div. 1') > -1 and name.find('Div. 2') > -1:
            kind = Kind.objects.get(division__number=3)
        elif name.find('Div. 1') > -1 and name.find('Educational') == -1:
            kind = Kind.objects.get(division__number=1)
        elif name.find('Div. 2') > -1 and name.find('Educational') == -1:
            kind = Kind.objects.get(division__number=2)
        elif name.find('Div. 3') > -1 and name.find('Educational') == -1:
            kind = Kind.objects.get(division__number=4)
        else:
            if name.find('Beta Round') > -1:
                kind = Kind.objects.get(division__number=3)
            else:
                kind = Kind.objects.get(division__number=0)

        Contest.objects.get_or_create(contest_id=contest_id, name=name, contest_url=contest_url, kind=kind,
                                      end_time=end_time)


def get_soup(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
    except:
        soup = BeautifulSoup('', 'lxml')
    return soup


def add_tag(problem, problem_url):
    new_soup = get_soup(problem_url)
    tags = new_soup.find_all('span', {'class': 'tag-box'})

    for tag_ in tags:
        tag_name = tag_.get_text().strip()
        tag_description = tag_.get('title')
        tag, created = Tag.objects.get_or_create(name=tag_name, description=tag_description)

        if not problem.tags.filter(name=tag.name):
            problem.tags.add(tag)
            problem.save()

    return problem


def add_new_problem():
    contests = Contest.objects.filter(done=False).order_by('contest_id')

    if len(contests) > 300:
        contests = contests[:300]

    for contest in contests:
        sibling = None
        soup = get_soup(contest.contest_url)

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
                problem = Problem.objects.create(name=problem_name)

            contest_info, created = ContestInfo.objects.get_or_create(contest=contest, index=problem_index,
                                                                      problem_url=problem_url)
            problem.contest_info.add(contest_info)
            problem.save()

            add_tag(problem, problem_url)

        contest.done = True
        contest.save()


def update_tags():
    interval = float(30 * 24 * 60 * 60)
    current_timestamp = datetime.datetime.timestamp(datetime.datetime.now())
    needed_datetime = datetime.datetime.fromtimestamp(current_timestamp - interval)

    contests = Contest.objects.filter(end_time__gte=needed_datetime)
    problems = Problem.objects.filter(contest_info__contest__in=contests)

    for problem in problems:
        problem.tags.clear()

        for contest_info in problem.contest_info.all():
            add_tag(problem, contest_info.problem_url)
