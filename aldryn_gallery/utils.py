from django.conf import settings


def get_additional_styles():
    choices = []
    # Get choices from settings
    raw = settings.GALLERY_STYLES or None
    if raw:
        raw_choices = raw.split(',')
        for choice in raw_choices:
            clean = choice.strip()
            choices.append((clean.lower(), clean.title()))
    return choices
