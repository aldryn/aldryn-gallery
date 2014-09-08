import sys
import os

import django


cmd = 'djangocms-helper aldryn_gallery test --cms --extra-settings=test_settings'

if django.VERSION[:2] < (1, 6):
    cmd += ' --runner=discover_runner.DiscoverRunner'

sys.exit(os.system(cmd))
