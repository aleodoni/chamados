from django.db import models

from .models import Status, Executor, Chamado, Urgencia

def status_default():
	status = Status.objects.filter(default=True)
	if status.count() > 0:
		return status[0].id
	else:
		return None

def executor_default():
	executor = Executor.objects.filter(default=True)
	if executor.count() > 0:
		return executor[0].id
	else:
		return None