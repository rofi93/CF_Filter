from django.contrib import admin

from .models import Contest, ContestInfo, Division, Kind, Problem, Tag

# Register your models here.

admin.site.register([Contest, ContestInfo, Division, Kind, Problem, Tag])
