from django.db import models

STATUS_CHOICES = [
    ("New", "New"),
    ("In progress", "In progress"),
    ("Pending", "Pending"),
    ("Blocked", "Blocked"),
    ("Done", "Done"),
]

class Category(models.Model):
    name = models.CharField(max_length=100)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New")
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class SubTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New")
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)






