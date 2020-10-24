from django.db.models.signals import post_save  #signal fired when user is created
from django.contrib.auth.models import User
from django.dispatch import receiver  #receives the signals and acts on it
from .models import Customer


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
	if created:
		Customer.objects.create(user=instance,first_name=instance.first_name,last_name=instance.last_name,email=instance.email)


@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
		instance.customer.save()
