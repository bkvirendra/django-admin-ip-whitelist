from __future__ import absolute_import

from django.contrib import admin

from .models import DjangoAdminAccessIPWhitelist

admin.site.register(DjangoAdminAccessIPWhitelist)
