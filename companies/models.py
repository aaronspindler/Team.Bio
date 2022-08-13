from django.db import models


class Company(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    name = models.TextField(unique=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'


class CompanyOwner(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    owner = models.ForeignKey('accounts.CustomUser', related_name='companies', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('company', 'owner')
        verbose_name = 'Company Owner'
        verbose_name_plural = 'Company Owners'
