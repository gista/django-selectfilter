from django.conf.urls.defaults import *

from selectfilter import auth
from selectfilter.views import json_index

if auth.AUTH_DECORATOR:
	json_index = auth.AUTH_DECORATOR(json_index)

urlpatterns = patterns('',
	(r'^json_index/$', json_index),
)
