test:
	test -d env || virtualenv env
	env/bin/pip install git+https://github.com/nephila/djangocms-helper#egg=djangocms-helper pysqlite django-nose
	env/bin/python setup.py install
	mkdir -p shippable/testresults
	. env/bin/activate; make runtest

runtest:
	djangocms-helper aldryn_gallery test --cms --extra-settings=test_settings.py --nose-runner
