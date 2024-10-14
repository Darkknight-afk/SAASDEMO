from django.db import models
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL

ALLOW_CUSTOM_GROUPS = True

SUB_PERMISSIONS = [
            ('advanced', 'Advanced Perm'),
            ('pro', 'Pro Perm'),
            ('basic', 'Basic Perm')
        ]

class Subscription(models.Model):
    name = models.CharField(max_length=120)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission, limit_choices_to={
        'content_type__app_label': 'subscriptions',
        'codename__in': [x[0] for x in SUB_PERMISSIONS]})
    active = models.BooleanField(default=True)

    class Meta:
        permissions = SUB_PERMISSIONS
    
    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)


@receiver(post_save, sender=UserSubscription)
def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_object = user_sub_instance.subscription
    groups_ids = []
    if subscription_object is not None:
        groups = subscription_object.groups.all()
        groups_ids = groups.values_list('id', flat=True)
    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups_ids)
    else:
        subs_qs = Subscription.objects.filter(active=True)
        if subscription_object is not None: 
            subs_qs = subs_qs.exclude(id=subscription_object.id)
        subs_groups = subs_qs.values_list('groups__id', flat=True)
        subs_groups_set = set(subs_groups)
        all_groups = user.groups.all().values_list('id', flat=True)
        groups_ids_set = set(groups_ids)
        all_groups_set = set(all_groups) - subs_groups_set
        final_group_ids = list(groups_ids_set | all_groups_set)
        user.groups.set(final_group_ids)