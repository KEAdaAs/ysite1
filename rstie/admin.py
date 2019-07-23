from django.contrib import admin

# Register your models here.

from rstie.models import Poem, abzats

admin.site.register(Poem)
admin.site.register(abzats)