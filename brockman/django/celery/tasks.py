from celery.task import task

from ..client import DjangoFocusLabClient
from ...exceptions import ServerError, UnknownError


@task(name='brockman.django.celery.tasks.record_trigger')
def record_trigger(actor_id, action, obj, identities=None, attributes=None, variables=None):
    client = DjangoFocusLabClient()
    try:
        client.record_trigger(
            actor_id=actor_id,
            action=action,
            obj=obj,
            identities=identities,
            attributes=attributes,
            variables=variables,
        )
    except (ServerError, UnknownError), exc:
        record_trigger.retry(exc=exc)
