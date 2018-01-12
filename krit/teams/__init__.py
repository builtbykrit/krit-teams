import pkg_resources

__version__ = pkg_resources.get_distribution("krit-teams").version
default_app_config = "krit.teams.apps.AppConfig"
