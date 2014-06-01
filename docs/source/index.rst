======================
PyAtTask: Python Bindings for the AtTask API
======================

Release v\ |version|

PyAtTask is a Python-native implementation of the AtTask REST API

.. code-block:: python

    >>> import pyattask.session
    >>> import pyattask.user
    >>> pyattask.session.create_session("https://mydomain.attask-ondemand.com/attask/api/v4.0/")
    >>> pyattask.session.get_session().login('davidr', 'XXXXXXXX', domain='mydomain')
    True
    >>> pyattask.user.User.current_user()
    <User: "David Ressman">


Guide
^^^^^

.. toctree::
   :maxdepth: 2

   modules
   pyattask
   todo

   :maxdepth: 0

   license
   help



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

