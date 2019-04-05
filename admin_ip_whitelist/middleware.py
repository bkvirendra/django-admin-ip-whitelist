from __future__ import absolute_import

import logging

import django
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import MiddlewareNotUsed
from django.http import Http404

from .models import DjangoAdminAccessIPWhitelist, ADMIN_ACCESS_WHITELIST_PREFIX

log = logging.getLogger(__name__)


class AdminAccessIPWhiteListMiddleware(object):
    def __init__(self):
        """
        Middleware init is called once per server on startup - do the heavy
        lifting here.
        """
        # If disabled or not enabled raise MiddleWareNotUsed so django
        # processes next middleware.
        self.ENABLED = getattr(settings, 'ADMIN_ACCESS_WHITELIST_ENABLED', False)
        self.USE_HTTP_X_FORWARDED_FOR = getattr(settings, 'ADMIN_ACCESS_WHITELIST_USE_HTTP_X_FORWARDED_FOR', False)
        self.ADMIN_ACCESS_WHITELIST_MESSAGE = getattr(settings, 'ADMIN_ACCESS_WHITELIST_MESSAGE', 'You are banned.')
        self.ADMIN_ACCESS_WHITELIST_PATHS = getattr(settings, 'ADMIN_ACCESS_WHITELIST_PATHS', [])
        self.ADMIN_ACCESS_WHITELIST_PATHS.append('/admin')

        if not self.ENABLED:
            raise MiddlewareNotUsed("django-admin-ip-whitelist is not enabled via settings.py")

        log.debug("[django-admin-ip-whitelist] status = enabled")

        # Prefix All keys in cache to avoid key collisions
        self.ABUSE_PREFIX = 'DJANGO_ADMIN_ACCESS_WHITELIST_ABUSE:'
        self.WHITELIST_PREFIX = ADMIN_ACCESS_WHITELIST_PREFIX

        for whitelist in DjangoAdminAccessIPWhitelist.objects.all():
            cache_key = self.WHITELIST_PREFIX + whitelist.ip
            cache.set(cache_key, "1")

    def _get_ip(self, request):
        ip = request.META['REMOTE_ADDR']
        if self.USE_HTTP_X_FORWARDED_FOR or not ip or ip == '127.0.0.1':
            ip = request.META.get('HTTP_X_FORWARDED_FOR', ip).split(',')[0].strip()
        return ip

    def process_request(self, request):
        if not request.path.startswith(tuple(self.ADMIN_ACCESS_WHITELIST_PATHS)):
            return None

        ip = self._get_ip(request)

        user_agent = request.META.get('HTTP_USER_AGENT', None)

        log.debug("GOT IP FROM Request: %s and User Agent %s" % (ip, user_agent))

        if self.is_whitelisted(ip):
            return None
        else:
            raise Http404

    def is_whitelisted(self, ip):
        # If a whitelist key exists, return True to allow the request through
        self.ADMIN_WHITELISTED_IPS = getattr(settings, 'ADMIN_WHITELISTED_IPS', [])

        is_whitelisted = cache.get(self.WHITELIST_PREFIX + ip) or ip in self.ADMIN_WHITELISTED_IPS

        if is_whitelisted:
            log.debug("/Admin access IP: " + self.WHITELIST_PREFIX + ip)
        return is_whitelisted

