from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from events.models import Event
from django.conf import settings


@receiver(m2m_changed, sender=Event.rsvp.through)
def rsvp_email_notification(sender, instance, action, pk_set, **kwargs):
	if action == 'post_add':
		event = instance
		for user_id in pk_set:
			try:
				user = User.objects.get(pk=user_id)
				send_mail(
					subject=f'RSVP Confirmation for {event.name}',
					message=f'Hi {user.username},\n\nYou have successfully RSVPed to the event: {event.name} on {event.date} at {event.location}.',
					from_email=settings.EMAIL_HOST_USER,
					recipient_list=[user.email],
					fail_silently=True,
				)
			except User.DoesNotExist:
				pass
