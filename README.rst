=============
DJ-BREAKFASTS
=============

-------------
Configuration
-------------

Add this to the end of your settings

.. code-block::

    EMAIL_HOST="<HOST>"
    EMAIL_PORT=<PORT>
    EMAIL_USE_TLS=<True|False>
    EMAIL_SUBJECT_PREFIX="[PETIT DEJ] "
    EMAIL_HOST_USER="<User>"
    EMAIL_HOST_PASSWORD="<Password>"

    BREAKFAST_DAY = 4

    CELERY_RESULT_BACKEND = 'django-db'

-------
Testing
-------

.. code-block:: bash

    $ virtualenv -p $(which python3) .venv
    $ source .venv/bin/activate
    $ pip install -r requirements/test.txt
    $ ./manage.py test --exclude-tag=functional

------------
Coding Style
------------

https://docs.djangoproject.com/en/2.1/internals/contributing/writing-code/coding-style/
