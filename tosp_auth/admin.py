from django.contrib import admin
from .models import SecretToken


class SecretTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    fields = ('user',)
    ordering = ('-created',)


admin.site.register(SecretToken, SecretTokenAdmin)
