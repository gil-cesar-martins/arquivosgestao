import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling, MediaCling


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestaoarquivos.settings')

application = Cling(MediaCling(get_wsgi_application()))
