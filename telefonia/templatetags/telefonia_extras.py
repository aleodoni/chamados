from mimetypes import guess_type

from django import template
from base64 import b64encode
from django.contrib.staticfiles import finders

import os


register = template.Library()


@register.filter
def datalize(filename, content_type=None):
	"""
	This filter will return data URI for given file, for more info go to:
	http://en.wikipedia.org/wiki/Data_URI_scheme
	Sample Usage:
	<img src="{{ 'image.jpg'|datalize }}"/> or 
	<img src="{% static 'image.jpg'|datalize %}"/>
	will be filtered into:
	<img src="data:image/png;base64,iVBORw0...">
	"""
	if filename:
		with open(filename, "rb") as f:
			data = f.read()

		encoded = b64encode(data)
		content_type, encoding = guess_type(filename)
		return "data:%s;base64,%s" % (content_type, encoded)
	else:
		return ''
