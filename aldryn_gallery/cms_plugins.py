# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import GalleryPluginForm
from .models import GalleryPlugin, SlidePlugin, SlideFolderPlugin


# Base Classes
class GalleryBase(CMSPluginBase):

    class Meta:
        abstract = True

    module = _('Gallery')


class GalleryChildBase(GalleryBase):
    class Meta:
        abstract = True

    require_parent = True
    parent_classes = ['GalleryCMSPlugin']

    def render(self, context, instance, placeholder):
        # get style from parent plugin, render chosen template
        context['instance'] = instance
        context['image'] = instance.image
        return context

    def get_slide_template(self, instance, name='slide'):
        if instance.parent is None:
            style = GalleryPlugin.STANDARD
        else:
            style = getattr(instance.parent.get_plugin_instance()[0], 'style',  GalleryPlugin.STANDARD)
        return 'aldryn_gallery/plugins/{}/{}.html'.format(style, name)

    def get_render_template(self, context, instance, placeholder):
        return self.get_slide_template(instance=instance)


# Plugins
class GalleryCMSPlugin(GalleryBase):
    render_template = False
    name = _('Gallery')
    model = GalleryPlugin
    form = GalleryPluginForm
    allow_children = True
    child_classes = ['SlideCMSPlugin', 'SlideFolderCMSPlugin']

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        if instance.child_plugin_instances:
            number_of_slides = sum([plugin.folder.file_count if isinstance(plugin, SlideFolderPlugin) else 1
                                    for plugin in instance.child_plugin_instances])
        else:
            number_of_slides = 0
        context['slides'] = range(number_of_slides)
        return context

    def get_render_template(self, context, instance, placeholder):
        return 'aldryn_gallery/plugins/{}/gallery.html'.format(instance.style)


class SlideCMSPlugin(GalleryChildBase):
    name = _('Slide')
    model = SlidePlugin


class SlideFolderCMSPlugin(GalleryChildBase):
    """
    Slide Plugin that renders a slide for each image in the linked folder.
    """
    name = _('Slide folder')
    model = SlideFolderPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        if settings.ALDRYN_BOILERPLATE_NAME == 'legacy':
            context['slide_template'] = self.get_slide_template(instance=instance, name='slide')
        else:  # for 'bootstrap3' boilerplate and the recommended structure for other boilerplates
            context['slide_template'] = self.get_slide_template(instance=instance, name='image_slide')
        return context

    def get_render_template(self, context, instance, placeholder):
        if settings.ALDRYN_BOILERPLATE_NAME == 'legacy':
            return 'aldryn_gallery/plugins/slide_folder.html'
        else:  # for 'bootstrap3' boilerplate and the recommended structure for other boilerplates
            return self.get_slide_template(instance=instance, name='slide_folder')


plugin_pool.register_plugin(GalleryCMSPlugin)
plugin_pool.register_plugin(SlideCMSPlugin)
plugin_pool.register_plugin(SlideFolderCMSPlugin)
