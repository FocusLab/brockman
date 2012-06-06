from urlparse import urljoin

import omnijson as json
import requests

from .exceptions import (BadAPIKey, BadRequest, ResourceNotFound, ServerError,
    UnknownError)

class FocusLabClient(object):

    def __init__(self, api_key, endpoint='https://api.focuslab.io/api/v1/'):
        self.api_key = api_key
        self.endpoint = endpoint

        super(FocusLabClient, self).__init__()

    def get_url(self, resource):
        if not resource.endswith('/'):
            resource = u'%s/' % resource

        return urljoin(self.endpoint, resource)

    def get_trigger_data(self, actor_id, action, obj, identities=None, attributes=None, variables=None):
        data = {
            'actor_id': unicode(actor_id),
            'action': unicode(action),
            'object': unicode(obj),
        }

        if identities:
            data['captured_identities'] = identities

        if attributes:
            data['captured_attributes'] = attributes

        if variables:
            data['variables'] = variables

        return data

    def get_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'X-FL-API-KEY': str(self.api_key),
        }

        return headers

    def record_trigger(self, actor_id, action, obj, identities=None, attributes=None, variables=None):
        url = self.get_url('trigger')
        headers = self.get_headers()
        data = self.get_trigger_data(
            actor_id=actor_id,
            action=action,
            obj=obj,
            identities=identities,
            attributes=attributes,
            variables=variables,
        )

        response = requests.post(url, data=json.dumps(data), headers=headers)

        status = response.status_code
        print status
        if status != 201:
            if status in (401, 403,):
                raise BadAPIKey
            elif status == 400:
                raise BadRequest
            elif status == 404:
                raise ResourceNotFound
            elif status == 500:
                raise ServerError
            else:
                raise UnknownError
