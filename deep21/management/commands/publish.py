import logging
from datetime import datetime

from django.core.management.base import BaseCommand

from deep21 import settings
from two1.commands import publish
from two1.server import rest_client


class Command(BaseCommand):
    help = 'Publish your app to the marketplace'

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger('deep21.publish')
        self._username = settings.TWO1_USERNAME
        self._client = rest_client.TwentyOneRestClient(username=self._username, wallet=settings.WALLET)

    def handle(self, *args, **options):
        manifest_path = 'deep21/manifest.yaml'
        app_name = 'Deep21'
        try:
            publish._publish(self._client, manifest_path, '21market', True, {})
            self._logger.info(
                '%s publishing %s - published: True, Timestamp: %s' %
                (self._username, app_name, datetime.now())
            )
        except Exception as e:
            self._logger.error(
                '%s publishing %s - published: False, error: %s, Timestamp: %s' %
                (self._username, app_name, e, datetime.now())
            )
