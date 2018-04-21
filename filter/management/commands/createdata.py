from django.core.management.base import BaseCommand

from filter.models import Division, Kind


class Command(BaseCommand):
    def handle(self, *args, **options):
        div_0, created = Division.objects.get_or_create(name='No Division', number=0)
        div_1, created = Division.objects.get_or_create(name='Division 1', number=1)
        div_2, created = Division.objects.get_or_create(name='Division 2', number=2)
        div_3, created = Division.objects.get_or_create(name='Division 1 + 2', number=3)

        kind_1, created = Kind.objects.get_or_create(name='Codeforces Regular Round', division=div_1)
        kind_2, created = Kind.objects.get_or_create(name='Codeforces Regular Round', division=div_2)
        kind_3, created = Kind.objects.get_or_create(name='Codeforces Regular Round', division=div_3)
        kind_4, created = Kind.objects.get_or_create(name='Other', division=div_0)
