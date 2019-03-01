from django.contrib import admin

from .models import Transaction, Sequence


admin.site.register(Transaction)
admin.site.register(Sequence)
