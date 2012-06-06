import unittest
import uuid

from mock import patch, Mock
import omnijson as json
import requests

from brockman.client import FocusLabClient
from brockman.exceptions import (BadAPIKey, BadRequest, ResourceNotFound,
    ServerError, UnknownError)


class ClientTests(unittest.TestCase):

    def get_client(self, **kwargs):
        client_kwargs = {
            'api_key': 'testing-key'
        }
        client_kwargs.update(kwargs)

        return FocusLabClient(**client_kwargs)

    def test_simple_init(self):
        key = 'testing-key'
        endpoint = 'https://api.focuslab.io/api/v1/'

        client = FocusLabClient(api_key=key)

        self.assertEquals(key, client.api_key)
        self.assertEquals(endpoint, client.endpoint)

    def test_full_init(self):
        key = 'testing-key'
        endpoint = 'https://api.focuslab-dev.io/api/v1/'

        client = FocusLabClient(api_key=key, endpoint=endpoint)

        self.assertEquals(key, client.api_key)
        self.assertEquals(endpoint, client.endpoint)

    def test_get_simple_url(self):
        client = self.get_client()

        resource = 'trigger'

        result = client.get_url(resource)
        expected = 'https://api.focuslab.io/api/v1/trigger/'

        self.assertEquals(expected, result)

    def test_get_item_url(self):
        client = self.get_client()

        resource = 'trigger/32'

        result = client.get_url(resource)
        expected = 'https://api.focuslab.io/api/v1/trigger/32/'

        self.assertEquals(expected, result)

    def test_get_basic_data(self):
        client = self.get_client()

        action = 'viewed'
        obj = 'blog post'
        actor_id = uuid.uuid4()

        result = client.get_trigger_data(action=action, obj=obj, actor_id=actor_id)
        expected = {
            'action': unicode(action),
            'object': unicode(obj),
            'actor_id': unicode(actor_id)
        }

        self.assertEquals(expected, result)

    def test_get_full_data(self):
        client = self.get_client()

        action = 'viewed'
        obj = 'blog post'
        actor_id = uuid.uuid4()
        identities = {
            'email': ['test1@test.com', 'test2@test.com'],
            'user_id': 42,
        }
        attributes = {
            'tags': ['high-risk', 'big-spender'],
            'plan': 'basic',
        }
        variables = {
            'tags': ['sales', 'promo'],
            'author': 'bob',
        }

        result = client.get_trigger_data(
            action=action,
            obj=obj,
            actor_id=actor_id,
            identities=identities,
            attributes=attributes,
            variables=variables,
        )
        expected = {
            'action': unicode(action),
            'object': unicode(obj),
            'actor_id': unicode(actor_id),
            'captured_identities': identities,
            'captured_attributes': attributes,
            'variables': variables,
        }

        self.assertEquals(expected, result)

    def test_get_headers(self):
        client = self.get_client()

        result = client.get_headers()
        expected = {
            'Content-Type': 'application/json',
            'X-FL-API-KEY': str(client.api_key),
        }

        self.assertEquals(expected, result)

    def record_trigger(self, client, post_mock, response_status=201, check_post_call=True):
        action = 'viewed'
        obj = 'blog post'
        actor_id = uuid.uuid4()
        identities = {
            'email': ['test1@test.com', 'test2@test.com'],
            'user_id': 42,
        }
        attributes = {
            'tags': ['high-risk', 'big-spender'],
            'plan': 'basic',
        }
        variables = {
            'tags': ['sales', 'promo'],
        }

        response_mock = Mock()
        response_mock.status_code = response_status
        post_mock.return_value = response_mock

        client.record_trigger(
            actor_id=actor_id,
            action=action,
            obj=obj,
            identities=identities,
            attributes=attributes,
            variables=variables,
        )

        if check_post_call:
            expected_post_data = json.dumps({
                'action': action,
                'object': obj,
                'actor_id': str(actor_id),
                'captured_identities': identities,
                'captured_attributes': attributes,
                'variables': variables,
            })
            expected_headers = {
                'Content-Type': 'application/json',
                'X-FL-API-KEY': str(client.api_key),
            }
            post_mock.assertCalledWith(
                'https://api.focuslab.io/api/v1/triggers/',
                data=expected_post_data,
                headers=expected_headers,
            )

    @patch.object(requests, 'post')
    def test_record_trigger(self, post_mock):
        client = self.get_client()
        self.record_trigger(client, post_mock)

    @patch.object(requests, 'post')
    def test_record_trigger_401(self, post_mock):
        client = self.get_client()

        with self.assertRaises(BadAPIKey):
            self.record_trigger(
                client,
                post_mock,
                response_status=401,
                check_post_call=False,
            )

    @patch.object(requests, 'post')
    def test_record_trigger_403(self, post_mock):
        client = self.get_client()

        with self.assertRaises(BadAPIKey):
            self.record_trigger(
                client,
                post_mock,
                response_status=403,
                check_post_call=False,
            )

    @patch.object(requests, 'post')
    def test_record_trigger_400(self, post_mock):
        client = self.get_client()

        with self.assertRaises(BadRequest):
            self.record_trigger(
                client,
                post_mock,
                response_status=400,
                check_post_call=False,
            )

    @patch.object(requests, 'post')
    def test_record_trigger_404(self, post_mock):
        client = self.get_client()

        with self.assertRaises(ResourceNotFound):
            self.record_trigger(
                client,
                post_mock,
                response_status=404,
                check_post_call=False,
            )

    @patch.object(requests, 'post')
    def test_record_trigger_500(self, post_mock):
        client = self.get_client()

        with self.assertRaises(ServerError):
            self.record_trigger(
                client,
                post_mock,
                response_status=500,
                check_post_call=False,
            )

    @patch.object(requests, 'post')
    def test_record_trigger_unkown_error(self, post_mock):
        client = self.get_client()

        with self.assertRaises(UnknownError):
            self.record_trigger(
                client,
                post_mock,
                response_status=417,
                check_post_call=False,
            )
