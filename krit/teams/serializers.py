from django.contrib.auth import get_user_model
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField

from krit.authentication.serializers import UserSerializer
from krit.invitations.models import Invitation
from .models import Membership, Team

UserModel = get_user_model()


# Monkey patch the JSONAPIMeta class onto whatever
# UserModel we are using.
class UserJSONAPIMeta:
        resource_name = "users"
UserModel.JSONAPIMeta = UserJSONAPIMeta


class MembershipSerializer(serializers.ModelSerializer):
    included_serializers = {
        'user': UserSerializer
    }

    user = ResourceRelatedField(
        queryset=UserModel.objects
    )

    invitation = ResourceRelatedField(
        queryset=Invitation.objects
    )

    team = ResourceRelatedField(
        queryset=Team.objects
    )

    class Meta:
        model = Membership
        fields = ('created_at', 'updated_at', 'id', 'role', 'state', 'user', 'team', 'invitation')

    class JSONAPIMeta:
        included_resources = ['user']


class TeamSerializer(serializers.ModelSerializer):
    included_serializers = {
        'memberships': MembershipSerializer
    }

    memberships = ResourceRelatedField(
        queryset=Membership.objects,
        many=True,
        default=[]
    )

    class Meta:
        model = Team
        fields = ('created_at', 'updated_at', 'id', 'memberships',
                  'name')

    class JSONAPIMeta:
        included_resources = ['memberships']

    def create(self, validated_data):
        team = Team(creator=validated_data['user'],
                    name=validated_data['name'])
        team.save()
        return team
