from django.contrib import admin
from .models import AccessToken, UserAgreement, UserAccount

admin.site.register(AccessToken)
admin.site.register(UserAgreement)
admin.site.register(UserAccount)

