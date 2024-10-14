from typing import Any
from django.core.management.base import BaseCommand
from subscriptions.models import Subscription


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        qs = Subscription.objects.filter(active=True)
        for object in qs:
            obj_perms = object.permissions.all()
            for group in object.groups.all():
                group.permissions.set(obj_perms)
            print(object.groups.all())
            print(object.permissions.all())
        