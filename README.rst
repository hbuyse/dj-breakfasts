=============
DJ-BREAKFASTS
=============

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
