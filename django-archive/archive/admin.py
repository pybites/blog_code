from django.contrib import admin

from .models import Script


class ScriptAdmin(admin.ModelAdmin):
    pass
admin.site.register(Script, ScriptAdmin)
