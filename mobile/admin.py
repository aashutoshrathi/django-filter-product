from django.contrib import admin

from .models import Mobile, OS, Brand, Bands

admin.site.register(Mobile)
admin.site.register(OS)
admin.site.register(Brand)
admin.site.register(Bands)