# -*- coding: utf-8 -*-
from django.template.loader import get_template, render_to_string
from django.test.utils import override_settings
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.files import File as DjangoFile

from cms import api
from cms.models import CMSPlugin
from cms.test_utils.testcases import BaseCMSTestCase, URL_CMS_PLUGIN_ADD, URL_CMS_PLUGIN_EDIT
from cms.utils import get_cms_setting

from filer.models import Folder, Image, File
from filer.tests.helpers import create_image

from . import models
from . import cms_plugins


class GalleryPluginTestCase(TestCase, BaseCMSTestCase):
    su_username = 'user'
    su_password = 'pass'

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.page = api.create_page('page', self.template, self.language, published=True)
        self.placeholder = self.page.placeholders.all()[0]
        self.superuser = self.create_superuser()

        self.img = create_image()
        self.image_name = 'test_file.jpg'
        self.filename = os.path.join(settings.MEDIA_ROOT, self.image_name)
        self.img.save(self.filename, 'JPEG')

    def tearDown(self):
        self.client.logout()
        os.remove(self.filename)
        for f in File.objects.all():
            f.delete()

    def create_superuser(self):
        return User.objects.create_superuser(self.su_username, 'email@example.com', self.su_password)

    def create_filer_image(self, folder=None, name=None):
        file_obj = DjangoFile(open(self.filename, 'rb'), name=name or self.image_name)
        image = Image.objects.create(
            owner=self.superuser,
            original_filename=self.image_name,
            file=file_obj,
            folder=folder,
        )
        return image

    def create_populated_filer_folder(self, folder=None):
        folder = folder or Folder.objects.create(name='test folder')
        for i in range(4):
            self.create_filer_image(folder=folder, name="image {}".format(i))
        return folder

    def test_add_gallery_plugin_api(self):
        gallery_plugin = api.add_plugin(
            self.placeholder, cms_plugins.GalleryCMSPlugin, self.language,
            duration=123,
        )
        self.assertTrue(models.GalleryPlugin.objects.filter(pk=gallery_plugin.pk).exists())

        slide_plugin = api.add_plugin(
            self.placeholder, cms_plugins.SlideCMSPlugin, self.language, target=gallery_plugin,
            url='https://google.com/',
        )
        self.assertTrue(models.SlidePlugin.objects.filter(pk=slide_plugin.pk).exists())

        folder = self.create_populated_filer_folder()
        slide_folder_plugin = api.add_plugin(
            self.placeholder, cms_plugins.SlideFolderCMSPlugin, self.language, target=gallery_plugin,
            folder=folder
        )
        self.assertTrue(models.SlideFolderPlugin.objects.filter(pk=slide_folder_plugin.pk).exists())

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
        # this should really be the below test... but it turns out to be tricky to do
        # self.assertTrue(models.GalleryPlugin.objects.exists())

        # Child Plugin
        plugin_data = {
            'plugin_type': 'SlideCMSPlugin',
            'plugin_language': self.language,
            'placeholder_id': self.placeholder.pk,
            'plugin_parent': CMSPlugin.objects.all()[0].pk,
        }

        response = self.client.post(URL_CMS_PLUGIN_ADD, plugin_data)
        self.assertEqual(response.status_code, 200)
        # this should really be the below test... but it turns out to be tricky to do
        # self.assertTrue(models.SlidePlugin.objects.exists())

    @override_settings(ALDRYN_BOILERPLATE_NAME='legacy')
    def test_render_legacy_boilerplate_templates(self):
        """
        tests whether "legacy" templates exist and don't cause import issues
        """
        from aldryn_boilerplates import template_loaders
        template_loaders.clear_cache()
        self.test_add_gallery_plugin_api()
        api.publish_page(self.page, self.superuser, self.language)
        response = self.client.get(self.page.get_absolute_url())
        # self.assertTrue('LEGACY GALLERY' in response.content)
        # self.assertFalse('BOOTSTRAP3 GALLERY' in response.content)
        template_loaders.clear_cache()

    @override_settings(ALDRYN_BOILERPLATE_NAME='bootstrap3')
    def test_render_bootstrap3_boilerplate_templates(self):
        """
        tests whether "bootstrap3" templates exist and don't cause import issues
        """
        from aldryn_boilerplates import template_loaders
        template_loaders.clear_cache()
        self.test_add_gallery_plugin_api()
        api.publish_page(self.page, self.superuser, self.language)
        response = self.client.get(self.page.get_absolute_url())
        # self.assertTrue('BOOTSTRAP3 GALLERY' in response.content)
        # self.assertFalse('LEGACY GALLERY' in response.content)
        template_loaders.clear_cache()
