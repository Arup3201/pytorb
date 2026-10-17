from django.core.paginator import Paginator

from . import models


def _exclude_actor(recipients, actor=None):
    if actor is None:
        return recipients

    actor_id = getattr(actor, "pk", actor)
    if actor_id is None:
        return recipients

    return recipients.exclude(pk=actor_id)


def create_notification(
        *, 
        recipient, 
        event_type, 
        payload, 
        actor=None
):
    if recipient == actor or getattr(recipient, "pk", None) == getattr(actor, "pk", None):
        return None

    return models.Notification.objects.create(
        recipient=recipient,
        actor=actor,
        event_type=event_type,
        payload=payload,
    )


def bulk_create_notification(
        *, 
        recipients, 
        event_type, 
        payload, 
        actor=None
):
    recipients = _exclude_actor(recipients, actor)

    notifications = []
    for recipient in recipients:
        notifications.append(models.Notification(
            recipient=recipient,
            event_type=event_type,
            payload=payload,
            actor=actor
        ))
    return models.Notification.objects.bulk_create(notifications)


def get_notifications(*, user: models.User):
    return models.Notification.objects.filter(recipient=user).order_by('-created_at')


def list_notifications(*, user: models.User, page_number: int = 1, per_page: int = 5):
    notifications = get_notifications(user=user)
    paginator = Paginator(notifications, per_page)
    return paginator.get_page(page_number)