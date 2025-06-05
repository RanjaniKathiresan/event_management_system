from django.contrib import admin
from .models import Events, Attendee

# Register your models here.
admin.site.register(Events)
admin.site.register(Attendee)