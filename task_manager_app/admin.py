from django.contrib import admin

from task_manager_app.models import Category, Task, SubTask

admin.site.register(Category)
admin.site.register(Task)
admin.site.register(SubTask)
