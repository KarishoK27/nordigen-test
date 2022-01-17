from django.db import models

class AccessToken(models.Model):
    access_token = models.TextField(null=False, blank=False)
    access_expires = models.DateTimeField(null=False, blank=False)
    refresh_token = models.TextField(null=False, blank=False)
    refresh_expires = models.DateTimeField(null=False, blank=False)

class UserAgreement(models.Model):
    institution_id = models.CharField(max_length=250, null=False, blank=False)
    agreement = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False)
    requisition_id = models.CharField(max_length=250, null=True, blank=True)
    link = models.TextField(null=True, blank=True)

class UserAccount(models.Model):
    agreement = models.ForeignKey(UserAgreement, on_delete=models.CASCADE)
    account = models.CharField(max_length=250, null=False, blank=False)
