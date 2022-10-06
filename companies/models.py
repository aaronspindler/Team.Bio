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

    def get_owners(self):
        company_owners = self.owners.all()
        owners_list = []
        for company_owner in company_owners:
            owners_list.append(company_owner.owner)
        return owners_list

    class Meta:
        verbose_name_plural = 'Companies'


class CompanyOwner(models.Model):
    company = models.ForeignKey(Company, related_name='owners', on_delete=models.CASCADE)
    owner = models.ForeignKey('accounts.CustomUser', related_name='companies', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.company} {self.owner}'

    class Meta:
        unique_together = ('company', 'owner')
        verbose_name = 'Company Owner'
        verbose_name_plural = 'Company Owners'
