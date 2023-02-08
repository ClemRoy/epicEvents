from django.contrib import admin
from authentication.models import User
from epicEvents.models import Client,Contract,Event

# Register your models here.

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
