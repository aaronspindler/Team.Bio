import tldextract as tldextract
from django.db import models


class Company(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    name = models.TextField(unique=True)
    url = models.URLField(unique=True)
    url_root = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        parsed = tldextract.extract(self.url)
        self.url_root = (parsed.domain + '.' + parsed.suffix).lower()
        super().save(*args, **kwargs)

    @property
    def get_owners(self):
        company_owners = self.owners.all()
        owners_list = []
        for company_owner in company_owners:
            owners_list.append(company_owner.owner)
        return owners_list

    @property
    def get_active_users(self):
        return self.users.filter(is_active=True)

    class Meta:
        verbose_name_plural = 'Companies'


class CompanyOwner(models.Model):
    company = models.ForeignKey(Company, related_name='owners', on_delete=models.CASCADE)
    owner = models.ForeignKey('accounts.User', related_name='companies', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.company} {self.owner}'

    class Meta:
        unique_together = ('company', 'owner')
        verbose_name = 'Company Owner'
        verbose_name_plural = 'Company Owners'


class Team(models.Model):
    company = models.ForeignKey(Company, related_name='teams', on_delete=models.CASCADE)
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('company', 'name')
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'


class Location(models.Model):
    company = models.ForeignKey(Company, related_name='locations', on_delete=models.CASCADE)
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('company', 'name')
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
