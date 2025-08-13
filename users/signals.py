from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if not created: return
    
    token = default_token_generator.make_token(instance)
    activation_url = f'{settings.CFRF_TRUSTED_ORIGINS[1]}/activate/{instance.id}/{token}'
    message_body = f"Hi {instance.username}\n\nPlsease active your account by clicking the link bellow \n{activation_url}\n\nThank you"

    send_mail(
        subject="Activation mail",
        message=message_body,
        from_email=settings.EMAIL_SENDER,
        recipient_list=[instance.email]
    )

@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name = "User")
        instance.groups.add(group)
        instance.save()
        
