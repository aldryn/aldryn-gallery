from aldryn_client import forms


class Form(forms.BaseForm):
    gallery_styles = forms.CharField('List of additional gallery styles (comma separated)', required=False)

    def to_settings(self, data, settings):
        settings['GALLERY_STYLES'] = data['gallery_styles']
        return settings
