# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.template import TemplateDoesNotExist
from django.template.loader import select_template

from .models import GalleryPlugin


class GalleryPluginForm(forms.ModelForm):

    class Meta:
        fields = ['style', 'engine', 'timeout', 'duration', 'shuffle']
        model = GalleryPlugin

    def get_slide_template(self, style, name='slide'):
        return 'aldryn_gallery/plugins/{}/{}.html'.format(
            style, name,
        )

    def clean_style(self):
        style = self.cleaned_data.get('style')
        # Check if template for style exists:
        try:
            if settings.ALDRYN_BOILERPLATE_NAME == 'legacy':
                select_template([self.get_slide_template(style=style, name='slide')])
            else:  # for 'bootstrap3' boilerplate and the recommended structure for other boilerplates
                select_template([self.get_slide_template(style=style, name='image_slide')])
        except TemplateDoesNotExist:
            raise forms.ValidationError("Not a valid style (Template does not exist)")
        return style
