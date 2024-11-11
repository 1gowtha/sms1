from django.contrib import admin
from .models import Task  # Correct the import statement

# Register your models here.
admin.site.register(Task)
