from django.dispatch import receiver
from krit.registration.models import SignupCodeResult
from krit.registration.signals import signup_code_used

from .models import Invitation


@receiver(signup_code_used, sender=SignupCodeResult)
def handle_signup_code_used(sender, **kwargs):
    result = kwargs.get("signup_code_result")
    try:
        invite = result.signup_code.invitation
        invite.accept(result.user)
    except Invitation.DoesNotExist:
        pass
