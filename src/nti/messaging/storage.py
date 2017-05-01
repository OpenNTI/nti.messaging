#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: storage.py 106422 2017-02-13 21:32:28Z carlos.sanchez $
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface
from zope import lifecycleevent

from zope.cachedescriptors.property import readproperty

from zope.container.contained import Contained

from zope.location import locate

from zope.location.interfaces import ISublocations

from ZODB.interfaces import IConnection

from nti.base.interfaces import ICreated

from nti.containers.containers import CaseInsensitiveCheckingLastModifiedBTreeContainer

from nti.dublincore.datastructures import PersistentCreatedModDateTrackingObject

from nti.messaging.interfaces import IMailbox
from nti.messaging.interfaces import IReceivedMessage
from nti.messaging.interfaces import IMessageContainer
from nti.messaging.interfaces import IReceivedMessageContainer

from nti.schema.schema import SchemaConfigured


def save_in_container(container, key, value, event=True):
    if event:
        container[key] = value
    else:
        # avoid dublincore annotations for performance
        container._setitemf(key, value)
        locate(value, parent=container, name=key)
        if      IConnection(container, None) is not None \
            and IConnection(value, None) is None:
            IConnection(container).add(value)
        lifecycleevent.added(value, container, key)
        try:
            container.updateLastMod()
        except AttributeError:
            pass
        container._p_changed = True
    return value


@interface.implementer(ICreated)
class MessageContainerBase(CaseInsensitiveCheckingLastModifiedBTreeContainer,
                           Contained):

    def __init__(self):
        CaseInsensitiveCheckingLastModifiedBTreeContainer.__init__(self)

    def _build_key(self):
        return self.generateId("msg_")

    @property
    def creator(self):
        return self.__parent__.creator
    owner = creator

    def get_message(self, mid):
        return self[mid]

    def append_message(self, message, event=False):
        key = message.__name__ or self._build_key()
        return save_in_container(self, key, message, event=event)
    add = append = append_message

    def delete_message(self, message):
        del self[message.__name__]
    remove = delete = delete_message


@interface.implementer(IReceivedMessageContainer)
class ReceivedMessageContainer(MessageContainerBase):

    def _build_key(self):
        return self.generateId("recv_msg_")


@interface.implementer(IMessageContainer)
class MessageContainer(MessageContainerBase):
    pass


@interface.implementer(IMailbox, ISublocations, ICreated)
class Mailbox(SchemaConfigured, PersistentCreatedModDateTrackingObject, Contained):

    __external_can_create__ = False
    __external_class_name__ = 'Mailbox'

    mimeType = mime_type = 'application/vnd.nextthought.messaging.mailbox'

    def __init__(self, owner=None):
        PersistentCreatedModDateTrackingObject.__init__(self)
        if owner:
            self.creator = owner

        self.Sent = MessageContainer()
        locate(self.Sent, parent=self, name="Sent")

        self.Received = ReceivedMessageContainer()
        locate(self.Received, parent=self, name="Received")

    @readproperty
    def creator(self):
        return self.__parent__

    def sublocations(self):
        yield self.Sent
        yield self.Received

    def send(self, message):
        if not message.creator:
            message.creator = message.From.id  # principal id
        return self.Sent.append_message(message)

    def receive(self, message):
        received_message = IReceivedMessage(message)
        return self.Received.append_message(received_message)

    def getReceived(self):
        return self.Received
    get_received = getReceived
    
    def getSent(self):
        return self.Sent
    get_sent = getSent
