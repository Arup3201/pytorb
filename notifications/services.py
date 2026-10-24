from django.core.paginator import Paginator
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.db import transaction
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

    notification = models.Notification.objects.create(
        recipient=recipient,
        actor=actor,
        event_type=event_type,
        payload=payload,
    )

    def publish_event():
        publish_notification(
            recipient_id=notification.recipient.pk,
            notification_data={
                "id": notification.pk,
                "event_type": notification.event_type,
                "payload": notification.payload,
                "actor": notification.actor.username if notification.actor else "",
                "created_at": notification.created_at.isoformat(),
            },
        )

    transaction.on_commit(publish_event)

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
    
    created_notifications = models.Notification.objects.bulk_create(notifications)

    def publish_events():
        for notification in created_notifications:
            publish_notification(
                recipient_id=notification.recipient.pk,
                notification_data={
                    "id": notification.pk,
                    "event_type": notification.event_type,
                    "payload": notification.payload,
                    "actor": notification.actor.username if notification.actor else "",
                    "created_at": notification.created_at.isoformat(),
                },
            )
    transaction.on_commit(publish_events)


def get_notifications(*, user: models.User):
    return models.Notification.objects.filter(recipient=user).order_by('-created_at')


def list_notifications(*, user: models.User, page_number: int = 1, per_page: int = 5):
    notifications = get_notifications(user=user)
    paginator = Paginator(notifications, per_page)
    return paginator.get_page(page_number)

def publish_notification(recipient_id, notification_data):
    channel_layer = get_channel_layer()
    if not channel_layer:
        raise ValueError("CHANNEL_LAYERS is not configured!")

    async_to_sync(channel_layer.group_send)(
        f"notification_group_{recipient_id}",
        {
            "type": "notification.message", # invokes notification_message function in NotificationConsumer
            "notification": notification_data,
        },
    )
