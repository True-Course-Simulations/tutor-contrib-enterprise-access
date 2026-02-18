enterprise-access plugin for `Tutor <https://docs.tutor.edly.io>`__
###################################################################

enterprise-access plugin for Tutor


Installation
************

.. code-block:: bash

    pip install git+https://github.com/True-Course-Simulations/tutor-contrib-enterprise-access

Usage
*****

.. code-block:: bash

    tutor plugins enable enterprise-access

Enterprise Access Superadmin Management Commands
*****

These commands allow you to create or promote superadmin
users inside the enterprise-access service.

Use create_enterprise_access_superadmin to create a new
superadmin user or update an existing one.

Examples:

tutor local run --rm enterprise-access bash -lc '
/openedx/venv/bin/python ./manage.py create_enterprise_access_superadmin \
  --username dev --email dev@dev.dev --no-password


./manage.py create_enterprise_access_superadmin
--username dev
--email dev@example.com

--no-password

./manage.py create_enterprise_access_superadmin
--username eaadmin
--email eaadmin@example.com

--password 'StrongPassword123'

Use promote_enterprise_access_superadmin to grant
superadmin rights to an existing user (typically after
first SSO login).

Example:

./manage.py promote_enterprise_access_superadmin
--username dev

These commands set:
is_staff = True
is_superuser = True

If --no-password is used, the account will be SSO-only
(no local password login).



License
*******

This software is licensed under the terms of the AGPLv3.
