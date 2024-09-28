"""
WSGI config for Blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys 

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings')

application = get_wsgi_application()

project_home = '/home/rinzaks/Blog'  # Adjust this if necessary
if project_home not in sys.path:
    sys.path.append(project_home)


