from django.contrib import admin

from task_manager_app.models import Category, SubTask, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "deadline", "created_at")
    list_filter = ("status", "categories", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    filter_horizontal = ("categories",)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "task", "status", "deadline", "created_at")
    list_filter = ("status", "task", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
