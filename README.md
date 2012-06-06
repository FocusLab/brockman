Brockman
========

A Python client for working with the FocusLab API.

![Kent Brockman](http://upload.wikimedia.org/wikipedia/en/9/9d/Kent_Brockman.jpg)

Currently this client only implements trigger recording but eventually it will
provide support for the full API.

Getting Started
---------------

First you need to create an instance of the `FocusLabClient`:

```python
from brockman.client import FocusLabClient

client = FocusLabClient(api_key='da9dcaa0364541498d4ae6b4865cf395')
```

The only required parameter for the client is `api_key`.  You can get your API
key from your [FocusLab Dashboard][1].  Optionally you can also pass an
`endpoint` parameter but you probably shouldn't do this unless you've been
told to do so by somebody from FocusLab.

You're now ready to start making calls to the FocusLab API.

Trigger Recording
-----------------

To record a trigger, all you need to do is call the `record_trigger` method
on a client instance:

```python
from brockman.client import FocusLabClient

client = FocusLabClient(api_key='da9dcaa0364541498d4ae6b4865cf395')

client.record_trigger(
    actor_id=user.id,
    action='viewed',
    obj='blog post',
    identities={'email': user.email, 'user_id': user.id},
    attributes={'plan': user.plan},
    variables={'tags': post.tags, 'title': post.title}
)
```

The parameters to `record_trigger` are described below:

`actor_id`
:   A required string that acts as a session token.  If you are using this
    client in combination with the [javascript tracking code][2], you can use
    the `fl_actor_id` cookie value as the user's actor_id.  Otherwise any
    string that will be relatively consistent for a user can be used (e.g. a
    user id).

`action`
:   A required string that describes the event that the trigger is
    representing (e.g. viewed, downloaded, streamed, etc).

`obj`
:   A required string that describes the thing that the event being
    represented by the trigger is happening to (e.g. artist, blog post,
    product).

`identities`
:   An optional dictionary of identities for the user.  Any identities
    provided will be returned when you download a group from FocusLab.
    Additionally they are used to connect together activity streams from the
    user.  Dictionary values can be strings, integers, floats, or lists.
    Possible identities include email addresses, user ids, and facebook ids.

`attributes`
:   An optional dictionary of attributes for the user.  Attributes are pieces
    of data about a user that you'd like to filter against, but should not be
    used for connecting activity streams.  Dictionary values can be strings,
    integers, floats, or lists.  Possible attributes include plan type, user
    level, or date joined.

`variables`
:   An optional dictionary of variables for the trigger.  Variables are pieces
    of data about the event the trigger is representing.  Dictionary values
    can be strings, integers, floats, or lists.  Possible variables include
    genres, tags, categories, titles, product code, or author.


Getting Help
------------

If you have any questions or run into any problems please feel free to email
us at help@focuslab.io or to use the chat box at http://focuslab.io.



[1]: https://app.focuslab.io/
[2]: https://github.com/focuslab/willie
