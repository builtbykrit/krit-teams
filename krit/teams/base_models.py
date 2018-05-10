from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.urls import reverse

from krit.invitations.models import Invitation
from krit.teams import signals
from krit.teams.hooks import hookset
from django.contrib.auth.models import User
from .conf import settings


class BaseMembership(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    role = models.CharField(max_length=50,
                            choices=settings.KRIT_TEAMS_ROLE_CHOICES,
                            default=settings.KRIT_TEAMS_ROLE_MEMBER,
                            verbose_name="role")

    STATE_INVITED = "invited"
    STATE_JOINED = "joined"
    STATE_CHOICES = [
        (STATE_INVITED, "invited"),
        (STATE_JOINED, "joined")
    ]
    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        verbose_name="state")

    class JSONAPIMeta:
        resource_name = "memberships"

    class Meta:
        abstract = True
        verbose_name = "Base Membership"
        verbose_name_plural = "Bases Memberships"

    invitation = models.ForeignKey(Invitation,
                                   related_name="memberships",
                                   null=True,
                                   blank=True,
                                   verbose_name="invitation",
                                   on_delete=models.SET_NULL)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="memberships",
                             null=True,
                             blank=True,
                             on_delete=models.CASCADE,
                             verbose_name="user")

    def accept(self):
        self.user = self.invitation.to_user
        self.state = BaseMembership.STATE_JOINED
        self.save()
        # Delete the invitation to prevent a frontend issue where
        # both the invitation and the membership get displayed
        self.invitation.delete()

    def __str__(self):
        return "{0} in {1}".format(self.user, self.team)

    @property
    def invitee(self):
        return self.user or self.invitation.to_user_email()

    def status(self):
        if self.user:
            return self.get_state_display()
        if self.invitation:
            return self.invitation.get_status_display()
        return "Unknown"


class BaseTeam(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name="teams_created",
                                verbose_name="creator",
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="name")

    class JSONAPIMeta:
        resource_name = "teams"

    class Meta:
        abstract = True
        verbose_name = "Base Team"
        verbose_name_plural = "Bases Teams"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("team_detail", args=[self.slug])

    @property
    def acceptances(self):
        return self.memberships.filter(state=BaseMembership.STATE_JOINED)

    @property
    def invitees(self):
        return self.memberships.filter(state=BaseMembership.STATE_INVITED)

    @property
    def members(self):
        return self.acceptances.filter(role=settings.KRIT_TEAMS_ROLE_MEMBER)

    @property
    def owners(self):
        return self.acceptances.filter(role=settings.KRIT_TEAMS_ROLE_OWNER)

    def can_join(self, user):
        if self.state_for(user) == BaseMembership.STATE_INVITED:
            return True
        else:
            return False

    def is_member(self, user):
        return self.members.filter(user=user).exists()

    def is_owner(self, user):
        return self.owners.filter(user=user).exists()

    def is_on_team(self, user):
        return self.acceptances.filter(user=user).exists()

    def invite_user(self, from_user, to_email,
                    role=settings.KRIT_TEAMS_ROLE_MEMBER, message=None):

        if Invitation.objects.filter(signup_code__email=to_email).exists():
            raise ValidationError('The email address you entered has already been invited to join a team.')
        try:
            if User.objects.get(email=to_email):
                raise ValidationError('This user is already apart of a team.')
        except User.DoesNotExist:
            # Send an invite if there is not an email address associated with that user
            invite = Invitation.invite(from_user, to_email,
                                       message, send=False)
            membership, created = self.memberships.get_or_create(
                invitation=invite,
                defaults={"role": role, "state": BaseMembership.STATE_INVITED}
            )
            invite.send_invite()
            signals.invited_user.send(sender=self, membership=membership)
            return membership

    def role_for(self, user):

        # if hookset.user_is_staff(user):
        #    return BaseMembership.ROLE_MANAGER

        membership = self.for_user(user)
        if membership:
            return membership.role

    def state_for(self, user):
        membership = self.for_user(user=user)
        if membership:
            return membership.state

    def team_for(self, user):
        try:
            return self.memberships.get(user=user)
        except ObjectDoesNotExist:
            pass
