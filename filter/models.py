from django.db import models


# Create your models here.

class Division(models.Model):
    name = models.CharField(verbose_name='Division Name', max_length=50)
    number = models.IntegerField(verbose_name='Number')

    def __str__(self):
        return str(self.name)


class Kind(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100)
    division = models.ForeignKey(Division, verbose_name='Division', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + ' ' + str(self.division)


class Tag(models.Model):
    name = models.CharField(verbose_name='Tag Name', max_length=50)
    description = models.CharField(verbose_name='Description', max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Contest(models.Model):
    contest_id = models.IntegerField(verbose_name='Contest ID')
    name = models.CharField(verbose_name='Contest Name', max_length=250)
    url = models.URLField(verbose_name='URL')
    kind = models.ForeignKey(Kind, verbose_name='Kind', on_delete=models.CASCADE)
    done = models.BooleanField(verbose_name='Done', default=False)

    def __str__(self):
        return str(self.name)


class ContestInfo(models.Model):
    contest = models.ForeignKey(Contest, verbose_name='Contest', on_delete=models.CASCADE)
    index = models.CharField(verbose_name='Index', max_length=5)

    def __str__(self):
        return str(self.contest.contest_id) + str(self.index)


class Problem(models.Model):
    name = models.CharField(verbose_name='Problem Name', max_length=250)
    contest_info = models.ManyToManyField(ContestInfo, verbose_name='Contest Info')
    tags = models.ManyToManyField(Tag, verbose_name='Tags')

    def __str__(self):
        return str(self.name)
