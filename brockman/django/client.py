from django.conf import settings

from ..client import FocusLabClient


class DjangoFocusLabClient(FocusLabClient):
    '''
    A subclass of FocusLabClient that automatically pulls config info in from
    the Django settings module.
    '''

    def __init__(self, api_key=None, endpoint=None):
        api_key = api_key or getattr(settings, 'FL_API_KEY', None)
        endpoint = endpoint or getattr(settings, 'FL_ENDPOINT', 'https://api.focuslab.io/api/v1/')

        super(DjangoFocusLabClient, self).__init__(
            api_key=api_key,
            endpoint=endpoint,
        )
