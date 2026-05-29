from django.db import models

from task_manager_app.models.caregory import Category

STATUS_CHOICES = [
    ("New", "New"),
    ("In progress", "In progress"),
    ("Pending", "Pending"),
    ("Blocked", "Blocked"),
    ("Done", "Done"),
]


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="New")
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "task_manager_task"
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        constraints = [
            models.UniqueConstraint(fields=["title"], name="unique_task_title")
        ]


class SubTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    task = models.ForeignKey(
        Task, on_delete=models.SET_NULL, null=True, related_name="subtasks"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="New")
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "task_manager_subtask"
        ordering = ["-created_at"]
        verbose_name = "Sub Task"
        verbose_name_plural = "Sub Tasks"
        constraints = [
            models.UniqueConstraint(fields=["title"], name="unique_sub_task_title")
        ]
