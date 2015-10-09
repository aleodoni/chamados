# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Departamento, Ramal, Problemas, Status, Urgencia, Executor, Chamado, TipoEquipamento, TrocaEquipamento

admin.site.register(Departamento)
admin.site.register(Ramal)
admin.site.register(Problemas)
admin.site.register(Status)
admin.site.register(Urgencia)
admin.site.register(Executor)
admin.site.register(Chamado)
admin.site.register(TipoEquipamento)
admin.site.register(TrocaEquipamento)