from django.contrib import admin

from task_manager_app.models import Category, SubTask, Task


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]
    list_display = ("id", "get_short_title", "status", "deadline", "created_at")
    list_filter = ("status", "categories", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    filter_horizontal = ("categories",)

    def get_short_title(self, obj):
        return f"{obj.title[:10]}..." if len(obj.title) > 10 else obj.title

    get_short_title.short_description = "Title"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "task", "status", "deadline", "created_at")
    list_filter = ("status", "task", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)

    actions = ["make_done"]

    @admin.action(description="Mark selected subtasks as Done")
    def make_done(self, request, queryset):
        queryset.update(status="Done")
