# krit-teams
Set of django apps for teams and invitations

This library uses `django-rest-auth`, `djangorestframework`, and `djangorestframework-jsonapi`.
Current version: 0.1

## Getting started

1. `pip install git+https://github.com/builtbykrit/krit-teams@0.1`
3. Add `krit-teams` and `krit-invitations` to your apps
4. Add `krit.teams.urls` and `krit.invitations.urls` to your urlpatterns. Add them to the bottom of the list if you need to override them.

## Usage

### Invitations

**Models**
- Invitations

**Serializers**
- InvitationCreateSerializer
- InvitationRetrieveSerializer

**Views**
- InvitationDetailView

**URLS**
```
url(r'^(?P<pk>[0-9]+)/$', InvitationDetailView.as_view(), name='invitations-detail')
```

**Settings**
None

### Teams

**Models**
- Team
- Membership

Both of these models inherit from a base class. If you want to extend these models, you can subclass `BaseTeam` or `BaseMembership` and add your properties and methods. Make sure your subclass is an abstract model. Then in your settings, set `KRIT_TEAMS_BASE_TEAM_MODEL` or `KRIT_TEAMS_BASE_MEMBERSHIP_MODEL` to the path of your subclass. To store the migrations in your project instead of the library add `MIGRATION_MODULES = {'krit_teams': 'krit_teams.migrations'}` to your settings and add a `krit_teams` folder in your project. 


**Serializers**
- TeamSerializer
- MembershipSerializer

If you extend the existing models, you'll need to subclass the serializers to add your new fields.

**Views**
- TeamCreateView
- TeamInviteView
- TeamRetrieveView

**URLS**
```
url(r'^$', TeamCreateView.as_view(), name="teams-create"),
url(r"^(?P<pk>[0-9]+)/$", TeamRetrieveView.as_view(), name="teams-detail"),
url(r"^(?P<pk>[0-9]+)/invite-user/$", TeamInviteView.as_view(), name="teams-invite-user")
```

**Settings**
- KRIT_TEAMS_BASE_TEAM_MODEL
- KRIT_TEAMS_BASE_MEMBERSHIP_MODEL
- KRIT_TEAMS_ROLE_MEMBER
- KRIT_TEAMS_ROLE_OWNER
- KRIT_TEAMS_ROLE_CHOICES
	- You can provide an array of custom roles. Make sure to include `KRIT_TEAMS_ROLE_MEMBER`and `KRIT_TEAMS_ROLE_OWNER` in your choices.


