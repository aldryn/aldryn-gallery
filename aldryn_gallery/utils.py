from django.conf import settings


def get_additional_styles():
    """
    Get additional styles choices from settings
    """
    choices = []
    try:
        raw = settings.GALLERY_STYLES
    except AttributeError:
        return choices

    if raw:
        raw_choices = raw.split(',')
        for choice in raw_choices:
            clean = choice.strip()
            choices.append((clean.lower(), clean.title()))
    return choices
