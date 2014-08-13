# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from cms import api
from cms.models import CMSPlugin
from cms.test_utils.testcases import BaseCMSTestCase, URL_CMS_PLUGIN_ADD
from cms.utils import get_cms_setting

from .cms_plugins import GalleryCMSPlugin, SlideCMSPlugin


class GalleryPluginTestCase(TestCase, BaseCMSTestCase):
    su_username = 'user'
    su_password = 'pass'

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.page = api.create_page('page', self.template, self.language, published=True)
        self.placeholder = self.page.placeholders.all()[0]
        self.superuser = self.create_superuser()

    def create_superuser(self):
        return User.objects.create_superuser(self.su_username, 'email@example.com', self.su_password)

    def test_add_gallery_plugin_api(self):
        gallery_plugin = api.add_plugin(self.placeholder, GalleryCMSPlugin, self.language)
        child_plugin = api.add_plugin(self.placeholder, SlideCMSPlugin, self.language, target=gallery_plugin)

    def test_add_gallery_plugin_client(self):
        self.client.login(username=self.su_username, password=self.su_password)

        # Parent Plugin
        plugin_data = {
            'plugin_type': 'GalleryCMSPlugin',
            'plugin_language': self.language,
            'placeholder_id': self.placeholder.pk,
        }

        response = self.client.post(URL_CMS_PLUGIN_ADD, plugin_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CMSPlugin.objects.exists())

        # Child Plugin
        plugin_data = {
            'plugin_type': 'SlideCMSPlugin',
            'plugin_language': self.language,
            'placeholder_id': self.placeholder.pk,
            'plugin_parent': CMSPlugin.objects.all()[0].pk,
        }

        response = self.client.post(URL_CMS_PLUGIN_ADD, plugin_data)
        self.assertEqual(response.status_code, 200)
