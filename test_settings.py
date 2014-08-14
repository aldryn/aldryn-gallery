HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Zurich',
    'INSTALLED_APPS': [
        'filer',
    ],
    'NOSE_ARGS': [
        '--with-xunit', '--xunit-file=shippable/testresults/test.xml',
    ],
}
