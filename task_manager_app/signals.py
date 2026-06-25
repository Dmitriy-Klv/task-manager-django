from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from task_manager_app.models.task import Task


@receiver(pre_save, sender=Task)
def capture_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_status = Task.objects.get(pk=instance.pk).status
        except Task.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Task)
def notify_owner_on_status_change(sender, instance, created, **kwargs):
    if created:
        return

    old_status = getattr(instance, "_old_status", None)
    new_status = instance.status

    if old_status == new_status:
        return

    owner = instance.owner
    if not owner or not owner.email:
        return

    if new_status == "Done":
        subject = f'Task "{instance.title}" has been closed'
        message = (
            f"Hello {owner.username},\n\n"
            f'Your task "{instance.title}" has been closed.\n'
            f"Status: {old_status} → {new_status}\n"
        )
    else:
        subject = f'Task "{instance.title}" status changed'
        message = (
            f"Hello {owner.username},\n\n"
            f'The status of your task "{instance.title}" has changed.\n'
            f"Status: {old_status} → {new_status}\n"
        )

    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[owner.email],
        fail_silently=True,
    )
