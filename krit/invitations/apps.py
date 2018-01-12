import importlib

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "krit.invitations"
    label = "krit_invitations"

    def ready(self):
        importlib.import_module("krit.invitations.receivers")