import os
from datetime import timedelta

import django
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from task_manager_app.models import Category, SubTask, Task

task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="New",
    deadline=timezone.now() + timedelta(days=3),
)

task.subtasks.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    status="New",
    deadline=timezone.now() + timedelta(days=2),
)

task.subtasks.create(
    title="Create slides",
    description="Create presentation slides",
    status="New",
    deadline=timezone.now() + timedelta(days=1),
)


new_tasks = Task.objects.filter(status="New")

print(new_tasks.query)
print(list(new_tasks))

expired_done_subtasks = SubTask.objects.filter(
    status="Done", deadline__lt=timezone.now()
)

print(expired_done_subtasks.query)
print(list(expired_done_subtasks))

update_tasks_status = Task.objects.get(title="Prepare presentation").subtasks.update(
    status="In progress"
)
print(update_tasks_status)

update_deadline = SubTask.objects.filter(title="Gather information").update(
    deadline=timezone.now() - timedelta(days=2)
)
print(update_deadline)

update_task_title = SubTask.objects.filter(title="Create slides").update(
    description="Create and format presentation slides"
)
print(update_task_title)

deleted_task = Task.objects.filter(title="Prepare presentation").delete()
print(deleted_task)
